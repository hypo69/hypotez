# Модуль `revai`

## Обзор

Модуль `revai` предоставляет инструменты для работы с API сервиса Rev.com, специализирующегося на транскрипции аудио и видео материалов.

## Подробней

Rev.com - это платформа, предоставляющая услуги автоматической транскрипции, перевода, субтитров и создания субтитров.  Этот модуль предоставляет инструменты для взаимодействия с API Rev.com, позволяя разработчикам автоматизировать задачи, связанные с обработкой аудио- и видеоданных.

## Использование

Модуль `revai` предназначен для интеграции с приложениями, работающими с аудио- и видеофайлами. Его функции позволяют:

-  **Загружать** аудиофайлы для транскрипции.
-  **Получать** транскрипты в различных форматах, включая текст, JSON и SRT.
-  **Анализировать** транскрипты, извлекая ключевые слова, темы и другие данные.
-  **Использовать** полученные транскрипты для дальнейшей обработки, например, для создания субтитров, перевода или анализа.

## Функции

### `revai`

**Описание:**

Модуль `revai` предоставляет функции для работы с API сервиса Rev.com.

**Пример использования:**

```python
from hypotez.src.llm.revai import revai

# ... (загрузка конфигурации, получение токена API)

# Загрузка аудиофайла для транскрипции
response = revai.upload_media(
    token='your_token',
    media='path/to/your/audio.mp3',
    media_type='audio/mpeg',
)

# Получение транскрипта
transcript = revai.get_transcript(
    token='your_token',
    job_id=response['job_id'],
    format='json',
)

# Обработка полученного транскрипта
# ...
```

**Параметры**:

- `token`: (str) Токен API, полученный от Rev.com.
- `media`: (str) Путь к аудиофайлу.
- `media_type`: (str) Тип медиафайла (например, 'audio/mpeg').
- `job_id`: (str) ID задания, созданного после загрузки файла.
- `format`: (str) Формат транскрипта (например, 'json', 'srt', 'text').

**Возвращает:**

- `dict`: Данные о задании на транскрипцию.
- `dict`: Данные о транскрипте.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `upload_media`

**Описание:**

Функция `upload_media` загружает аудиофайл в Rev.com для транскрипции.

**Пример использования:**

```python
response = revai.upload_media(
    token='your_token',
    media='path/to/your/audio.mp3',
    media_type='audio/mpeg',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `media`: (str) Путь к аудиофайлу.
- `media_type`: (str) Тип медиафайла (например, 'audio/mpeg').

**Возвращает:**

- `dict`: Данные о задании на транскрипцию, включая `job_id`.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `get_transcript`

**Описание:**

Функция `get_transcript` получает транскрипт аудиофайла в заданном формате.

**Пример использования:**

```python
transcript = revai.get_transcript(
    token='your_token',
    job_id='your_job_id',
    format='json',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `job_id`: (str) ID задания, созданного после загрузки файла.
- `format`: (str) Формат транскрипта (например, 'json', 'srt', 'text').

**Возвращает:**

- `dict`: Данные о транскрипте в заданном формате.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `get_status`

**Описание:**

Функция `get_status` получает статус задания на транскрипцию.

**Пример использования:**

```python
status = revai.get_status(
    token='your_token',
    job_id='your_job_id',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `job_id`: (str) ID задания, созданного после загрузки файла.

**Возвращает:**

- `dict`: Данные о статусе задания, включая `status` (например, 'in_progress', 'completed').

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `cancel_job`

**Описание:**

Функция `cancel_job` отменяет задание на транскрипцию.

**Пример использования:**

```python
response = revai.cancel_job(
    token='your_token',
    job_id='your_job_id',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `job_id`: (str) ID задания, созданного после загрузки файла.

**Возвращает:**

- `dict`: Данные о результате отмены задания.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `get_media_metadata`

**Описание:**

Функция `get_media_metadata` получает метаданные аудиофайла.

**Пример использования:**

```python
metadata = revai.get_media_metadata(
    token='your_token',
    media_id='your_media_id',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `media_id`: (str) ID аудиофайла.

**Возвращает:**

- `dict`: Данные о метаданных аудиофайла.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `get_media_url`

**Описание:**

Функция `get_media_url` получает URL-адрес аудиофайла.

**Пример использования:**

```python
url = revai.get_media_url(
    token='your_token',
    media_id='your_media_id',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `media_id`: (str) ID аудиофайла.

**Возвращает:**

- `str`: URL-адрес аудиофайла.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `create_project`

**Описание:**

Функция `create_project` создает новый проект в Rev.com.

**Пример использования:**

```python
project_id = revai.create_project(
    token='your_token',
    name='My new project',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `name`: (str) Название проекта.

**Возвращает:**

- `str`: ID созданного проекта.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `get_project`

**Описание:**

Функция `get_project` получает информацию о проекте.

**Пример использования:**

```python
project = revai.get_project(
    token='your_token',
    project_id='your_project_id',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `project_id`: (str) ID проекта.

**Возвращает:**

- `dict`: Данные о проекте.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `update_project`

**Описание:**

Функция `update_project` обновляет информацию о проекте.

**Пример использования:**

```python
response = revai.update_project(
    token='your_token',
    project_id='your_project_id',
    name='Updated project name',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `project_id`: (str) ID проекта.
- `name`: (str) Новое название проекта.

**Возвращает:**

- `dict`: Данные о результате обновления проекта.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `delete_project`

**Описание:**

Функция `delete_project` удаляет проект.

**Пример использования:**

```python
response = revai.delete_project(
    token='your_token',
    project_id='your_project_id',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.
- `project_id`: (str) ID проекта.

**Возвращает:**

- `dict`: Данные о результате удаления проекта.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.


### `get_projects`

**Описание:**

Функция `get_projects` получает список всех проектов.

**Пример использования:**

```python
projects = revai.get_projects(
    token='your_token',
)
```

**Параметры:**

- `token`: (str) Токен API, полученный от Rev.com.

**Возвращает:**

- `list`: Список данных о проектах.

**Вызывает исключения:**

- `Exception`: Если возникает ошибка при работе с API Rev.com.

## Примеры

### Загрузка аудиофайла для транскрипции

```python
from hypotez.src.llm.revai import revai

# ... (загрузка конфигурации, получение токена API)

# Загрузка аудиофайла для транскрипции
response = revai.upload_media(
    token='your_token',
    media='path/to/your/audio.mp3',
    media_type='audio/mpeg',
)

print(response)
```

### Получение транскрипта

```python
from hypotez.src.llm.revai import revai

# ... (загрузка конфигурации, получение токена API)

# Получение транскрипта
transcript = revai.get_transcript(
    token='your_token',
    job_id='your_job_id',
    format='json',
)

print(transcript)
```

### Создание проекта

```python
from hypotez.src.llm.revai import revai

# ... (загрузка конфигурации, получение токена API)

# Создание проекта
project_id = revai.create_project(
    token='your_token',
    name='My new project',
)

print(project_id)
```

## Дополнительная информация

- Для работы с модулем `revai` необходимо получить токен API от Rev.com.
- Более подробная информация о API Rev.com доступна на [официальном сайте](https://www.rev.com/api/docs).
- Примеры использования кода можно найти в документации Rev.com ([https://docs.rev.ai/resources/code-samples/python/](https://docs.rev.ai/resources/code-samples/python/)).