# Модуль AiService

## Обзор

Модуль `AiService` предоставляет класс `AiService`, который является провайдером для взаимодействия с AI моделями через API `https://aiservice.vercel.app/`. Он поддерживает модель `gpt-3.5-turbo` и предоставляет метод для создания завершений (completion) на основе входных сообщений.

## Подробней

Модуль `AiService` является частью системы провайдеров, используемых для получения ответов от различных AI моделей. Он использует API `https://aiservice.vercel.app/` для отправки запросов и получения ответов. Этот модуль предназначен для интеграции с другими частями проекта, которые требуют взаимодействия с AI моделями.

## Классы

### `AiService`

**Описание**: Класс `AiService` реализует интерфейс `AbstractProvider` и предоставляет метод для создания завершений на основе модели `gpt-3.5-turbo`.

**Наследует**:
- `AbstractProvider`:  `AiService` наследует базовый класс `AbstractProvider`, определяющий общий интерфейс для всех провайдеров AI моделей.

**Аттрибуты**:
- `url` (str): URL API `https://aiservice.vercel.app/`, используемый для взаимодействия с AI моделью.
- `working` (bool): Флаг, указывающий, работает ли провайдер. По умолчанию `False`.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий, поддерживает ли провайдер модель `gpt-3.5-turbo`. По умолчанию `True`.

**Методы**:
- `create_completion`: Создает завершение на основе предоставленных сообщений.

## Функции

### `create_completion`

```python
    def create_completion(
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs: Any,
    ) -> CreateResult:
        """
        Создает завершение (completion) на основе предоставленных сообщений, используя API `https://aiservice.vercel.app/`.

        Args:
            model (str): Идентификатор модели, которую необходимо использовать.
            messages (Messages): Список сообщений, используемых в качестве контекста для генерации завершения.
            stream (bool): Флаг, указывающий, нужно ли возвращать результат в виде потока.
            **kwargs (Any): Дополнительные аргументы, которые могут быть переданы в API.

        Returns:
            CreateResult: Объект, представляющий собой результат создания завершения.

        Raises:
            requests.exceptions.HTTPError: Если HTTP запрос возвращает код ошибки.

        """
        ...
```

**Назначение**: Создает запрос к API `https://aiservice.vercel.app/` и возвращает ответ в виде генератора.

**Параметры**:
- `model` (str): Идентификатор модели, которую необходимо использовать.
- `messages` (Messages): Список сообщений, используемых в качестве контекста для генерации завершения.
- `stream` (bool): Флаг, указывающий, нужно ли возвращать результат в виде потока.
- `**kwargs` (Any): Дополнительные аргументы, которые могут быть переданы в API.

**Возвращает**:
- `CreateResult`: Генератор, который возвращает части завершения по мере их получения от API.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если HTTP запрос возвращает код ошибки.

**Как работает функция**:

1. **Формирование запроса**:
   - Преобразует список сообщений в текстовый формат, где каждое сообщение состоит из роли и содержимого.
   - Формирует строку запроса `base`, объединяя все сообщения и добавляя префикс "assistant: ".

2. **Подготовка заголовков**:
   - Определяет заголовки HTTP запроса, включая `accept`, `content-type`, `sec-fetch-dest`, `sec-fetch-mode`, `sec-fetch-site` и `Referer`.

3. **Отправка запроса**:
   - Отправляет POST запрос к API `https://aiservice.vercel.app/api/chat/answer` с заголовками и данными, содержащими сформированную строку запроса.
   - Использует библиотеку `requests` для отправки запроса.

4. **Обработка ответа**:
   - Проверяет статус ответа с помощью `response.raise_for_status()`, чтобы убедиться, что запрос выполнен успешно.
   - Извлекает данные из JSON ответа и возвращает их в виде генератора.

5. **Генерация результата**:
   - Использует `yield` для возвращения данных из ответа в виде генератора.

```
Формирование запроса
     │
     │ Преобразование сообщений в текст
     ↓
     │
     │ Подготовка HTTP заголовков
     ↓
     │
     │ Отправка POST запроса к API
     ↓
     │
     │ Обработка ответа
     │ Проверка статуса
     ↓
     │
     │ Извлечение данных из JSON
     ↓
     │
     │ Генерация результата
     │  Возврат данных через yield
     ↓
     End
```

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"}
]
model = "gpt-3.5-turbo"
stream = False

result = AiService.create_completion(model=model, messages=messages, stream=stream)
for chunk in result:
    print(chunk)  # Вывод: How can I help you today?
```
```python
messages = [
    {"role": "user", "content": "Как дела?"},
    {"role": "assistant", "content": "Все хорошо!"}
]
model = "gpt-3.5-turbo"
stream = False

result = AiService.create_completion(model=model, messages=messages, stream=stream)
for chunk in result:
    print(chunk)  # Вывод: Отлично, чем могу помочь?
```
```python
messages = [
    {"role": "user", "content": "Как написать функцию на Python?"}
]
model = "gpt-3.5-turbo"
stream = False

result = AiService.create_completion(model=model, messages=messages, stream=stream)
for chunk in result:
    print(chunk) # Вывод: Конечно, вот пример: def hello_world(): print("Hello, World!")
```