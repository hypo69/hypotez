# Модуль MetaAI

## Обзор

Модуль `MetaAI` предоставляет асинхронный интерфейс для взаимодействия с Meta AI. Он позволяет генерировать текст и изображения, используя API Meta AI. Модуль поддерживает прокси и использует `aiohttp` для асинхронных запросов.

## Подробней

Этот модуль предназначен для работы с Meta AI API, обеспечивая функциональность для генерации текста и изображений. Он включает в себя обработку cookies, access token, и формирование запросов к API. Он также включает в себя обработку ошибок и исключений, специфичных для Meta AI, таких как `AbraGeoBlockedError`.

## Классы

### `Sources`

**Описание**: Класс представляет собой список источников (ссылок) с информацией о заголовке и URL.

**Принцип работы**: Класс инициализируется списком словарей, каждый из которых содержит информацию о ссылке (`title` и `link`). Метод `__str__` форматирует список ссылок в Markdown.

**Аттрибуты**:

- `list` (List[Dict[str, str]]): Список словарей, где каждый словарь содержит ключи `title` и `link`.

**Методы**:

- `__init__(self, link_list: List[Dict[str, str]]) -> None`: Инициализирует объект `Sources` списком ссылок.
- `__str__(self) -> str`: Возвращает строковое представление списка ссылок в формате Markdown.

### `AbraGeoBlockedError`

**Описание**: Класс исключения, которое выбрасывается, когда Meta AI недоступен в определенной стране.

**Принцип работы**: Простое исключение, используемое для обозначения географической блокировки.

### `MetaAI`

**Описание**: Класс `MetaAI` предоставляет асинхронный интерфейс для взаимодействия с Meta AI.

**Принцип работы**: Класс управляет сессиями, cookies, access token и формирует запросы к API Meta AI для генерации текста и изображений. Он также включает обработку ошибок и исключений, специфичных для Meta AI, таких как `AbraGeoBlockedError`.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает поддержку асинхронной генерации.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Аттрибуты**:

- `label` (str): Метка провайдера ("Meta AI").
- `url` (str): URL Meta AI ("https://www.meta.ai").
- `working` (bool): Флаг, указывающий, работает ли провайдер (True).
- `default_model` (str): Модель по умолчанию ('meta-ai').
- `session` (ClientSession): Асинхронная клиентская сессия для выполнения HTTP-запросов.
- `cookies` (Cookies): Cookies для аутентификации.
- `access_token` (str): Access token для доступа к API.
- `lsd` (str): Значение LSD (Login Session Data), необходимое для запросов.
- `dtsg` (str): Значение DTSG (Data Transfer Security Guard), необходимое для запросов.

**Методы**:

- `__init__(self, proxy: str = None, connector: BaseConnector = None)`: Инициализирует объект `MetaAI`.

- `create_async_generator(cls, model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от Meta AI.

- `update_access_token(self, birthday: str = "1999-01-01")`: Обновляет access token, используя birthday.

- `prompt(self, message: str, cookies: Cookies = None) -> AsyncResult`: Отправляет запрос к Meta AI и возвращает асинхронный генератор для получения ответа.

- `update_cookies(self, cookies: Cookies = None)`: Обновляет cookies для аутентификации.

- `fetch_sources(self, fetch_id: str) -> Sources`: Получает источники для данного fetch_id.

- `extract_value(text: str, key: str = None, start_str = None, end_str = ',') -> str`: Извлекает значение из текста, используя начальную и конечную строки.

## Функции

### `generate_offline_threading_id`

```python
def generate_offline_threading_id() -> str:
    """
    Generates an offline threading ID.

    Returns:
        str: The generated offline threading ID.
    """
    # Generate a random 64-bit integer
    random_value = random.getrandbits(64)
    
    # Get the current timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    
    # Combine timestamp and random value
    threading_id = (timestamp << 22) | (random_value & ((1 << 22) - 1))
    
    return str(threading_id)
```

**Назначение**: Генерирует ID для оффлайн тредов.

**Параметры**:
- Нет.

**Возвращает**:
- `str`: Сгенерированный ID для оффлайн треда.

**Как работает функция**:

1. **Генерация случайного значения**: Генерируется случайное 64-битное целое число.
2. **Получение текущего времени**: Получается текущая метка времени в миллисекундах.
3. **Объединение времени и случайного значения**: Метка времени сдвигается влево на 22 бита, а затем объединяется с случайным значением, используя побитовое И.
4. **Возврат строкового представления**: Возвращается строковое представление полученного ID.

```
Генерация случайного значения --> Получение текущего времени --> Объединение времени и случайного значения --> Возврат строкового представления
```

**Примеры**:

```python
offline_id = generate_offline_threading_id()
print(offline_id)  # Пример: 1678886400000000000