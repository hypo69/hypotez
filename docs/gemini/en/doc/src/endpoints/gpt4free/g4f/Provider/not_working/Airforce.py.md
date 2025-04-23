# Модуль: Airforce

## Обзор

Модуль `Airforce` представляет собой асинхронный провайдер для работы с API Airforce, который предоставляет возможности генерации текста и изображений. Он поддерживает потоковую передачу данных, системные сообщения и историю сообщений. Модуль включает в себя методы для получения списка доступных моделей, фильтрации содержимого и обработки ответов от API.

## Подробнее

Модуль предназначен для интеграции с API Airforce для предоставления функциональности генерации текста и изображений. Он обрабатывает запросы к API, фильтрует ответы и предоставляет результаты в удобном формате. Airforce использует `aiohttp` для асинхронных запросов.

## Классы

### `Airforce`

**Описание**:
Класс `Airforce` является асинхронным провайдером, который предоставляет методы для генерации текста и изображений с использованием API Airforce.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет функциональность для работы с моделями.

**Атрибуты**:
- `url` (str): Базовый URL API Airforce.
- `api_endpoint_completions` (str): URL для запросов на генерацию текста.
- `api_endpoint_imagine2` (str): URL для запросов на генерацию изображений.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `models` (List[str]): Список доступных моделей для генерации текста.
- `image_models` (List[str]): Список доступных моделей для генерации изображений.
- `hidden_models` (Set[str]): Набор скрытых моделей, которые не должны отображаться в списке доступных моделей.
- `additional_models_imagine` (List[str]): Список дополнительных моделей для генерации изображений.
- `model_aliases` (Dict[str, str]): Словарь, содержащий псевдонимы моделей.

**Принцип работы**:
Класс `Airforce` предоставляет методы для взаимодействия с API Airforce для генерации текста и изображений. Он использует `aiohttp` для асинхронных HTTP-запросов. Класс также содержит методы для фильтрации содержимого и обработки ответов от API.

## Методы класса

- `get_models`: Получение доступных моделей с обработкой ошибок.
- `get_model`: Получение имени модели из псевдонима.
- `_filter_content`: Фильтрация нежелательного содержимого из частичного ответа.
- `_filter_response`: Фильтрация полного ответа для удаления системных ошибок и нежелательного текста.
- `generate_image`: Асинхронная генерация изображений на основе запроса.
- `generate_text`: Асинхронная генерация текста на основе запроса.
- `create_async_generator`: Создание асинхронного генератора для генерации текста или изображений.

### `get_models`

```python
    @classmethod
    def get_models(cls) -> List[str]:
        """
        Получает список доступных моделей с обработкой ошибок.

        Returns:
            List[str]: Список доступных моделей.
        """
        ...
```

**Описание**:
Метод класса `get_models` получает список доступных моделей из API Airforce. Если список моделей еще не был получен, он выполняет HTTP-запрос для получения списка моделей для генерации текста и изображений. В случае ошибки при получении списка моделей, он логирует ошибку и возвращает список псевдонимов моделей.

**Как работает**:
1. Проверяет, был ли уже получен список моделей для генерации изображений (`cls.image_models`).
2. Если список моделей для генерации изображений пуст, выполняет HTTP-запрос к API Airforce для получения списка моделей для генерации изображений.
3. Обрабатывает ответ от API, извлекая список моделей для генерации изображений.
4. Если произошла ошибка при получении списка моделей для генерации изображений, логирует ошибку и использует локальный список дополнительных моделей.
5. Проверяет, был ли уже получен список моделей для генерации текста (`cls.models`).
6. Если список моделей для генерации текста пуст, выполняет HTTP-запрос к API Airforce для получения списка моделей для генерации текста.
7. Обрабатывает ответ от API, извлекая список моделей для генерации текста.
8. Если произошла ошибка при получении списка моделей для генерации текста, логирует ошибку и использует локальный список псевдонимов моделей.
9. Возвращает список доступных моделей.

**Примеры**:
```python
models = Airforce.get_models()
print(models)
```

### `get_model`

```python
    @classmethod
    def get_model(cls, model: str) -> str:
        """
        Получает фактическое имя модели из псевдонима.

        Args:
            model (str): Псевдоним модели.

        Returns:
            str: Фактическое имя модели.
        """
        ...
```

