# Модуль для работы с изображениями через Reka

## Обзор

Модуль предоставляет пример кода для взаимодействия с моделью Reka для анализа изображений. Он демонстрирует, как загрузить изображение и отправить запрос на его анализ, используя API `g4f`.

## Более подробно

Этот код предназначен для демонстрации возможностей анализа изображений с использованием модели `reka-core` через библиотеку `g4f`. Для успешной работы требуется наличие учетной записи и авторизация на сайте `chat.reka.ai`, а также наличие изображения `cat.jpeg` в директории `docs/images/`. Код отправляет изображение модели и запрашивает описание содержимого изображения.

## Классы

В данном модуле классы не используются.

## Функции

### `Client`

```python
from g4f.client import Client
```

### `create`

```python
completion = client.chat.completions.create(
    model = "reka-core",
    messages = [
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream = True,
    image = open("docs/images/cat.jpeg", "rb")
)
```

**Описание**: Функция выполняет запрос к модели `reka-core` для анализа изображения.

**Параметры**:

*   `model` (str): Имя используемой модели (`reka-core`).
*   `messages` (list): Список сообщений для отправки модели. В данном случае содержит запрос на анализ изображения.
*   `stream` (bool): Указывает, следует ли использовать потоковый режим получения ответа.
*   `image` (file): Объект файла изображения для анализа.

**Возвращает**:

*   `Generator[str, None, None]`: Генератор, возвращающий части ответа модели.

**Как работает функция**:

1.  Создается клиент для взаимодействия с API `g4f`.
2.  Формируется запрос к модели `reka-core` с указанием роли пользователя и содержимого запроса ("What can you see in the image ?").
3.  Открывается файл изображения `cat.jpeg` в режиме чтения байтов (`"rb"`).
4.  Вызывается метод `create` клиента `client.chat.completions` для отправки запроса на анализ изображения.
5.  Результат представляет собой генератор, из которого извлекаются части ответа модели.

**Примеры**:

```python
from g4f.client import Client
from g4f.Provider import Reka

client = Client(
    provider = Reka # Optional if you set model name to reka-core
)

completion = client.chat.completions.create(
    model = "reka-core",
    messages = [
        {
            "role": "user",
            "content": "What can you see in the image ?"
        }
    ],
    stream = True,
    image = open("docs/images/cat.jpeg", "rb")
)

for message in completion:
    print(message.choices[0].delta.content or "")
```
```python
from g4f.client import Client
from g4f.Provider import Reka

client = Client(
    provider = Reka # Optional if you set model name to reka-core
)

completion = client.chat.completions.create(
    model = "reka-core",
    messages = [
        {
            "role": "user",
            "content": "Опиши, что ты видишь на картинке?"
        }
    ],
    stream = True,
    image = open("docs/images/cat.jpeg", "rb")
)

for message in completion:
    print(message.choices[0].delta.content or "")
```

## Цикл for для обработки ответа

```python
for message in completion:
    print(message.choices[0].delta.content or "")
```

**Описание**: Цикл обрабатывает ответ модели, полученный в потоковом режиме.

**Как работает цикл**:

1.  Перебирает сообщения, возвращаемые генератором `completion`.
2.  Извлекает содержимое каждого сообщения (`message.choices[0].delta.content`).
3.  Выводит содержимое сообщения в консоль. Если содержимое отсутствует, выводит пустую строку.

**Примеры**:

```python
for message in completion:
    print(message.choices[0].delta.content or "")
```
```python
for message in completion:
    print(message.choices[0].delta.content or "")