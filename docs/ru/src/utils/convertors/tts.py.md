# Модуль `tts`

## Обзор

Модуль `tts` предоставляет функциональность для распознавания речи и преобразования текста в речь. Он включает функции для загрузки аудиофайлов, распознавания речи в них и синтеза речи из заданного текста. Модуль использует библиотеки `speech_recognition`, `pydub` и `gtts` для выполнения этих задач.

## Подробней

Модуль предназначен для интеграции в системы, требующие преобразования текста в речь и наоборот. Распознавание речи полезно для обработки голосовых команд или анализа аудиозаписей, а преобразование текста в речь может использоваться для озвучивания текста или создания аудио-контента.

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
```

**Назначение**: Распознает речь в аудиофайле, который может быть загружен по URL или указан локальным путем.

**Параметры**:

-   `audio_url` (str, optional): URL-адрес аудиофайла для загрузки. По умолчанию `None`.
-   `audio_file_path` (Path, optional): Локальный путь к аудиофайлу. По умолчанию `None`.
-   `language` (str): Языковой код для распознавания (например, 'ru-RU'). По умолчанию 'ru-RU'.

**Возвращает**:

-   `str`: Распознанный текст из аудиофайла или сообщение об ошибке.

**Вызывает исключения**:

-   `Exception`: Возникает при ошибках в процессе распознавания речи, таких как проблемы с доступом к файлу или невозможность распознать речь.
-   `sr.UnknownValueError`: Возникает, когда Google Speech Recognition не может распознать аудио.
-   `sr.RequestError`: Возникает, когда не удается запросить результаты у сервиса Google Speech Recognition.

**Как работает функция**:

1.  **Проверка наличия URL-адреса аудиофайла**: Если указан `audio_url`, функция загружает аудиофайл по указанному URL, используя библиотеку `requests`.
2.  **Сохранение аудиофайла**: Временный аудиофайл сохраняется во временной директории с именем `recognized_audio.ogg`.
3.  **Преобразование OGG в WAV**: Используя библиотеку `pydub`, аудиофайл конвертируется из формата OGG в WAV для совместимости с `speech_recognition`.
4.  **Распознавание речи**: Инициализируется объект `Recognizer` из библиотеки `speech_recognition`.
5.  **Чтение аудиоданных**: Аудиоданные считываются из WAV-файла с использованием `sr.AudioFile` в качестве источника.
6.  **Попытка распознавания речи через Google Speech Recognition**: Функция пытается распознать речь с использованием `recognizer.recognize_google()`.
7.  **Обработка результатов**: Если распознавание успешно, функция возвращает распознанный текст. В случае неудачи возвращает сообщение об ошибке.
8.  **Логирование ошибок**: В случае возникновения исключений в процессе распознавания речи, функция логирует ошибку с использованием `logger.error()`.

```
    A
    │
    ├── audio_url?
    │   ├── Да: Загрузка аудиофайла по URL
    │   │   │
    │   │   └── Сохранение во временный файл
    │   │
    │   └── Нет: Использовать audio_file_path
    │
    │
    B
    │
    └── Конвертация OGG в WAV
    │
    C
    │
    └── Инициализация распознавателя речи
    │
    D
    │
    └── Чтение аудиоданных из WAV
    │
    E
    │
    └── Распознавание речи через Google Speech Recognition
    │
    F
    │
    └── Возврат распознанного текста или сообщения об ошибке
```

**Примеры**:

```python
# Пример 1: Распознавание речи из аудиофайла по URL
recognized_text = speech_recognizer(audio_url='https://example.com/audio.ogg')
print(recognized_text)

# Пример 2: Распознавание речи из локального аудиофайла
from pathlib import Path
file_path = Path('/path/to/audio.ogg')
recognized_text = speech_recognizer(audio_file_path=file_path)
print(recognized_text)
```

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
```

**Назначение**: Преобразует текст в речь и сохраняет его в виде аудиофайла.

**Параметры**:

-   `text` (str): Текст, который нужно преобразовать в речь.
-   `lang` (str, optional): Языковой код для речи (например, 'ru'). По умолчанию 'ru'.

**Возвращает**:

-   `str`: Путь к сгенерированному аудиофайлу.

**Вызывает исключения**:

-   `Exception`: Возникает при ошибках в процессе преобразования текста в речь, таких как проблемы с доступом к файлу или невозможность преобразовать текст.

**Как работает функция**:

1.  **Генерация речи с использованием gTTS**: Используется библиотека `gTTS` для преобразования текста в речь.
2.  **Сохранение аудиофайла**: Аудиофайл сохраняется во временной директории с именем `response.mp3`.
3.  **Загрузка и экспорт аудио с использованием pydub**: Библиотека `pydub` используется для загрузки аудиофайла и его экспорта в формат WAV.
4.  **Логирование**: Логируется информация о сохранении аудиофайла с использованием `logger.info()`.
5.  **Обработка ошибок**: В случае возникновения исключений в процессе преобразования текста в речь, функция логирует ошибку с использованием `logger.error()`.

```
    A
    │
    └── Генерация речи с использованием gTTS
    │
    B
    │
    └── Сохранение аудиофайла в формате MP3
    │
    C
    │
    └── Загрузка и экспорт аудио в формат WAV с использованием pydub
    │
    D
    │
    └── Возврат пути к сгенерированному аудиофайлу
```

**Примеры**:

```python
# Пример 1: Преобразование текста в речь на русском языке
import asyncio
async def main():
    audio_path = await text2speech('Привет', lang='ru')
    print(audio_path)

asyncio.run(main())

# Пример 2: Преобразование текста в речь на английском языке
import asyncio
async def main():
    audio_path = await text2speech('Hello', lang='en')
    print(audio_path)
asyncio.run(main())