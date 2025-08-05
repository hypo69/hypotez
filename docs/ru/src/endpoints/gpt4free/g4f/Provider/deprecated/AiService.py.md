# Документация модуля AiService.py

## Обзор

Модуль `AiService.py` предоставляет класс `AiService`, который является устаревшим (deprecated) провайдером для взаимодействия с AI Service API. Он используется для создания завершений текста на основе предоставленных сообщений, имитируя работу с моделями GPT.

## Подробнее

Этот модуль интегрируется с AI Service API для генерации ответов на основе входных сообщений. Он отправляет запросы к API и возвращает сгенерированный текст. Модуль поддерживает модель `gpt-3.5-turbo`, но в целом считается устаревшим.

## Классы

### `AiService`

**Описание**: Класс `AiService` предоставляет интерфейс для взаимодействия с AI Service API. Он наследует `AbstractProvider` и реализует метод `create_completion` для генерации текста на основе входных сообщений.
**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL AI Service API.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.

**Методы**:
- `create_completion`: Создает завершение текста на основе предоставленных сообщений.

**Принцип работы**:
Класс `AiService` отправляет POST-запрос к AI Service API с входными сообщениями и заголовками, необходимыми для аутентификации и форматирования запроса. После получения ответа он извлекает сгенерированный текст из JSON-ответа и возвращает его.

## Методы класса

### `create_completion`

```python
    @staticmethod
    def create_completion(
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs: Any,
    ) -> CreateResult:
        """
        Создает завершение текста на основе предоставленных сообщений.

        Args:
            model (str): Имя модели для генерации текста.
            messages (Messages): Список сообщений для контекста.
            stream (bool): Указывает, должен ли ответ быть потоковым.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            CreateResult: Генератор, возвращающий сгенерированный текст.

        Raises:
            requests.exceptions.RequestException: Если возникает ошибка при выполнении запроса к API.

        Пример:
            messages = [{"role": "user", "content": "Hello, how are you?"}]
            result = AiService.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
            for chunk in result:
                print(chunk)
        """
```

**Назначение**: Метод `create_completion` отправляет запрос к AI Service API для генерации завершения текста на основе предоставленных сообщений.

**Параметры**:
- `model` (str): Имя модели для генерации текста.
- `messages` (Messages): Список сообщений для контекста.
- `stream` (bool): Указывает, должен ли ответ быть потоковым.
- `**kwargs` (Any): Дополнительные аргументы.

**Возвращает**:
- `CreateResult`: Генератор, возвращающий сгенерированный текст.

**Вызывает исключения**:
- `requests.exceptions.RequestException`: Если возникает ошибка при выполнении запроса к API.

**Как работает функция**:
1. Формирует базовый текст запроса из списка сообщений, объединяя роль и содержимое каждого сообщения.
2. Определяет заголовки для HTTP-запроса, включая `accept`, `content-type`, `sec-fetch-dest`, `sec-fetch-mode`, `sec-fetch-site` и `Referer`.
3. Формирует данные запроса в виде JSON, содержащие базовый текст.
4. Отправляет POST-запрос к AI Service API (`https://aiservice.vercel.app/api/chat/answer`) с заголовками и данными.
5. Проверяет статус ответа и вызывает исключение, если произошла ошибка.
6. Извлекает сгенерированный текст из JSON-ответа (`response.json()["data"]`) и возвращает его в виде генератора.

**Примеры**:

```python
messages = [{"role": "user", "content": "Hello, how are you?"}]
result = AiService.create_completion(model="gpt-3.5-turbo", messages=messages, stream=False)
for chunk in result:
    print(chunk)
```

## Параметры класса

- `url` (str): URL AI Service API.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.