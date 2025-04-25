# Модуль `stubs.py`

## Обзор

Этот модуль содержит набор классов, которые имитируют (stub) структуру ответов от модели GPT-4Free, включая:

- **ChatCompletionChunk**:  Имитирует структуру ответа от GPT-4Free при пошаговом генерировании текста.
- **ChatCompletionMessage**: Представляет собой сообщение, сгенерированное моделью GPT-4Free.
- **ChatCompletionChoice**: Содержит информацию о выборе, сделанном моделью GPT-4Free.
- **ChatCompletion**: Имитирует полную структуру ответа от модели GPT-4Free.
- **ChatCompletionDelta**: Представляет собой изменения в сообщении, сгенерированном моделью GPT-4Free.
- **ChatCompletionDeltaChoice**:  Имитирует структуру ответа от GPT-4Free при пошаговом генерировании текста.
- **Image**:  Имитирует структуру ответа от GPT-4Free, когда модель генерирует изображения.
- **ImagesResponse**: Представляет собой ответ от модели GPT-4Free, содержащий список сгенерированных изображений.
- **UsageModel**: Содержит информацию об использовании токенов модели GPT-4Free.
- **ToolFunctionModel**: Представляет информацию о функции, которую может использовать модель GPT-4Free.
- **ToolCallModel**: Имитирует структуру запроса к функции, которую может использовать модель GPT-4Free.

## Классы

### `ChatCompletionChunk`

**Описание**: Представляет собой структуру ответа от модели GPT-4Free при пошаговом генерировании текста. 

**Атрибуты**:

- `id` (str): Идентификатор фрагмента ответа.
- `object` (str): Тип объекта, в данном случае "chat.completion.cunk".
- `created` (int): Время создания фрагмента ответа.
- `model` (str): Имя модели GPT-4Free, которая сгенерировала ответ.
- `provider` (Optional[str]): Дополнительная информация о поставщике модели.
- `choices` (List[ChatCompletionDeltaChoice]): Список выборов, сделанных моделью GPT-4Free.
- `usage` (UsageModel): Информация об использовании токенов модели GPT-4Free.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ChatCompletionChunk` с помощью ключевых слов. 

### `ChatCompletionMessage`

**Описание**: Представляет собой сообщение, сгенерированное моделью GPT-4Free.

**Атрибуты**:

- `role` (str): Роль отправителя сообщения.
- `content` (str): Содержимое сообщения.
- `tool_calls` (list[ToolCallModel]): Список вызовов функций, которые были использованы моделью GPT-4Free при генерации сообщения.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ChatCompletionMessage` с помощью ключевых слов.
- `save(self, filepath: str, allowd_types = None)`: Метод для сохранения сообщения в файл.


### `ChatCompletionChoice`

**Описание**: Содержит информацию о выборе, сделанном моделью GPT-4Free.

**Атрибуты**:

- `index` (int): Индекс выбора.
- `message` (ChatCompletionMessage): Сообщение, которое было выбрано моделью GPT-4Free.
- `finish_reason` (str): Причина окончания генерации сообщения.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ChatCompletionChoice` с помощью ключевых слов.


### `ChatCompletion`

**Описание**: Имитирует полную структуру ответа от модели GPT-4Free.

**Атрибуты**:

- `id` (str): Идентификатор ответа.
- `object` (str): Тип объекта, в данном случае "chat.completion".
- `created` (int): Время создания ответа.
- `model` (str): Имя модели GPT-4Free, которая сгенерировала ответ.
- `provider` (Optional[str]): Дополнительная информация о поставщике модели.
- `choices` (list[ChatCompletionChoice]): Список выборов, сделанных моделью GPT-4Free.
- `usage` (UsageModel): Информация об использовании токенов модели GPT-4Free.
- `conversation` (dict): Информация о контексте разговора.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ChatCompletion` с помощью ключевых слов. 

### `ChatCompletionDelta`

**Описание**: Представляет собой изменения в сообщении, сгенерированном моделью GPT-4Free.

**Атрибуты**:

- `role` (str): Роль отправителя сообщения.
- `content` (str): Содержимое сообщения.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ChatCompletionDelta` с помощью ключевых слов.

### `ChatCompletionDeltaChoice`

**Описание**: Имитирует структуру ответа от GPT-4Free при пошаговом генерировании текста.

**Атрибуты**:

- `index` (int): Индекс выбора.
- `delta` (ChatCompletionDelta): Изменения в сообщении, сгенерированном моделью GPT-4Free.
- `finish_reason` (Optional[str]): Причина окончания генерации сообщения.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ChatCompletionDeltaChoice` с помощью ключевых слов.

### `Image`

**Описание**:  Имитирует структуру ответа от GPT-4Free, когда модель генерирует изображения.

**Атрибуты**:

- `url` (Optional[str]): URL-адрес изображения.
- `b64_json` (Optional[str]): Кодированное в base64 изображение в формате JSON.
- `revised_prompt` (Optional[str]): Измененная подсказка, которая использовалась для генерации изображения.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `Image` с помощью ключевых слов.

### `ImagesResponse`

**Описание**: Представляет собой ответ от модели GPT-4Free, содержащий список сгенерированных изображений.

**Атрибуты**:

