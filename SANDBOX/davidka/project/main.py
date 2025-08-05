import os
import logging
import asyncio
import math
import time
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import requests

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TELEGRAM_API = 'https://api.telegram.org'
OPENAI_API = 'https://api.openai.com/v1'

# OpenAI API Key and Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    logger.error("TELEGRAM_BOT_TOKEN or OPENAI_API_KEY not found in environment variables.")
    exit(1)

# --- Services ---

class SpeechService:
    """
    Service to handle voice message transcription using OpenAI Whisper.
    """
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.client = openai.OpenAI(api_key=self.openai_api_key)

    async def transcribe_voice(self, file_path: str) -> str:
        """
        Transcribes an audio file using OpenAI Whisper.
        """
        file_url = f"{TELEGRAM_API}/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
        
        # Download the audio file
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        # Save to a temporary file
        temp_audio_path = "temp_audio.ogg"
        with open(temp_audio_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        try:
            with open(temp_audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            return transcript.text
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

class AIService:
    """
    Service to generate timestamps and key ideas using OpenAI GPT-4o.
    """
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.client = openai.OpenAI(api_key=self.openai_api_key)

    def _build_timestamp_system_prompt(self) -> str:
        return """
Ты — ассистент, который составляет тайм-коды к голосовым сообщениям.
У тебя есть расшифровка текста, разбитая на временные блоки.
Твоя задача — выбрать из каждого блока ОДНУ ключевую идею (если она есть)
и указать её с точным тайм-кодом начала блока.

Правила:
- Не выдумывай тем, которых не было в тексте.
- Не объединяй идеи из разных блоков.
- Не используй больше 10 пунктов.
- Не добавляй "Заключение", "Финал", если этого не было в речи.
- Сохраняй реальный тайминг — не позже времени блока.
- Пропускай блок, если в нём нет ничего важного.

Формат:
00:00 - Введение
00:35 - Почему важно планировать день
01:10 - Проблема прокрастинации
"""

    def _build_timestamp_user_prompt(self, prepared_text: str) -> str:
        return f"""
Вот текст, расшифрованный из голосового сообщения. Каждый блок соответствует примерно 30-40 секундам речи.
Для каждого блока выдели ключевую идею (если она есть), строго по времени начала блока.

Текст:
{prepared_text}
"""

    async def generate_timestamps(self, text: str, audio_duration_sec: int) -> dict:
        """
        Generates timestamps and calculates cost using OpenAI GPT-4o.
        """
        max_segments = 10  # Максимум логических блоков для разметки

        words = text.split()
        words_per_segment = math.ceil(len(words) / max_segments)
        seconds_per_segment = math.floor(audio_duration_sec / max_segments)

        segments = []
        for i in range(max_segments):
            from_sec = i * seconds_per_segment
            from_min = str(math.floor(from_sec / 60)).zfill(2)
            from_sec_rest = str(from_sec % 60).zfill(2)
            time_str = f"{from_min}:{from_sec_rest}"

            start = i * words_per_segment
            end = start + words_per_segment
            content = " ".join(words[start:end])

            if content.strip():
                segments.append({"time": time_str, "content": content})

        prepared_text = "".join([f"[{s['time']}] {s['content']}" for s in segments])

        system_message = self._build_timestamp_system_prompt()
        user_message = self._build_timestamp_user_prompt(prepared_text)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        result = response.choices[0].message.content
        usage = response.usage

        input_cost = (usage.prompt_tokens / 1_000_000) * 0.15
        output_cost = (usage.completion_tokens / 1_000_000) * 0.6
        total_cost = input_cost + output_cost

        cost_text = f"💸 Стоимость генерации: ~${total_cost:.4f}"

        return {"timestamps": result, "cost": cost_text}

# --- Telegram Bot Handlers ---

speech_service = SpeechService(OPENAI_API_KEY)
ai_service = AIService(OPENAI_API_KEY)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    await update.message.reply_text(
        "👋 Привет! Отправь мне голосовое сообщение, и я расставлю тайм-коды."
    )

def render_progress(percent: int) -> str:
    """Renders a progress bar string."""
    total_blocks = 10
    block_char = '▒'
    filled_blocks = max(1, round((percent / 100) * total_blocks))
    empty_blocks = total_blocks - filled_blocks
    return f"🔄 Прогресс: [{block_char * filled_blocks}{'░' * empty_blocks}] {percent}%"

async def update_progress_message(bot: Bot, chat_id: int, message_id: int, percent: int) -> None:
    """Edits a message to update the progress bar."""
    try:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=render_progress(percent))
    except Exception as e:
        logger.warning(f"Could not update progress message: {e}")

async def voice_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles voice messages."""
    voice = update.message.voice
    duration = voice.duration
    chat_id = update.message.chat_id

    progress_message = None
    progress_interval_task = None

    try:
        await update.message.reply_text(f"🎤 Длина голосового сообщения: {duration} сек.")

        # Send initial progress message
        progress_message = await update.message.reply_text(render_progress(10))
        progress_message_id = progress_message.message_id

        # Start updating progress
        percent = 10
        async def progress_updater():
            nonlocal percent
            while percent < 90:
                await asyncio.sleep(2 if duration <= 300 else 3) # Adjust interval based on duration
                percent += 5
                if percent > 90: percent = 90 # Cap at 90% before final step
                await update_progress_message(context.bot, chat_id, progress_message_id, percent)

        progress_interval_task = asyncio.create_task(progress_updater())

        # Get file path from Telegram
        file_id = voice.file_id
        file = await context.bot.get_file(file_id)
        file_path = file.file_path

        # Transcribe voice
        transcription = await speech_service.transcribe_voice(file_path)

        # Generate timestamps
        result = await ai_service.generate_timestamps(transcription, duration)
        timestamps = result["timestamps"]
        cost = result["cost"]

        # Stop and finalize progress
        if progress_interval_task:
            progress_interval_task.cancel()
        await update_progress_message(context.bot, chat_id, progress_message_id, 100)

        await update.message.reply_text(
            f"""⏳ Тайм-коды:

{timestamps}

<i>🤖 Таймы генерирует нейросеть, через наш бот</i>""",
            parse_mode='HTML'
        )
        await update.message.reply_text(cost)

    except Exception as e:
        logger.error(f"Error processing voice message: {e}", exc_info=True)
        if progress_interval_task:
            progress_interval_task.cancel()
        if progress_message:
            await update_progress_message(context.bot, chat_id, progress_message_id, 100) # Ensure progress is finalized
        await update.message.reply_text("⚠️ Ошибка при обработке голосового сообщения.")

def main() -> None:
    """Starts the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters. voice & ~filters.COMMAND, voice_message_handler))

    logger.info("Bot started. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
