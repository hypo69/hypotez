# Модуль Airforce - Бесплатный провайдер GPT-4

## Обзор

Модуль `Airforce` предоставляет доступ к бесплатному API GPT-4, который позволяет генерировать текст и изображения. Он реализует интерфейсы `AsyncGeneratorProvider` и `ProviderModelMixin` для удобства использования.

## Подробей

Модуль Airforce использует API Airforce, чтобы предоставить возможность генерировать текст и изображения с помощью моделей GPT-4. Он поддерживает как потоковый режим (`stream = True`) для получения результатов по частям, так и не потоковый (`stream = False`) для получения всего ответа сразу.

## Классы

### `class Airforce`

**Описание**: Класс `Airforce` реализует функциональность провайдера Airforce для GPT-4. Он наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, обеспечивая базовые функции генерации текста и изображений.

**Наследует**: 
  - `AsyncGeneratorProvider`:  Предоставляет методы для асинхронной генерации текста.
  - `ProviderModelMixin`: Обеспечивает функции для работы с моделями GPT-4.

**Атрибуты**:
  - `url (str)`: Базовый URL API Airforce.
  - `api_endpoint_completions (str)`:  URL-путь для запросов к модели GPT-4 для генерации текста.
  - `api_endpoint_imagine2 (str)`: URL-путь для запросов к модели GPT-4 для генерации изображений.
  - `working (bool)`: Указывает, работает ли провайдер. 
  - `supports_stream (bool)`: Указывает, поддерживает ли провайдер потоковую генерацию.
  - `supports_system_message (bool)`: Указывает, поддерживает ли провайдер системные сообщения.
  - `supports_message_history (bool)`: Указывает, поддерживает ли провайдер историю сообщений.
  - `default_model (str)`:  Модель по умолчанию для генерации текста.
  - `default_image_model (str)`: Модель по умолчанию для генерации изображений.
  - `models (List[str])`: Список доступных текстовых моделей.
  - `image_models (List[str])`: Список доступных моделей для генерации изображений.
  - `hidden_models (set[str])`: Набор скрытых моделей, которые не должны быть доступны пользователю.
  - `additional_models_imagine (List[str])`: Дополнительные модели для генерации изображений.
  - `model_aliases (dict[str, str])`: Словарь, который сопоставляет псевдонимы моделей с их фактическими именами.

**Методы**:

  - `get_models()`: Возвращает список доступных моделей.
  - `get_model(model: str) -> str`: Возвращает фактическое имя модели по её псевдониму.
  - `_filter_content(part_response: str) -> str`: Фильтрует частичные ответы, удаляя нежелательный контент.
  - `_filter_response(response: str) -> str`: Фильтрует полный ответ, удаляя системные ошибки и нежелательный текст.
  - `generate_image(model: str, prompt: str, size: str, seed: int, proxy: str = None) -> AsyncResult`:  Генерирует изображение.
  - `generate_text(model: str, messages: Messages, max_tokens: int, temperature: float, top_p: float, stream: bool, proxy: str = None) -> AsyncResult`: Генерирует текст.
  - `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, max_tokens: int = 512, temperature: float = 1, top_p: float = 1, stream: bool = True, size: str = "1:1", seed: int = None, **kwargs) -> AsyncResult`: Создает асинхронный генератор для генерации текста или изображения.

## Методы класса

### `get_models()`

**Назначение**: Возвращает список доступных моделей GPT-4.

**Параметры**:
  - Отсутствуют.

**Возвращает**:
  - `List[str]`: Список доступных моделей.

**Как работает функция**:
  - Метод `get_models` использует API Airforce для получения списка доступных моделей GPT-4. 
  - Он обрабатывает ошибки запроса к API и возвращает список моделей. 
  - Также этот метод дополняет список моделей GPT-4 моделями, предназначенными для генерации изображений.
  - Исключает из списка доступных моделей, нежелательные.

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

  # Получение списка доступных моделей
  available_models = Airforce.get_models()

  # Печать списка моделей
  print(available_models)
  ```

### `get_model(model: str) -> str`

**Назначение**: Возвращает фактическое имя модели по её псевдониму.

**Параметры**:
  - `model (str)`: Псевдоним модели.

**Возвращает**:
  - `str`: Фактическое имя модели или псевдоним, если имя не найдено.

**Как работает функция**:
  - Метод `get_model` проверяет, существует ли псевдоним модели в словаре `model_aliases`.
  - Если псевдоним найден, он возвращает соответствующее фактическое имя модели.
  - В противном случае он возвращает переданный псевдоним или модель по умолчанию (`default_model`).

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

  # Получение фактического имени модели по псевдониму
  actual_model_name = Airforce.get_model("openchat-3.5")

  # Печать фактического имени модели
  print(actual_model_name) # Вывод: "openchat-3.5-0106"
  ```

### `_filter_content(part_response: str) -> str`

