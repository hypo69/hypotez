# Модуль HuggingFaceInference

## Обзор

Модуль `HuggingFaceInference` предназначен для взаимодействия с моделями Hugging Face Inference API. Он предоставляет функциональность для генерации текста и изображений, используя различные модели, размещенные на платформе Hugging Face. Модуль поддерживает как потоковую передачу данных, так и обработку изображений, а также предоставляет возможность настраивать параметры запросов, такие как максимальное количество токенов, температуру и случайное начальное число.

## Подробней

Модуль `HuggingFaceInference` является асинхронным провайдером, который позволяет взаимодействовать с API Hugging Face для выполнения задач генерации текста и изображений. Он использует библиотеку `requests` для отправки HTTP-запросов и `json` для обработки данных в формате JSON. Модуль также включает поддержку потоковой передачи данных, что позволяет получать результаты генерации в режиме реального времени.

## Классы

### `HuggingFaceInference`

**Описание**: Класс `HuggingFaceInference` является основным классом, предоставляющим функциональность для взаимодействия с Hugging Face Inference API.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL главной страницы Hugging Face.
- `parent` (str): Название родительского провайдера ("HuggingFace").
- `working` (bool): Флаг, указывающий на работоспособность провайдера (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию для генерации текста.
- `default_image_model` (str): Модель, используемая по умолчанию для генерации изображений.
- `model_aliases` (dict): Словарь псевдонимов моделей.
- `image_models` (list): Список моделей, поддерживающих генерацию изображений.
- `model_data` (dict[str, dict]): Кэш для хранения данных о моделях.

**Методы**:
- `get_models()`: Возвращает список доступных моделей.
- `get_model_data(session: StreamSession, model: str)`: Возвращает данные о конкретной модели.
- `create_async_generator(...)`: Создает асинхронный генератор для выполнения запросов к API Hugging Face.

## Методы класса

### `get_models`

```python
@classmethod
def get_models() -> list[str]:
    """Возвращает список доступных моделей.

    Извлекает список моделей для генерации текста и изображений из API Hugging Face.

    Returns:
        list[str]: Список идентификаторов доступных моделей.
    """
```

**Назначение**:
Метод `get_models` предназначен для получения списка доступных моделей из API Hugging Face. Он выполняет HTTP-запросы к API для получения списка моделей для генерации текста и изображений, а затем объединяет эти списки в один общий список.

**Как работает функция**:
1. Проверяет, был ли уже получен список моделей (`cls.models`). Если да, возвращает его.
2. Инициализирует список `models` копией списка `text_models`.
3. Выполняет GET-запрос к API Hugging Face для получения списка моделей для генерации текста.
4. Если запрос успешен, извлекает идентификаторы моделей с `trendingScore >= 10` и добавляет их в список `models`.
5. Выполняет GET-запрос к API Hugging Face для получения списка моделей для генерации изображений.
6. Если запрос успешен, извлекает идентификаторы моделей с `trendingScore >= 20` и добавляет их в список `cls.image_models`.
7. Расширяет список `models` моделями генерации изображений.
8. Сохраняет полученный список моделей в `cls.models` и возвращает его.

**Примеры**:

```python
models = HuggingFaceInference.get_models()
print(models)
```

### `get_model_data`

```python
@classmethod
async def get_model_data(cls, session: StreamSession, model: str) -> str:
    """Возвращает данные о конкретной модели.

    Извлекает данные о модели из API Hugging Face.

    Args:
        session (StreamSession): Асинхронная сессия для выполнения HTTP-запросов.
        model (str): Идентификатор модели.

    Returns:
        str: Данные о модели в формате JSON.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
    """
```

**Назначение**:
Метод `get_model_data` предназначен для получения данных о конкретной модели из API Hugging Face. Он использует асинхронную сессию для выполнения HTTP-запроса к API и возвращает данные о модели в формате JSON.

**Как работает функция**:
1. Проверяет, есть ли данные о модели в кэше `cls.model_data`. Если да, возвращает их.
2. Выполняет GET-запрос к API Hugging Face для получения данных о модели.
3. Если статус ответа 404, вызывает исключение `ModelNotSupportedError`.
4. Преобразует ответ в формат JSON и сохраняет его в кэше `cls.model_data`.
5. Возвращает полученные данные о модели.

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
    """Создает асинхронный генератор для выполнения запросов к API Hugging Face.

    Args:
        model (str): Идентификатор модели.
        messages (Messages): Список сообщений для передачи в модель.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
        proxy (str): URL прокси-сервера.
        timeout (int): Время ожидания ответа от API.
        api_base (str): Базовый URL API Hugging Face.
        api_key (str): API-ключ для доступа к API Hugging Face.
        max_tokens (int): Максимальное количество токенов для генерации.
        temperature (float): Температура для генерации текста.
        prompt (str): Шаблон подсказки для генерации текста.
        action (str): Действие, которое необходимо выполнить (например, "continue").
        extra_data (dict): Дополнительные данные для передачи в модель.
        seed (int): Зерно для генерации случайных чисел.
        aspect_ratio (str): Соотношение сторон для генерации изображений.
        width (int): Ширина изображения.
        height (int): Высота изображения.
        **kwargs: Дополнительные аргументы.

    Yields:
        AsyncResult: Асинхронный генератор, возвращающий результаты генерации.

    Raises:
        ModelNotSupportedError: Если модель не поддерживается.
        ResponseError: Если произошла ошибка при выполнении запроса к API.
    """
```

**Назначение**:
Метод `create_async_generator` создает асинхронный генератор, который выполняет запросы к API Hugging Face для генерации текста или изображений.

**Как работает функция**:

1. **Подготовка заголовков**:
   - Устанавливает заголовки `Accept-Encoding` и `Content-Type`.
   - Если предоставлен `api_key`, добавляет его в заголовок `Authorization`.

2. **Обработка параметров изображения**:
   - Использует функцию `use_aspect_ratio` для обработки параметров `width`, `height` и `aspect_ratio`.

3. **Создание асинхронной сессии**:
   - Создает `StreamSession` с заданными заголовками, прокси и временем ожидания.

4. **Обработка модели**:
   - Пытается получить модель с помощью `cls.get_model(model)`.

5. **Генерация изображений (Together AI)**:
   - Если модель находится в `provider_together_urls`:
     - Формирует данные запроса для генерации изображений.
     - Отправляет POST-запрос к API Together AI.
     - Обрабатывает ответ и возвращает URL изображений.

6. **Формирование полезной нагрузки (payload)**:
   - Если `payload` не определен:
     - Получает данные модели с помощью `cls.get_model_data(session, model)`.
     - Определяет тип конвейера (`pipeline_tag`).

7. **Генерация текста**:
   - Если `pipeline_tag` равен `"text-generation"` или `"image-text-to-text"`:
     - Определяет тип модели (`model_type`).
     - Формирует входные данные с помощью функции `get_inputs`.
     - Устанавливает параметры запроса (`params`).
     - Формирует `payload` для запроса.

8. **Генерация изображений (Hugging Face)**:
   - Если `pipeline_tag` равен `"text-to-image"`:
     - Формирует входные данные с помощью функции `format_image_prompt`.
     - Формирует `payload` для запроса с параметрами генерации изображений.

9. **Отправка запроса и обработка ответа**:
   - Отправляет POST-запрос к API Hugging Face.
   - Обрабатывает потоковый ответ, если `stream` равен `True`.
   - Обрабатывает не потоковый ответ, если `stream` равен `False`.

**Внутренние функции**:
- Здесь нет внутренних функций.

**Примеры**:

```python
import asyncio
from aiohttp import ClientSession
from src.providers.response import FinishReason, ImageResponse

async def main():
    model = "google/gemma-7b"
    messages = [{"role": "user", "content": "Напиши стихотворение о весне"}]

    async with ClientSession() as session:
        async for chunk in HuggingFaceInference.create_async_generator(
            model=model,
            messages=messages,
            stream=True
        ):
            if isinstance(chunk, str):
                print(chunk, end="")
            elif isinstance(chunk, FinishReason):
                print(f"\nЗавершено с причиной: {chunk}")
            elif isinstance(chunk, ImageResponse):
                print(f"\nПолучено изображение: {chunk.image_urls}")

asyncio.run(main())
```

## Функции

### `format_prompt_mistral`

```python
def format_prompt_mistral(messages: Messages, do_continue: bool = False) -> str:
    """Форматирует подсказку для модели Mistral.

    Формирует строку подсказки для модели Mistral на основе списка сообщений.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на необходимость продолжения предыдущего текста.

    Returns:
        str: Отформатированная строка подсказки.
    """
```

**Назначение**:
Функция `format_prompt_mistral` предназначена для форматирования подсказки (prompt) для модели Mistral на основе списка сообщений. Она создает строку, содержащую историю разговора и последний вопрос пользователя, в формате, ожидаемом моделью Mistral.

**Как работает функция**:
1. Извлекает все системные сообщения из списка сообщений.
2. Формирует вопрос, объединяя последнее сообщение пользователя и все системные сообщения.
3. Формирует историю разговора, объединяя сообщения пользователя и ассистента в формате `<s>[INST]...[/INST]...</s>`.
4. Если `do_continue` равно `True`, обрезает последний тег `</s>` из истории.
5. Возвращает отформатированную строку подсказки, объединяя историю и вопрос.

**Примеры**:

```python
messages = [
    {"role": "system", "content": "Ты - полезный ассистент."},
    {"role": "user", "content": "Что такое машинное обучение?"},
    {"role": "assistant", "content": "Машинное обучение - это..."}
]
prompt = format_prompt_mistral(messages)
print(prompt)
```

### `format_prompt_qwen`

```python
def format_prompt_qwen(messages: Messages, do_continue: bool = False) -> str:
    """Форматирует подсказку для модели Qwen.

    Формирует строку подсказки для модели Qwen на основе списка сообщений.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на необходимость продолжения предыдущего текста.

    Returns:
        str: Отформатированная строка подсказки.
    """
```

**Назначение**:
Функция `format_prompt_qwen` предназначена для форматирования подсказки для модели Qwen на основе списка сообщений. Она создает строку, содержащую историю разговора в формате, ожидаемом моделью Qwen.

**Как работает функция**:
1. Объединяет все сообщения пользователя и ассистента в формате `<|im_start|>role\ncontent\n<|im_end|>\n`.
2. Если `do_continue` равно `True`, обрезает последний тег `\n<|im_end|>\n` из подсказки.
3. Добавляет тег `<|im_start|>assistant\n`, если `do_continue` равно `False`.
4. Возвращает отформатированную строку подсказки.

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Что такое машинное обучение?"},
    {"role": "assistant", "content": "Машинное обучение - это..."}
]
prompt = format_prompt_qwen(messages)
print(prompt)
```

### `format_prompt_qwen2`

```python
def format_prompt_qwen2(messages: Messages, do_continue: bool = False) -> str:
    """Форматирует подсказку для модели Qwen2.

    Формирует строку подсказки для модели Qwen2 на основе списка сообщений.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на необходимость продолжения предыдущего текста.

    Returns:
        str: Отформатированная строка подсказки.
    """
```

**Назначение**:
Функция `format_prompt_qwen2` предназначена для форматирования подсказки для модели Qwen2 на основе списка сообщений. Она создает строку, содержащую историю разговора в формате, ожидаемом моделью Qwen2.

**Как работает функция**:
1. Объединяет все сообщения пользователя и ассистента в формате `\u003C｜Role｜\u003Econtent\u003C｜end of sentence｜\u003E`.
2. Если `do_continue` равно `True`, обрезает тег `\u003C｜Assistant｜\u003E` из подсказки.
3. Добавляет тег `\u003C｜Assistant｜\u003E`, если `do_continue` равно `False`.
4. Возвращает отформатированную строку подсказки.

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Что такое машинное обучение?"},
    {"role": "assistant", "content": "Машинное обучение - это..."}
]
prompt = format_prompt_qwen2(messages)
print(prompt)
```

### `format_prompt_llama`

```python
def format_prompt_llama(messages: Messages, do_continue: bool = False) -> str:
    """Форматирует подсказку для модели Llama.

    Формирует строку подсказки для модели Llama на основе списка сообщений.

    Args:
        messages (Messages): Список сообщений.
        do_continue (bool): Флаг, указывающий на необходимость продолжения предыдущего текста.

    Returns:
        str: Отформатированная строка подсказки.
    """
