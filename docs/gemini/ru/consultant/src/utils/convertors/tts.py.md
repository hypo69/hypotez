### **Анализ кода модуля `tts`**

## \file /src/utils/convertors/tts.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
.. module:: src.utils.convertors.tts
	:platform: Windows, Unix
	:synopsis: speech recognition and text-to-speech conversion

"""

Модуль для распознавания речи и преобразования текста в речь.
=============================================================

Модуль содержит функции для преобразования текста в речь и распознавания речи из аудиофайлов.
Он использует библиотеки `speech_recognition`, `pydub` и `gTTS`.

## Качество кода:

- **Соответствие стандартам**: 7/10
- **Плюсы**:
  - Наличие документации к функциям.
  - Использование логирования.
  - Обработка исключений.
- **Минусы**:
  - Отсутствуют аннотации типов для переменных внутри функций.
  - Используются f-строки без необходимости (например, в `text2speech`).
  - Смешанный стиль кавычек (используются как одинарные, так и двойные).
  - docstring на английском языке
  - в docstring используется code:: для примеров. Лучше это делать через >>>

## Рекомендации по улучшению:

1.  **Общие улучшения**:

*   *Заменить двойные кавычки на одинарные*.
*   *Перевести docstring на русский язык*.
*   *Изменить `code::` в docstring на `>>>`*.
*   *Добавить аннотации типов для всех переменных*.

2.  **`speech_recognizer`**:

*   *Удалить неиспользуемые импорты, такие как `j_loads`, `j_loads_ns`, `j_dumps`*.
*   *В блоке `try` добавить аннотации типов для переменных `response`, `audio_file_path`, `wav_file_path`, `audio`, `recognizer`, `source`, `audio_data`, `text`*.
*   *Уточнить сообщение логирования в случае ошибки распознавания речи*.
*   *Использовать `ex` вместо `e` в блоках `except`*.
*   *Уточнить docstring, добавив информацию о возможных исключениях*.

3.  **`text2speech`**:

*   *В блоке `try` добавить аннотации типов для переменных `tts`, `audio_file_path`, `audio`, `wav_file_path`*.
*   *Использовать конкатенацию строк вместо f-строк для формирования пути к файлу*.
*   *Использовать `ex` вместо `e` в блоках `except`*.
*   *Уточнить docstring, добавив информацию о возможных исключениях*.

## Оптимизированный код:

```python
## \file /src/utils/convertors/tts.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль для распознавания речи и преобразования текста в речь.
=============================================================

Модуль содержит функции для преобразования текста в речь и распознавания речи из аудиофайлов.
Он использует библиотеки `speech_recognition`, `pydub` и `gTTS`.

Пример использования:
----------------------
    >>> recognized_text = speech_recognizer(audio_url='https://example.com/audio.ogg')
    >>> print(recognized_text)  # Output: "Привет"

    >>> audio_path = await text2speech('Привет', lang='ru')
    >>> print(audio_path)  # Output: "/tmp/response.mp3"

 .. module:: src.utils.convertors.tts
"""

from pathlib import Path
import tempfile
import asyncio
import requests
import speech_recognition as sr  # Библиотека для распознавания речи
from pydub import AudioSegment  # Library for audio conversion
from gtts import gTTS  # Генерация текста в речь

from src.logger.logger import logger


def speech_recognizer(audio_url: str = None, audio_file_path: Path = None, language: str = 'ru-RU') -> str:
    """Функция загружает аудиофайл и распознает речь в нем.

    Args:
        audio_url (str, optional): URL аудиофайла для загрузки. По умолчанию `None`.
        audio_file_path (Path, optional): Локальный путь к аудиофайлу. По умолчанию `None`.
        language (str): Код языка для распознавания (например, 'ru-RU'). По умолчанию 'ru-RU'.

    Returns:
        str: Распознанный текст из аудио или сообщение об ошибке.

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при загрузке аудиофайла.
        pydub.exceptions.CouldntDecodeError: Если `pydub` не может декодировать аудиофайл.
        speech_recognition.UnknownValueError: Если Google Speech Recognition не может понять аудио.
        speech_recognition.RequestError: Если не удается запросить результаты от сервиса Google Speech Recognition.
        Exception: При возникновении любой другой ошибки.

    Example:
        >>> recognized_text = speech_recognizer(audio_url='https://example.com/audio.ogg')
        >>> print(recognized_text)  # Output: "Привет"
    """
    try:
        if audio_url:
            # Загрузка аудиофайла
            response: requests.Response = requests.get(audio_url)
            audio_file_path: Path = Path(tempfile.gettempdir()) / 'recognized_audio.ogg'

            with open(audio_file_path, 'wb') as f:
                f.write(response.content)

        # Преобразование OGG в WAV
        wav_file_path: Path = audio_file_path.with_suffix('.wav')
        audio: AudioSegment = AudioSegment.from_file(audio_file_path)  # Загрузка OGG файла
        audio.export(wav_file_path, format='wav')  # Экспорт в WAV

        # Инициализация распознавателя
        recognizer: sr.Recognizer = sr.Recognizer()
        with sr.AudioFile(str(wav_file_path)) as source:
            audio_data: sr.AudioData = recognizer.record(source)
            try:
                # Распознавание речи с использованием Google Speech Recognition
                text: str = recognizer.recognize_google(audio_data, language=language)
                logger.info(f'Распознанный текст: {text}')
                return text
            except sr.UnknownValueError as ex:
                logger.error('Google Speech Recognition не смог распознать аудио', ex)
                return 'Извините, я не смог понять аудио.'
            except sr.RequestError as ex:
                logger.error('Не удалось запросить результаты от сервиса Google Speech Recognition:', ex)
                return 'Не удалось запросить результаты от сервиса распознавания речи.'
    except Exception as ex:
        logger.error('Ошибка в speech_recognizer:', ex)
        return 'Ошибка во время распознавания речи.'


async def text2speech(text: str, lang: str = 'ru') -> str:
    """Функция преобразует текст в речь и сохраняет его как аудиофайл.

    Args:
        text (str): Текст для преобразования в речь.
        lang (str, optional): Код языка для речи (например, 'ru'). По умолчанию 'ru'.

    Returns:
        str: Путь к сгенерированному аудиофайлу.

    Raises:
        gtts.tts.gTTSError: Если возникает ошибка при генерации речи.
        pydub.exceptions.CouldntDecodeError: Если `pydub` не может декодировать аудиофайл.
        Exception: При возникновении любой другой ошибки.

    Example:
        >>> audio_path = await text2speech('Привет', lang='ru')
        >>> print(audio_path)  # Output: "/tmp/response.mp3"
    """
    try:
        # Генерация речи с использованием gTTS
        tts: gTTS = gTTS(text=text, lang=lang)
        audio_file_path: str = tempfile.gettempdir() + '/response.mp3'
        tts.save(audio_file_path)  # Сохранение аудиофайла

        # Загрузка и экспорт аудио с использованием pydub
        audio: AudioSegment = AudioSegment.from_file(audio_file_path, format='mp3')
        wav_file_path: str = audio_file_path.replace('.mp3', '.wav')
        audio.export(wav_file_path, format='wav')

        logger.info(f'TTS аудио сохранено в: {wav_file_path}')
        return wav_file_path
    except Exception as ex:
        logger.error('Ошибка в text2speech:', ex)
        return 'Ошибка во время преобразования текста в речь.'