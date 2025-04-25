# Модуль Revai

## Обзор

Модуль `revai` предназначен для работы с API сервиса Revai (rev.com), предоставляющего услуги по транскрипции и переводу аудио и видео файлов. 

## Подробней

Этот модуль позволяет взаимодействовать с API Revai, выполняя такие задачи, как:

- Загрузка аудио и видео файлов для транскрипции.
- Получение транскрипции в текстовом формате.
- Просмотр статуса обработки файлов.
- Управление транскрипционными задачами.

## Классы

### `class Revai`

**Описание**: Класс `Revai` предоставляет основные функции для работы с API Revai.

**Атрибуты**:

- `api_key` (str): API ключ для доступа к сервису Revai.
- `base_url` (str): Базовый URL API Revai.
- `headers` (dict): Заголовки запросов к API Revai.

**Методы**:

- `get_token()`: Получает токен доступа к API Revai.
- `create_job(media_url: str, config: dict) -> dict`: Создает новую транскрипционную задачу.
- `get_job_status(job_id: str) -> dict`: Получает статус транскрипционной задачи.
- `get_job_transcript(job_id: str) -> str`: Получает текст транскрипции.

## Функции

### `get_token()`

**Назначение**: Функция `get_token` получает токен доступа к API Revai.

**Параметры**:

-  `api_key` (str): API ключ для доступа к сервису Revai.

**Возвращает**:

- `str`: Токен доступа к API Revai.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при получении токена.

**Пример**:

```python
token = get_token(api_key='your_api_key')
```

### `create_job(media_url: str, config: dict) -> dict`

**Назначение**: Функция `create_job` создает новую транскрипционную задачу.

**Параметры**:

- `media_url` (str): URL-адрес аудио или видео файла для транскрипции.
- `config` (dict): Конфигурация транскрипционной задачи. 

**Возвращает**:

- `dict`: Информация о созданной задаче.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при создании задачи.

**Пример**:

```python
job_config = {
  "language": "en-US",
  "model": "base",
  "transcription_options": {
    "speaker_channels": True
  }
}
job_data = create_job(media_url='https://www.example.com/audio.mp3', config=job_config)
```

### `get_job_status(job_id: str) -> dict`

**Назначение**: Функция `get_job_status` получает статус транскрипционной задачи.

**Параметры**:

- `job_id` (str): Идентификатор транскрипционной задачи.

**Возвращает**:

- `dict`: Статус транскрипционной задачи.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при получении статуса задачи.

**Пример**:

```python
status = get_job_status(job_id='your_job_id')
```

### `get_job_transcript(job_id: str) -> str`

**Назначение**: Функция `get_job_transcript` получает текст транскрипции.

**Параметры**:

- `job_id` (str): Идентификатор транскрипционной задачи.

**Возвращает**:

- `str`: Текст транскрипции.

**Вызывает исключения**:

- `Exception`: Если возникает ошибка при получении текста транскрипции.

**Пример**:

```python
transcript = get_job_transcript(job_id='your_job_id')
```

## Примеры

```python
# Пример использования модуля Revai

from revai import Revai

# Создаем объект Revai
revai = Revai(api_key='your_api_key')

# Получаем токен доступа
token = revai.get_token()

# Создаем новую задачу транскрипции
job_config = {
  "language": "en-US",
  "model": "base",
  "transcription_options": {
    "speaker_channels": True
  }
}
job_data = revai.create_job(media_url='https://www.example.com/audio.mp3', config=job_config)

# Получаем статус задачи
status = revai.get_job_status(job_id=job_data['id'])

# Получаем текст транскрипции
transcript = revai.get_job_transcript(job_id=job_data['id'])

# Выводим текст транскрипции
print(transcript)
```

## Дополнительная информация

Дополнительную информацию о сервисе Revai и API можно найти на сайте: https://www.rev.com/api/docs