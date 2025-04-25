# Модуль FastGpt
## Обзор

Модуль `FastGpt` реализует класс `FastGpt`, представляющий собой провайдера для взаимодействия с API сервиса `fastgpt.me`, 
предоставляющего доступ к языковым моделям  GPT-3.5 Turbo. 

## Подробнее

Класс `FastGpt` наследуется от базового класса `AbstractProvider` и предоставляет следующие возможности:

* **Использование API `fastgpt.me`:** Класс `FastGpt` позволяет отправлять запросы к API сервиса `fastgpt.me` для получения ответов от языковой модели.
* **Поддержка потоковой передачи (streaming):** Класс `FastGpt` позволяет получать ответы от модели по частям, используя потоковую передачу.
* **Поддержка GPT-3.5 Turbo:** Класс `FastGpt` поддерживает использование модели GPT-3.5 Turbo.

## Классы

### `class FastGpt`

**Описание**: Класс `FastGpt`, реализующий провайдера для сервиса `fastgpt.me`.

**Наследует**: `AbstractProvider`

**Атрибуты**:

* `url (str)`: Базовый URL для отправки запросов к API сервиса `fastgpt.me`.
* `working (bool)`: Флаг, указывающий на доступность сервиса `fastgpt.me`.
* `needs_auth (bool)`: Флаг, указывающий на необходимость аутентификации для использования сервиса `fastgpt.me`.
* `supports_stream (bool)`: Флаг, указывающий на поддержку потоковой передачи ответов от модели.
* `supports_gpt_35_turbo (bool)`: Флаг, указывающий на поддержку модели GPT-3.5 Turbo.
* `supports_gpt_4 (bool)`: Флаг, указывающий на поддержку модели GPT-4.

**Методы**:

* `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

## Методы класса

### `create_completion`

```python
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        """
        Метод, отправляющий запрос к API `fastgpt.me` для получения ответа от языковой модели.

        Args:
            model (str): Имя модели, используемой для генерации текста.
            messages (list[dict[str, str]]): Список сообщений, составляющих контекст для генерации ответа.
            stream (bool): Флаг, указывающий на использование потоковой передачи.
            **kwargs: Any): Дополнительные аргументы, передаваемые в API `fastgpt.me`.

        Returns:
            CreateResult: Объект, содержащий результат генерации текста.

        Raises:
            Exception: В случае возникновения ошибок при отправке запроса к API `fastgpt.me`.
        """
```

**Назначение**: Метод `create_completion` отправляет запрос к API `fastgpt.me` для получения ответа от языковой модели.

**Параметры**:

* `model (str)`: Имя модели, используемой для генерации текста.
* `messages (list[dict[str, str]])`: Список сообщений, составляющих контекст для генерации ответа.
* `stream (bool)`: Флаг, указывающий на использование потоковой передачи.
* `**kwargs (Any)`: Дополнительные аргументы, передаваемые в API `fastgpt.me`.

**Возвращает**:

* `CreateResult`: Объект, содержащий результат генерации текста.

**Вызывает исключения**:

* `Exception`: В случае возникновения ошибок при отправке запроса к API `fastgpt.me`.

**Как работает функция**:

* Функция формирует запрос к API `fastgpt.me` с использованием параметров `model`, `messages`, `stream` и `**kwargs`.
* Запрос отправляется с использованием библиотеки `requests`.
* Полученный от API `fastgpt.me` ответ анализируется и преобразуется в объект `CreateResult`.
* Объект `CreateResult` возвращается в качестве результата работы функции.

**Примеры**:

```python
>>> messages = [{'role': 'user', 'content': 'Привет! Как дела?'}]
>>> model = 'gpt-3.5-turbo'
>>> response = FastGpt.create_completion(model=model, messages=messages, stream=True)
>>> print(response)
```

## Параметры класса

* `url (str)`: Базовый URL для отправки запросов к API сервиса `fastgpt.me`. 
* `working (bool)`: Флаг, указывающий на доступность сервиса `fastgpt.me`.
* `needs_auth (bool)`: Флаг, указывающий на необходимость аутентификации для использования сервиса `fastgpt.me`.
* `supports_stream (bool)`: Флаг, указывающий на поддержку потоковой передачи ответов от модели.
* `supports_gpt_35_turbo (bool)`: Флаг, указывающий на поддержку модели GPT-3.5 Turbo.
* `supports_gpt_4 (bool)`: Флаг, указывающий на поддержку модели GPT-4.

**Примеры**:

```python
>>> from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.FastGpt import FastGpt
>>> FastGpt.url
'https://chat9.fastgpt.me/'
>>> FastGpt.working
False
>>> FastGpt.needs_auth
False
>>> FastGpt.supports_stream
True
>>> FastGpt.supports_gpt_35_turbo
True
>>> FastGpt.supports_gpt_4
False