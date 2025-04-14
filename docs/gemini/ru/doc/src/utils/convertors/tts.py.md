# Модуль `tts`

## Обзор

Модуль `tts` предназначен для распознавания речи и преобразования текста в речь. Он включает функции для загрузки аудиофайлов, распознавания речи в них и генерации речи на основе заданного текста. Модуль использует библиотеки `speech_recognition`, `pydub` и `gtts` для выполнения этих задач.

## Подробней

Этот модуль предоставляет следующие возможности:

- Распознавание речи из аудиофайлов, расположенных по URL-адресу или локальному пути.
- Преобразование текста в речь с использованием различных языков.
- Сохранение сгенерированной речи в виде аудиофайла.

## Функции

### `speech_recognizer`

**Назначение**: Распознает речь в аудиофайле, расположенном по URL-адресу или локальному пути.

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

**Параметры**:

- `audio_url` (str, optional): URL-адрес аудиофайла для загрузки. По умолчанию `None`.
- `audio_file_path` (Path, optional): Локальный путь к аудиофайлу. По умолчанию `None`.
- `language` (str, optional): Языковой код для распознавания речи (например, 'ru-RU'). По умолчанию 'ru-RU'.

**Возвращает**:

- `str`: Распознанный текст из аудио или сообщение об ошибке.

**Как работает функция**:

1. Проверяет, предоставлен ли URL-адрес аудиофайла (`audio_url`). Если да, загружает файл и сохраняет его во временном каталоге.
2. Конвертирует аудиофайл из формата OGG в формат WAV.
3. Инициализирует распознаватель речи (`sr.Recognizer`).
4. Открывает WAV-файл и записывает аудиоданные.
5. Пытается распознать речь с использованием Google Speech Recognition.
6. Возвращает распознанный текст или сообщение об ошибке в случае неудачи.

**Вызывает исключения**:

- `sr.UnknownValueError`: Если Google Speech Recognition не может понять аудио.
- `sr.RequestError`: Если не удается получить результаты от сервиса Google Speech Recognition.
- `Exception`: В случае любой другой ошибки при распознавании речи.

**Примеры**:

```python
# Пример использования с URL-адресом аудиофайла
recognized_text = speech_recognizer(audio_url='https://example.com/audio.ogg')
print(recognized_text)  # Вывод: "Привет"

# Пример использования с локальным путем к аудиофайлу
from pathlib import Path
recognized_text = speech_recognizer(audio_file_path=Path('/path/to/audio.ogg'))
print(recognized_text)  # Вывод: "Привет"
```

### `text2speech`

**Назначение**: Преобразует текст в речь и сохраняет его в виде аудиофайла.

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

**Параметры**:

- `text` (str): Текст для преобразования в речь.
- `lang` (str, optional): Языковой код для речи (например, 'ru'). По умолчанию 'ru'.

**Возвращает**:

- `str`: Путь к сгенерированному аудиофайлу.

**Как работает функция**:

1. Генерирует речь на основе заданного текста и языка с использованием `gTTS`.
2. Сохраняет сгенерированный аудиофайл во временном каталоге в формате MP3.
3. Загружает аудиофайл с использованием `pydub`.
4. Экспортирует аудиофайл в формат WAV.
5. Возвращает путь к сгенерированному WAV-файлу.

**Вызывает исключения**:

- `Exception`: В случае ошибки при преобразовании текста в речь.

**Примеры**:

```python
# Пример использования для преобразования текста в речь на русском языке
import asyncio
async def main():
    audio_path = await text2speech('Привет', lang='ru')
    print(audio_path)  # Вывод: "/tmp/response.mp3"

asyncio.run(main())

# Пример использования для преобразования текста в речь на английском языке
async def main():
    audio_path = await text2speech('Hello', lang='en')
    print(audio_path)

asyncio.run(main())