```

**Назначение**:
Функция `format_prompt_llama` предназначена для форматирования подсказки для модели Llama на основе списка сообщений. Она создает строку, содержащую историю разговора в формате, ожидаемом моделью Llama.

**Как работает функция**:
1. Объединяет все сообщения пользователя и ассистента в формате `<|start_header_id|>role<|end_header_id|>\n\ncontent\n<|eot_id|>\n`.
2. Если `do_continue` равно `True`, обрезает тег `\n<|eot_id|>\n` из подсказки.
3. Добавляет тег `<|start_header_id|>assistant<|end_header_id|>\n\n`, если `do_continue` равно `False`.
4. Возвращает отформатированную строку подсказки.

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Что такое машинное обучение?"},
    {"role": "assistant", "content": "Машинное обучение - это..."}
]
prompt = format_prompt_llama(messages)
print(prompt)
```

### `format_prompt_custom`

```python
def format_prompt_custom(messages: Messages, end_token: str = "</s>", do_continue: bool = False) -> str:
    """Форматирует подсказку для пользовательских моделей.

    Формирует строку подсказки для моделей с пользовательским форматом на основе списка сообщений.

    Args:
        messages (Messages): Список сообщений.
        end_token (str): Конечный токен.
        do_continue (bool): Флаг, указывающий на необходимость продолжения предыдущего текста.

    Returns:
        str: Отформатированная строка подсказки.
    """
```

