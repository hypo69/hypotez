# Модуль HuggingFaceInference

## Обзор

Модуль `HuggingFaceInference` предназначен для взаимодействия с моделями Hugging Face Inference API. Он поддерживает как текстовые, так и графические модели, предоставляя функциональность для генерации текста и изображений на основе предоставленных входных данных. Модуль асинхронный и использует генераторы для обработки потоковых ответов от API.

## Подробней

Модуль является частью системы, взаимодействующей с Hugging Face Inference API для выполнения задач генерации текста и изображений. Он включает в себя поддержку различных моделей и форматов запросов, а также обработку ошибок и исключений, которые могут возникнуть в процессе взаимодействия с API.

## Классы

### `HuggingFaceInference`

**Описание**: Класс `HuggingFaceInference` предоставляет функциональность для взаимодействия с Hugging Face Inference API. Он поддерживает как текстовые, так и графические модели, предоставляя функциональность для генерации текста и изображений на основе предоставленных входных данных.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL Hugging Face.
- `parent` (str): Родительский провайдер.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `default_model` (str): Модель по умолчанию для текстовых задач.
- `default_image_model` (str): Модель по умолчанию для графических задач.
- `model_aliases` (dict): Алиасы моделей.
- `image_models` (list): Список поддерживаемых графических моделей.
- `model_data` (dict): Кэш данных моделей.

**Методы**:
- `get_models()`: Возвращает список поддерживаемых моделей.
- `get_model_data(session: StreamSession, model: str)`: Возвращает данные о модели из API.
- `create_async_generator(...)`: Создает асинхронный генератор для взаимодействия с API.

## Методы класса

### `get_models`

```python
@classmethod
def get_models() -> list[str]:
    """ Функция возвращает список поддерживаемых моделей.

    Returns:
        list[str]: Список поддерживаемых моделей.
    """
```

**Назначение**:
Функция `get_models` возвращает список поддерживаемых моделей, получая информацию как из статических списков, так и из API Hugging Face.

**Как работает функция**:
- Если список моделей ещё не был загружен, функция выполняет следующие действия:
  - Копирует список текстовых моделей `text_models`.
  - Запрашивает список популярных текстовых моделей из API Hugging Face (`https://huggingface.co/api/models?inference=warm&pipeline_tag=text-generation`).
  - Добавляет популярные модели в общий список, избегая дублирования.
  - Запрашивает список моделей для генерации изображений из API Hugging Face (`https://huggingface.co/api/models?pipeline_tag=text-to-image`).
  - Добавляет модели для генерации изображений в общий список, избегая дублирования.
  - Объединяет все модели в общий список `models`.
- Функция кэширует список моделей в атрибуте класса `cls.models` для последующего использования.

**Примеры**:
```python
models = HuggingFaceInference.get_models()
print(models)
```

### `get_model_data`

```python
@classmethod
async def get_model_data(cls, session: StreamSession, model: str) -> str:
    """ Функция возвращает данные о модели из API.

    Args:
        session (StreamSession): Асинхровая сессия для выполнения HTTP-запросов.
        model (str): Название модели.

    Returns:
        str: Данные о модели в формате JSON.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
    """
```

**Назначение**:
Функция `get_model_data` асинхронно получает данные о конкретной модели из API Hugging Face.

**Как работает функция**:
- Проверяет, есть ли данные о модели в кэше `cls.model_data`. Если есть, возвращает их.
- Если данных в кэше нет, выполняет GET-запрос к API Hugging Face (`https://huggingface.co/api/models/{model}`) для получения информации о модели.
- Если запрос возвращает статус 404, выбрасывает исключение `ModelNotSupportedError`.
- Кэширует полученные данные в `cls.model_data` и возвращает их.

**Примеры**:
```python
import asyncio
from aiohttp import ClientSession

async def main():
    async with ClientSession() as session:
        model_data = await HuggingFaceInference.get_model_data(session, "gpt2")
        print(model_data)

asyncio.run(main())
```

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    stream: bool = True,
    proxy: str = None,
    timeout: int = 600,
    api_base: str = "https://api-inference.huggingface.co",
    api_key: str = None,
    max_tokens: int = 1024,
    temperature: float = None,
    prompt: str = None,
    action: str = None,
    extra_data: dict = {},
    seed: int = None,
    aspect_ratio: str = None,
    width: int = None,
    height: int = None,
    **kwargs
) -> AsyncResult:
    """ Функция создает асинхронный генератор для взаимодействия с API.

    Args:
        model (str): Название модели.
        messages (Messages): Список сообщений для формирования запроса.
        stream (bool, optional): Флаг, указывающий на использование потокового режима. По умолчанию `True`.
        proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
        timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 600.
        api_base (str, optional): Базовый URL API. По умолчанию `"https://api-inference.huggingface.co"`.
        api_key (str, optional): API-ключ. По умолчанию `None`.
        max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию 1024.
        temperature (float, optional): Температура для генерации текста. По умолчанию `None`.
        prompt (str, optional): Дополнительный промпт для запроса. По умолчанию `None`.
        action (str, optional): Действие, которое нужно выполнить. По умолчанию `None`.
        extra_data (dict, optional): Дополнительные данные для запроса. По умолчанию `{}`.
        seed (int, optional): Зерно для генерации случайных чисел. По умолчанию `None`.
        aspect_ratio (str, optional): Соотношение сторон изображения. По умолчанию `None`.
        width (int, optional): Ширина изображения. По умолчанию `None`.
        height (int, optional): Высота изображения. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Yields:
        AsyncResult: Части ответа API.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
        ResponseError: Если произошла ошибка при выполнении запроса.
    """
