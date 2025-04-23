# Документация для xAI API Client

## Обзор

Этот репозиторий содержит Python клиент для взаимодействия с xAI API. Клиент разработан, чтобы упростить процесс отправки запросов к xAI API, включая как стандартные, так и потоковые запросы.

## Особенности

- **Аутентификация**: Безопасная аутентификация ваших запросов с использованием вашего ключа xAI API.
- **Chat Completion**: Генерация ответов от моделей xAI с использованием метода `chat_completion`.
- **Streaming Responses**: Потоковая передача ответов от моделей xAI с использованием метода `stream_chat_completion`.

## Установка

Для использования этого клиента у вас должен быть установлен Python. Вы можете установить необходимые зависимости, используя pip:

```bash
pip install requests
```

## Использование

### Инициализация

Сначала инициализируйте класс `XAI` с вашим ключом API:

```python
from xai import XAI

api_key = "your_api_key_here"  # Замените своим фактическим ключом API
xai = XAI(api_key)
```

### Chat Completion

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

### Streaming Chat Completion

Чтобы передавать ответы от модели xAI в потоковом режиме, используйте метод `stream_chat_completion`:

```python
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Пример

Вот полный пример того, как использовать клиент `XAI`:

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Замените своим фактическим ключом API
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

Вклады приветствуются! Пожалуйста, не стесняйтесь отправлять pull request или открывать issue, если у вас возникнут какие-либо проблемы или предложения по улучшению.

## Лицензия

Этот проект лицензирован в соответствии с лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

## Благодарности

- Спасибо xAI за предоставление API, который питает этот клиент.
- Вдохновлен потребностью в простом и эффективном способе взаимодействия с мощными моделями xAI.

---

Для получения дополнительной информации, пожалуйста, обратитесь к [документации xAI API](https://api.x.ai/docs).

https://console.x.ai/team/4cd3d20f-f1d9-4389-9ffb-87c855e5ffac
https://docs.x.ai/docs