**Назначение**:
Функция `format_prompt_custom` предназначена для форматирования подсказки для моделей с пользовательским форматом на основе списка сообщений. Она создает строку, содержащую историю разговора с использованием заданного конечного токена.

**Как работает функция**:
1. Объединяет все сообщения пользователя и ассистента в формате `<|role|>\ncontentend_token\n`.
2. Если `do_continue` равно `True`, обрезает `end_token + "\n"` из подсказки.
3. Добавляет тег `<|assistant|>\n`, если `do_continue` равно `False`.
4. Возвращает отформатированную строку подсказки.

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Что такое машинное обучение?"},
    {"role": "assistant", "content": "Машинное обучение - это..."}
]
prompt = format_prompt_custom(messages, end_token="<|file_separator|>")
print(prompt)
```

### `get_inputs`

```python
def get_inputs(messages: Messages, model_data: dict, model_type: str, do_continue: bool = False) -> str:
    """Получает входные данные для модели.

    Формирует строку входных данных для модели на основе списка сообщений и данных о модели.

    Args:
        messages (Messages): Список сообщений.
        model_data (dict): Данные о модели.
        model_type (str): Тип модели.
        do_continue (bool): Флаг, указывающий на необходимость продолжения предыдущего текста.

    Returns:
        str: Строка входных данных для модели.
    """
