# Модуль для преобразования текста в речь и распознавания речи (tts.py)

## Обзор

Этот модуль предоставляет функции для преобразования текста в речь и распознавания речи из аудиофайлов.

## Подробней

Модуль `src/utils/convertors/tts.py` предназначен для работы с аудио и речью. Он содержит функции для распознавания речи из аудиофайла (с использованием Google Speech Recognition) и преобразования текста в речь (с использованием gTTS). Модуль использует библиотеки `speech_recognition`, `pydub` и `gtts`, а также модуль логирования `src.logger.logger`.

## Функции

### `speech_recognizer`

**Назначение**: Загружает аудиофайл и распознает речь в нем.

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

-   `audio_url` (str, optional): URL аудиофайла для скачивания. По умолчанию `None`.
-   `audio_file_path` (Path, optional): Локальный путь к аудиофайлу. По умолчанию `None`.
-   `language` (str): Код языка для распознавания (например, 'ru-RU'). По умолчанию 'ru-RU'.

**Возвращает**:

-   `str`: Распознанный текст из аудио или сообщение об ошибке.

**Как работает функция**:

1.  Проверяет, указан ли URL аудиофайла (`audio_url`). Если указан, скачивает файл и сохраняет его во временную директорию.
2.  Преобразует аудиофайл из формата OGG в WAV.
3.  Инициализирует распознаватель речи `sr.Recognizer()`.
4.  Открывает WAV-файл и использует Google Speech Recognition для распознавания речи.
5.  Логирует распознанный текст или сообщение об ошибке, используя `logger.info` и `logger.error`.
6.  Обрабатывает возможные исключения, такие как `sr.UnknownValueError` (не удалось распознать речь) и `sr.RequestError` (ошибка при запросе к сервису распознавания речи).

### `text2speech`

**Назначение**: Преобразует текст в речь и сохраняет его в аудиофайл.

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

-   `text` (str): Текст для преобразования в речь.
-   `lang` (str, optional): Код языка для синтеза речи (например, 'ru'). По умолчанию 'ru'.

**Возвращает**:

-   `str`: Путь к созданному аудиофайлу.

**Как работает функция**:

1.  Использует `gTTS` для генерации речи из текста на указанном языке.
2.  Сохраняет аудиофайл в формате MP3 во временную директорию.
3.  Преобразует аудиофайл из формата MP3 в WAV, используя `pydub`.
4.  Логирует информацию об успешном сохранении аудиофайла, используя `logger.info`.
5.  Обрабатывает возможные исключения, логируя ошибки с использованием `logger.error`.

## Переменные модуля

В данном модуле отсутствуют переменные, за исключением констант, определенных внутри функций (если бы они были).

## Пример использования

**Распознавание речи из аудиофайла:**

```python
from src.utils.convertors import tts
import asyncio

async def main():
    recognized_text = tts.speech_recognizer(audio_url='https://example.com/audio.ogg', language='ru-RU')
    print(recognized_text)
asyncio.run(main())
```

**Преобразование текста в речь:**

```python
from src.utils.convertors import tts
import asyncio

async def main():
    audio_path = await tts.text2speech('Привет', lang='ru')
    print(audio_path)

if __name__ == "__main__":
    asyncio.run(main())
```

## Взаимосвязь с другими частями проекта

-   Этот модуль использует библиотеку `speech_recognition` для распознавания речи, `pydub` для работы с аудио и `gtts` для синтеза речи.
-   Для логирования ошибок используется модуль `src.logger.logger`.
-   Модуль может использоваться другими частями проекта `hypotez` для обработки аудио и речи.