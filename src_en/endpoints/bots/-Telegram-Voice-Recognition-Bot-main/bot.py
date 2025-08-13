import os
import pickle
import torch
import librosa
import numpy as np
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from pydub import AudioSegment
from train_nn import VoiceClassifier  # I import the model
from dotenv import load_dotenv
load_dotenv()

# Telegram token
TOKEN = os.getenv("TOKEN")

# We create a session
session = AiohttpSession()

# Create a bot
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)

# Create a dispatcher and router
dp = Dispatcher()
router = Router()

# Ways to models
MODEL_PATH = "model_nn.pth"
ENCODER_PATH = "label_encoder.pkl"

# Download Labelencoder
with open(ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

# We load the trained model
model = VoiceClassifier(input_size=40, num_classes=len(label_encoder.classes_))
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()


# The function for predicting the speaker
def predict_speaker(file_path):
    try:
        y, sr = librosa.load(file_path, sr=22050)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)

        if mfcc.shape[1] == 0:
            return "Не удалось распознать голос."

        mfcc = np.mean(mfcc.T, axis=0)

        # Normalization
        mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)

        # We convert to the tensor and submit to the model
        tensor = torch.tensor(mfcc, dtype=torch.float32).unsqueeze(0)
        output = model(tensor)
        predicted_idx = torch.argmax(output, dim=1).item()

        return label_encoder.inverse_transform([predicted_idx])[0]
    except Exception as e:
        return f"Ошибка при распознавании: {e}"


# Voice messenger
@router.message(F.voice)
async def handle_voice(message: types.Message):
    voice = message.voice  # We get a voice message object
    file_path = f"audio/{voice.file_id}.ogg"
    wav_path = file_path.replace(".ogg", ".wav")

    try:
        # Download the voice message
        await bot.download(voice.file_id, destination=file_path)

        # We convert to WAV
        AudioSegment.from_file(file_path).export(wav_path, format="wav")

        # We predict the speaker
        speaker = predict_speaker(wav_path)

        # We send the answer
        await message.answer(f"Это говорит: {speaker}")

    except Exception as e:
        await message.answer(f"Ошибка при обработке голосового сообщения: {e}")

    finally:
        # We delete files after processing
        for f in [file_path, wav_path]:
            if os.path.exists(f):
                os.remove(f)


# Team handler /Speakers
@router.message(F.text == "/speakers")
async def list_speakers(message: types.Message):
    speakers = label_encoder.classes_  # We get a list of famous speakers
    speaker_list = "\n".join(speakers) if len(speakers) > 0 else "Пока нет записанных голосов."
    await message.answer(f"Известные говорящие:\n{speaker_list}")


# Launch of the bot
async def main():
    dp.include_router(router)  # Connect Router
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Бот был остановлен.")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем.")
