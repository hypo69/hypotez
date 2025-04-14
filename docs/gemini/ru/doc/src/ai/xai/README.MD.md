# Документация для модуля xAI API Client

## Обзор

Этот модуль представляет собой Python-клиент для взаимодействия с xAI API. Он упрощает процесс отправки запросов к xAI API, включая как стандартные, так и потоковые запросы.

## Подробнее

Модуль предоставляет удобный интерфейс для аутентификации и выполнения запросов к моделям xAI.  Он позволяет генерировать ответы от моделей xAI с использованием метода `chat_completion` и получать потоковые ответы с использованием метода `stream_chat_completion`.

## Содержание

- [Основные возможности](#основные-возможности)
- [Установка](#установка)
- [Использование](#использование)
    - [Инициализация](#инициализация)
    - [Завершение чата](#завершение-чата)
    - [Потоковое завершение чата](#потоковое-завершение-чата)
- [Пример](#пример)
- [Вклад](#вклад)
- [Лицензия](#лицензия)
- [Благодарности](#благодарности)

## Основные возможности

- **Аутентификация**: Безопасная аутентификация запросов с использованием xAI API key.
- **Завершение чата**: Генерация ответов от моделей xAI с использованием метода `chat_completion`.
- **Потоковые ответы**: Получение потоковых ответов от моделей xAI с использованием метода `stream_chat_completion`.

## Установка

Для использования этого клиента необходимо установить Python.  Вы можете установить необходимые зависимости с помощью pip:

```bash
pip install requests
```

## Использование

### Инициализация

Сначала инициализируйте класс `XAI` с вашим API key:

```python
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш фактический API key
xai = XAI(api_key)
```

### Завершение чата

Чтобы сгенерировать ответ от модели xAI, используйте метод `chat_completion`:

```python
messages = [
    {
        "role": "system",
        "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
    },
    {
        "role": "user",
        "content": "What is the answer to life and universe?"
    }
]

completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)
```

### Потоковое завершение чата

Чтобы получать потоковые ответы от модели xAI, используйте метод `stream_chat_completion`:

```python
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Пример

Полный пример использования клиента `XAI`:

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш фактический API key
xai = XAI(api_key)

messages = [
    {
        "role": "system",
        "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
    },
    {
        "role": "user",
        "content": "What is the answer to life and universe?"
    }
]

# Non-streaming request
completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)

# Streaming request
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Вклад

Приветствуются любые вклады! Пожалуйста, не стесняйтесь отправлять pull request или открывать issue, если у вас возникнут какие-либо проблемы или предложения по улучшению.

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT.  Подробнее см. файл [LICENSE](LICENSE).

## Благодарности

- Спасибо xAI за предоставление API, который лежит в основе этого клиента.
- Вдохновлен потребностью в простом и эффективном способе взаимодействия с мощными моделями xAI.

---

Для получения дополнительной информации обратитесь к [документации xAI API](https://api.x.ai/docs).

https://console.x.ai/team/4cd3d20f-f1d9-4389-9ffb-87c855e5ffac
https://docs.x.ai/docs