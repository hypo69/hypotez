# Модуль типов для g4f client

## Обзор

Модуль `types.py` определяет типы данных, используемые в клиентской части библиотеки `g4f` (gpt4free). Он содержит определения для `ChatCompletion`, `ChatCompletionChunk`, `BaseProvider`, `ImageProvider`, `Proxies`, `IterResponse` и `AsyncIterResponse`, а также класс `Client`.

## Подробней

Этот модуль предоставляет типы для работы с различными провайдерами, прокси и потоками данных, используемыми для взаимодействия с API.
Определяет структуры данных для обмена сообщениями и управления соединениями, что позволяет упростить интеграцию и использование различных API.

## Типы

### `ImageProvider`

```python
ImageProvider = Union[BaseProvider, object]
```

**Описание**: Объединение типов `BaseProvider` или `object`. Используется для указания провайдера изображений.

### `Proxies`

```python
Proxies = Union[dict, str]
```

**Описание**: Объединение типов `dict` или `str`. Используется для представления прокси-серверов, которые могут быть строкой или словарём.

### `IterResponse`

```python
IterResponse = Iterator[Union[ChatCompletion, ChatCompletionChunk]]
```

**Описание**: Тип представляет собой итератор, возвращающий объекты типа `ChatCompletion` или `ChatCompletionChunk`.

### `AsyncIterResponse`

```python
AsyncIterResponse = AsyncIterator[Union[ChatCompletion, ChatCompletionChunk]]
```

**Описание**: Тип представляет собой асинхронный итератор, возвращающий объекты типа `ChatCompletion` или `ChatCompletionChunk`.

## Классы

### `Client`

**Описание**: Класс `Client` предназначен для управления API ключами и прокси-серверами.

**Принцип работы**:

Класс `Client` инициализируется с API-ключом и прокси-серверами. Он предоставляет методы для получения прокси-серверов из различных источников (строка, словарь или переменные окружения).

**Атрибуты**:

- `api_key` (str): API-ключ для аутентификации.
- `proxies` (Proxies): Прокси-серверы для использования при подключении.
- `proxy` (str | None): Текущий прокси-сервер.

**Методы**:

- `get_proxy()`: Возвращает прокси-сервер из различных источников.

#### `get_proxy`

```python
def get_proxy(self) -> Union[str, None]:
    ...
```

**Назначение**: Получение прокси-сервера из различных источников.

**Параметры**:
- Отсутствуют

**Возвращает**:
- `str | None`: Строка, представляющая прокси-сервер, или `None`, если прокси не найден.

**Как работает функция**:

1. Проверяется, является ли `self.proxies` строкой. Если да, то возвращается эта строка.
2. Если `self.proxies` равен `None`, то функция пытается получить значение переменной окружения `G4F_PROXY` и возвращает его.
3. Если `self.proxies` является словарём, то проверяется наличие ключей `all` или `https` и возвращается соответствующее значение.
4. Если ни одно из условий не выполнено, возвращается `None`.

```
Проверка типа прокси (self.proxies) --> Если строка --> Возврат строки
|
Если None --> Попытка получить переменную окружения G4F_PROXY --> Возврат значения переменной или None
|
Если словарь --> Проверка наличия ключей "all" или "https" --> Возврат соответствующего значения или None
|
Возврат None
```

**Примеры**:

```python
client = Client(proxies='http://proxy.example.com')
proxy = client.get_proxy()
print(proxy)  # Вывод: http://proxy.example.com

client = Client(proxies={'https': 'http://proxy.example.com'})
proxy = client.get_proxy()
print(proxy)  # Вывод: http://proxy.example.com

client = Client()
os.environ['G4F_PROXY'] = 'http://proxy.example.com'
proxy = client.get_proxy()
print(proxy)  # Вывод: http://proxy.example.com