# Модуль AIChatFree

## Обзор

Этот модуль содержит класс `AIChatFree`, представляющий собой провайдера для взаимодействия с API AIChatFree. AIChatFree - это платформа, предоставляющая доступ к различным языковым моделям, таким как Gemini-1.5-pro.

## Подробней

Модуль реализует асинхронный генератор, который позволяет получать ответы от модели AIChatFree по частям. 

## Классы

### `class AIChatFree`

**Описание**: Класс `AIChatFree` реализует асинхронный генератор для получения ответов от API AIChatFree. 

**Наследует**: 
  - `AsyncGeneratorProvider`: Класс для асинхронного генератора.
  - `ProviderModelMixin`: Класс для настройки модели.

**Атрибуты**:

  - `url (str)`: URL-адрес API AIChatFree.
  - `working (bool)`: Флаг, указывающий на работоспособность провайдера.
  - `supports_stream (bool)`: Флаг, указывающий на поддержку потоковой передачи ответов.
  - `supports_message_history (bool)`: Флаг, указывающий на поддержку истории сообщений.
  - `default_model (str)`: Имя модели по умолчанию.

**Методы**:

  - `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для получения ответов от API AIChatFree.

### Методы класса

#### `create_async_generator(model: str, messages: Messages, proxy: str = None, connector: BaseConnector = None, **kwargs) -> AsyncResult`

**Назначение**: Создает асинхронный генератор для получения ответов от API AIChatFree.

**Параметры**:

  - `model (str)`: Имя модели, с которой будет взаимодействовать провайдер.
  - `messages (Messages)`: Список сообщений в истории.
  - `proxy (str, optional)`: Прокси-сервер для использования. По умолчанию `None`.
  - `connector (BaseConnector, optional)`: Подключение aiohttp. По умолчанию `None`.
  - `**kwargs`: Дополнительные аргументы для настройки.

**Возвращает**:

  - `AsyncResult`: Асинхронный результат, содержащий генератор.

**Вызывает исключения**:

  - `RateLimitError`: Возникает, если достигнут лимит запросов.

**Как работает функция**:

1. Функция создает заголовок запроса с соответствующими значениями.
2. Создание асинхронной сессии aiohttp с использованием указанных параметров.
3.  Функция формирует объект `data` с параметрами запроса, включая `messages`, `time`, `pass` и `sign`.
4.  Используя метод `session.post`,  отправляется POST-запрос к API AIChatFree с объектом `data`.
5.  Проверка статуса ответа. Если статус равен 500 и в ответе содержится сообщение "Quota exceeded",  сгенерируется исключение `RateLimitError`.
6.  Обработка ответа с помощью функции `raise_for_status`, чтобы проверить, не произошли ли какие-либо ошибки.
7.  Используя `response.content.iter_any()`,  получаются части ответов от сервера, преобразуются в текст и возвращаются в виде асинхронного генератора.

## Внутренние функции

### `generate_signature(time: int, text: str, secret: str = "") -> str`

**Назначение**:  Генерирует подпись для запроса к API AIChatFree.

**Параметры**:

  - `time (int)`: Текущее время в миллисекундах.
  - `text (str)`: Сообщение для отправки.
  - `secret (str, optional)`: Секретный ключ. По умолчанию пустая строка.

**Возвращает**:

  - `str`:  Шестнадцатеричная строка с подписью, сгенерированной с использованием алгоритма SHA256.

**Как работает функция**:

1. Функция объединяет время, сообщение и секретный ключ в строку.
2.  Используя `sha256` кодируется строка в байты и вычисляется хэш.
3.  Хэш преобразуется в шестнадцатеричную строку и возвращается в виде подписи.


## Примеры

```python
from src.endpoints.gpt4free.g4f.Provider.not_working.AIChatFree import AIChatFree

# Инициализация модели AIChatFree
aichatfree = AIChatFree(model='gemini-1.5-pro')

# Создание асинхронного генератора для получения ответов
async_generator = aichatfree.create_async_generator(model='gemini-1.5-pro', messages=[
    {"role": "user", "content": "Привет, как дела?"},
])

# Получение ответов от API AIChatFree по частям
async for chunk in async_generator:
    print(chunk)
```
```markdown