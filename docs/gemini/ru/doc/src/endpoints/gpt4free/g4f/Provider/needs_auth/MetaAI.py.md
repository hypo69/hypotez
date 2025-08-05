# Модуль MetaAI
## Обзор

Модуль `MetaAI` реализует асинхронный генератор, взаимодействующий с API Meta AI для генерации ответов на запросы. 

## Подробнее

Модуль обеспечивает реализацию класса `MetaAI`, который наследует функциональность от `AsyncGeneratorProvider` и `ProviderModelMixin`.

## Классы

### `MetaAI`

**Описание**: Класс `MetaAI` обеспечивает асинхронную генерацию ответов от модели Meta AI.

**Наследует**:
- `AsyncGeneratorProvider`: предоставляет асинхронный генератор для получения ответов от модели.
- `ProviderModelMixin`: обеспечивает доступ к модели и ее настройкам.

**Атрибуты**:
- `label`: (str) - Название провайдера (Meta AI).
- `url`: (str) - URL-адрес API Meta AI.
- `working`: (bool) - Флаг доступности провайдера (True - доступен).
- `default_model`: (str) - Название модели по умолчанию (meta-ai).
- `session`: (ClientSession) - Сессия HTTP-запросов.
- `cookies`: (Cookies) - Словарь с куки-файлами для авторизации.
- `access_token`: (str) - Токен доступа к API Meta AI.

**Методы**:

- `__init__(self, proxy: str = None, connector: BaseConnector = None)`: Конструктор класса. Создает объект сессии `ClientSession` с использованием предоставленного прокси или стандартного коннектора.
- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Статический метод для создания асинхронного генератора. Форматирует сообщения для запроса, создает объект `MetaAI` и запускает генератор ответов.
- `update_access_token(self, birthday: str = "1999-01-01")`: Обновляет токен доступа к API Meta AI, используя предоставленную дату рождения.
- `prompt(self, message: str, cookies: Cookies = None) -> AsyncResult`: Асинхронный генератор ответов на запрос. Выполняет запрос к API Meta AI, отправляя сообщение, и возвращает поток ответов.
- `update_cookies(self, cookies: Cookies = None)`: Обновляет куки-файлы для сессии HTTP-запросов.
- `fetch_sources(self, fetch_id: str) -> Sources`: Получает ссылки на источники информации, связанные с ответом, используя ID запроса.
- `extract_value(text: str, key: str = None, start_str = None, end_str = '\',') -> str`: Статический метод для извлечения значения из строки по ключу или начальной и конечной строкам.
- `generate_offline_threading_id() -> str`: Статический метод для генерации уникального ID для запроса.

**Принцип работы**:
Класс `MetaAI` обеспечивает взаимодействие с API Meta AI. 

- При инициализации устанавливается соединение с API Meta AI, используя сессию HTTP-запросов.
-  `update_access_token` - функция получения токена доступа.
-  `prompt` - выполняет асинхронный запрос к API Meta AI. 

## Функции

### `generate_offline_threading_id() -> str`

**Назначение**: Генерация уникального ID для запроса к API Meta AI.

**Параметры**:
- Нет

**Возвращает**:
- `str`: Сгенерированный ID.

**Как работает**:
- Использует текущее время в миллисекундах и случайное 64-битное число для создания уникального ID.

**Примеры**:
```python
>>> generate_offline_threading_id()
'16857684700002335296'
```

### `Sources`

**Описание**: Класс `Sources` представляет собой набор источников информации, связанных с ответом от модели Meta AI.

**Атрибуты**:
- `list`: (List[Dict[str, str]]) - Список объектов с заголовком (`title`) и ссылкой (`link`) на источник информации.

**Методы**:
- `__str__(self) -> str`: Преобразует объект `Sources` в строку, представляющую ссылки на источники информации.

**Как работает**:
- Класс `Sources` хранит список ссылок на источники, предоставляемых моделью Meta AI.
- Метод `__str__` формирует строку с заголовком и ссылкой для каждого источника.

**Примеры**:
```python
>>> sources = Sources([{'title': 'Wikipedia', 'link': 'https://en.wikipedia.org/wiki/Artificial_intelligence'}])
>>> print(sources)

[Wikipedia](https://en.wikipedia.org/wiki/Artificial_intelligence)
```


## Параметры класса

- `proxy` (str, optional): Прокси-сервер для HTTP-запросов. По умолчанию `None`.
- `connector` (BaseConnector, optional): HTTP-коннектор для сессии запросов. По умолчанию `None`.

## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.MetaAI import MetaAI

# Создание объекта MetaAI с использованием прокси-сервера
meta_ai = MetaAI(proxy="http://127.0.0.1:8080")

# Отправка запроса к модели Meta AI
async for response in meta_ai.prompt("What is the meaning of life?"):
    print(response)

# Получение ссылок на источники информации
sources = await meta_ai.fetch_sources("your_fetch_id")
print(sources)
```