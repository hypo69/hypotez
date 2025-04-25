## Как использовать HuggingChat
=========================================================================================

Описание
-------------------------
HuggingChat — это асинхронный провайдер для работы с моделями Hugging Face, предоставляющий доступ к  моделям  как для генерации текста, так и для работы с изображениями.

Шаги выполнения
-------------------------
1. **Инициализация**: Импортируй `HuggingChat`  и создай экземпляр класса.
2. **Авторизация**: Вызови метод `on_auth_async`  для авторизации в сервисе.
3. **Создание сессии**:  Создай новую сессию с помощью метода `create_authed`,  указав модель и сообщения.
4. **Отправка запроса**:  Отправь сообщение модели с помощью метода `create_authed`, используя созданную сессию.
5. **Обработка ответа**:  Получи ответ от модели в виде потока текста или объекта `ImageResponse`.
6. **Закрытие сессии**: Закрой сессию после завершения работы с ней.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingChat import HuggingChat

async def main():
    # Инициализируем HuggingChat
    provider = HuggingChat()

    # Авторизуемся в сервисе
    async for auth_result in provider.on_auth_async():
        # Обработка результата авторизации
        if isinstance(auth_result, RequestLogin):
            # Если нужна авторизация, запросите у пользователя данные
            auth_result = await provider.on_auth_async(username="user@example.com", password="password")
            print(f"Авторизован: {auth_result}")
        else:
            print(f"Авторизован: {auth_result}")

    # Создание сессии с моделью "gpt-neo-2.7B"
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
    ]
    async for response in provider.create_authed(model="gpt-neo-2.7B", messages=messages, auth_result=auth_result):
        print(response)

    # Закрытие сессии 
    # ...

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```