**Назначение**: Фильтрует частичные ответы, удаляя нежелательный контент.

**Параметры**:
  - `part_response (str)`: Частичный ответ, который необходимо фильтровать.

**Возвращает**:
  - `str`: Отфильтрованный частичный ответ.

**Как работает функция**:
  - Метод `_filter_content` использует регулярные выражения для удаления нежелательного контента из частичных ответов.
  - Он удаляет ссылки на Discord, которые часто появляются в ответах от GPT-4, а также сообщения об ошибках.

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

  # Пример частичного ответа с нежелательным контентом
  partial_response = "One message exceeds the 1000chars per message limit... https://discord.com/invite/..."

  # Фильтрация частичного ответа
  filtered_response = Airforce._filter_content(partial_response)

  # Печать отфильтрованного ответа
  print(filtered_response) # Вывод: ""
  ```

### `_filter_response(response: str) -> str`

**Назначение**: Фильтрует полный ответ, удаляя системные ошибки и нежелательный текст.

**Параметры**:
  - `response (str)`: Полный ответ, который необходимо фильтровать.

**Возвращает**:
  - `str`: Отфильтрованный полный ответ.

**Как работает функция**:
  - Метод `_filter_response` применяет несколько регулярных выражений для удаления нежелательного контента из полного ответа.
  - Он удаляет сообщения об ошибках, которые часто появляются в ответах от GPT-4, а также специальные символы, которые могут быть нежелательны.

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

  # Пример полного ответа с системными ошибками
  full_response = "[ERROR] 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx' Model not found or too long input. Or any other error (xD)"

  # Фильтрация полного ответа
  filtered_response = Airforce._filter_response(full_response)

  # Печать отфильтрованного ответа
  print(filtered_response) # Вывод: ""
  ```

### `generate_image(model: str, prompt: str, size: str, seed: int, proxy: str = None) -> AsyncResult`

**Назначение**: Генерирует изображение с помощью модели GPT-4.

**Параметры**:
  - `model (str)`:  Модель для генерации изображения.
  - `prompt (str)`: Текстовое описание изображения.
  - `size (str)`: Размер изображения.
  - `seed (int)`: Случайное число для генерации изображения.
  - `proxy (str, optional)`: Прокси-сервер для запроса. По умолчанию `None`.

**Возвращает**:
  - `AsyncResult`: Асинхронный результат, который содержит URL сгенерированного изображения.

**Как работает функция**:
  - Метод `generate_image` отправляет запрос к API Airforce с использованием модели GPT-4, указанной в `model`, для генерации изображения по заданному `prompt`.
  - Он использует указанные `size` и `seed` для настройки процесса генерации.
  -  Метод возвращает асинхронный результат, который содержит URL изображения.

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

  # Генерация изображения с помощью модели "flux"
  image_result = Airforce.generate_image(model="flux", prompt="A beautiful sunset over the ocean", size="512:512", seed=1234)

  # Получение URL изображения
  image_url = image_result.images[0]

  # Вывод URL изображения
  print(image_url)
  ```

### `generate_text(model: str, messages: Messages, max_tokens: int, temperature: float, top_p: float, stream: bool, proxy: str = None) -> AsyncResult`

**Назначение**: Генерирует текст с помощью модели GPT-4.

**Параметры**:
  - `model (str)`: Модель для генерации текста.
  - `messages (Messages)`: Список сообщений для модели GPT-4.
  - `max_tokens (int)`: Максимальное количество токенов в ответе.
  - `temperature (float)`: Температура генерации, влияет на креативность ответа.
  - `top_p (float)`: Вероятность выбора токена.
  - `stream (bool)`:  Включить потоковый режим (по частям).
  - `proxy (str, optional)`: Прокси-сервер для запроса. По умолчанию `None`.

**Возвращает**:
  - `AsyncResult`: Асинхронный результат, который содержит сгенерированный текст.

**Как работает функция**:
  - Метод `generate_text` отправляет запрос к API Airforce с использованием модели GPT-4, указанной в `model`, для генерации текста.
  - Он использует `messages`, `max_tokens`, `temperature`, `top_p` и `stream` для настройки процесса генерации.
  - Он обрабатывает ответы от API, фильтруя их, и возвращает асинхронный результат, который содержит сгенерированный текст.

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

  # Создание списка сообщений для модели GPT-4
  messages = [
      {"role": "user", "content": "Напиши мне стихотворение о любви."}
  ]

  # Генерация текста с помощью модели "llama-3.1-70b-chat"
  text_result = Airforce.generate_text(model="llama-3.1-70b-chat", messages=messages, max_tokens=512, temperature=0.7, top_p=1, stream=False)

  # Получение сгенерированного текста
  generated_text = text_result[0]

  # Вывод сгенерированного текста
  print(generated_text)
  ```

