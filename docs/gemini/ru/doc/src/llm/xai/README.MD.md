# xAI API Client

## Обзор

Этот репозиторий содержит Python-клиент для взаимодействия с API xAI. Клиент разработан для упрощения процесса отправки запросов к API xAI, включая как стандартные, так и потоковые запросы.

## Возможности

- **Аутентификация**: Безопасная аутентификация ваших запросов с использованием вашего ключа API xAI.
- **Завершение чата**: Генерация ответов от моделей xAI с помощью метода `chat_completion`.
- **Потоковые ответы**: Потоковая передача ответов от моделей xAI с помощью метода `stream_chat_completion`.

## Установка

Для использования этого клиента вам необходимо иметь установленный Python на вашей системе. Вы можете установить необходимые зависимости с помощью pip:

```bash
pip install requests
```

## Использование

### Инициализация

Сначала инициализируйте класс `XAI` с помощью вашего ключа API:

```python
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш фактический ключ API
xai = XAI(api_key)
```

### Завершение чата

Чтобы получить ответ от модели xAI, используйте метод `chat_completion`:

```python
messages = [
    {
        "role": "system",
        "content": "Вы - Грок, чат-бот, вдохновленный автостопом по галактике."
    },
    {
        "role": "user",
        "content": "Какой ответ на главный вопрос жизни, вселенной и всего такого?"
    }
]

completion_response = xai.chat_completion(messages)
print("Не потоковый ответ:", completion_response)
```

### Потоковое завершение чата

Чтобы получить потоковые ответы от модели xAI, используйте метод `stream_chat_completion`:

```python
stream_response = xai.stream_chat_completion(messages)
print("Потоковый ответ:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Пример

Вот полный пример того, как использовать клиент `XAI`:

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш фактический ключ API
xai = XAI(api_key)

messages = [
    {
        "role": "system",
        "content": "Вы - Грок, чат-бот, вдохновленный автостопом по галактике."
    },
    {
        "role": "user",
        "content": "Какой ответ на главный вопрос жизни, вселенной и всего такого?"
    }
]

# Не потоковый запрос
completion_response = xai.chat_completion(messages)
print("Не потоковый ответ:", completion_response)

# Потоковый запрос
stream_response = xai.stream_chat_completion(messages)
print("Потоковый ответ:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

## Вклад

Вклад приветствуется! Не стесняйтесь отправлять запрос на вытягивание или открывать проблему, если вы столкнулись с какими-либо проблемами или у вас есть предложения по улучшениям.

## Лицензия

Этот проект лицензирован под лицензией MIT. См. файл [LICENSE](LICENSE) для получения более подробной информации.

## Благодарности

- Спасибо xAI за предоставление API, который поддерживает этот клиент.
- Вдохновлено необходимостью простого и эффективного способа взаимодействия с мощными моделями xAI.

---

Дополнительную информацию см. в [документации API xAI](https://api.x.ai/docs).

https://console.x.ai/team/4cd3d20f-f1d9-4389-9ffb-87c855e5ffac
https://docs.x.ai/docs