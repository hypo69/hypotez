# Модуль для работы с нейронными сетями 
=====================================================

Модуль содержит класс `neural_networks`, который используется для работы с различными нейронными сетями.

## Содержание
-  [neural_networks](#neural_networks)

## Классы
### `neural_networks`

**Описание**: Класс для работы с нейронными сетями.

**Атрибуты**:

- **`__mistral_large_2407`**: Метод для работы с нейронной сетью `mistral-12b-2409` от Mistral AI.

- **`_FLUX_schnell`**: Метод для работы с нейронной сетью `FLUX.1-schnell` от Black Forest Labs.

- **`_free_gpt_4o_mini`**: Метод для работы с нейронной сетью `gpt-4o-mini` от Inference.ai.

**Методы**:

- **`_FLUX_schnell(self, prompt: str, size: list[int, int], seed: int, num_inference_steps: int) -> str|None`**: Метод для отправки запроса в API нейронной сети `FLUX.1-schnell` для генерации изображения по текстовому запросу.

    **Аргументы**:
    -  `prompt` (`str`): Текстовый запрос для генерации изображения.
    -  `size` (`list[int, int]`): Размеры изображения в пикселях.
    -  `seed` (`int`): Значение для генератора случайных чисел, чтобы обеспечить воспроизводимость результатов.
    -  `num_inference_steps` (`int`): Количество шагов для генерации изображения.

    **Возвращает**:
    -  `str|None`:  Путь к сгенерированному изображению или `None`, если возникла ошибка.

    **Пример**:
    ```python
    nn = neural_networks()
    image_path = nn._FLUX_schnell(prompt='A cat sitting on a chair', size=[512, 512], seed=42, num_inference_steps=50)
    ```

- **`__mistral_large_2407(self, prompt: list[dict[str, str]]) -> tuple[str, int, int]|str`**: Метод для отправки запроса в API нейронной сети `mistral-12b-2409` для генерации текста по текстовому запросу.

    **Аргументы**:
    -  `prompt` (`list[dict[str, str]]`): Список текстовых сообщений, которые будут использоваться в качестве контекста для генерации ответа.

    **Возвращает**:
    -  `tuple[str, int, int]|str`: Кортеж, содержащий сгенерированный текст, количество токенов в запросе и количество токенов в ответе.  Если возникла ошибка, возвращает строку с ошибкой.

    **Пример**:
    ```python
    nn = neural_networks()
    response, prompt_tokens, completion_tokens = nn.__mistral_large_2407(prompt=[
        {'role': 'user', 'content': 'Привет! Как дела?'},
        {'role': 'assistant', 'content': 'Хорошо, а у тебя?'},
        {'role': 'user', 'content': 'Тоже неплохо. Расскажи мне анекдот.'}
    ])
    ```

- **`_free_gpt_4o_mini(self, prompt: list[dict[str, str]]) -> tuple[str, int, int]|str`**: Метод для отправки запроса в API нейронной сети `gpt-4o-mini` для генерации текста по текстовому запросу.

    **Аргументы**:
    -  `prompt` (`list[dict[str, str]]`): Список текстовых сообщений, которые будут использоваться в качестве контекста для генерации ответа.

    **Возвращает**:
    -  `tuple[str, int, int]|str`: Кортеж, содержащий сгенерированный текст, количество токенов в запросе и количество токенов в ответе.  Если возникла ошибка, возвращает строку с ошибкой.

    **Пример**:
    ```python
    nn = neural_networks()
    response, prompt_tokens, completion_tokens = nn._free_gpt_4o_mini(prompt=[
        {'role': 'user', 'content': 'Привет! Как дела?'},
        {'role': 'assistant', 'content': 'Хорошо, а у тебя?'},
        {'role': 'user', 'content': 'Тоже неплохо. Расскажи мне анекдот.'}
    ])
    ```

## Примечания
-  Все методы класса `neural_networks`  используют  `requests` для отправки запросов в API нейронных сетей.
-  Методы  `_FLUX_schnell`,  `__mistral_large_2407` и  `_free_gpt_4o_mini`  ожидают, что в переменных  `HF_TOKEN`, `MISTRAL_TOKEN`, `GIT_TOKEN`  будут  содержаться  токены  для  соответствующих  API. 
-  Метод `_FLUX_schnell`  использует  `PIL` для  загрузки  и  обработки  сгенерированных  изображений.
-  Методы  `__mistral_large_2407`  и  `_free_gpt_4o_mini`  используют  `json`  для  десериализации  ответов  API  в  формате  JSON.