### `create_async_generator(model: str, messages: Messages, prompt: str = None, proxy: str = None, max_tokens: int = 512, temperature: float = 1, top_p: float = 1, stream: bool = True, size: str = "1:1", seed: int = None, **kwargs) -> AsyncResult`

**Назначение**: Создает асинхронный генератор для генерации текста или изображения.

**Параметры**:
  - `model (str)`: Модель для генерации текста или изображения.
  - `messages (Messages)`: Список сообщений для модели GPT-4.
  - `prompt (str, optional)`: Текстовое описание изображения (для генерации изображения). По умолчанию `None`.
  - `proxy (str, optional)`: Прокси-сервер для запроса. По умолчанию `None`.
  - `max_tokens (int, optional)`: Максимальное количество токенов в ответе (для генерации текста). По умолчанию `512`.
  - `temperature (float, optional)`: Температура генерации, влияет на креативность ответа (для генерации текста). По умолчанию `1`.
  - `top_p (float, optional)`: Вероятность выбора токена (для генерации текста). По умолчанию `1`.
  - `stream (bool, optional)`:  Включить потоковый режим (по частям) (для генерации текста). По умолчанию `True`.
  - `size (str, optional)`: Размер изображения (для генерации изображения). По умолчанию "1:1".
  - `seed (int, optional)`: Случайное число для генерации изображения (для генерации изображения). По умолчанию `None`.
  - `**kwargs`: Дополнительные аргументы.

**Возвращает**:
  - `AsyncResult`: Асинхронный результат, который содержит сгенерированный текст или URL изображения.

**Как работает функция**:
  - Метод `create_async_generator` определяет фактическое имя модели, используя `get_model`.
  - Он определяет, является ли модель моделью для генерации текста или изображения.
  - В зависимости от типа модели он вызывает `generate_text` или `generate_image` для генерации текста или изображения.
  - Метод возвращает асинхронный результат, который содержит сгенерированный текст или URL изображения.

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

  # Генерация текста с помощью модели "llama-3.1-70b-chat"
  async_generator = Airforce.create_async_generator(model="llama-3.1-70b-chat", messages=messages, max_tokens=512, temperature=0.7, top_p=1, stream=False)

  # Получение сгенерированного текста
  async for result in async_generator:
      print(result)

  # Генерация изображения с помощью модели "flux"
  async_generator = Airforce.create_async_generator(model="flux", prompt="A beautiful sunset over the ocean", size="512:512", seed=1234)

  # Получение URL изображения
  async for result in async_generator:
      print(result.images[0])
  ```

## Параметры класса

  - `url (str)`: Базовый URL API Airforce. 
  - `api_endpoint_completions (str)`: URL-путь для запросов к модели GPT-4 для генерации текста.
  - `api_endpoint_imagine2 (str)`: URL-путь для запросов к модели GPT-4 для генерации изображений.
  - `working (bool)`: Указывает, работает ли провайдер. 
  - `supports_stream (bool)`: Указывает, поддерживает ли провайдер потоковую генерацию.
  - `supports_system_message (bool)`: Указывает, поддерживает ли провайдер системные сообщения.
  - `supports_message_history (bool)`: Указывает, поддерживает ли провайдер историю сообщений.
  - `default_model (str)`:  Модель по умолчанию для генерации текста.
  - `default_image_model (str)`: Модель по умолчанию для генерации изображений.
  - `models (List[str])`: Список доступных текстовых моделей.
  - `image_models (List[str])`: Список доступных моделей для генерации изображений.
  - `hidden_models (set[str])`: Набор скрытых моделей, которые не должны быть доступны пользователю.
  - `additional_models_imagine (List[str])`: Дополнительные модели для генерации изображений.
  - `model_aliases (dict[str, str])`: Словарь, который сопоставляет псевдонимы моделей с их фактическими именами.

## Внутренние функции 

### `split_message(message: str, max_length: int = 1000) -> List[str]`

**Назначение**: Разделяет сообщение на части, не превышающие максимальную длину.

**Параметры**:
  - `message (str)`: Сообщение, которое необходимо разделить.
  - `max_length (int, optional)`: Максимальная длина части сообщения. По умолчанию `1000`.

**Возвращает**:
  - `List[str]`: Список частей сообщения, разделенных на части, не превышающие `max_length`.

**Как работает функция**:
  - Функция `split_message` разбивает сообщение на части, не превышающие максимальную длину `max_length`.
  - Она ищет пробелы в сообщении, чтобы разделить его на части.
  - Если пробелы не найдены, она разделяет сообщение по максимальной длине.

**Примеры**:
  ```python
  from src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import split_message

  # Разделение сообщения на части с максимальной длиной 10
  message = "Это очень длинное сообщение, которое нужно разделить на части."
  parts = split_message(message, max_length=10)

  # Печать частей сообщения
  print(parts) # Вывод: ['Это очень', 'длинное', 'сообщение,', 'которое', 'нужно', 'разделить', 'на', 'части.']
  ```