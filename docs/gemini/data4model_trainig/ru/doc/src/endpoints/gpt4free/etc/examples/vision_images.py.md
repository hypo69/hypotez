# Модуль для обработки изображений с использованием g4f (GPT4Free)

## Обзор

Этот модуль демонстрирует, как использовать библиотеку `g4f` для анализа изображений с использованием модели GPT4Free vision. Он показывает примеры обработки как удаленных, так и локальных изображений.
Модуль использует клиент `g4f.client.Client` для взаимодействия с API и отправки запросов на анализ изображений.

## Подробней

Этот код демонстрирует использование библиотеки `g4f` для обработки изображений. Он содержит примеры обработки удаленных и локальных изображений. 
В данном случае используется модель `g4f.models.default_vision` для анализа содержимого изображений и получения ответов на вопрос "Что на этом изображении?".

## Функции

### `Client()`
**Описание**: Создает экземпляр класса `Client` из модуля `g4f.client`. Этот класс используется для взаимодействия с API g4f.

**Принцип работы**:
- Создает клиент, который будет использоваться для отправки запросов к API.

### `requests.get(url: str, stream: bool = True)`

**Описание**: Функция отправляет HTTP GET-запрос по указанному URL и возвращает объект `Response`.

**Параметры**:
- `url` (str): URL, по которому отправляется запрос.
- `stream` (bool): Если `True`, содержимое ответа не загружается сразу, а доступно как поток. По умолчанию `True`.

**Возвращает**:
- `Response`: Объект ответа, содержащий данные, возвращенные сервером.

**Принцип работы**:
- Функция отправляет GET-запрос к указанному URL, чтобы получить содержимое изображения. `stream=True` позволяет загружать изображение потоком, что полезно для больших файлов.

**Примеры**:
```python
import requests
# Пример вызова функции requests.get для получения изображения
remote_image = requests.get("https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg", stream=True).content
```

### `client.chat.completions.create(model: str, messages: list, image: bytes | file)`

**Описание**: Функция отправляет запрос на создание завершения чата с использованием указанной модели и изображения.

**Параметры**:
- `model` (str): Идентификатор модели, используемой для анализа изображения.
- `messages` (list): Список сообщений, содержащих контекст запроса. В данном случае содержит вопрос "Что на этом изображении?".
- `image` (bytes | file): Данные изображения в виде байтов или открытого файла.

**Возвращает**:
- `ChatCompletion`: Объект завершения чата, содержащий ответ модели.

**Принцип работы**:
- Функция отправляет запрос к API для анализа изображения с использованием указанной модели и сообщения. Она возвращает ответ, содержащий анализ изображения.

**Примеры**:
```python
import g4f
from g4f.client import Client

client = Client()

# Пример вызова функции create для обработки удаленного изображения
remote_image = requests.get("https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg", stream=True).content
response_remote = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=remote_image
)

# Пример вызова функции create для обработки локального изображения
local_image = open("docs/images/cat.jpeg", "rb")
response_local = client.chat.completions.create(
    model=g4f.models.default_vision,
    messages=[
        {"role": "user", "content": "What are on this image?"}
    ],
    image=local_image
)
local_image.close()
```

### Обработка удаленного изображения

1.  **Загрузка изображения**:
    *   Используется `requests.get` для загрузки изображения по URL. Атрибут `stream=True` позволяет загружать изображение потоком, что уменьшает использование памяти.
    *   `remote_image = requests.get("https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/cat.jpeg", stream=True).content`

2.  **Создание запроса**:
    *   Создается запрос к модели `g4f.models.default_vision` через метод `client.chat.completions.create`.
    *   В запросе передается изображение и сообщение с вопросом о содержимом изображения.
    *   `response_remote = client.chat.completions.create(model=g4f.models.default_vision, messages=[{"role": "user", "content": "What are on this image?"}], image=remote_image)`

3.  **Вывод ответа**:
    *   Выводится ответ модели, содержащий описание содержимого изображения.
    *   `print(response_remote.choices[0].message.content)`

### Обработка локального изображения

1.  **Открытие изображения**:
    *   Локальное изображение открывается в режиме чтения байтов (`"rb"`).
    *   `local_image = open("docs/images/cat.jpeg", "rb")`

2.  **Создание запроса**:
    *   Аналогично обработке удаленного изображения, создается запрос к модели `g4f.models.default_vision` через метод `client.chat.completions.create`.
    *   В запросе передается открытый файл изображения и сообщение с вопросом о содержимом изображения.
    *   `response_local = client.chat.completions.create(model=g4f.models.default_vision, messages=[{"role": "user", "content": "What are on this image?"}], image=local_image)`

3.  **Вывод ответа**:
    *   Выводится ответ модели, содержащий описание содержимого изображения.
    *   `print(response_local.choices[0].message.content)`

4.  **Закрытие файла**:
    *   После использования файл изображения закрывается.
    *   `local_image.close()`