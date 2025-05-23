## Как использовать этот блок кода
========================================================================================

### Описание
-------------------------
Этот фрагмент кода представляет собой класс `ChatGptEs`, который реализует асинхронный генератор для взаимодействия с API ChatGPT.es. 

Класс использует библиотеку `curl_cffi` для обхода Cloudflare и выполнения запросов к API. Он также включает в себя логику для обработки ответов API, включая извлечение данных, проверку ошибок и обработку различных форматов ответов. 

### Шаги выполнения
-------------------------
1. **Инициализация класса `ChatGptEs`**: Создается экземпляр класса `ChatGptEs`.
2. **Получение модели**: Вызывается метод `get_model` для получения модели ChatGPT, доступной на `ChatGPT.es`.
3. **Формирование запроса**: Формируется запрос с использованием `SYSTEM_PROMPT` и `format_prompt`, который преобразует список сообщений в текстовый формат для отправки в API.
4. **Инициализация сессии `curl_cffi`**: Создается сессия `curl_cffi` с заданными заголовками и прокси (если указано).
5. **Получение `nonce` и `post_id`**: Выполняется GET-запрос к URL `ChatGPT.es` для извлечения `nonce` и `post_id`, необходимых для отправки запроса.
6. **Извлечение `nonce`**: Применяется несколько регулярных выражений для извлечения `nonce` из HTML-кода ответа.
7. **Извлечение `post_id`**: Применяется несколько регулярных выражений для извлечения `post_id` из HTML-кода ответа.
8. **Подготовка данных**: Формируется словарь с параметрами для POST-запроса.
9. **Отправка запроса**: Выполняется POST-запрос к API-endpoint `ChatGPT.es` с использованием подготовленных данных.
10. **Обработка ответа**: Проверяется статус-код ответа, извлекаются данные из ответа и возвращаются в виде асинхронного генератора.

### Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.ChatGptEs import ChatGptEs
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"},
]

async def main():
    provider = ChatGptEs()
    async for response in provider.create_async_generator(model="gpt-4o", messages=messages):
        print(f"Ответ: {response}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Описание примера**:
- Создается экземпляр класса `ChatGptEs`.
- Создается список сообщений `messages`.
- В цикле `async for` итерация выполняется по асинхронному генератору, который возвращает ответы от `ChatGPT.es`.
- Ответы выводим на экран.