- `data` (List[Image]): Список сгенерированных изображений.
- `model` (str): Имя модели GPT-4Free, которая сгенерировала изображения.
- `provider` (str): Дополнительная информация о поставщике модели.
- `created` (int): Время создания ответа.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ImagesResponse` с помощью ключевых слов.

### `UsageModel`

**Описание**: Содержит информацию об использовании токенов модели GPT-4Free.

**Атрибуты**:

- `prompt_tokens` (int): Количество токенов, использованных для подсказки.
- `completion_tokens` (int): Количество токенов, использованных для генерации ответа.
- `total_tokens` (int): Общее количество использованных токенов.
- `prompt_tokens_details` (TokenDetails): Подробная информация об использовании токенов для подсказки.
- `completion_tokens_details` (TokenDetails): Подробная информация об использовании токенов для генерации ответа.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `UsageModel` с помощью ключевых слов. 

### `ToolFunctionModel`

**Описание**: Представляет информацию о функции, которую может использовать модель GPT-4Free.

**Атрибуты**:

- `name` (str): Название функции.
- `arguments` (str): Аргументы функции.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ToolFunctionModel` с помощью ключевых слов.

### `ToolCallModel`

**Описание**: Имитирует структуру запроса к функции, которую может использовать модель GPT-4Free.

**Атрибуты**:

- `id` (str): Идентификатор вызова функции.
- `type` (str): Тип вызова функции.
- `function` (ToolFunctionModel): Информация о функции, к которой был сделан вызов.

**Методы**:

- `model_construct(*args, **kwargs)`: Конструктор класса, который позволяет создать объект `ToolCallModel` с помощью ключевых слов. 


## Параметры классов

- `cached_tokens` (int): Количество кэшированных токенов.
- `prompt_tokens` (int): Количество токенов, использованных для подсказки.
- `completion_tokens` (int): Количество токенов, использованных для генерации ответа.
- `total_tokens` (int): Общее количество использованных токенов.
- `prompt_tokens_details` (TokenDetails): Подробная информация об использовании токенов для подсказки.
- `completion_tokens_details` (TokenDetails): Подробная информация об использовании токенов для генерации ответа.
- `name` (str): Название функции.
- `arguments` (str): Аргументы функции.
- `id` (str): Идентификатор вызова функции.
- `type` (str): Тип вызова функции.
- `function` (ToolFunctionModel): Информация о функции, к которой был сделан вызов.
- `role` (str): Роль отправителя сообщения.
- `content` (str): Содержимое сообщения.
- `tool_calls` (list[ToolCallModel]): Список вызовов функций, которые были использованы моделью GPT-4Free при генерации сообщения.
- `index` (int): Индекс выбора.
- `message` (ChatCompletionMessage): Сообщение, которое было выбрано моделью GPT-4Free.
- `finish_reason` (str): Причина окончания генерации сообщения.
- `url` (Optional[str]): URL-адрес изображения.
- `b64_json` (Optional[str]): Кодированное в base64 изображение в формате JSON.
- `revised_prompt` (Optional[str]): Измененная подсказка, которая использовалась для генерации изображения.
- `data` (List[Image]): Список сгенерированных изображений.
- `model` (str): Имя модели GPT-4Free, которая сгенерировала изображения.
- `provider` (str): Дополнительная информация о поставщике модели.
- `created` (int): Время создания ответа.
- `conversation` (dict): Информация о контексте разговора.
- `allowd_types` (List[str]): Список разрешенных типов файлов.
- `filepath` (str): Путь к файлу для сохранения.


## Примеры

```python
# Создание объекта ChatCompletionMessage
message = ChatCompletionMessage.model_construct(content="Hello, world!", tool_calls=[
    ToolCallModel.model_construct(
        function=ToolFunctionModel.model_construct(name="my_function", arguments="arg1, arg2")
    )
])

# Сохранение сообщения в файл
message.save("my_message.txt")

# Создание объекта ChatCompletion
completion = ChatCompletion.model_construct(
    content="This is a response.",
    finish_reason="stop",
    created=int(time()),
    usage=UsageModel.model_construct(
        prompt_tokens=10, completion_tokens=20, total_tokens=30
    ),
    conversation={"history": []},
)

# Создание объекта ImagesResponse
images_response = ImagesResponse.model_construct(
    data=[Image.model_construct(url="https://example.com/image.jpg")],
    model="gpt-4free-image",
    provider="openai",
)

# Создание объекта UsageModel
usage = UsageModel.model_construct(
    prompt_tokens=10, completion_tokens=20, total_tokens=30
)

# Создание объекта ToolCallModel
tool_call = ToolCallModel.model_construct(
    function=ToolFunctionModel.model_construct(name="my_function", arguments="arg1, arg2")
)
```

## Как работает модуль

Этот модуль предоставляет набор классов, которые имитируют структуру ответов от модели GPT-4Free. Это позволяет разработчикам работать с данными, как если бы они были получены от модели GPT-4Free, даже если модель недоступна.

Классы предоставляют возможность создавать объекты с помощью конструктора `model_construct`. 

## Зачем использовать этот модуль

Этот модуль необходим для тестирования кода, который взаимодействует с моделью GPT-4Free. Он позволяет разработчикам симулировать получение данных от модели, даже если модель недоступна. Это позволяет ускорить процесс разработки и тестирования.

## Дополнительная информация

- Для работы с веб-драйвером используйте классы `Driver`, `Chrome`, `Firefox`, `Playwright` из модуля `src.webdirver`.
- Классы `Driver`, `Chrome`, `Firefox`, `Playwright` уже содержат все настройки Selenium.
- Основная команда для взаимодействия с веб-драйвером: `driver.execute_locator(l:dict)`, которая возвращает значение веб-элемента по локатору.
- Пример использования веб-драйвера:

```python
from src.webdirver import Driver, Chrome
driver = Driver(Chrome)

close_banner = {
    "attribute": null,
    "by": "XPATH",
    "selector": "//button[@id = 'closeXButton']",
    "if_list": "first",
    "use_mouse": false,
    "mandatory": false,
    "timeout": 0,
    "timeout_for_event": "presence_of_element_located",
    "event": "click()",
    "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

## Изменения

- Нет изменений.