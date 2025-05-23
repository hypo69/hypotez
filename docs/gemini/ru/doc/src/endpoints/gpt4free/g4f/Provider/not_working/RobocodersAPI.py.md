# Провайдер Robocoders API
## Обзор
Данный модуль предоставляет реализацию `RobocodersAPI` - провайдера для взаимодействия с API Robocoders.ai. Используется для генерации текста и кода с помощью различных AI-моделей, таких как `GeneralCodingAgent`, `RepoAgent`, `FrontEndAgent`. 
## Подробнее 
Модуль `RobocodersAPI` предоставляет асинхронный генератор для получения ответов от AI-модели. Поддерживает историю сообщений, использует кэширование токенов и сессий для оптимизации производительности. 

## Классы
### `class RobocodersAPI(AsyncGeneratorProvider, ProviderModelMixin)`
**Описание**: Класс, реализующий провайдер для взаимодействия с API Robocoders.ai. 
**Наследует**: 
- `AsyncGeneratorProvider`: Базовый класс, предоставляющий асинхронный генератор для получения ответов.
- `ProviderModelMixin`: Миксин, добавляющий поддержку выбора модели.

**Атрибуты**:
- `label`: Строка, представляющая название провайдера.
- `url`: Строка, содержащая URL документации API Robocoders.ai.
- `api_endpoint`: Строка, содержащая URL конечной точки API для отправки запросов.
- `working`: Булево значение, указывающее на работоспособность провайдера.
- `supports_message_history`: Булево значение, указывающее на поддержку истории сообщений.
- `default_model`: Строка, указывающая на модель по умолчанию.
- `agent`: Список строк, содержащий доступные модели.
- `models`: Список строк, содержащий доступные модели (дублирует `agent`).
- `CACHE_DIR`: Объект `Path`, указывающий на каталог для кэширования токенов и сессий.
- `CACHE_FILE`: Объект `Path`, указывающий на файл для кэширования токенов и сессий.

**Методы**:
- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API Robocoders.ai.

**Параметры**:
- `model`: Строка, указывающая на модель, которую нужно использовать.
- `messages`: Список объектов `Message`, представляющий историю сообщений.
- `proxy`: Строка, указывающая на прокси-сервер.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Объект, представляющий результат асинхронного вызова.

**Вызывает исключения**:
- `Exception`: Если возникла ошибка при инициализации взаимодействия с API.
- `Exception`: Если возникла ошибка при отправке запроса.
- `Exception`: Если возникла ошибка при обработке ответа.
- `MissingRequirementsError`: Если не установлен пакет `beautifulsoup4`.
- `Exception`: Если возникла ошибка при получении токена.
- `Exception`: Если возникла ошибка при создании сессии.
- `Exception`: Если возникла ошибка при очистке кэша.

**Как работает**:
- Метод `create_async_generator` создает асинхронный генератор, который посылает запрос на API Robocoders.ai с помощью библиотеки `aiohttp`.
- Используется `ClientTimeout` для ограничения времени ожидания ответа от API.
- Загружает или создает токены доступа и сессии ID из кэша.
- Форматирует запрос с помощью `format_prompt`.
- Отправляет запрос с помощью `session.post` и обрабатывает ответ, получая сообщения из поля `args.content` или `message`.
- Обрабатывает ошибки:
    - 401 - Неавторизованный доступ, очищает кэш и выдает исключение.
    - 422 - Ошибка валидации, выдает исключение.
    - 500+ - Ошибка сервера, выдает исключение.
    - Другие ошибки - выдает исключение.
- Проверяет, достигнут ли лимит ресурсов, и автоматически продолжает диалог, если это необходимо.
- Декодирует полученные данные из JSON.
- Обрабатывает ошибки декодирования JSON.