**Описание**:
Метод класса `get_model` получает фактическое имя модели из псевдонима, используя словарь `model_aliases`. Если псевдоним не найден, возвращает сам псевдоним или модель по умолчанию.

**Как работает**:
1. Проверяет, есть ли псевдоним модели в словаре `model_aliases`.
2. Если псевдоним найден, возвращает соответствующее ему фактическое имя модели.
3. Если псевдоним не найден, возвращает сам псевдоним или модель по умолчанию (`cls.default_model`), если псевдоним пуст.

**Примеры**:
```python
model_name = Airforce.get_model("openchat-3.5")
print(model_name)  # openchat-3.5-0106

model_name = Airforce.get_model("unknown_model")
print(model_name)  # unknown_model
```

### `_filter_content`

```python
    @classmethod
    def _filter_content(cls, part_response: str) -> str:
        """
        Фильтрует нежелательное содержимое из частичного ответа.
        """
        ...
```

**Описание**:
Метод класса `_filter_content` фильтрует нежелательное содержимое из частичного ответа, удаляя сообщения о превышении лимита символов и превышении лимита запросов.

**Как работает**:
1. Использует регулярные выражения для удаления сообщений о превышении лимита символов.
2. Использует регулярные выражения для удаления сообщений о превышении лимита запросов.
3. Возвращает отфильтрованный ответ.

**Примеры**:
```python
filtered_content = Airforce._filter_content("One message exceeds the \\d+chars per message limit\\..+https:\\/\\/discord\\.com\\/invite\\/\\S+")
print(filtered_content)

filtered_content = Airforce._filter_content("Rate limit \\(\\d+\\/minute\\) exceeded\\. Join our discord for more: .+https:\\/\\/discord\\.com\\/invite\\/\\S+")
print(filtered_content)
```

### `_filter_response`

```python
    @classmethod
    def _filter_response(cls, response: str) -> str:\n        """\n        Фильтрует полный ответ для удаления системных ошибок и другого нежелательного текста.\n        """
        ...
```

**Описание**:
Метод класса `_filter_response` фильтрует полный ответ для удаления системных ошибок и другого нежелательного текста, такого как токены и префиксы.

**Как работает**:
1. Проверяет, содержит ли ответ сообщение об ошибке "Model not found or too long input. Or any other error (xD)". Если да, вызывает исключение `ValueError`.
2. Использует регулярные выражения для удаления системных ошибок, токенов и префиксов.
3. Вызывает метод `_filter_content` для дополнительной фильтрации содержимого.
4. Возвращает отфильтрованный ответ.

**Примеры**:
```python
filtered_response = Airforce._filter_response("Model not found or too long input. Or any other error (xD)")
print(filtered_response)

filtered_response = Airforce._filter_response("\\[ERROR\\] \'\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12}\'")
print(filtered_response)

filtered_response = Airforce._filter_response("<\\|im_end\\|>")
print(filtered_response)

filtered_response = Airforce._filter_response("</s>")
print(filtered_response)

filtered_response = Airforce._filter_response("Assistant: ")
print(filtered_response)

filtered_response = Airforce._filter_response("AI: ")
print(filtered_response)

filtered_response = Airforce._filter_response("ANSWER: ")
print(filtered_response)

filtered_response = Airforce._filter_response("Output: ")
print(filtered_response)
```

### `generate_image`

```python
    @classmethod
    async def generate_image(\n        cls,\n        model: str,\n        prompt: str,\n        size: str,\n        seed: int,\n        proxy: str = None\n    ) -> AsyncResult:\n        """\n        Асинхронно генерирует изображения на основе запроса.\n        """
        ...
```

**Описание**:
Метод класса `generate_image` асинхронно генерирует изображения на основе запроса к API Airforce. Он отправляет HTTP-запрос с указанными параметрами и возвращает URL сгенерированного изображения.

**Параметры**:
- `model` (str): Модель для генерации изображения.
- `prompt` (str): Текст запроса для генерации изображения.
- `size` (str): Размер изображения.
- `seed` (int): Зерно для генерации случайных чисел.
- `proxy` (str, optional): Прокси-сервер для подключения к API. По умолчанию `None`.