```

**Назначение**:
Функция `create_async_generator` создает асинхронный генератор для взаимодействия с API Hugging Face Inference.

**Как работает функция**:

1.  **Подготовка заголовков**:
    *   Формирует заголовки запроса, включая `Content-Type` и `Authorization` (если предоставлен `api_key`).

2.  **Создание сессии**:
    *   Использует `StreamSession` для выполнения асинхронных HTTP-запросов.

3.  **Обработка потоковых ответов**:
    *   Если `stream=True`, обрабатывает потоковые ответы от API:
        *   Читает ответ построчно, начиная с `data:`.
        *   Извлекает данные из JSON-формата каждой строки.
        *   Проверяет наличие ошибок в данных.
        *   Извлекает текстовые фрагменты из токенов, исключая специальные токены.
        *   Удаляет лишние пробелы в начале первого фрагмента (если это не продолжение).
        *   Возвращает фрагменты текста с помощью `yield`.
        *   Возвращает `FinishReason("stop" if is_special else "length")`, чтобы указать причину завершения.

4.  **Обработка не потоковых ответов**:
    *   Если `stream=False`, обрабатывает ответ целиком:
        *   Вызывает функцию `save_response_media` для сохранения медиа-файлов ответа (изображений).
        *   Извлекает сгенерированный текст из ответа JSON.
        *   Удаляет лишние пробелы в начале и конце текста.
        *   Возвращает текст с помощью `yield`.

**Внутренние функции**:
В данной функции не используются внутренние функции.

**Примеры**:

```python
import asyncio

from src.logger import logger

async def main():
    messages = [
        {"role": "user", "content": "Напиши короткий рассказ о кошке."},
    ]
    async for chunk in HuggingFaceInference.create_async_generator(model="gpt2", messages=messages):
        print(chunk, end="")

asyncio.run(main())
```

## Функции

### `format_prompt_mistral`

```python
def format_prompt_mistral(messages: Messages, do_continue: bool = False) -> str:
    """ Функция форматирует промпт для модели Mistral.

    Args:
        messages (Messages): Список сообщений для формирования промпта.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего запроса. По умолчанию `False`.

    Returns:
        str: Сформированный промпт.
    """
```

**Назначение**:
Функция `format_prompt_mistral` форматирует список сообщений в строку, пригодную для использования в качестве промпта для модели Mistral.

**Как работает функция**:
- Извлекает системные сообщения из списка сообщений.
- Формирует строку вопроса, объединяя последнее сообщение пользователя и системные сообщения.
- Формирует историю, объединяя сообщения пользователя и ассистента в формате `<s>[INST] {user_message} [/INST] {assistant_message}</s>`.
- Если `do_continue` равно `True`, возвращает историю без завершающего тега `</s>`.
- Иначе возвращает полную строку промпта, включающую историю и вопрос в формате `f"{history}\\n<s>[INST] {question} [/INST]"`.

**Примеры**:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is the population of Paris?"}
]
prompt = format_prompt_mistral(messages)
print(prompt)
```

### `format_prompt_qwen`

```python
def format_prompt_qwen(messages: Messages, do_continue: bool = False) -> str:
    """ Функция форматирует промпт для модели Qwen.

    Args:
        messages (Messages): Список сообщений для формирования промпта.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего запроса. По умолчанию `False`.

    Returns:
        str: Сформированный промпт.
    """
```

**Назначение**:
Функция `format_prompt_qwen` форматирует список сообщений в строку, пригодную для использования в качестве промпта для модели Qwen.

**Как работает функция**:
- Объединяет сообщения в формате `<|im_start|>{role}\n{content}\n<|im_end|>\n`.
- Если `do_continue` равно `True`, возвращает строку без завершающего тега `<|im_start|>assistant\n`.
- Иначе возвращает полную строку промпта.

