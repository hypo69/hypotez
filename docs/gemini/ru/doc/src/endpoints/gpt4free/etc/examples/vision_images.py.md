# Модуль `vision_images.py`

## Обзор

Этот файл демонстрирует пример использования API `gpt4free` для обработки изображений с помощью модели `g4f.models.default_vision`. В примере показано, как обрабатывать изображения как из локальных файлов, так и из удаленных источников.

## Подробнее

Файл `vision_images.py` демонстрирует два основных способа работы с API `gpt4free` для анализа изображений:

1. **Обработка удаленного изображения**: 
   - Сначала с помощью библиотеки `requests` загружается изображение из удаленного URL.
   - Затем `client.chat.completions.create` отправляет запрос модели `g4f.models.default_vision`, передавая изображение в качестве параметра `image`.
   - Модель анализирует изображение и возвращает ответ в виде текста.

2. **Обработка локального изображения**:
   - В этом случае изображение загружается из локального файла с помощью `open` в режиме "rb" (чтение в двоичном формате).
   - Остальной процесс аналогичен обработке удаленного изображения.
   - После завершения обработки файл изображения необходимо закрыть с помощью `local_image.close()`.

## Использование

```python
import g4f
import requests

from g4f.client import Client

client = Client()

# Обработка удаленного изображения
remote_image = requests.get(
    "https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg",
    stream=True,
).content
response_remote = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=remote_image
)
print("Response for remote image:")
print(response_remote.choices[0].message.content)

print("\n" + "-"*50 + "\n")  # Разделитель

# Обработка локального изображения
local_image = open("docs/images/cat.jpeg", "rb")
response_local = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=local_image
)
print("Response for local image:")
print(response_local.choices[0].message.content)
local_image.close()  # Закрытие файла после использования
```

## Классы

### `Client`

**Описание**: Класс `Client` из библиотеки `g4f` предоставляет доступ к API `gpt4free` для отправки запросов и получения ответов от модели.

**Методы**:

- `chat.completions.create()`: Метод для отправки запроса модели `g4f.models.default_vision` с текстовыми сообщениями и изображением.

## Параметры

### `model` (str):

**Описание**: Параметр `model` в методе `client.chat.completions.create` указывает, какую модель использовать для обработки. В этом примере используется `g4f.models.default_vision` для анализа изображений.

### `messages` (list[dict]):

**Описание**: Параметр `messages` содержит список объектов, представляющих текстовые сообщения, которые отправляются модели. В данном случае используется список с одним элементом:
```python
messages=[
    {"role": "user", "content": "What are on this image?"}
]
```
- `role`: Указывает роль отправителя сообщения (в этом случае "user").
- `content`: Содержит текст сообщения.

### `image` (bytes):

**Описание**: Параметр `image` содержит изображение, которое необходимо анализировать. Изображение может быть передано в виде байтового потока (например, из `requests.get` или `open`).

## Примеры

### Пример 1: Обработка удаленного изображения

```python
import requests

from g4f.client import Client

client = Client()

remote_image = requests.get(
    "https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg",
    stream=True,
).content

response = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=remote_image
)

print(response.choices[0].message.content)
```

### Пример 2: Обработка локального изображения

```python
from g4f.client import Client

client = Client()

local_image = open("docs/images/cat.jpeg", "rb")

response = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=local_image
)

print(response.choices[0].message.content)

local_image.close()