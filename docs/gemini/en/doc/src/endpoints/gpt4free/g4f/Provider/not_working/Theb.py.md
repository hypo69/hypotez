# TheB.AI Provider

## Overview

This module implements the `Theb` class, a provider for the `TheB.AI` language model. It enables interaction with the `TheB.AI` service through a web interface and utilizes Selenium for browser automation.

## Details

The `Theb` class is a subclass of `AbstractProvider`, defining the core functionalities for interacting with the `TheB.AI` model. It leverages the `WebDriverSession` class to manage the browser instance and provides methods for sending prompts and receiving responses.

The provider utilizes a custom JavaScript snippet injected into the browser to intercept responses and stream them back to the user. It features robust error handling and retry mechanisms to ensure consistent and reliable communication with the `TheB.AI` service.

## Classes

### `Theb`

**Description**: Класс-провайдер для модели `TheB.AI`, позволяющий взаимодействовать с моделью через веб-интерфейс.

**Inherits**: `AbstractProvider`

**Attributes**:

- `label (str)`: Метка провайдера, соответствующая модели.
- `url (str)`: Базовый URL для доступа к веб-интерфейсу `TheB.AI`.
- `working (bool)`: Флаг, указывающий на доступность провайдера.
- `supports_stream (bool)`: Флаг, указывающий на поддержку потоковой передачи ответов.
- `models (dict)`: Словарь с доступными моделями и их названиями.

**Methods**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, webdriver: WebDriver = None, virtual_display: bool = True, **kwargs) -> CreateResult`

#### `create_completion`

**Purpose**: Функция отправки запроса с prompt`ом к модели `TheB.AI` и получения ответа.

**Parameters**:

- `model (str)`: Имя модели.
- `messages (Messages)`: История сообщений.
- `stream (bool)`: Флаг, указывающий на потоковую передачу ответа.
- `proxy (str, optional)`: Прокси-сервер для подключения. Defaults to `None`.
- `webdriver (WebDriver, optional)`: Экземпляр драйвера браузера. Defaults to `None`.
- `virtual_display (bool, optional)`: Флаг, указывающий на использование виртуального дисплея. Defaults to `True`.

**Returns**:

- `CreateResult`: Результат запроса с prompt`ом к модели.

**Raises Exceptions**:

- `Exception`: Если возникают ошибки во время обработки запроса к модели `TheB.AI`.

**How the Function Works**:

1. **Preparation:**
    - Проверка наличия модели в словаре `models`.
    - Форматирование `prompt` из истории сообщений `messages`.
    - Создание экземпляра `WebDriverSession` для управления браузером, указав параметры `webdriver`, `virtual_display` и `proxy`.
    - Запуск блока `with` для управления контекстом `driver`.

2. **Browser Automation:**
    - Загрузка `TheB.AI` веб-страницы.
    - Ожидание появления текстового поля `textareaAutosize`.
    - Регистрация хука для перехвата запросов `fetch`.
    - Добавление скрипта в браузер для перехвата и обработки ответов с помощью `driver.execute_cdp_cmd`.

3. **Model Selection:**
    - Если модель не задана (`model` - `None`), то используется модель по умолчанию.
    - Если модель задана, то:
        - Ожидание появления панели выбора модели.
        - Клик по панели выбора модели.
        - Ожидание появления списка доступных моделей.
        - Нажатие на кнопку выбора заданной модели.

4. **Prompt Submission:**
    - Ожидание появления текстового поля `textareaAutosize`.
    - Ввод prompt`а в текстовое поле.
    - Клик по кнопке отправки prompt`а.

5. **Response Handling:**
    - Использование JavaScript-кода для чтения потока ответа.
    - Выдача фрагментов ответа по мере их получения.

**Examples**:

```python
from ...typing import Messages
from ..base_provider import AbstractProvider
from ..helper import format_prompt

# Создание экземпляра провайдера
provider = Theb(label="TheB.AI")

# Определение истории сообщений
messages = Messages(messages=[
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "Хорошо, спасибо за вопрос. А у тебя как?"}
])

# Отправка запроса к модели с prompt`ом
result = provider.create_completion(model="theb-ai-free", messages=messages, stream=False)

# Получение ответа от модели
print(result.content)
```
```python
## \file hypotez/src/endpoints/gpt4free/g4f/Provider/not_working/Theb.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для провайдера TheB.AI
===============================================================
Модуль обеспечивает взаимодействие с моделью TheB.AI через веб-интерфейс. 
Использует Selenium для автоматизации браузера.

Использует WebDriverSession для управления экземпляром браузера, 
предоставляет методы для отправки prompt`ов и получения ответов. 
Загружает страницу TheB.AI,  вводит prompt`ы и получает ответы, 
используя JavaScript-код для обработки потока ответов.