**Примеры**:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is the population of Paris?"}
]
prompt = format_prompt_qwen(messages)
print(prompt)
```

### `format_prompt_qwen2`

```python
def format_prompt_qwen2(messages: Messages, do_continue: bool = False) -> str:
    """ Функция форматирует промпт для модели Qwen2.

    Args:
        messages (Messages): Список сообщений для формирования промпта.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего запроса. По умолчанию `False`.

    Returns:
        str: Сформированный промпт.
    """
```

**Назначение**:
Функция `format_prompt_qwen2` форматирует список сообщений в строку, пригодную для использования в качестве промпта для модели Qwen2.

**Как работает функция**:
- Объединяет сообщения в формате `\u003C｜{role.capitalize()}｜\u003E{content}\u003C｜end of sentence｜\u003E`.
- Если `do_continue` равно `True`, возвращает строку без завершающего тега `\u003C｜Assistant｜\u003E`.
- Иначе возвращает полную строку промпта.

**Примеры**:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is the population of Paris?"}
]
prompt = format_prompt_qwen2(messages)
print(prompt)
```

### `format_prompt_llama`

```python
def format_prompt_llama(messages: Messages, do_continue: bool = False) -> str:
    """ Функция форматирует промпт для модели Llama.

    Args:
        messages (Messages): Список сообщений для формирования промпта.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего запроса. По умолчанию `False`.

    Returns:
        str: Сформированный промпт.
    """
```

**Назначение**:
Функция `format_prompt_llama` форматирует список сообщений в строку, пригодную для использования в качестве промпта для модели Llama.

**Как работает функция**:
- Объединяет сообщения в формате `<|begin_of_text|><|start_header_id|>{role}<|end_header_id|>\n\n{content}\n<|eot_id|>\n`.
- Если `do_continue` равно `True`, возвращает строку без завершающего тега `\n<|eot_id|>\n`.
- Иначе возвращает полную строку промпта.

**Примеры**:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is the population of Paris?"}
]
prompt = format_prompt_llama(messages)
print(prompt)
```

### `format_prompt_custom`

```python
def format_prompt_custom(messages: Messages, end_token: str = "</s>", do_continue: bool = False) -> str:
    """ Функция форматирует промпт с пользовательским токеном конца.

    Args:
        messages (Messages): Список сообщений для формирования промпта.
        end_token (str, optional): Токен конца сообщения. По умолчанию `"</s>"`.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего запроса. По умолчанию `False`.

    Returns:
        str: Сформированный промпт.
    """
```

**Назначение**:
Функция `format_prompt_custom` форматирует список сообщений в строку, используя заданный токен конца сообщения.

**Как работает функция**:
- Объединяет сообщения в формате `<|{role}|>\n{content}{end_token}\n`.
- Если `do_continue` равно `True`, возвращает строку без завершающего тега `{end_token}\n`.
- Иначе возвращает полную строку промпта.

**Примеры**:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is the population of Paris?"}
]
prompt = format_prompt_custom(messages, end_token="<|end|>")
print(prompt)
```

### `get_inputs`

```python
def get_inputs(messages: Messages, model_data: dict, model_type: str, do_continue: bool = False) -> str:
    """ Функция выбирает формат промпта в зависимости от типа модели.

    Args:
        messages (Messages): Список сообщений для формирования промпта.
        model_data (dict): Данные о модели.
        model_type (str): Тип модели.
        do_continue (bool, optional): Флаг, указывающий на продолжение предыдущего запроса. По умолчанию `False`.

    Returns:
        str: Сформированный промпт.
    """
```

**Назначение**:
Функция `get_inputs` выбирает и применяет правильный формат промпта на основе типа модели и данных о модели.

**Как работает функция**:
- В зависимости от `model_type`, вызываются различные функции форматирования промптов:
  - Если `model_type` - один из `("gpt2", "gpt_neo", "gemma", "gemma2")`, используется `format_prompt`.
  - Если `model_type == "mistral"` и автор модели `mistralai`, используется `format_prompt_mistral`.
  - В противном случае проверяется наличие `eos_token` в данных о модели и на его основе выбирается функция форматирования:
    - Если `eos_token` - один из `("<|endoftext|>", "<eos>", "</s>")`, используется `format_prompt_custom`.
    - Если `eos_token == "<|im_end|>"` используется `format_prompt_qwen`.
    - Если `"content" in eos_token and eos_token["content"] == "\\u003C｜end of sentence｜\\u003E"`, используется `format_prompt_qwen2`.
    - Если `eos_token == "<|eot_id|>"` используется `format_prompt_llama`.
    - В противном случае используется `format_prompt`.

**Примеры**:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is the population of Paris?"}
]
model_data = {"config": {"tokenizer_config": {"eos_token": "</s>"}}}
model_type = "gpt2"
prompt = get_inputs(messages, model_data, model_type)
print(prompt)