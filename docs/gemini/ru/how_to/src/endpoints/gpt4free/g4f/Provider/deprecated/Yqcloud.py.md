### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет асинхронного провайдера `Yqcloud` для работы с моделью GPT-3.5 Turbo через API `chat9.yqcloud.top`. Он включает в себя функции для создания заголовков и полезной нагрузки запроса, а также для асинхронной генерации ответов от API.

Шаги выполнения
-------------------------
1. **Инициализация класса `Yqcloud`**:
   - Определяется класс `Yqcloud`, который наследуется от `AsyncGeneratorProvider`.
   - Указывается URL `https://chat9.yqcloud.top/`, поддержка `gpt-3.5-turbo` и статус `working`.

2. **Создание асинхронного генератора `create_async_generator`**:
   - Функция `create_async_generator` принимает параметры модели, сообщения, прокси и таймаут.
   - Создается асинхронная сессия с использованием `StreamSession` для отправки запросов.
   - Формируется `payload` с использованием функции `_create_payload` и отправляется POST-запрос к API `https://api.aichatos.cloud/api/generateStream`.
   - Полученные чанки данных декодируются и проверяются на наличие сообщения о блокировке IP-адреса.
   - Если IP-адрес заблокирован, вызывается исключение `RuntimeError`.
   - Чанки данных возвращаются как асинхронный генератор.

3. **Создание заголовков `_create_header`**:
   - Функция `_create_header` возвращает словарь с необходимыми HTTP-заголовками для запроса.
   - Заголовки включают `accept`, `content-type`, `origin` и `referer`.

4. **Создание полезной нагрузки `_create_payload`**:
   - Функция `_create_payload` принимает сообщения, системное сообщение, идентификатор пользователя и дополнительные аргументы.
   - Если `user_id` не предоставлен, генерируется случайный `user_id`.
   - Формируется словарь `payload` с использованием предоставленных параметров и функции `format_prompt`.
   - В `payload` включаются поля `prompt`, `network`, `system`, `withoutContext`, `stream` и `userId`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.Yqcloud import Yqcloud
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    messages: Messages = [
        {"role": "user", "content": "Hello, GPT!"}
    ]

    async for chunk in Yqcloud.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())