# Модуль для работы с медиафайлами

## Обзор

Модуль `media.py` предоставляет функции для обработки медиафайлов, таких как изображения и аудио, используемых в рамках проекта `hypotez`. 

## Подробнее

Модуль `media.py` используется для обработки и рендеринга медиафайлов в контексте взаимодействия с различными AI-моделями. Он позволяет:

- Преобразовывать медиафайлы в формат `base64` для отправки в API AI-моделей
- Рендерить медиафайлы в формате `data URI` или `URL` для отображения на странице.
- Объединять медиафайлы с текстовыми сообщениями в единый список для отправки в AI-модель.
- Рендерить сообщения с медиафайлами в формате, который подходит для отправки в AI-модель.


## Функции

### `render_media`

**Назначение**: Функция для рендеринга медиафайла. 

**Параметры**:

- `bucket_id` (str): Идентификатор хранилища.
- `name` (str): Имя файла.
- `url` (str): URL медиафайла.
- `as_path` (bool, optional): Если `True`, возвращает путь к файлу. По умолчанию `False`.
- `as_base64` (bool, optional): Если `True`, возвращает медиафайл в формате `base64`. По умолчанию `False`.

**Возвращает**:

- `Union[str, Path]`: Путь к файлу или медиафайл в формате `base64` или `data URI`.

**Как работает функция**:

- Если `as_base64` или `as_path` равно `True` или `url` начинается с "/", функция извлекает медиафайл из хранилища по заданному `bucket_id` и `name`.
- Если `as_path` равно `True`, функция возвращает путь к файлу.
- Если `as_base64` равно `True`, функция считывает файл и возвращает его в формате `base64`.
- Если `as_base64` равно `False`, функция возвращает медиафайл в формате `data URI`.
- В противном случае функция возвращает `url`.


**Примеры**:

```python
# Рендеринг медиафайла в формате `base64`
media_base64 = render_media(bucket_id='my_bucket', name='image.jpg', as_base64=True)

# Рендеринг медиафайла в формате `data URI`
media_uri = render_media(bucket_id='my_bucket', name='image.jpg')

# Рендеринг медиафайла по URL
media_url = render_media(bucket_id='my_bucket', name='image.jpg', url='https://example.com/image.jpg')
```

### `render_part`

**Назначение**: Функция для рендеринга отдельного элемента списка `content`.

**Параметры**:

- `part` (dict): Словарь, содержащий информацию об элементе списка `content`.

**Возвращает**:

- `dict`: Словарь с обновленной информацией об элементе списка `content`.

**Как работает функция**:

- Если `part` содержит ключ `type`, функция возвращает `part` без изменений.
- Если `part` содержит ключ `name`, функция проверяет тип файла:
    - Если файл является аудиофайлом, функция рендерит его в формате `input_audio` с использованием `render_media`.
    - Если файл является изображением, функция рендерит его в формате `image_url` с использованием `render_media`.
- Если `part` не содержит ключ `name`, функция рендерит содержимое файла в формате `text`.

**Примеры**:

```python
# Рендеринг аудиофайла
audio_part = {'name': 'audio.mp3', 'bucket_id': 'my_bucket'}
rendered_audio_part = render_part(audio_part)

# Рендеринг изображения
image_part = {'name': 'image.jpg', 'bucket_id': 'my_bucket'}
rendered_image_part = render_part(image_part)

# Рендеринг текстового файла
text_part = {'bucket_id': 'my_bucket'}
rendered_text_part = render_part(text_part)
```

### `merge_media`

**Назначение**: Функция для объединения медиафайлов с текстовыми сообщениями.

**Параметры**:

- `media` (list): Список медиафайлов.
- `messages` (list): Список сообщений.

**Возвращает**:

- `Iterator`: Итератор, содержащий пары (путь к файлу, имя файла) или словарь с информацией о медиафайле.

**Как работает функция**:

- Функция проходит по списку сообщений.
- Если сообщение является сообщением пользователя, функция проверяет `content` сообщения.
    - Если `content` является списком, функция проходит по каждому элементу списка.
        - Если элемент списка содержит ключ `name`, функция добавляет пару (путь к файлу, имя файла) в `buffer`.
        - Если элемент списка содержит ключ `type` и значение `image_url`, функция добавляет словарь с информацией о медиафайле в `buffer`.
- Если сообщение не является сообщением пользователя, функция очищает `buffer`.
- Функция возвращает итератор, содержащий пары (путь к файлу, имя файла) или словарь с информацией о медиафайле.

**Примеры**:

```python
# Объединение медиафайлов с сообщениями
media_files = [('image.jpg', 'image.jpg'), ('audio.mp3', 'audio.mp3')]
messages = [
    {'role': 'user', 'content': [{'name': 'image.jpg', 'bucket_id': 'my_bucket'}]},
    {'role': 'assistant', 'content': 'Hello, world!'},
    {'role': 'user', 'content': [{'name': 'audio.mp3', 'bucket_id': 'my_bucket'}]}
]
merged_media = merge_media(media_files, messages)
for item in merged_media:
    print(item)

# Вывод:
# ('/path/to/image.jpg', 'image.jpg')
# ('/path/to/audio.mp3', 'audio.mp3')
# ('/path/to/image.jpg', 'image.jpg')
```

### `render_messages`

**Назначение**: Функция для рендеринга списка сообщений с медиафайлами.

**Параметры**:

- `messages` (Messages): Список сообщений.
- `media` (list, optional): Список медиафайлов. По умолчанию `None`.

**Возвращает**:

- `Iterator`: Итератор, содержащий список сообщений с медиафайлами.

**Как работает функция**:

- Функция проходит по списку сообщений.
- Если `content` сообщения является списком, функция рендерит каждый элемент списка с использованием `render_part`.
- Если `content` сообщения не является списком, функция проверяет, является ли последнее сообщение в списке сообщением пользователя.
    - Если это так, функция добавляет в `content` список медиафайлов в формате `input_audio` или `image_url`.
- Функция возвращает итератор, содержащий список сообщений с медиафайлами.

**Примеры**:

```python
# Рендеринг списка сообщений с медиафайлами
messages = [
    {'role': 'user', 'content': [{'name': 'image.jpg', 'bucket_id': 'my_bucket'}]},
    {'role': 'assistant', 'content': 'Hello, world!'},
    {'role': 'user', 'content': 'How are you?'}
]
media_files = [('image.jpg', 'image.jpg'), ('audio.mp3', 'audio.mp3')]
rendered_messages = render_messages(messages, media_files)
for message in rendered_messages:
    print(message)

# Вывод:
# {'role': 'user', 'content': [{'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,...'}}]}
# {'role': 'assistant', 'content': 'Hello, world!'}
# {'role': 'user', 'content': [{'type': 'input_audio', 'input_audio': {'data': 'base64,...', 'format': 'mp3'}}, {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,...'}}]}