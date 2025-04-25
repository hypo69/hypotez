# Модуль `Hashnode`

## Обзор

Модуль `Hashnode` предоставляет класс `Hashnode`, который реализует асинхронный генератор для взаимодействия с API сервиса Hashnode для получения ответов от модели GPT-3.5 Turbo. 

## Подробнее

Класс `Hashnode` наследует от класса `AsyncGeneratorProvider` и предоставляет следующие возможности:

- Асинхронный генератор, который возвращает текст ответа чат-бота.
- Поддержка поиска в Интернете (`search_type = "websearch"`).
- Поддержка истории сообщений.
- Поддержка модели GPT-3.5 Turbo.

## Классы

### `class Hashnode`

**Описание**: Класс, реализующий асинхронный генератор для взаимодействия с API сервиса Hashnode для получения ответов от модели GPT-3.5 Turbo. 

**Наследует**: `AsyncGeneratorProvider`

**Атрибуты**:

- `url` (str): Базовый URL сервиса Hashnode.
- `working` (bool): Флаг, указывающий на доступность сервиса.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.
- `_sources` (list): Список источников для поиска в Интернете.


**Методы**:

- `create_async_generator(model: str, messages: Messages, search_type: str = SearchTypes.websearch, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от модели GPT-3.5 Turbo с заданными параметрами.

    **Параметры**:
    - `model` (str): Имя модели, например, "gpt-3.5-turbo".
    - `messages` (Messages): Список сообщений в истории чата.
    - `search_type` (str): Тип поиска, например, "websearch".
    - `proxy` (str): Прокси-сервер для запросов.
    - `**kwargs`: Дополнительные аргументы для запроса.

    **Возвращает**:
    - `AsyncResult`: Асинхронный результат, который содержит асинхронный генератор, генерирующий текст ответа чат-бота.

- `get_sources() -> list`: Возвращает список источников для поиска в Интернете.


## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        search_type: str = SearchTypes.websearch,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор для получения ответов от модели GPT-3.5 Turbo с заданными параметрами.

        Args:
            model (str): Имя модели, например, "gpt-3.5-turbo".
            messages (Messages): Список сообщений в истории чата.
            search_type (str): Тип поиска, например, "websearch".
            proxy (str): Прокси-сервер для запросов.
            **kwargs: Дополнительные аргументы для запроса.

        Returns:
            AsyncResult: Асинхронный результат, который содержит асинхронный генератор, генерирующий текст ответа чат-бота.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "Accept": "*/*",
            "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/rix",
            "Content-Type": "application/json",
            "Origin": cls.url,
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }
        async with ClientSession(headers=headers) as session:
            prompt = messages[-1]["content"]
            cls._sources = []
            if search_type == "websearch":
                async with session.post(
                    f"{cls.url}/api/ai/rix/search",
                    json={"prompt": prompt},
                    proxy=proxy,
                ) as response:
                    response.raise_for_status()
                    cls._sources = (await response.json())["result"]
            data = {
                "chatId": get_random_hex(),
                "history": messages,
                "prompt": prompt,
                "searchType": search_type,
                "urlToScan": None,
                "searchResults": cls._sources,
            }
            async with session.post(
                f"{cls.url}/api/ai/rix/completion",
                json=data,
                proxy=proxy,
            ) as response:
                response.raise_for_status()
                async for chunk in response.content.iter_any():
                    if chunk:
                        yield chunk.decode()
```

**Как работает функция**:

1. **Настройка заголовков запроса**:  Функция определяет набор заголовков для HTTP-запроса к API сервиса Hashnode, чтобы имитировать браузер пользователя.
2. **Создание асинхронного сеанса**:  Создается асинхронный сеанс `ClientSession` с заданными заголовками для отправки запросов к API.
3. **Получение последнего сообщения**: Извлекается последнее сообщение из истории чата (`messages[-1]["content"]`).
4. **Поиск в Интернете (опционально)**: Если `search_type` установлен в `"websearch"`, функция отправляет POST-запрос к API `"/api/ai/rix/search"` с последним сообщением в качестве запроса.  Результат поиска (`cls._sources`) сохраняется в атрибут класса `_sources`.
5. **Формирование данных для запроса**:  Создается словарь `data` с необходимой информацией для запроса к API `"/api/ai/rix/completion"`, включая:
    - `chatId`: случайный уникальный идентификатор для чата.
    - `history`:  история сообщений.
    - `prompt`:  последнее сообщение в истории чата.
    - `searchType`: тип поиска (например, `"websearch"`).
    - `urlToScan`:  URL-адрес для сканирования (не используется в этом случае).
    - `searchResults`:  результаты поиска из предыдущего шага.
6. **Отправка запроса к API**:  Отправляется POST-запрос к API `/api/ai/rix/completion` с созданным словарем `data` в качестве тела запроса.
7. **Обработка ответа**: Функция обрабатывает ответ API и итерирует по частям ответа (`response.content.iter_any()`) и преобразует их в текст (`chunk.decode()`), который затем возвращается как асинхронный генератор.

### `get_sources`

```python
    @classmethod
    def get_sources(cls) -> list:
        """
        Возвращает список источников для поиска в Интернете.

        Returns:
            list: Список источников, где каждый источник представлен словарем с ключами "title" и "url".
        """
        return [
            {
                "title": source["name"],
                "url": source["url"]
            } for source in cls._sources
        ]
```

**Как работает функция**:

1. **Извлечение источников**:  Функция извлекает список источников из атрибута класса `_sources`, который содержит информацию о результатах поиска в Интернете.
2. **Преобразование данных**:  Функция преобразует каждый источник в словарь с ключами "title" и "url", где "title" - это название источника, а "url" - это URL-адрес источника.
3. **Возврат результата**:  Функция возвращает список преобразованных источников.

## Параметры класса

- `url` (str): Базовый URL сервиса Hashnode.
- `working` (bool): Флаг, указывающий на доступность сервиса.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.
- `_sources` (list): Список источников для поиска в Интернете.

## Примеры

```python
from src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode
from src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import SearchTypes
from src.endpoints.gpt4free.g4f.typing import Messages

# Создание истории сообщений
messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Хорошо, а у тебя как?"},
    {"role": "user", "content": "Тоже отлично! Расскажи мне что-нибудь интересное."},
]

# Создание асинхронного генератора для получения ответа
async_generator = await Hashnode.create_async_generator(
    model="gpt-3.5-turbo",
    messages=messages,
    search_type=SearchTypes.websearch,
)

# Получение текста ответа
async for chunk in async_generator:
    print(chunk)

# Получение списка источников для поиска в Интернете
sources = Hashnode.get_sources()
print(sources)