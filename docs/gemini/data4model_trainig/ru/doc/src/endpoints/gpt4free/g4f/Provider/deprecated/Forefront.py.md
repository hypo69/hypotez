# Документация модуля Forefront

## Обзор

Модуль `Forefront.py` предоставляет класс `Forefront`, который является провайдером для взаимодействия с моделью GPT-4 через API forefront.com. Этот модуль поддерживает потоковую передачу данных и предназначен для использования с моделью `gpt-35-turbo`.

## Подробнее

Модуль содержит класс `Forefront`, который наследуется от `AbstractProvider`. Он позволяет отправлять запросы к API forefront.com и получать ответы в потоковом режиме. Модуль использует библиотеку `requests` для отправки HTTP-запросов и библиотеку `json` для обработки данных в формате JSON.

## Классы

### `Forefront`

**Описание**: Класс `Forefront` предоставляет методы для взаимодействия с API forefront.com. Он наследуется от `AbstractProvider` и реализует метод `create_completion` для отправки запросов и получения ответов.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL-адрес API forefront.com.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (значение `True`).
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-35-turbo` (значение `True`).

**Методы**:
- `create_completion`: Отправляет запрос к API forefront.com и возвращает ответ.

## Методы класса

### `create_completion`

```python
    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        """ Функция отправляет запрос к API forefront.com и возвращает ответ.
        Args:
            model (str): Имя модели для использования.
            messages (list[dict[str, str]]): Список сообщений для отправки.
            stream (bool): Указывает, следует ли использовать потоковую передачу данных.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            CreateResult: Результат выполнения запроса.

        Raises:
            requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.
        Как работает функция:
         - Формирует JSON-данные для отправки запроса.
         - Отправляет POST-запрос к API forefront.com.
         - Обрабатывает ответ и возвращает токены в потоковом режиме.
        Внутренние функции:
        - нет
        """
```

**Назначение**: Отправляет запрос к API forefront.com и возвращает ответ.

**Параметры**:
- `model` (str): Имя модели для использования.
- `messages` (list[dict[str, str]]): Список сообщений для отправки.
- `stream` (bool): Указывает, следует ли использовать потоковую передачу данных.
- `**kwargs` (Any): Дополнительные аргументы.

**Возвращает**:
- `CreateResult`: Результат выполнения запроса.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если HTTP-запрос завершается с ошибкой.

**Как работает функция**:

1. Формирует JSON-данные для отправки запроса, включая текст сообщения, идентификаторы, параметры персоны и модели.
2. Отправляет POST-запрос к API forefront.com (`https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat`) с использованием библиотеки `requests`.
3. Обрабатывает ответ в потоковом режиме, итерируясь по строкам ответа.
4. Извлекает данные из каждой строки, содержащей `"delta"`, декодирует JSON и извлекает значение `"delta"`.
5. Возвращает токены в потоковом режиме с использованием `yield`.

**Примеры**:

Пример использования функции `create_completion` с потоковой передачей данных:

```python
model = "gpt-4"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True

# Вызов функции create_completion
result = Forefront.create_completion(model=model, messages=messages, stream=stream)

# Итерация по результатам
for token in result:
    print(token, end="")
```

В этом примере функция `create_completion` вызывается с параметрами `model`, `messages` и `stream`. Результат представляет собой генератор, который возвращает токены в потоковом режиме. Затем происходит итерация по токенам и их вывод на экран.