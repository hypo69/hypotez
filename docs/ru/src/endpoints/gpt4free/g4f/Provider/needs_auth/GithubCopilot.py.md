# Модуль GithubCopilot

## Обзор

Модуль `GithubCopilot` предоставляет класс `GithubCopilot`, который является асинхронным провайдером для взаимодействия с GitHub Copilot. Он поддерживает потоковую передачу сообщений и требует аутентификации.

## Подробнее

Модуль предназначен для интеграции с GitHub Copilot через API. Он включает в себя создание сессий, получение токенов, управление беседами и отправку/получение сообщений.

## Классы

### `Conversation`

**Описание**: Класс представляет собой беседу с GitHub Copilot.

**Атрибуты**:
- `conversation_id` (str): Идентификатор беседы.

**Методы**:
- `__init__(self, conversation_id: str)`: Инициализирует объект беседы с заданным идентификатором.

### `GithubCopilot`

**Описание**: Класс для взаимодействия с GitHub Copilot в качестве асинхронного провайдера.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Добавляет функциональность выбора модели.

**Атрибуты**:
- `label` (str): Метка провайдера ("GitHub Copilot").
- `url` (str): URL GitHub Copilot ("https://github.com/copilot").
- `working` (bool): Указывает, что провайдер работает (True).
- `needs_auth` (bool): Указывает, что требуется аутентификация (True).
- `supports_stream` (bool): Указывает, что поддерживается потоковая передача (True).
- `default_model` (str): Модель по умолчанию ("gpt-4o").
- `models` (list[str]): Список поддерживаемых моделей (["gpt-4o", "o1-mini", "o1-preview", "claude-3.5-sonnet"]).

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        stream: bool = False,
        api_key: str = None,
        proxy: str = None,
        cookies: Cookies = None,
        conversation_id: str = None,
        conversation: Conversation = None,
        return_conversation: bool = False,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для взаимодействия с GitHub Copilot.

        Args:
            model (str): Используемая модель.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг потоковой передачи. По умолчанию `False`.
            api_key (str): API-ключ для аутентификации. По умолчанию `None`.
            proxy (str): Адрес прокси-сервера. По умолчанию `None`.
            cookies (Cookies): Cookie для аутентификации. По умолчанию `None`.
            conversation_id (str): Идентификатор беседы. По умолчанию `None`.
            conversation (Conversation): Объект беседы. По умолчанию `None`.
            return_conversation (bool): Флаг для возврата объекта беседы. По умолчанию `False`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, выдающий ответы от GitHub Copilot.

        Raises:
            Exception: В случае ошибок при создании сессии, получении токена или отправке сообщений.

        
        1. Функция определяет используемую модель, если она не была указана.
        2. Если cookies не предоставлены, функция пытается получить их для домена github.com.
        3. Функция создает асинхронную сессию `aiohttp.ClientSession` с заданными параметрами (прокси, cookies, заголовки).
        4. Если `api_key` не предоставлен, функция пытается получить его, отправляя POST-запрос на "https://github.com/github-copilot/chat/token".
        5. Функция устанавливает заголовки, включая `Authorization` с полученным `api_key`.
        6. Если `conversation_id` не предоставлен, функция создает новую беседу, отправляя POST-запрос на "https://api.individual.githubcopilot.com/github/chat/threads".
        7. Если `return_conversation` установлен в `True`, функция возвращает объект `Conversation` с полученным `conversation_id`.
        8. Формирует JSON-данные для отправки сообщения, включая контент, модель и режим.
        9. Отправляет POST-запрос на "https://api.individual.githubcopilot.com/github/chat/threads/{conversation_id}/messages" с JSON-данными и заголовками.
        10. Асинхронно читает ответ от GitHub Copilot построчно, извлекая содержимое из строк, начинающихся с "data: ".
        11. Возвращает извлеченное содержимое в виде асинхронного генератора.

        Внутренние функции: Отсутствуют.
        """
```

### Примеры использования

```python
# Пример: Создание асинхронного генератора для получения ответа от GitHub Copilot
messages = [{"role": "user", "content": "Hello, GitHub Copilot!"}]
api_key = "your_github_api_key"  # Замените на ваш фактический API-ключ

async def main():
    async for response in GithubCopilot.create_async_generator(model="gpt-4o", messages=messages, api_key=api_key):
        print(response)

# Запуск примера (необходимо в асинхронной среде)
# asyncio.run(main())