# Модуль `Theb`

## Обзор

Модуль `Theb` предоставляет класс `Theb`, который является провайдером для взаимодействия с различными моделями AI через веб-интерфейс `TheB.AI`. Он поддерживает потоковую передачу данных и использует `selenium` для автоматизации взаимодействия с веб-сайтом.

## Подробней

Модуль предназначен для обеспечения доступа к моделям, предоставляемым `TheB.AI`, таким как `GPT-3.5 Turbo`, `GPT-4`, `Claude 2` и другие, путем автоматизации действий пользователя в браузере. Это позволяет обходить ограничения API или получать доступ к моделям, которые не предоставляют прямого API.

## Классы

### `Theb(AbstractProvider)`

**Описание**: Класс `Theb` наследуется от `AbstractProvider` и реализует логику взаимодействия с веб-сайтом `TheB.AI`.

**Принцип работы**:

1.  **Инициализация**: При инициализации класса устанавливаются основные параметры, такие как `label`, `url`, `working` и `supports_stream`.
2.  **Создание запроса (create_completion)**: Метод `create_completion` является основным методом для отправки запроса к модели и получения ответа. Он выполняет следующие шаги:

    *   Форматирует запрос, используя предоставленные сообщения.
    *   Инициализирует сессию веб-драйвера.
    *   Переходит на веб-сайт `TheB.AI`.
    *   Внедряет JavaScript для перехвата ответов API.
    *   Выбирает модель, если указана.
    *   Отправляет запрос и получает ответ по частям, используя потоковую передачу.

**Аттрибуты**:

*   `label` (str): Метка провайдера (`"TheB.AI"`).
*   `url` (str): URL веб-сайта (`"https://beta.theb.ai"`).
*   `working` (bool): Указывает, работает ли провайдер в данный момент (`False`).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (`True`).
*   `models` (dict): Список поддерживаемых моделей.

**Методы**:

*   `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, webdriver: WebDriver = None, virtual_display: bool = True, \*\*kwargs) -> CreateResult`: Создает запрос к модели и возвращает результат.

## Функции

### `create_completion`

```python
@classmethod
def create_completion(
    cls,
    model: str,
    messages: Messages,
    stream: bool,
    proxy: str = None,
    webdriver: WebDriver = None,
    virtual_display: bool = True,
    **kwargs
) -> CreateResult:
    """
    Создает запрос к модели AI через веб-интерфейс TheB.AI.

    Args:
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в модель.
        stream (bool): Флаг, указывающий, использовать ли потоковую передачу.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        webdriver (WebDriver, optional): Инстанс веб-драйвера Selenium. По умолчанию `None`.
        virtual_display (bool, optional): Флаг, указывающий, использовать ли виртуальный дисплей. По умолчанию `True`.
        **kwargs: Дополнительные аргументы.

    Returns:
        CreateResult: Результат выполнения запроса.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с веб-сайтом.

    """
    ...
```

**Назначение**: Создает запрос к модели AI через веб-интерфейс `TheB.AI`.

**Параметры**:

*   `cls`: Ссылка на класс `Theb`.
*   `model` (str): Название модели для использования.
*   `messages` (Messages): Список сообщений для отправки в модель.
*   `stream` (bool): Флаг, указывающий, использовать ли потоковую передачу.
*   `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
*   `webdriver` (WebDriver, optional): Инстанс веб-драйвера Selenium. По умолчанию `None`.
*   `virtual_display` (bool, optional): Флаг, указывающий, использовать ли виртуальный дисплей. По умолчанию `True`.
*   `**kwargs`: Дополнительные аргументы.

**Возвращает**:

*   `CreateResult`: Результат выполнения запроса.

**Вызывает исключения**:

*   `Exception`: Если возникает ошибка при взаимодействии с веб-сайтом.

**Как работает функция**:

1.  **Преобразование названия модели**: Если название модели находится в словаре `models`, оно заменяется на соответствующее значение.
2.  **Форматирование запроса**: Запрос форматируется с использованием функции `format_prompt`.
3.  **Инициализация веб-сессии**: Создается и инициализируется сессия веб-драйвера с использованием `WebDriverSession`.
4.  **Внедрение скрипта**: Внедряется JavaScript-код для перехвата ответов API.
5.  **Навигация на сайт**: Веб-драйвер переходит на главную страницу `TheB.AI`.
6.  **Выбор модели (если указана)**: Если указана модель, скрипт пытается выбрать её на веб-сайте.
7.  **Отправка запроса**: Запрос отправляется путем заполнения текстового поля и отправки формы.
8.  **Чтение ответа**: Ответ читается по частям с использованием потоковой передачи данных.

**Внутренние функции**:

*   Отсутствуют

**ASCII flowchart**:

```
A [Преобразование названия модели]
|
B [Форматирование запроса]
|
C [Инициализация веб-сессии]
|
D [Внедрение скрипта]
|
E [Навигация на сайт]
|
F [Выбор модели (если указана)]
|
G [Отправка запроса]
|
H [Чтение ответа]
```

**Примеры**:

Пример 1: Отправка запроса с использованием `GPT-3.5 Turbo` без потоковой передачи.

```python
from selenium import webdriver
from src.webdirver import Driver, Chrome, Firefox, Playwright, WebDriverSession # пример импорта webdriver
from typing import List, Dict
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
#from fake_useragent import UserAgent  # Можно попробовать сгенерировать случайный юзерагент
#ua = UserAgent()
#user_agent = ua.random

messages: Messages = [{"role": "user", "content": "Hello, how are you?"}]
model = "gpt-3.5-turbo"
stream = False
# Добавление опций для Chrome
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument(f"user-agent={user_agent}")  # Установка случайного User-Agent

#driver = webdriver.Chrome(options=chrome_options)

#driver = webdriver.Chrome()
#result = Theb.create_completion(model=model, messages=messages, stream=stream, webdriver=driver)
#print(result)
```

Пример 2: Отправка запроса с использованием `GPT-4` с потоковой передачей через прокси.

```python
from selenium import webdriver
from src.webdirver import Driver, Chrome, Firefox, Playwright, WebDriverSession # пример импорта webdriver
from typing import List, Dict
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)
#from fake_useragent import UserAgent  # Можно попробовать сгенерировать случайный юзерагент
#ua = UserAgent()
#user_agent = ua.random

messages: Messages = [{"role": "user", "content": "Tell me a joke."}]
model = "gpt-4"
stream = True
proxy = "http://your_proxy:8080"

# Добавление опций для Chrome
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument(f"user-agent={user_agent}")  # Установка случайного User-Agent

#driver = webdriver.Chrome(options=chrome_options)

#driver = webdriver.Chrome()
#result = Theb.create_completion(model=model, messages=messages, stream=stream, proxy=proxy, webdriver=driver)
#print(result)