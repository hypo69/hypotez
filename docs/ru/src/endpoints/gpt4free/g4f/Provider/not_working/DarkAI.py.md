# Модуль `DarkAI`

## Обзор

Модуль `DarkAI` предоставляет асинхронный интерфейс для взаимодействия с сервисом DarkAI, позволяя генерировать текст на основе предоставленных сообщений, используя различные модели, такие как `gpt-4o`, `gpt-3.5-turbo` и `llama-3-70b`. Модуль поддерживает потоковую передачу данных и использует `aiohttp` для выполнения асинхронных HTTP-запросов.

## Подробней

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется использование AI-моделей для генерации текста. Он обеспечивает гибкость в выборе модели и поддерживает проксирование запросов. Для обработки ответов от сервера используется потоковый режим, что позволяет получать результаты по частям.
Данный модуль в данный момент **не работает**, о чем говорит название поддиректории `not_working`.

## Классы

### `DarkAI`

**Описание**: Класс `DarkAI` реализует асинхронного провайдера, взаимодействующего с API DarkAI для генерации текста.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров, возвращающих генератор.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL сервиса DarkAI (`"https://darkai.foundation/chat"`).
- `api_endpoint` (str): URL API для чата (`"https://darkai.foundation/chat"`).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (в данном случае `False`).
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`'llama-3-70b'`).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Методы**:
- `create_async_generator`: Асинхронный генератор для получения текстовых фрагментов от API DarkAI.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        """Асинхронный генератор для получения текстовых фрагментов от API DarkAI.

        Args:
            cls (DarkAI): Ссылка на класс `DarkAI`.
            model (str): Название используемой модели.
            messages (Messages): Список сообщений для отправки в API.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор текстовых фрагментов.

        Raises:
            Exception: Если возникает ошибка при выполнении запроса.

        Внутренние функции:
            Нет.
        """
```

**Назначение**: Создает и возвращает асинхронный генератор, который отправляет запросы к API DarkAI и выдает текстовые фрагменты по мере их поступления.

**Параметры**:
- `cls` (DarkAI): Ссылка на класс `DarkAI`.
- `model` (str): Название используемой модели.
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор текстовых фрагментов.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при выполнении запроса.

**Как работает функция**:

1. **Получение модели**: Функция `create_async_generator` сначала получает название модели, используя метод `cls.get_model(model)`.
2. **Формирование заголовков**:  Определяются заголовки HTTP-запроса, включая `accept`, `content-type` и `user-agent`.
3. **Создание сессии aiohttp**: Создается асинхронная сессия `aiohttp` с заданными заголовками и увеличенным таймаутом (600 секунд).
4. **Формирование данных запроса**:  Преобразует список сообщений в строку запроса, используя функцию `format_prompt(messages)`. Затем формирует JSON-данные для отправки, включая `query` (сформированный запрос) и `model` (название модели).
5. **Отправка POST-запроса**:  Отправляет асинхронный POST-запрос к API DarkAI (`cls.api_endpoint`) с JSON-данными и прокси-сервером (если указан).
6. **Обработка потока данных**:  Получает содержимое ответа как поток и читает его небольшими частями (1024 байта).
7. **Разбор фрагментов данных**:  Разделяет полученные данные на строки, ищет строки, начинающиеся с `'data: '`, и пытается извлечь JSON из этих строк.
8. **Извлечение текстовых фрагментов**:  Если удается извлечь JSON, проверяет наличие события `'text-chunk'` и выдает текстовый фрагмент (`chunk`).
9. **Завершение потока**:  Если встречается событие `'stream-end'`, генератор завершает работу.
10. **Обработка ошибок JSON**: Обрабатывает исключения `json.JSONDecodeError`, которые могут возникнуть при разборе JSON, пропуская некорректные строки.

```
                                     Начало
                                       ↓
                Получение названия модели и формирование заголовков
                                       ↓
                       Создание асинхронной сессии aiohttp
                                       ↓
                  Преобразование сообщений в строку запроса и
                         формирование JSON-данных для запроса
                                       ↓
                            Отправка POST-запроса к API
                                       ↓
                       Получение содержимого ответа как поток
                                       ↓
       Разделение данных на строки и поиск строк, начинающихся с "data: "
                                       ↓
                         Извлечение JSON из найденных строк
                                       ↓
  Проверка наличия события "text-chunk" и выдача текстового фрагмента
                                       ↓
               Если встречается событие "stream-end" → Завершение потока
                                       ↓
           Обработка ошибок JSON и пропуск некорректных JSON-строк
                                       ↓
                                     Конец
```

**Примеры**:

```python
# Пример использования асинхронного генератора
async def example():
    from src.logger import logger
    try:
        model = "gpt-4o"
        messages = [{"role": "user", "content": "Напиши стихотворение о весне."}]
        async for chunk in DarkAI.create_async_generator(model=model, messages=messages):
            print(chunk, end="")
    except Exception as ex:
        logger.error('Ошибка при вызове DarkAI', ex, exc_info=True)

import asyncio
asyncio.run(example())
```
```python
# Пример с использованием прокси-сервера
async def example_with_proxy():
    from src.logger import logger
    try:
        model = "gpt-3.5-turbo"
        messages = [{"role": "user", "content": "Расскажи анекдот."}]
        proxy = "http://your_proxy_address:your_proxy_port"  # Замените на реальный адрес и порт прокси
        async for chunk in DarkAI.create_async_generator(model=model, messages=messages, proxy=proxy):
            print(chunk, end="")
    except Exception as ex:
        logger.error('Ошибка при вызове DarkAI с прокси', ex, exc_info=True)
import asyncio
asyncio.run(example_with_proxy())
```
```python
# Пример обработки ошибок при вызове API
async def example_error_handling():
    from src.logger import logger
    try:
        model = "invalid-model"
        messages = [{"role": "user", "content": "Hello"}]
        async for chunk in DarkAI.create_async_generator(model=model, messages=messages):
            print(chunk, end="")
    except Exception as ex:
        logger.error('Ошибка при вызове DarkAI', ex, exc_info=True)

import asyncio
asyncio.run(example_error_handling())