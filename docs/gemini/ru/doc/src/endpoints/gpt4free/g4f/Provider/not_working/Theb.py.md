# Модуль Theb

## Обзор

Модуль `Theb` предоставляет реализацию класса `Theb`, который представляет собой провайдера для доступа к API TheB.AI. 

## Подробнее

Класс `Theb` реализует интерфейс `AbstractProvider` и позволяет взаимодействовать с различными моделями искусственного интеллекта (ИИ), доступными через TheB.AI, такими как GPT-3.5 Turbo, GPT-4, Claude 2, PaLM 2 и другие. 

Он использует Selenium WebDriver для взаимодействия с веб-интерфейсом TheB.AI и позволяет получать ответы от моделей ИИ в режиме потоковой передачи (streaming).

## Классы

### `class Theb`

**Описание**: Класс `Theb` реализует провайдера для доступа к API TheB.AI.

**Наследует**: `AbstractProvider`

**Атрибуты**:

- `label` (str): Метка провайдера (TheB.AI).
- `url` (str): Базовый URL TheB.AI.
- `working` (bool): Флаг, указывающий на то, работает ли провайдер (в данном случае `False`, поскольку провайдер TheB.AI временно не работает).
- `supports_stream` (bool): Флаг, указывающий на то, поддерживает ли провайдер потоковую передачу ответов (в данном случае `True`).
- `models` (list): Список доступных моделей ИИ.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, webdriver: WebDriver = None, virtual_display: bool = True, **kwargs) -> CreateResult`

    **Описание**: Метод для создания завершения (completion) с использованием выбранной модели ИИ TheB.AI.

    **Параметры**:

    - `model` (str): Название модели ИИ, например, "gpt-3.5-turbo".
    - `messages` (Messages): Список сообщений для модели ИИ.
    - `stream` (bool): Флаг, указывающий на то, должна ли передача ответа быть потоковой.
    - `proxy` (str, optional): Прокси-сервер. По умолчанию `None`.
    - `webdriver` (WebDriver, optional): Экземпляр Selenium WebDriver. По умолчанию `None`.
    - `virtual_display` (bool, optional): Флаг, указывающий на то, следует ли использовать виртуальный дисплей. По умолчанию `True`.
    - `**kwargs`: Дополнительные аргументы.

    **Возвращает**:

    - `CreateResult`: Результат создания завершения (completion), включая сообщение, идентификатор и т. д.

    **Вызывает исключения**:

    - `Exception`: В случае возникновения ошибки при взаимодействии с веб-интерфейсом TheB.AI или получении ответа от модели ИИ.

    **Как работает функция**:

    1. Проверяет, доступна ли выбранная модель ИИ.
    2. Форматирует сообщение для модели ИИ.
    3. Инициализирует сессию WebDriver.
    4. Открывает веб-страницу TheB.AI.
    5. Ждет появления текстового поля для ввода сообщения.
    6. Выполняет скрипт, который перехватывает все запросы `fetch` и позволяет получать данные о модели ИИ в режиме потоковой передачи.
    7. Проверяет доступность модели ИИ и устанавливает ее, если необходимо.
    8. Вводит сообщение в текстовое поле.
    9. Ждет появления завершения (completion).
    10. Читает ответ от модели ИИ в режиме потоковой передачи.
    11. Возвращает результат создания завершения (completion).


## Примеры

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Theb import Theb
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.helper import Messages

# Создание экземпляра класса Theb
provider = Theb()

# Список сообщений для модели ИИ
messages = Messages(
    [
        {"role": "user", "content": "Привет! Как дела?"},
    ]
)

# Создание завершения (completion) с использованием модели GPT-3.5 Turbo
result = provider.create_completion(model="gpt-3.5-turbo", messages=messages, stream=True)

# Вывод ответа от модели ИИ
for chunk in result:
    print(chunk)
```
```python
# Создание экземпляра класса Theb
provider = Theb()

# Список сообщений для модели ИИ
messages = Messages(
    [
        {"role": "user", "content": "Привет! Как дела?"},
    ]
)

# Создание завершения (completion) с использованием модели GPT-4
result = provider.create_completion(model="gpt-4", messages=messages, stream=True)

# Вывод ответа от модели ИИ
for chunk in result:
    print(chunk)
```
```python
# Создание экземпляра класса Theb
provider = Theb()

# Список сообщений для модели ИИ
messages = Messages(
    [
        {"role": "user", "content": "Привет! Как дела?"},
    ]
)

# Создание завершения (completion) с использованием модели Claude 2
result = provider.create_completion(model="claude-2", messages=messages, stream=True)

# Вывод ответа от модели ИИ
for chunk in result:
    print(chunk)
```
```python
# Создание экземпляра класса Theb
provider = Theb()

# Список сообщений для модели ИИ
messages = Messages(
    [
        {"role": "user", "content": "Привет! Как дела?"},
    ]
)

# Создание завершения (completion) с использованием модели PaLM 2
result = provider.create_completion(model="palm-2", messages=messages, stream=True)

# Вывод ответа от модели ИИ
for chunk in result:
    print(chunk)