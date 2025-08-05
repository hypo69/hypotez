# Модуль OpenAI Chat

## Обзор

Этот модуль предоставляет пример использования OpenAI Chat API для создания чат-бота с помощью модели `gpt-3.5-turbo`. Он демонстрирует базовые операции взаимодействия с OpenAI API, включая отправку запросов, получение ответов и обработку потоковых данных.

## Подробней

Модуль использует библиотеку `g4f` для взаимодействия с API. Библиотека `g4f` предоставляет классы `Client` и `Provider` для управления соединениями и настройками. В этом примере используется провайдер `OpenaiChat` для доступа к OpenAI Chat API. 

Код демонстрирует использование `RetryProvider` для обработки возможных ошибок и повторных попыток запросов. Также показано использование потокового режима (`stream=True`) для получения ответов чат-бота по частям.

## Функции

### `client.chat.completions.create`

**Назначение**: Эта функция отправляет запрос к OpenAI Chat API для получения завершения диалога.

**Параметры**:

- `model` (str): Идентификатор модели, с помощью которой генерируется текст. В этом примере используется `gpt-3.5-turbo`.
- `messages` (List[dict]): Список сообщений в диалоге. Каждое сообщение представлено словарем с ключами `role` и `content`.
- `stream` (bool): Указывает, нужно ли использовать потоковый режим.

**Возвращает**:
- `Generator[dict, None, None]`: Генератор, который выдает части ответа от модели.

**Как работает**:

Функция формирует запрос к OpenAI Chat API с указанными параметрами. В потоковом режиме она получает части ответа по мере их готовности. 

**Примеры**:

```python
messages = [
    {'role': 'user', 'content': 'Привет'}
]

response = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages, stream=True)

for message in response:
    print(message.choices[0].delta.content or "")
```

## Пример файла

```python
from g4f.client   import Client
from g4f.Provider import OpenaiChat, RetryProvider

# compatible countries: https://pastebin.com/UK0gT9cn
client = Client(
    proxies = {
        'http': 'http://username:password@host:port', # MUST BE WORKING OPENAI COUNTRY PROXY ex: USA
        'https': 'http://username:password@host:port' # MUST BE WORKING OPENAI COUNTRY PROXY ex: USA
    },
    provider = RetryProvider([OpenaiChat],
                             single_provider_retry=True, max_retries=5)
)

messages = [
    {'role': 'user', 'content': 'Hello'}
]

response = client.chat.completions.create(model='gpt-3.5-turbo',
                                     messages=messages, 
                                     stream=True)

for message in response:
    print(message.choices[0].delta.content or "")