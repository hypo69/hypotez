# Модуль Theb

## Обзор

Модуль `Theb` предназначен для взаимодействия с различными моделями искусственного интеллекта через веб-интерфейс [TheB.AI](https://beta.theb.ai). Он предоставляет возможность отправлять запросы к моделям, таким как GPT-3.5, GPT-4, Claude 2, PaLM 2 и Llama 2, а также получать ответы в потоковом режиме. Модуль использует Selenium WebDriver для автоматизации взаимодействия с веб-сайтом TheB.AI.

## Подробнее

Этот модуль является провайдером для проекта `hypotez`, позволяя использовать модели, доступные через TheB.AI. Он автоматизирует процесс выбора модели, ввода запроса и получения ответа через веб-интерфейс.  Модуль предназначен для интеграции с другими частями проекта `hypotez`, предоставляя унифицированный интерфейс для работы с различными AI-моделями. 

## Классы

### `Theb(AbstractProvider)`

**Описание**: Класс `Theb` реализует взаимодействие с веб-сайтом [TheB.AI](https://beta.theb.ai) для отправки запросов к различным моделям ИИ и получения ответов.
**Наследует**: `AbstractProvider`
**Атрибуты**:

-   `label` (str): Название провайдера ("TheB.AI").
-   `url` (str): URL веб-сайта TheB.AI ("https://beta.theb.ai").
-   `working` (bool): Указывает, работает ли провайдер в данный момент (False).
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (True).
-   `models` (dict): Словарь доступных моделей и их отображаемые названия.

**Методы**:

-   `create_completion()`: Отправляет запрос к выбранной модели и возвращает результат.

#### Принцип работы:

1.  **Инициализация**: При создании экземпляра класса `Theb` устанавливаются основные параметры провайдера, такие как URL, поддержка потоковой передачи и список доступных моделей.
2.  **`create_completion()`**: Этот метод является основным для взаимодействия с TheB.AI. Он принимает параметры, такие как модель, сообщения, флаг потоковой передачи, прокси и другие параметры, необходимые для настройки веб-драйвера.
3.  **Автоматизация через Selenium**: Использует Selenium WebDriver для автоматизации взаимодействия с веб-сайтом TheB.AI. WebDriver открывает веб-страницу, выбирает модель (если указана) и отправляет запрос.
4.  **Получение ответа**: После отправки запроса, код отслеживает изменения на веб-странице и извлекает ответ модели. Если включена потоковая передача, ответ возвращается частями по мере поступления.
5.  **Обработка ошибок**: В случае возникновения ошибок в процессе выполнения, код обрабатывает их и возвращает соответствующее сообщение об ошибке.

## Методы класса

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
    Отправляет запрос к выбранной модели через веб-интерфейс TheB.AI и возвращает результат.

    Args:
        cls (Theb): Класс Theb.
        model (str): Название модели для использования.
        messages (Messages): Список сообщений для отправки в запросе.
        stream (bool): Флаг, указывающий, следует ли возвращать ответ в потоковом режиме.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        webdriver (WebDriver, optional): Инстанс WebDriver для управления браузером. По умолчанию `None`.
        virtual_display (bool, optional): Флаг, указывающий, следует ли использовать виртуальный дисплей. По умолчанию `True`.
        **kwargs: Дополнительные параметры.

    Returns:
        CreateResult: Результат выполнения запроса.

    Raises:
        Exception: Если возникает ошибка при взаимодействии с веб-сайтом.
    """
    ...
```

**Назначение**: Метод `create_completion` отправляет запрос к выбранной модели через веб-интерфейс TheB.AI и возвращает результат. Он использует Selenium WebDriver для автоматизации взаимодействия с веб-сайтом, включая выбор модели, ввод запроса и получение ответа.

**Параметры**:

-   `cls` (Theb): Класс Theb.
-   `model` (str): Название модели для использования.
-   `messages` (Messages): Список сообщений для отправки в запросе.
-   `stream` (bool): Флаг, указывающий, следует ли возвращать ответ в потоковом режиме.
-   `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
-   `webdriver` (WebDriver, optional): Инстанс WebDriver для управления браузером. По умолчанию `None`.
-   `virtual_display` (bool, optional): Флаг, указывающий, следует ли использовать виртуальный дисплей. По умолчанию `True`.
-   `**kwargs`: Дополнительные параметры.

**Возвращает**:

-   `CreateResult`: Результат выполнения запроса.

**Вызывает исключения**:

-   `Exception`: Если возникает ошибка при взаимодействии с веб-сайтом.

**Как работает функция**:

1.  **Преобразование модели**: Если `model` находится в словаре `models`, то её значение заменяется на соответствующее значение из словаря.
2.  **Форматирование запроса**: Запрос `messages` форматируется с использованием функции `format_prompt`.
3.  **Создание веб-сессии**: Создается веб-сессия с использованием `WebDriverSession`, который управляет инстансом `webdriver`.
4.  **Перехват fetch запросов**: С помощью JavaScript кода перехватываются все fetch запросы к `/api/conversation`, чтобы получить ответ от сервера.
5.  **Взаимодействие с веб-сайтом**: Открывается веб-страница TheB.AI, и с помощью Selenium автоматизируется взаимодействие с элементами страницы, такими как выбор модели и ввод запроса.
6.  **Чтение ответа**: С помощью JavaScript кода читается ответ от сервера.
7.  **Потоковая передача**: Если `stream` установлен в `True`, ответ возвращается частями по мере поступления.
8.  **Обработка ошибок**: В случае возникновения ошибок, функция обрабатывает их и возвращает соответствующее сообщение об ошибке.

**Примеры**:

```python
# Пример вызова create_completion с потоковой передачей
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
stream = True
result = Theb.create_completion(model=model, messages=messages, stream=stream)
for chunk in result:
    print(chunk)

# Пример вызова create_completion без потоковой передачи
model = "gpt-4"
messages = [{"role": "user", "content": "What is the meaning of life?"}]
stream = False
result = Theb.create_completion(model=model, messages=messages, stream=stream)
print(result)
```

## Параметры класса

-   `label` (str): Название провайдера ("TheB.AI").
-   `url` (str): URL веб-сайта TheB.AI ("https://beta.theb.ai").
-   `working` (bool): Указывает, работает ли провайдер в данный момент (False).
-   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (True).
-   `models` (dict): Словарь доступных моделей и их отображаемые названия.