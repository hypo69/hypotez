### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `MetaAIAccount`, который является подклассом `MetaAI`. Класс предназначен для работы с Meta AI, требующей аутентификации. Он настраивает необходимые параметры, такие как `needs_auth`, `parent` и `image_models`, и предоставляет метод `create_async_generator` для создания асинхронного генератора, который взаимодействует с Meta AI через прокси и cookie.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются `AsyncResult`, `Messages`, `Cookies` из модуля `...typing`.
   - Импортируются `format_prompt` и `get_cookies` из модуля `..helper`.
   - Импортируется класс `MetaAI` из модуля `.MetaAI`.

2. **Определение класса `MetaAIAccount`**:
   - Класс `MetaAIAccount` наследуется от класса `MetaAI`.
   - Устанавливается атрибут `needs_auth` в `True`, указывая на необходимость аутентификации.
   - Устанавливается атрибут `parent` в `"MetaAI"`, обозначая родительский класс.
   - Устанавливается атрибут `image_models` в `["meta"]`, указывая поддерживаемые модели изображений.

3. **Определение метода `create_async_generator`**:
   - Этот метод является асинхронным и предназначен для создания асинхронного генератора, который взаимодействует с Meta AI.
   - Принимает параметры: `model` (строка), `messages` (сообщения), `proxy` (строка, опционально), `cookies` (cookie, опционально) и `kwargs` (дополнительные аргументы).
   - Функция извлекает cookie из домена ".meta.ai" если параметр `cookies` не определен.
   - Создается экземпляр класса `MetaAIAccount` с использованием прокси.
   - Вызывается метод `prompt` с форматированными сообщениями и cookie, итерируясь по чанкам, которые генерирует метод `prompt`.
   - Каждый чанк передается через `yield`, создавая асинхронный генератор.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAIAccount import MetaAIAccount
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    # Пример сообщений для отправки
    messages: Messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]

    # Создание асинхронного генератора
    generator = MetaAIAccount.create_async_generator(
        model="default",  # Укажите нужную модель
        messages=messages,
        proxy=None,  # Укажите прокси, если необходимо
        cookies=None  # Укажите cookie, если необходимо
    )

    # Асинхронный перебор чанков и их вывод
    async for chunk in await generator:
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())