```

**Назначение**:
Функция `get_inputs` предназначена для формирования входных данных для модели на основе списка сообщений и данных о модели. Она выбирает подходящий формат подсказки в зависимости от типа модели и данных о модели.

**Как работает функция**:
1. В зависимости от `model_type` и `model_data`, выбирает функцию для форматирования подсказки:
    - `"gpt2"`, `"gpt_neo"`, `"gemma"`, `"gemma2"`: `format_prompt`.
    - `"mistral"` и `model_data["author"] == "mistralai"`: `format_prompt_mistral`.
    - Если в `model_data["config"]["tokenizer_config"]` есть `eos_token`:
        - Если `eos_token` равен `"<|endoftext|>"` или `"<eos>"` или `"</s>"`: `format_prompt_custom`.
        - Если `eos_token` равен `"<|im_end|>"`: `format_prompt_qwen`.
        - Если `eos_token["content"]` равен `"\u003C｜end of sentence｜\u003E"`: `format_prompt_qwen2`.
        - Если `eos_token` равен `"<|eot_id|>"`: `format_prompt_llama`.
        - Иначе: `format_prompt`.
    - Иначе: `format_prompt`.
2. Возвращает отформатированную строку входных данных.

**Примеры**:

```python
messages = [
    {"role": "user", "content": "Что такое машинное обучение?"},
    {"role": "assistant", "content": "Машинное обучение - это..."}
]
model_data = {"config": {"model_type": "gpt2"}}
inputs = get_inputs(messages, model_data, "gpt2")
print(inputs)