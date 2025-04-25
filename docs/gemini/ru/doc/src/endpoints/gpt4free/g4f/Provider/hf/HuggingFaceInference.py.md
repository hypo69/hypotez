# Модуль HuggingFaceInference

## Обзор

Модуль `HuggingFaceInference` предоставляет асинхронный генератор для взаимодействия с различными моделями, доступными на платформе Hugging Face, используя их API для вывода текста и изображений. 

## Подробнее

Модуль `HuggingFaceInference` реализует асинхронный генератор, который позволяет взаимодействовать с моделями Hugging Face, такими как `gpt2`, `gpt_neo`, `mistral`, `llama`, `qwen`, `qwen2` и другие. Он использует API Hugging Face для вывода текста и изображений, позволяя получить асинхронный поток ответов от модели. 

## Классы

### `class HuggingFaceInference`

**Описание**: Класс `HuggingFaceInference` реализует асинхронный генератор для вывода текста и изображений с использованием моделей Hugging Face. Наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin`.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовые функции для асинхронной генерации.
- `ProviderModelMixin`: Предоставляет функции для работы с моделями.

**Атрибуты**:

- `url (str)`: Базовый URL для API Hugging Face.
- `parent (str)`: Название платформы модели.
- `working (bool)`: Указывает на доступность API.
- `default_model (str)`:  Название модели по умолчанию для генерации текста.
- `default_image_model (str)`: Название модели по умолчанию для генерации изображений.
- `model_aliases (dict)`: Словарь с псевдонимами для моделей.
- `image_models (list)`: Список моделей для генерации изображений.
- `model_data (dict)`: Словарь с данными о моделях.

**Методы**:

- `get_models()`:  Возвращает список доступных моделей.
- `get_model_data(session: StreamSession, model: str) -> str`: Получает данные о модели с API Hugging Face.
- `create_async_generator()`:  Создает асинхронный генератор для вывода текста или изображений с использованием выбранной модели.

**Принцип работы**:

Класс `HuggingFaceInference` реализует асинхронный генератор для взаимодействия с моделями Hugging Face. Он использует API Hugging Face для вывода текста и изображений, позволяя получить асинхронный поток ответов от модели. 

**Методы**:

- `get_models()`:  Этот метод возвращает список доступных моделей, которые могут быть использованы для генерации текста или изображений. Он получает список моделей с API Hugging Face.
- `get_model_data(session: StreamSession, model: str) -> str`:  Этот метод получает данные о модели с API Hugging Face. Он принимает в качестве аргументов сессию `StreamSession` и имя модели. В случае успеха возвращает данные о модели в формате JSON.
- `create_async_generator()`:  Этот метод создает асинхронный генератор для вывода текста или изображений с использованием выбранной модели. Он принимает в качестве аргументов имя модели, список сообщений `messages`, флаг потоковой передачи `stream`, прокси-сервер `proxy`, время ожидания `timeout`, базовый URL API `api_base`, ключ API `api_key`, максимальное количество токенов `max_tokens`, температуру `temperature`, подсказку `prompt`, действие `action`, дополнительные данные `extra_data`, seed `seed`, аспектный коэффициент `aspect_ratio`, ширину `width` и высоту `height`.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingFaceInference import HuggingFaceInference

# Создание экземпляра класса
huggingface_inference = HuggingFaceInference()

# Получение списка доступных моделей
models = huggingface_inference.get_models()

# Получение данных о модели
model_data = huggingface_inference.get_model_data(session, "gpt2")

# Создание асинхронного генератора
async_generator = huggingface_inference.create_async_generator(model="gpt2", messages=[{"role": "user", "content": "Привет"}], stream=True)

# Использование генератора
async for chunk in async_generator:
    print(chunk)
```

## Внутренние функции

### `format_prompt_mistral(messages: Messages, do_continue: bool = False) -> str`:

**Назначение**: Форматирует подсказку для модели Mistral. 

**Параметры**:
- `messages (Messages)`: Список сообщений для модели.
- `do_continue (bool)`: Флаг для продолжения генерации.

**Возвращает**:
- `str`: Сформированная подсказка.

