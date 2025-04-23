## \file hypotez/src/endpoints/bots/discord/README.MD
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Документация для Discord-бота
==============================
"""

```rst
 .. module:: src.endpoints.bots.discord
```

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/README.MD'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/README.MD'>src</A> /
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/endpoints/README.MD'>endpoints</A> /
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/bots/README.MD'>bots</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/bots/discord/readme.ru.md'>Русский</A>
</TD>
</TABLE>

Этот код представляет собой Discord-бота, написанного на Python с использованием библиотеки `discord.py`. Бот выполняет несколько функций, связанных с управлением моделью машинного обучения, обработкой аудио и взаимодействием с пользователями как в текстовых, так и в голосовых каналах Discord. Ниже приведено краткое описание основных функций и команд, которые реализует этот бот:

### Основные функции и команды бота:

1. **Инициализация бота:**
   - Бот инициализируется с командным префиксом `!` и включает необходимые intents (intents — это разрешения на доступ к определенным событиям Discord).

2. **Команды:**
   - `!hi`: Отправляет приветственное сообщение.
   - `!join`: Подключает бота к голосовому каналу, в котором находится пользователь.
   - `!leave`: Отключает бота от голосового канала.
   - `!train`: Обучает модель на предоставленных данных. Данные могут быть переданы как файл или текст.
   - `!test`: Тестирует модель на предоставленных данных.
   - `!archive`: Архивирует файлы в указанном каталоге.
   - `!select_dataset`: Выбирает набор данных для обучения модели.
   - `!instruction`: Отправляет инструкции из внешнего файла.
   - `!correct`: Позволяет пользователю исправить предыдущее сообщение бота.
   - `!feedback`: Позволяет пользователю отправить отзыв о работе бота.
   - `!getfile`: Отправляет файл из указанного пути.

3. **Обработка сообщений:**
   - Бот обрабатывает входящие сообщения, игнорируя свои собственные сообщения.
   - Если пользователь отправляет аудиофайл, бот распознает речь в аудио и отправляет текст в ответ.
   - Если пользователь находится в голосовом канале, бот преобразует текст в речь и воспроизводит его в голосовом канале.

4. **Распознавание речи:**
   - Функция `recognizer` загружает аудиофайл, преобразует его в формат WAV и распознает речь, используя Google Speech Recognition.

5. **Преобразование текста в речь:**
   - Функция `text_to_speech_and_play` преобразует текст в речь с использованием библиотеки `gTTS` и воспроизводит его в голосовом канале.

6. **Логирование:**
   - Модуль `logger` используется для логирования событий и ошибок.

### Основные модули и библиотеки:
- `discord.py`: Основная библиотека для создания Discord-ботов.
- `speech_recognition`: Для распознавания речи.
- `pydub`: Для преобразования аудиофайлов.
- `gtts`: Для преобразования текста в речь.
- `requests`: Для загрузки файлов.
- `pathlib`: Для работы с путями к файлам.
- `tempfile`: Для создания временных файлов.
- `asyncio`: Для асинхронного выполнения задач.

### Запуск бота:
- Бот запускается с использованием токена, хранящегося в переменной `gs.credentials.discord.bot_token`.

### Вывод:
Этот бот предназначен для интерактивного взаимодействия с пользователями в Discord, включая обработку голосовых команд, обучение и тестирование модели машинного обучения, предоставление инструкций и получение обратной связи.

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный раздел описывает функциональность Discord-бота, написанного на Python с использованием библиотеки `discord.py`. Бот предоставляет интерактивное взаимодействие с пользователями в текстовых и голосовых каналах, включая обработку команд, распознавание речи, преобразование текста в речь, а также управление моделью машинного обучения.

Шаги выполнения
-------------------------
1. **Инициализация бота**: Бот инициализируется с префиксом `!` и необходимыми разрешениями (intents) для доступа к событиям Discord.
2. **Регистрация команд**: Бот регистрирует команды, такие как `!hi`, `!join`, `!leave`, `!train`, `!test`, `!archive`, `!select_dataset`, `!instruction`, `!correct`, `!feedback` и `!getfile`, для выполнения различных действий.
3. **Обработка сообщений**: Бот проверяет, не является ли сообщение его собственным, и если нет, обрабатывает его. Если сообщение содержит аудиофайл, бот распознает речь в аудио и отправляет текст в ответ. Если пользователь находится в голосовом канале, бот преобразует текст в речь и воспроизводит его в этом канале.
4. **Распознавание речи**: Функция `recognizer` извлекает аудиоданные, преобразует их в формат WAV и использует Google Speech Recognition для распознавания речи.
5. **Преобразование текста в речь**: Функция `text_to_speech_and_play` преобразует текст в речь с использованием библиотеки `gTTS` и воспроизводит аудио в голосовом канале.
6. **Логирование**: События и ошибки записываются с использованием модуля `logger` для отслеживания и отладки.

Пример использования
-------------------------

```python
import discord
from discord.ext import commands
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import requests
from pathlib import Path
import tempfile
import asyncio
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Инициализация бота
intents = discord.Intents.default()
intents.message_content = True  # Разрешение на чтение содержимого сообщений
intents.voice_states = True   # Разрешение на отслеживание статуса голосовых каналов
bot = commands.Bot(command_prefix='!', intents=intents)

# Команда приветствия
@bot.command()
async def hi(ctx):
    """
    Отправляет приветственное сообщение.
    """
    await ctx.send("Привет! Я Discord-бот.")

# Пример обработки аудиофайла
@bot.event
async def on_message(message):
    """
    Обрабатывает входящие сообщения, распознает речь в аудиофайлах и отправляет текст в ответ.
    """
    if message.author == bot.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.mp3', '.wav', '.ogg')):
                try:
                    # Скачивание файла
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    await attachment.save(temp_file.name)
                    temp_file.close()

                    # Распознавание речи
                    text = await recognizer(temp_file.name)
                    await message.channel.send(f"Распознанный текст: {text}")
                except Exception as e:
                    logger.error(f"Ошибка при обработке аудио: {e}", exc_info=True)
                    await message.channel.send("Произошла ошибка при обработке аудио.")
                finally:
                    Path(temp_file.name).unlink()  # Удаление временного файла
    
    await bot.process_commands(message)  # Обработка команд

async def recognizer(audio_file):
    """
    Распознает речь в аудиофайле с использованием Google Speech Recognition.

    Args:
        audio_file (str): Путь к аудиофайлу.

    Returns:
        str: Распознанный текст.
    """
    try:
        # Преобразование в WAV
        wav_file = audio_file + ".wav"
        AudioSegment.from_file(audio_file).export(wav_file, format="wav")

        # Распознавание речи
        r = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio = r.record(source)
        text = r.recognize_google(audio, language="ru-RU")
        return text
    except Exception as e:
        logger.error(f"Ошибка при распознавании речи: {e}", exc_info=True)
        return "Не удалось распознать речь."

# Запуск бота
# bot.run(gs.credentials.discord.bot_token) # Токен бота (закомментировано в примере)