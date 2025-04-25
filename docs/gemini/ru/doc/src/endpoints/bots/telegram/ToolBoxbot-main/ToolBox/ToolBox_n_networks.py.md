# Модуль для работы с нейронными сетями 
===================================================

Модуль содержит класс :class:`neural_networks`, который используется для работы с различными нейронными сетями, такими как FLUX.1-schnell, Mistral 12B и Free GPT 4O Mini.

## Обзор

Модуль обеспечивает интерфейс для взаимодействия с различными нейронными сетями, предоставляя методы для отправки запросов и получения ответов. Класс :class:`neural_networks` предоставляет методы для работы с моделями FLUX.1-schnell, Mistral 12B и Free GPT 4O Mini.

## Подробнее

Класс :class:`neural_networks` обеспечивает методы для работы с различными нейронными сетями.

## Классы

### `neural_networks`
**Описание**: Класс для работы с различными нейронными сетями.

**Атрибуты**:
- Нет атрибутов.

**Методы**:
- `_FLUX_schnell`: Возвращает изображение, сгенерированное нейронной сетью FLUX.1-schnell.
- `__mistral_large_2407`: Возвращает текст, сгенерированный нейронной сетью Mistral 12B.
- `_free_gpt_4o_mini`: Возвращает текст, сгенерированный нейронной сетью Free GPT 4O Mini.



## Методы класса

### `_FLUX_schnell`

```python
def _FLUX_schnell(self, prompt: str, size: list[int, int], seed: int, num_inference_steps: int) -> str|None:
    """
    Функция отправляет запрос к API FLUX.1-schnell и возвращает сгенерированное изображение.
    Args:
        prompt (str): Текстовый запрос для генерации изображения.
        size (list[int, int]): Размер изображения в пикселях.
        seed (int): Семенное значение для генератора случайных чисел.
        num_inference_steps (int): Количество шагов для генерации изображения.
    Returns:
        str|None: Возвращает изображение, сгенерированное FLUX.1-schnell, или `None` в случае ошибки.
    Raises:
        Exception: Если возникает ошибка при взаимодействии с API.
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "guidance_scale": 1.5,
            "num_inference_steps": num_inference_steps,
            "width": size[0],
            "height": size[1],
            "seed": seed
        }
    }
    for i in range(1, 7):
        response = requests.post("https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell",
                                headers={"Authorization": "Bearer " + os.environ[f"HF_TOKEN{i}"], "Content-Type": "application/json"},
                                json=payload)
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image
```

**Назначение**: Функция отправляет запрос к API FLUX.1-schnell с текстовым запросом и параметрами генерации. После успешного запроса возвращает изображение в формате `Image`.

**Параметры**:
- `prompt` (str): Текстовый запрос для генерации изображения.
- `size` (list[int, int]): Размер изображения в пикселях.
- `seed` (int): Семенное значение для генератора случайных чисел.
- `num_inference_steps` (int): Количество шагов для генерации изображения.

**Возвращает**:
- `str|None`: Возвращает изображение, сгенерированное FLUX.1-schnell, или `None` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при взаимодействии с API.

**Как работает функция**:
- Функция формирует тело запроса с текстовым запросом, параметрами генерации (размер, seed, num_inference_steps) и заголовками авторизации.
- Цикл `for i in range(1, 7)` перебирает 6 API-ключей для FLUX.1-schnell.
- Внутри цикла отправляется запрос к API с использованием `requests.post`.
- Если код ответа `200` (успешный), то извлечение изображения с помощью `Image.open(io.BytesIO(response.content))`.
- Функция возвращает изображение или `None` в случае неудачи.

**Примеры**:
```python
>>> prompt = "Апельсин на ветке"
>>> size = [512, 512]
>>> seed = 42
>>> num_inference_steps = 50
>>> image = neural_networks._FLUX_schnell(prompt, size, seed, num_inference_steps)
>>> if image:
...     image.show()
... else:
...     print("Ошибка генерации изображения.")
```



### `__mistral_large_2407`

```python
def __mistral_large_2407(self, prompt: list[dict[str, str]]) -> tuple[str, int, int]|str:
    """
    Функция отправляет запрос к API Mistral 12B и возвращает сгенерированный текст.
    Args:
        prompt (list[dict[str, str]]): Текстовый запрос в формате списка словарей, где каждый словарь содержит ключ "role" и "content".
    Returns:
        tuple[str, int, int]|str: Возвращает кортеж с текстом, количество токенов в запросе и ответе, или `str` в случае ошибки.
    Raises:
        Exception: Если возникает ошибка при взаимодействии с API.
    """
    data = {
        "messages": prompt,
        "temperature": 1.0,
        "top_p": 1.0,
        "max_tokens": 1024,
        "model": "pixtral-12b-2409"
    }
    response = requests.post("https://api.mistral.ai/v1/chat/completions",
                            headers={"Content-Type": "application/json", "Authorization": "Bearer "+ os.environ['MISTRAL_TOKEN']},
                            json=data)
    response = json.loads(response.text)
    return response["choices"][0]["message"], response["usage"]["prompt_tokens"], response["usage"]["completion_tokens"]
```

