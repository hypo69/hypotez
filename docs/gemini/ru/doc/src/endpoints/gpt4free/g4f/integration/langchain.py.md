# Модуль `langchain.py`

## Обзор

Этот модуль предоставляет расширения для LangChain, которые позволяют использовать GPT-4 Free API для моделей LangChain.

## Содержание

- [Функции](#функции)
    - [`new_convert_message_to_dict`](#new_convert_message_to_dict)
- [Классы](#классы)
    - [`ChatAI`](#chatai)

## Функции

### `new_convert_message_to_dict`

```python
def new_convert_message_to_dict(message: BaseMessage) -> dict:
    """
    Преобразует объект LangChain BaseMessage в словарь.

    Args:
        message (BaseMessage): Объект LangChain BaseMessage.

    Returns:
        dict: Словарь, представляющий сообщение.
    """
    ...
```

**Назначение**: 
- Преобразует объект LangChain `BaseMessage` в словарь для совместимости с GPT-4 Free API.

**Параметры**:

- `message (BaseMessage)`: Объект LangChain `BaseMessage`, который нужно преобразовать.

**Возвращает**:

- `dict`: Словарь, представляющий сообщение.

**Как работает функция**:

- Проверяет тип `message`. 
- Если `message` является объектом `ChatCompletionMessage`, то формирует словарь с ключами `"role"`, `"content"` и `"tool_calls"` (если есть).
- Если `message` не является объектом `ChatCompletionMessage`, то использует стандартный метод `convert_message_to_dict` из LangChain для преобразования.

## Классы

### `ChatAI`

```python
class ChatAI(ChatOpenAI):
    """
    Класс для использования GPT-4 Free API в качестве модели LangChain.

    Inherits:
        ChatOpenAI: Базовый класс для использования модели OpenAI.

    Attributes:
        model_name (str): Название модели, по умолчанию "gpt-4o".

    Methods:
        validate_environment(): Проверяет и инициализирует клиент GPT-4 Free API.
    """
    ...
```

**Описание**: 
- Представляет модель ChatOpenAI, которая использует GPT-4 Free API. 
- Наследует от базового класса ChatOpenAI.

**Атрибуты**:

- `model_name (str)`: Название модели, по умолчанию "gpt-4o".

**Методы**:

- `validate_environment()`: Проверяет и инициализирует клиент GPT-4 Free API.

**Принцип работы**:

- Класс `ChatAI` наследует от базового класса `ChatOpenAI` и переопределяет метод `validate_environment()`, чтобы инициализировать клиент GPT-4 Free API. 
- При инициализации класса `ChatAI` этот метод вызывается, чтобы настроить клиент для взаимодействия с GPT-4 Free API.

**Примеры**:

```python
from langchain import PromptTemplate, LLMChain
from langchain_community.chat_models.openai import ChatOpenAI
from hypotez.src.endpoints.gpt4free.g4f.integration.langchain import ChatAI

# Инициализация модели GPT-4 Free API
model = ChatAI(api_key="YOUR_API_KEY", model_kwargs={"provider": "gpt4free"})

# Создание шаблона запроса
template = PromptTemplate(
    input_variables=["text"],
    template="Переведите этот текст на русский язык: {text}",
)

# Создание цепочки LangChain с использованием модели GPT-4 Free API
llm_chain = LLMChain(prompt=template, llm=model)

# Выполнение запроса
response = llm_chain.run("This is a text in English.")

# Вывод ответа
print(response)
```

**Внутренние функции**:

- None

**Как работает функция**:

- Метод `validate_environment` проверяет наличие ключа API (`api_key`) и провайдера (`provider`) в конфигурации.
- Затем инициализирует клиент GPT-4 Free API (классы `Client` и `AsyncClient`) с полученными параметрами.
- В итоге возвращает обновленную конфигурацию с клиентом GPT-4 Free API.

**Примеры**:

- None