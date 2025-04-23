# Модуль `Theb`

## Обзор

Модуль `Theb` предоставляет интерфейс для взаимодействия с сервисом `TheB.AI` для создания завершений текста на основе предоставленных сообщений. Он поддерживает потоковую передачу данных и использует Selenium WebDriver для автоматизации взаимодействия с веб-интерфейсом `TheB.AI`. Модуль содержит класс `Theb`, который является провайдером для `TheB.AI`. Он позволяет выбирать различные модели, такие как GPT-3.5 Turbo, GPT-4, Claude 2 и другие.

## Подробней

Модуль автоматизирует процесс отправки запросов к `TheB.AI` через веб-интерфейс, используя Selenium WebDriver. Он выполняет следующие шаги:

1.  Открывает веб-страницу `TheB.AI`.
2.  Выбирает модель, если она указана.
3.  Вводит предоставленный текст в поле ввода.
4.  Считывает ответ, используя JavaScript для перехвата данных, отправляемых сервером.
5.  Возвращает текст ответа в потоковом режиме.

## Классы

### `Theb`

**Описание**: Класс `Theb` является провайдером для `TheB.AI`. Он наследует `AbstractProvider` и предоставляет метод `create_completion` для создания завершений текста.

**Наследует**: `AbstractProvider`

**Атрибуты**:

*   `label` (str): Метка провайдера (`"TheB.AI"`).
*   `url` (str): URL веб-сайта `TheB.AI` (`"https://beta.theb.ai"`).
*   `working` (bool): Указывает, работает ли провайдер (`False`).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (`True`).
*   `models` (dict): Список поддерживаемых моделей.

#### `create_completion`

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
    """ Функция создает завершение текста на основе предоставленных сообщений, используя веб-интерфейс TheB.AI.

    Args:
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки.
        stream (bool): Указывает, следует ли использовать потоковую передачу данных.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        webdriver (WebDriver, optional): Инстанс WebDriver для управления браузером. По умолчанию `None`.
        virtual_display (bool, optional): Указывает, следует ли использовать виртуальный дисплей. По умолчанию `True`.
        **kwargs: Дополнительные аргументы.

    Returns:
        CreateResult: Генератор, возвращающий чанки текста ответа.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с веб-интерфейсом.
    """
```

**Назначение**: Создает запрос к TheB.AI и возвращает ответ.

**Параметры**:

*   `cls`: Ссылка на класс.
*   `model` (str): Модель, которую нужно использовать. Если модель есть в словаре `models`, она заменяется на соответствующее значение для TheB.AI.
*   `messages` (Messages): Список сообщений, которые нужно отправить.
*   `stream` (bool): Флаг, указывающий, нужно ли использовать потоковый режим.
*   `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
*   `webdriver (WebDriver, optional)`: Драйвер веб-браузера. По умолчанию `None`.
*   `virtual_display` (bool, optional): Использовать ли виртуальный дисплей. По умолчанию `True`.
*   `**kwargs`: Дополнительные параметры.

**Возвращает**:

*   `CreateResult`: Генератор, выдающий чанки текста ответа.

**Вызывает исключения**:

*   `Exception`: В случае возникновения ошибок при взаимодействии с веб-интерфейсом.

**Как работает функция**:

1.  **Форматирование запроса**:
    *   Если `model` есть в словаре `models`, функция заменяет ее на соответствующее значение для TheB.AI.
    *   Форматирует список `messages` в единую строку `prompt`, используя функцию `format_prompt`.

2.  **Настройка WebDriver**:
    *   Создает экземпляр `WebDriverSession` для управления сессией браузера.
    *   Устанавливает хук для перехвата запросов `/api/conversation` с помощью JavaScript.

3.  **Взаимодействие с веб-интерфейсом TheB.AI**:
    *   Открывает страницу `/home` на `TheB.AI`.
    *   Ожидает загрузки элемента `textareaAutosize`.
    *   Если происходит ошибка, перезапускает сессию и повторяет попытку.

4.  **Выбор модели (если указана)**:
    *   Кликает на элемент `#SelectModel svg`, чтобы открыть панель выбора модели.
    *   Выбирает нужную модель из списка, кликая на соответствующий элемент.

5.  **Отправка запроса**:
    *   Вводит текст запроса `prompt` в элемент `textareaAutosize`.

6.  **Чтение ответа**:
    *   Использует JavaScript для чтения данных из потока ответа.
    *   Выделяет полезную нагрузку JSON из каждой строки, начинающейся с `data: `.
    *   Удаляет уже обработанную часть сообщения.
    *   Возвращает чанки текста с помощью `yield`.

**Внутренние функции**:

Внутри функции `create_completion` нет определения внутренних функций.

**Примеры**:

```python
# Пример вызова функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
stream = True
proxy = None
webdriver = None
virtual_display = True

result = Theb.create_completion(
    model=model,
    messages=messages,
    stream=stream,
    proxy=proxy,
    webdriver=webdriver,
    virtual_display=virtual_display
)

for chunk in result:
    print(chunk)
```

## Параметры класса

*   `label` (str): Метка провайдера (`"TheB.AI"`).
*   `url` (str): URL веб-сайта `TheB.AI` (`"https://beta.theb.ai"`).
*   `working` (bool): Указывает, работает ли провайдер (`False`).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (`True`).
*   `models` (dict): Список поддерживаемых моделей.

## Методы класса

### `create_completion`

Краткое описание метода: Создает завершение текста на основе предоставленных сообщений, используя веб-интерфейс `TheB.AI`.

**Параметры**:

*   `model` (str): Название модели для использования.
*   `messages` (Messages): Список сообщений для отправки.
*   `stream` (bool): Указывает, следует ли использовать потоковую передачу данных.
*   `proxy` (str, optional): URL прокси-сервера. По умолчанию `None`.
*   `webdriver (WebDriver, optional)`: Драйвер веб-браузера. По умолчанию `None`.
*   `virtual_display` (bool, optional): Указывает, следует ли использовать виртуальный дисплей. По умолчанию `True`.
*   `**kwargs`: Дополнительные аргументы.

**Примеры**:

```python
# Пример вызова функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Напиши короткий рассказ."}]
stream = True
proxy = None
webdriver = None
virtual_display = True

result = Theb.create_completion(
    model=model,
    messages=messages,
    stream=stream,
    proxy=proxy,
    webdriver=webdriver,
    virtual_display=virtual_display
)

for chunk in result:
    print(chunk)