**Назначение**: Функция отправляет запрос к API Mistral 12B с текстовым запросом в формате списка словарей. После успешного запроса возвращает текст и информацию о количестве токенов.

**Параметры**:
- `prompt` (list[dict[str, str]]): Текстовый запрос в формате списка словарей, где каждый словарь содержит ключ "role" и "content".

**Возвращает**:
- `tuple[str, int, int]|str`: Возвращает кортеж с текстом, количество токенов в запросе и ответе, или `str` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при взаимодействии с API.

**Как работает функция**:
- Функция формирует тело запроса с текстовым запросом, параметрами генерации и заголовками авторизации.
- Отправляется запрос к API с использованием `requests.post`.
- Если код ответа `200` (успешный), то извлечение текста, количество токенов в запросе и ответе из ответа API.
- Функция возвращает кортеж с текстом, количество токенов в запросе и ответе или `str` в случае ошибки.

**Примеры**:
```python
>>> prompt = [
...     {"role": "user", "content": "Напиши мне стихотворение про кота."}
... ]
>>> text, prompt_tokens, completion_tokens = neural_networks.__mistral_large_2407(prompt)
>>> print(f"Текст: {text}")
>>> print(f"Токенов в запросе: {prompt_tokens}")
>>> print(f"Токенов в ответе: {completion_tokens}")
```


### `_free_gpt_4o_mini`

```python
def _free_gpt_4o_mini(self, prompt: list[dict[str, str]]) -> tuple[str, int, int]|str:
    """
    Функция отправляет запрос к API Free GPT 4O Mini и возвращает сгенерированный текст.
    Args:
        prompt (list[dict[str, str]]): Текстовый запрос в формате списка словарей, где каждый словарь содержит ключ "role" и "content".
    Returns:
        tuple[str, int, int]|str: Возвращает кортеж с текстом, количество токенов в запросе и ответе, или `str` в случае ошибки.
    Raises:
        Exception: Если возникает ошибка при взаимодействии с API.
    """
    data = {
        "messages": prompt,
        "temperature": 1.0,
        "top_p": 1.0,
        "max_tokens": 1024,
        "model": "gpt-4o-mini"
    }
    for i in range(1, 7):
        response = requests.post("https://models.inference.ai.azure.com/chat/completions",
                                headers={"Authorization": os.environ[f'GIT_TOKEN{i}'], "Content-Type" : "application/json"},
                                json=data)
        if response.status_code == 200:
            response = json.loads(response.text)
            return response["choices"][0]["message"], response["usage"]["prompt_tokens"], response["usage"]["completion_tokens"]
        
        return self.__mistral_large_2407(prompt)
```

**Назначение**: Функция отправляет запрос к API Free GPT 4O Mini с текстовым запросом в формате списка словарей. После успешного запроса возвращает текст и информацию о количестве токенов.

**Параметры**:
- `prompt` (list[dict[str, str]]): Текстовый запрос в формате списка словарей, где каждый словарь содержит ключ "role" и "content".

**Возвращает**:
- `tuple[str, int, int]|str`: Возвращает кортеж с текстом, количество токенов в запросе и ответе, или `str` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при взаимодействии с API.

**Как работает функция**:
- Функция формирует тело запроса с текстовым запросом, параметрами генерации и заголовками авторизации.
- Цикл `for i in range(1, 7)` перебирает 6 API-ключей для Free GPT 4O Mini.
- Внутри цикла отправляется запрос к API с использованием `requests.post`.
- Если код ответа `200` (успешный), то извлечение текста, количество токенов в запросе и ответе из ответа API.
- Если запросов с 6 ключами не удалось отправить, функция вызывает `self.__mistral_large_2407`, чтобы попробовать сгенерировать текст с помощью Mistral 12B.
- Функция возвращает кортеж с текстом, количество токенов в запросе и ответе или `str` в случае ошибки.

**Примеры**:
```python
>>> prompt = [
...     {"role": "user", "content": "Расскажи мне историю про кота."}
... ]
>>> text, prompt_tokens, completion_tokens = neural_networks._free_gpt_4o_mini(prompt)
>>> print(f"Текст: {text}")
>>> print(f"Токенов в запросе: {prompt_tokens}")
>>> print(f"Токенов в ответе: {completion_tokens}")