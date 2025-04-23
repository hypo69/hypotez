# Модуль FlowGpt для работы с FlowGPT API
## Обзор

Модуль `FlowGpt` предназначен для взаимодействия с API сервиса FlowGPT. Он предоставляет асинхронный генератор, позволяющий получать ответы от различных моделей, таких как GPT-3.5 Turbo, GPT-4 Turbo, Google Gemini и других. Модуль поддерживает передачу истории сообщений и системные сообщения для более точной настройки ответов модели.

## Подробней

Модуль `FlowGpt` использует асинхронные запросы для взаимодействия с API FlowGPT, что позволяет эффективно обрабатывать запросы и получать ответы в режиме реального времени. Он также включает в себя механизмы для формирования правильных заголовков и данных запроса, необходимых для аутентификации и взаимодействия с API FlowGPT. Расположение файла в проекте `hypotez` указывает на его роль как одного из провайдеров для работы с различными моделями через API FlowGPT.

## Классы

### `FlowGpt`

**Описание**: Класс `FlowGpt` реализует асинхронный генератор для взаимодействия с API FlowGPT.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL для взаимодействия с API FlowGPT.
- `working` (bool): Флаг, указывающий на работоспособность провайдера (в данном случае `False`).
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений (`True`).
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений (`True`).
- `default_model` (str): Модель, используемая по умолчанию (`"gpt-3.5-turbo"`).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь с альтернативными названиями моделей.

**Методы**:

- `create_async_generator`
## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    temperature: float = 0.7,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с API FlowGPT.

    Args:
        cls (FlowGpt): Ссылка на класс `FlowGpt`.
        model (str): Название используемой модели.
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        temperature (float, optional): Температура генерации текста. По умолчанию `0.7`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от API FlowGPT.
    """
```

**Назначение**: Создает асинхронный генератор, который взаимодействует с API FlowGPT для получения ответов от выбранной модели на основе предоставленных сообщений и параметров.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Имя модели, которую нужно использовать для генерации ответа.
- `messages` (Messages): Список сообщений, представляющих историю разговора и запрос пользователя.
- `proxy` (str, optional): URL прокси-сервера, если необходимо использовать прокси для подключения к API. По умолчанию `None`.
- `temperature` (float, optional): Параметр, определяющий "температуру" генерации текста, влияющий на случайность и креативность ответов. По умолчанию `0.7`.
- `**kwargs`: Дополнительные параметры, которые могут быть переданы в API FlowGPT.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который при итерации возвращает части ответа от API FlowGPT.

**Как работает функция**:

1. **Подготовка данных**:
   - Функция извлекает имя модели, устанавливает текущее время, генерирует случайные данные для аутентификации.
   - Создает хеш-подпись для запроса.
   - Извлекает историю сообщений и системное сообщение из списка `messages`.
2. **Формирование заголовков**:
   - Создает словарь `headers` с необходимыми HTTP-заголовками для аутентификации и указания типа контента.
3. **Создание сессии**:
   - Использует `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.
4. **Формирование данных запроса**:
   - Создает словарь `data` с параметрами запроса, включая модель, сообщение пользователя, историю разговора, системное сообщение и другие параметры.
5. **Отправка запроса**:
   - Отправляет POST-запрос на URL `https://prod-backend-k8s.flowgpt.com/v3/chat-anonymous` с использованием `session.post`.
6. **Обработка ответа**:
   - Итерируется по чанкам, полученным из ответа сервера.
   - Преобразует каждый чанк в JSON и извлекает данные, если событие равно `"text"`.
   - Генерирует извлеченные данные.

**Примеры**:

```python
# Пример использования create_async_generator
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
async def main():
    generator = await FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages)
    async for chunk in generator:
        print(chunk)

# Пример с использованием прокси
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
async def main():
    generator = await FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages, proxy="http://your_proxy:8080")
    async for chunk in generator:
        print(chunk)
```

## Параметры класса

- `url` (str): URL для взаимодействия с API FlowGPT.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_message_history` (bool): Флаг, указывающий на поддержку истории сообщений.
- `supports_system_message` (bool): Флаг, указывающий на поддержку системных сообщений.
- `default_model` (str): Модель, используемая по умолчанию.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь с альтернативными названиями моделей.

## Примеры

```python
# Пример создания экземпляра класса FlowGpt
flow_gpt = FlowGpt()

# Пример вызова метода create_async_generator
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

async def main():
    generator = await FlowGpt.create_async_generator(model="gpt-3.5-turbo", messages=messages)
    async for chunk in generator:
        print(chunk)