**Как работает**:
-  Функция `format_prompt_mistral` форматирует подсказку для модели Mistral,  собирая сообщения в необходимый формат.

### `format_prompt_qwen(messages: Messages, do_continue: bool = False) -> str`:

**Назначение**: Форматирует подсказку для модели Qwen. 

**Параметры**:
- `messages (Messages)`: Список сообщений для модели.
- `do_continue (bool)`: Флаг для продолжения генерации.

**Возвращает**:
- `str`: Сформированная подсказка.

**Как работает**:
-  Функция `format_prompt_qwen` форматирует подсказку для модели Qwen,  собирая сообщения в необходимый формат.

### `format_prompt_qwen2(messages: Messages, do_continue: bool = False) -> str`:

**Назначение**: Форматирует подсказку для модели Qwen2. 

**Параметры**:
- `messages (Messages)`: Список сообщений для модели.
- `do_continue (bool)`: Флаг для продолжения генерации.

**Возвращает**:
- `str`: Сформированная подсказка.

**Как работает**:
-  Функция `format_prompt_qwen2` форматирует подсказку для модели Qwen2,  собирая сообщения в необходимый формат.

### `format_prompt_llama(messages: Messages, do_continue: bool = False) -> str`:

**Назначение**: Форматирует подсказку для модели Llama. 

**Параметры**:
- `messages (Messages)`: Список сообщений для модели.
- `do_continue (bool)`: Флаг для продолжения генерации.

**Возвращает**:
- `str`: Сформированная подсказка.

**Как работает**:
-  Функция `format_prompt_llama` форматирует подсказку для модели Llama,  собирая сообщения в необходимый формат.

### `format_prompt_custom(messages: Messages, end_token: str = "</s>", do_continue: bool = False) -> str`:

**Назначение**: Форматирует подсказку для модели с использованием пользовательского токена окончания. 

**Параметры**:
- `messages (Messages)`: Список сообщений для модели.
- `end_token (str)`: Токен окончания текста.
- `do_continue (bool)`: Флаг для продолжения генерации.

**Возвращает**:
- `str`: Сформированная подсказка.

**Как работает**:
-  Функция `format_prompt_custom` форматирует подсказку для модели с использованием пользовательского токена окончания,  собирая сообщения в необходимый формат.

### `get_inputs(messages: Messages, model_data: dict, model_type: str, do_continue: bool = False) -> str`:

**Назначение**: Форматирует подсказку для модели в зависимости от её типа. 

**Параметры**:
- `messages (Messages)`: Список сообщений для модели.
- `model_data (dict)`: Данные о модели.
- `model_type (str)`: Тип модели.
- `do_continue (bool)`: Флаг для продолжения генерации.

**Возвращает**:
- `str`: Сформированная подсказка.

**Как работает**:
- Функция `get_inputs` выбирает соответствующую функцию форматирования подсказки в зависимости от типа модели и формирует её.


```markdown
## Параметры класса

- `url (str)`: Базовый URL для API Hugging Face, по умолчанию `https://huggingface.co`.
- `parent (str)`: Название платформы модели, по умолчанию `HuggingFace`.
- `working (bool)`: Флаг, указывающий на доступность API, по умолчанию `True`.
- `default_model (str)`: Название модели по умолчанию для генерации текста.
- `default_image_model (str)`: Название модели по умолчанию для генерации изображений.
- `model_aliases (dict)`: Словарь с псевдонимами для моделей.
- `image_models (list)`: Список моделей для генерации изображений.
- `model_data (dict)`: Словарь с данными о моделях.


## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf.HuggingFaceInference import HuggingFaceInference

# Создание экземпляра класса
huggingface_inference = HuggingFaceInference()

# Получение списка доступных моделей
models = huggingface_inference.get_models()

# Получение данных о модели
model_data = huggingface_inference.get_model_data(session, "gpt2")

# Создание асинхронного генератора
async_generator = huggingface_inference.create_async_generator(model="gpt2", messages=[{"role": "user", "content": "Привет"}], stream=True)

# Использование генератора
async for chunk in async_generator:
    print(chunk)
```