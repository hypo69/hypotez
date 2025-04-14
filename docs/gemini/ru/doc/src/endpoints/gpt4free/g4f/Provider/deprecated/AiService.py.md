# Модуль для взаимодействия с AiService
## Обзор

Модуль предоставляет класс `AiService`, который является провайдером для взаимодействия с сервисом aiservice.vercel.app. 
Он поддерживает модель `gpt-3.5-turbo` и предоставляет метод для создания завершений на основе предоставленных сообщений.

## Подробней

Модуль `AiService.py` предназначен для интеграции с сервисом aiservice.vercel.app, предоставляя возможность использовать его API для генерации текста. Класс `AiService` наследуется от `AbstractProvider` и реализует метод `create_completion`, который отправляет запрос к API сервиса и возвращает результат.
Сервис aiservice.vercel.app используется для работы с большими языковыми моделями.

## Классы

### `AiService`

**Описание**: Класс `AiService` предоставляет интерфейс для взаимодействия с сервисом aiservice.vercel.app.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL сервиса aiservice.vercel.app.
- `working` (bool): Указывает, работает ли сервис в данный момент.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли сервис модель gpt-3.5-turbo.

**Методы**:
- `create_completion`: Создает завершение на основе предоставленных сообщений.

### `create_completion`

```python
    @staticmethod
    def create_completion(
        model: str,
        messages: Messages,
        stream: bool,
        **kwargs: Any,
    ) -> CreateResult:
        """ Создает завершение на основе предоставленных сообщений.

        Args:
            model (str): Название модели.
            messages (Messages): Список сообщений для отправки в API.
            stream (bool): Указывает, должен ли быть использован потоковый режим.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            CreateResult: Результат создания завершения.

        Raises:
            requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.

        Как работает функция:
            1. Формирует базовый текст запроса, объединяя сообщения с ролями и контентом.
            2. Определяет заголовки запроса, включая `accept`, `content-type`, `sec-fetch-dest`, `sec-fetch-mode`, `sec-fetch-site` и `Referer`.
            3. Формирует данные запроса в формате JSON, включая базовый текст запроса.
            4. Отправляет POST-запрос к API сервиса aiservice.vercel.app.
            5. Проверяет статус ответа и вызывает исключение `HTTPError`, если запрос завершился с ошибкой.
            6. Извлекает данные из JSON-ответа и возвращает их.

        Внутренние функции:
            Отсутствуют.

        """
```

**Примеры**:
```python
# Пример использования функции create_completion
messages = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I am doing well, thank you for asking."},
]
model = "gpt-3.5-turbo"
stream = False
# Предполагается, что AiService уже инициализирован
# completion_result = AiService.create_completion(model=model, messages=messages, stream=stream)
# print(completion_result)