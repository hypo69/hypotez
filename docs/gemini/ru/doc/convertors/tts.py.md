### Анализ кода `hypotez/src/utils/convertors/tts.py.md`

## Обзор

Модуль предоставляет утилиты для распознавания речи и преобразования текста в речь.

## Подробнее

Этот модуль содержит функции для работы с аудио и речью. Он позволяет распознавать речь из аудиофайлов и URL-адресов, а также преобразовывать текст в речь и сохранять результат в аудиофайл. Модуль использует библиотеки `speech_recognition`, `pydub` и `gTTS` для выполнения этих задач.

## Функции

### `speech_recognizer`

```python
def speech_recognizer(audio_url: str = None, audio_file_path: Path = None, language: str = 'ru-RU') -> str:
    """ Download an audio file and recognize speech in it.

    Args:
        audio_url (str, optional): URL of the audio file to be downloaded. Defaults to `None`.
        audio_file_path (Path, optional): Local path to an audio file. Defaults to `None`.
        language (str): Language code for recognition (e.g., 'ru-RU'). Defaults to 'ru-RU'.

    Returns:
        str: Recognized text from the audio or an error message.

    Example:
        .. code::

            recognized_text = speech_recognizer(audio_url='https://example.com/audio.ogg')
            print(recognized_text)  # Output: "Привет"
    """
    ...
```

**Назначение**:
Распознает речь в аудиофайле, загруженном с URL или указанном локально.

**Параметры**:

*   `audio_url` (str, optional): URL аудиофайла для скачивания. По умолчанию `None`.
*   `audio_file_path` (Path, optional): Локальный путь к аудиофайлу. По умолчанию `None`.
*   `language` (str): Код языка для распознавания (например, 'ru-RU'). По умолчанию 'ru-RU'.

**Возвращает**:

*   `str`: Распознанный текст из аудио или сообщение об ошибке.

**Как работает функция**:

1.  Определяет источник аудио (URL или локальный файл).
2.  Если указан URL, скачивает аудиофайл во временную директорию.
3.  Преобразует аудиофайл в формат WAV.
4.  Инициализирует распознаватель речи `sr.Recognizer()`.
5.  Использует Google Speech Recognition для распознавания речи из аудиоданных.
6.  Обрабатывает возможные ошибки:

    *   `sr.UnknownValueError`: Если Google Speech Recognition не может распознать аудио.
    *   `sr.RequestError`: Если не удается запросить результаты от сервиса Google Speech Recognition.
    *   `Exception`: При возникновении других ошибок.
7. Логгирует информацию об ошибках

### `text2speech`

```python
async def text2speech(text: str, lang: str = 'ru') -> str:
    """ Convert text to speech and save it as an audio file.

    Args:
        text (str): The text to be converted into speech.
        lang (str, optional): Language code for the speech (e.g., 'ru'). Defaults to 'ru'.

    Returns:
        str: Path to the generated audio file.

    Example:
        .. code::

            audio_path = await text2speech('Привет', lang='ru')
            print(audio_path)  # Output: "/tmp/response.mp3"
    """
    ...
```

**Назначение**:
Преобразует текст в речь и сохраняет его как аудиофайл.

**Параметры**:

*   `text` (str): Текст для преобразования в речь.
*   `lang` (str, optional): Код языка для речи (например, 'ru'). По умолчанию 'ru'.

**Возвращает**:

*   `str`: Путь к сгенерированному аудиофайлу.

**Как работает функция**:

1.  Использует `gTTS` для генерации речи из текста.
2.  Сохраняет аудиофайл во временной директории в формате MP3.
3.  Загружает MP3-файл с помощью `pydub.AudioSegment`.
4.  Экспортирует аудиофайл в формат WAV.
5.  Логирует успешное сохранение аудиофайла и возвращает путь к нему.
6.  В случае ошибки логирует её и возвращает сообщение об ошибке.

## Переменные

Отсутствуют

## Примеры использования

```python
import asyncio
from src.utils.convertors.tts import speech_recognizer, text2speech
from pathlib import Path

async def main():
    # Пример распознавания речи из аудиофайла
    recognized_text = speech_recognizer(audio_file_path=Path("audio.ogg"))
    print(f"Распознанный текст: {recognized_text}")

    # Пример преобразования текста в речь
    audio_path = await text2speech("Привет, мир!", lang='ru')
    print(f"Аудиофайл сохранен по пути: {audio_path}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Зависимости

*   `pathlib.Path`: Для работы с путями к файлам.
*   `tempfile`: Для создания временных файлов и директорий.
*   `asyncio`: Для использования асинхронных функций.
*   `requests`: Для загрузки файлов по URL.
*   `speech_recognition`: Для распознавания речи.
*   `pydub`: Для работы с аудиофайлами.
*   `gTTS`: Для преобразования текста в речь.
*    `src.logger.logger`: Для логирования

## Взаимосвязи с другими частями проекта

Модуль `tts.py` предоставляет утилиты для работы с речью и аудио и может использоваться в других частях проекта `hypotez`, где требуется распознавание речи, синтез речи или обработка аудиофайлов.