- `_get_or_create_access_and_session(session: aiohttp.ClientSession)`: Статический метод, который загружает или создает токены доступа и сессии ID из кэша.
- `_fetch_and_cache_access_token(session: aiohttp.ClientSession) -> str`: Статический метод, который получает и кэширует токены доступа. 
- `_create_and_cache_session(session: aiohttp.ClientSession, access_token: str) -> str`: Статический метод, который создает и кэширует сессии ID. 
- `_save_cached_data(new_data: dict)`: Статический метод, который сохраняет новые данные в файл кэша.
- `_update_cached_data(updated_data: dict)`: Статический метод, который обновляет существующие данные в файле кэша.
- `_clear_cached_data()`: Статический метод, который удаляет файл кэша.
- `_get_cached_data() -> dict`: Статический метод, который получает все данные из файла кэша.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI
from hypotez.src.endpoints.gpt4free.g4f.Provider.helper import Message

# Создание инстанса провайдера
robocoders_api = RobocodersAPI()

# Создание сообщения
message = Message(role='user', content='Привет, как дела?')

# Вызов асинхронного генератора для получения ответа
async def get_response():
    async for response in robocoders_api.create_async_generator(model='GeneralCodingAgent', messages=[message]):
        print(response)

# Запуск асинхронного генератора
asyncio.run(get_response())
```

## Внутренние функции
### `_get_or_create_access_and_session(session: aiohttp.ClientSession)`
**Назначение**: Загружает или создает токены доступа и сессии ID из кэша.

**Параметры**:
- `session`: Объект `aiohttp.ClientSession` для взаимодействия с API.

**Возвращает**:
- `tuple[str, str]`: Кортеж, содержащий токен доступа и сессии ID.

**Как работает**:
- Проверяет, существует ли файл кэша.
- Если файл кэша существует, загружает данные из него.
- Если данные в кэше недействительны или отсутствуют, создает новые токены доступа и сессии ID.

### `_fetch_and_cache_access_token(session: aiohttp.ClientSession) -> str`
**Назначение**: Получает и кэширует токены доступа.

**Параметры**:
- `session`: Объект `aiohttp.ClientSession` для взаимодействия с API.

**Возвращает**:
- `str`: Токен доступа.

**Как работает**:
- Отправляет запрос на `https://api.robocoders.ai/auth` с помощью `session.get` и парсит полученный HTML с помощью `BeautifulSoup`.
- Извлекает токен доступа из элемента `pre` с id `token`.
- Сохраняет полученный токен в файл кэша.

### `_create_and_cache_session(session: aiohttp.ClientSession, access_token: str) -> str`
**Назначение**: Создает и кэширует сессии ID.

**Параметры**:
- `session`: Объект `aiohttp.ClientSession` для взаимодействия с API.
- `access_token`: Токен доступа.

**Возвращает**:
- `str`: Сессии ID.

**Как работает**:
- Отправляет запрос на `https://api.robocoders.ai/create-session` с помощью `session.get` и получает JSON-ответ.
- Извлекает сессии ID из поля `sid` в JSON-ответе.
- Сохраняет полученный сессии ID в файл кэша.

### `_save_cached_data(new_data: dict)`
**Назначение**: Сохраняет новые данные в файл кэша.

**Параметры**:
- `new_data`: Словарь с новыми данными для сохранения.

**Как работает**:
- Создает директорию для кэша, если она не существует.
- Создает файл кэша, если он не существует.
- Записывает новые данные в файл кэша в формате JSON.

### `_update_cached_data(updated_data: dict)`
**Назначение**: Обновляет существующие данные в файле кэша.

**Параметры**:
- `updated_data`: Словарь с данными, которые нужно обновить.

**Как работает**:
- Загружает данные из файла кэша, если он существует.
- Обновляет данные в словаре с помощью `data.update(updated_data)`.
- Записывает обновленные данные в файл кэша в формате JSON.

### `_clear_cached_data()`
**Назначение**: Удаляет файл кэша.

**Как работает**:
- Проверяет, существует ли файл кэша.
- Если файл кэша существует, удаляет его.

### `_get_cached_data() -> dict`
**Назначение**: Получает все данные из файла кэша.

**Возвращает**:
- `dict`: Словарь с данными из файла кэша.

**Как работает**:
- Проверяет, существует ли файл кэша.
- Если файл кэша существует, загружает данные из него в формате JSON.
- Возвращает пустой словарь, если файл кэша не существует или не удается его прочитать.