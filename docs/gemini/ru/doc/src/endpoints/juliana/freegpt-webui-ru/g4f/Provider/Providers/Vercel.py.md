# Модуль Vercel

## Обзор

Этот модуль предоставляет реализацию провайдера `Vercel` для `g4f.Provider`. Он обеспечивает доступ к различным языковым моделям, размещенным на платформе Vercel, через API.

## Подробности

Модуль использует библиотеку `curl_cffi` для выполнения HTTP-запросов к API Vercel. Он определяет класс `Client`, который предоставляет методы для получения токена аутентификации, отправки запросов на генерацию текста и обработки ответов.

## Классы

### `class Client`

**Описание**: Класс `Client` обеспечивает взаимодействие с API Vercel для генерации текста.

**Атрибуты**:

- `session (requests.Session)`: Объект сессии `requests` для выполнения HTTP-запросов.
- `headers (Dict[str, str])`: Заголовки HTTP-запросов.

**Методы**:

- `get_token() -> str`: Получает токен аутентификации для доступа к API Vercel.
- `get_default_params(model_id: str) -> Dict[str, Any]`: Возвращает словарь с параметрами по умолчанию для заданной модели.
- `generate(model_id: str, prompt: str, params: Dict[str, Any] = {}) -> Generator[Dict[str, Any], None, None]`: Отправляет запрос на генерацию текста к API Vercel.

## Функции

### `_create_completion(model: str, messages: list, stream: bool, **kwargs)`

**Назначение**: Функция `_create_completion` создает объект завершения, используя API Vercel.

**Параметры**:

- `model (str)`: Идентификатор модели Vercel.
- `messages (list)`: Список сообщений для контекста диалога.
- `stream (bool)`: Флаг, указывающий на то, следует ли использовать потоковую передачу ответа.
- `**kwargs`: Дополнительные параметры для модели.

**Возвращает**:

- `Generator[Dict[str, Any], None, None]`: Генератор, который выдает токены ответа.

**Как работает функция**:

- Функция собирает сообщения из списка `messages` в строку `conversation`.
- Затем она использует метод `Client.generate()` для отправки запроса к API Vercel с помощью собранной `conversation`.
- Функция обрабатывает ответ от API Vercel и выдает токены ответа через генератор.

**Примеры**:

```python
model = 'gpt-3.5-turbo'
messages = [
    {'role': 'user', 'content': 'Hello, how are you?'},
    {'role': 'assistant', 'content': 'I am doing well, thank you.'}
]

for token in _create_completion(model, messages, stream=True):
    print(token)
```

**Внутренние функции**:

- Нет

## Параметры класса

- `url (str)`: URL-адрес API Vercel.
- `supports_stream (bool)`: Флаг, указывающий на то, поддерживает ли API Vercel потоковую передачу ответа.
- `needs_auth (bool)`: Флаг, указывающий на то, требуется ли аутентификация для доступа к API.
- `models (Dict[str, str])`: Словарь с сопоставлением имен моделей Vercel с их идентификаторами.
- `vercel_models (Dict[str, Dict[str, Any]])`: Словарь, содержащий информацию о моделях Vercel, включая их идентификаторы, поставщиков, параметры и т. д.

## Примеры

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Drivewr(Chrome)

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```
```python
# Создание клиента Vercel
client = Client()

# Генерация текста с помощью модели gpt-3.5-turbo
prompt = 'Привет, как дела?'
for token in client.generate('gpt-3.5-turbo', prompt):
    print(token)