# Клиент API xAI

## Обзор

Этот репозиторий содержит Python-клиент для взаимодействия с API xAI. Клиент разработан для упрощения процесса отправки запросов к API xAI, включая как стандартные, так и потоковые запросы.

## Возможности

*   **Аутентификация**: Безопасная аутентификация ваших запросов с использованием ключа API xAI.
*   **Завершение чата**: Генерация ответов от моделей xAI с использованием метода `chat_completion`.
*   **Потоковая передача ответов**: Потоковая передача ответов от моделей xAI с использованием метода `stream_chat_completion`.

## Установка

Для использования этого клиента вам необходимо установить Python на вашей системе. Вы можете установить необходимые зависимости с помощью pip:

```bash
pip install requests
```

## Использование

### Инициализация

Сначала инициализируйте класс `XAI` с вашим API-ключом:

```python
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш реальный API-ключ
xai = XAI(api_key)
```
**Для работы с API XAI необходимо зарегистрироваться и получить API ключ**
### Завершение чата

Для генерации ответа от модели xAI используйте метод `chat_completion`:

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

### Потоковая передача завершения чата

Для потоковой передачи ответов от модели xAI используйте метод `stream_chat_completion`:

```python
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

### Пример

Вот полный пример использования клиента `XAI`:

```python
import json
from xai import XAI

api_key = "your_api_key_here"  # Замените на ваш реальный ключ API
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

# Непотоковый запрос
completion_response = xai.chat_completion(messages)
print("Non-streaming response:", completion_response)

# Потоковый запрос
stream_response = xai.stream_chat_completion(messages)
print("Streaming response:")
for line in stream_response:
    if line.strip():
        print(json.loads(line))
```

### Настройка
Укажите свой API ключ в параметре `api_key`.

Замените `your_api_key_here` на свой личный ключ.
Строку:
```"content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."```
Можно изменить, чтобы поменять роль chat gpt.

## Вклад

Вклад приветствуется! Не стесняйтесь отправлять pull request или открывать issue, если вы столкнулись с какими-либо проблемами или имеете предложения по улучшению.

## Лицензия

Этот проект лицензирован под MIT License. Подробности смотрите в файле [LICENSE](../../LICENSE).

## Благодарности

*   Спасибо xAI за предоставление API, которое делает возможным работу этого клиента.
*   Вдохновлен необходимостью простого и эффективного способа взаимодействия с мощными моделями xAI.

---

Для получения дополнительной информации, пожалуйста, обратитесь к [документации API xAI](https://api.x.ai/docs).
https://console.x.ai/team/4cd3d20f-f1d9-4389-9ffb-87c855e5ffac
https://docs.x.ai/docs

---

Уберите лишнее форматирование. оставьте чисто синтаксис Markdown
Нужно указать, что для работы с API XAI - необходимо создать учетную запись, и получить ключ
В остальном все хорошо