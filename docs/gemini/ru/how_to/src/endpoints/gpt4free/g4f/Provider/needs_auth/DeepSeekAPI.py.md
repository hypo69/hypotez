### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `DeepSeekAPI`, который является асинхронным провайдером для работы с API DeepSeek. Он реализует аутентификацию через браузер и предоставляет методы для создания чат-сессий и получения ответов от модели.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `os`, `json`, `time`, `asyncio` и типы из `typing`.
   - Импортируются классы и функции из других модулей проекта, такие как `AsyncAuthedProvider`, `ProviderModelMixin`, `get_last_user_message`, `get_nodriver`, `AuthResult`, `RequestLogin`, `Reasoning`, `JsonConversation`, `FinishReason`, `AsyncResult`, `Messages`.
   - Проверяется наличие установленной библиотеки `dsk.api` и импортируется класс `DeepSeekAPI` из нее.

2. **Определение класса `DeepSeekAPI`**:
   - Класс `DeepSeekAPI` наследуется от `AsyncAuthedProvider` и `ProviderModelMixin`.
   - Указываются атрибуты класса:
     - `url` - URL для доступа к API DeepSeek.
     - `working` - флаг, указывающий, работает ли провайдер (зависит от наличия `dsk.api`).
     - `needs_auth` - флаг, указывающий, требуется ли аутентификация.
     - `use_nodriver` - флаг, указывающий, используется ли бездрайверный режим.
     - `_access_token` - атрибут для хранения токена доступа.
     - `default_model` - модель, используемая по умолчанию.
     - `models` - список поддерживаемых моделей.

3. **Реализация метода `on_auth_async`**:
   - Метод `on_auth_async` выполняет аутентификацию пользователя.
   - Если браузер еще не инициализирован, он инициализируется с помощью `get_nodriver`.
   - Генерируется `RequestLogin` для запроса URL аутентификации.
   - Определяется асинхронная функция `callback`, которая периодически проверяет наличие токена доступа в `localStorage` браузера и сохраняет его в `cls._access_token`.
   - Получаются аргументы для запуска браузера с помощью `get_args_from_nodriver`, передавая URL, прокси и функцию `callback`.
   - Генерируется `AuthResult` с токеном доступа и аргументами.

4. **Реализация метода `create_authed`**:
   - Метод `create_authed` создает аутентифицированный запрос к API DeepSeek.
   - Инициализируется API с использованием токена доступа из `auth_result`.
   - Если отсутствует `conversation`, создается новая чат-сессия с помощью `api.create_chat_session()` и инициализируется `JsonConversation`.
   - Генерируется объект `conversation`.
   - Выполняется цикл по чанкам, возвращаемым из `api.chat_completion()`:
     - Если `chunk['type'] == 'thinking'`, генерируется `Reasoning` с информацией о процессе обдумывания.
     - Если `chunk['type'] == 'text'`, генерируется текст ответа.
     - Если `chunk['finish_reason']`, генерируется `FinishReason` с причиной завершения.

Пример использования
-------------------------

```python
import asyncio
import os
from src.endpoints.gpt4free.g4f.Provider.needs_auth.DeepSeekAPI import DeepSeekAPI
from src.endpoints.gpt4free.g4f.providers.response import AuthResult, JsonConversation
from src.typing import Messages

async def main():
    # Укажите URL для входа в систему, если он не задан в переменных окружения
    # os.environ["G4F_LOGIN_URL"] = "your_login_url_here"

    # Пример использования on_auth_async
    auth_iterator = DeepSeekAPI.on_auth_async()
    auth_result = None
    async for item in auth_iterator:
        print(f"Auth step: {item}")
        if isinstance(item, AuthResult):
            auth_result = item
            break

    if not auth_result:
        print("Authentication failed.")
        return

    # Пример использования create_authed
    model = "deepseek-v3"
    messages: Messages = [{"role": "user", "content": "Hello, DeepSeek!"}]
    conversation = JsonConversation(chat_id="your_chat_id")  # Замените на существующий chat_id, если необходимо

    result_iterator = DeepSeekAPI.create_authed(
        model=model,
        messages=messages,
        auth_result=auth_result,
        conversation=conversation,
        web_search=False
    )

    async for item in result_iterator:
        print(f"Response item: {item}")

if __name__ == "__main__":
    asyncio.run(main())
```