**Как работает**:
1. Формирует заголовки HTTP-запроса.
2. Формирует параметры запроса.
3. Отправляет GET-запрос к API Airforce с использованием `aiohttp`.
4. Если запрос выполнен успешно (status code 200), извлекает URL изображения из ответа и возвращает объект `ImageResponse`.
5. Если запрос не выполнен успешно, вызывает исключение `RuntimeError` с описанием ошибки.

**Примеры**:
```python
async for result in Airforce.generate_image(model="flux", prompt="cat", size="1:1", seed=123):
    print(result)
```

### `generate_text`

```python
    @classmethod
    async def generate_text(\n        cls,\n        model: str,\n        messages: Messages,\n        max_tokens: int,\n        temperature: float,\n        top_p: float,\n        stream: bool,\n        proxy: str = None\n    ) -> AsyncResult:\n        """\n        Генерирует текст, буферизует ответ, фильтрует его и возвращает окончательный результат.\n        """
        ...
```

**Описание**:
Метод класса `generate_text` генерирует текст на основе запроса к API Airforce. Он отправляет HTTP-запрос с указанными параметрами и возвращает сгенерированный текст.

**Параметры**:
- `model` (str): Модель для генерации текста.
- `messages` (Messages): Список сообщений для генерации текста.
- `max_tokens` (int): Максимальное количество токенов в ответе.
- `temperature` (float): Температура для генерации текста.
- `top_p` (float): Top-p для генерации текста.
- `stream` (bool): Указывает, использовать ли потоковую передачу данных.
- `proxy` (str, optional): Прокси-сервер для подключения к API. По умолчанию `None`.

**Как работает**:
1. Формирует заголовки HTTP-запроса.
2. Разбивает сообщения на части, если они превышают максимальную длину.
3. Формирует данные запроса.
4. Отправляет POST-запрос к API Airforce с использованием `aiohttp`.
5. Если используется потоковая передача данных, обрабатывает ответ по частям, фильтрует его и возвращает.
6. Если потоковая передача данных не используется, обрабатывает полный ответ, фильтрует его и возвращает.

**Примеры**:
```python
messages = [{"role": "user", "content": "Hello, world!"}]
async for result in Airforce.generate_text(model="llama-3.1-70b-chat", messages=messages, max_tokens=512, temperature=1, top_p=1, stream=True):
    print(result)
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(\n        cls,\n        model: str,\n        messages: Messages,\n        prompt: str = None,\n        proxy: str = None,\n        max_tokens: int = 512,\n        temperature: float = 1,\n        top_p: float = 1,\n        stream: bool = True,\n        size: str = "1:1",\n        seed: int = None,\n        **kwargs\n    ) -> AsyncResult:\n        """\n        Создает асинхронный генератор для генерации текста или изображений.\n        """
        ...
```

**Описание**:
Метод класса `create_async_generator` создает асинхронный генератор для генерации текста или изображений на основе указанных параметров.

**Параметры**:
- `model` (str): Модель для генерации.
- `messages` (Messages): Список сообщений для генерации текста.
- `prompt` (str, optional): Текст запроса для генерации изображения. По умолчанию `None`.
- `proxy` (str, optional): Прокси-сервер для подключения к API. По умолчанию `None`.
- `max_tokens` (int, optional): Максимальное количество токенов в ответе. По умолчанию 512.
- `temperature` (float, optional): Температура для генерации текста. По умолчанию 1.
- `top_p` (float, optional): Top-p для генерации текста. По умолчанию 1.
- `stream` (bool, optional): Указывает, использовать ли потоковую передачу данных. По умолчанию `True`.
- `size` (str, optional): Размер изображения. По умолчанию "1:1".
- `seed` (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Как работает**:
1. Получает фактическое имя модели из псевдонима с помощью метода `get_model`.
2. Если модель является моделью для генерации изображений, генерирует изображение с помощью метода `generate_image`.
3. Если модель не является моделью для генерации изображений, генерирует текст с помощью метода `generate_text`.

**Примеры**:
```python
messages = [{"role": "user", "content": "Hello, world!"}]
async for result in Airforce.create_async_generator(model="llama-3.1-70b-chat", messages=messages):
    print(result)
```