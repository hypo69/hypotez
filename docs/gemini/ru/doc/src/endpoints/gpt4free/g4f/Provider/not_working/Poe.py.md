# Модуль Poe

## Обзор

Модуль `Poe` предоставляет реализацию класса `Poe`, который представляет собой провайдера для работы с сервисом Poe. Poe - это платформа для общения с различными языковыми моделями, предоставляя доступ к моделям, таким как GPT-3.5-Turbo, GPT-4, Llama-2 и др. 

## Подробнее

Модуль использует Selenium WebDriver для взаимодействия с веб-интерфейсом Poe. 

## Классы

### `class Poe`

**Описание**:  Класс `Poe` наследуется от абстрактного класса `AbstractProvider`, реализуя методы для отправки запросов и получения ответов от моделей Poe. 

**Наследует**:  `AbstractProvider`

**Атрибуты**:

- `url` (str): URL-адрес сервиса Poe.
- `working` (bool):  Флаг, указывающий на работоспособность провайдера.
- `needs_auth` (bool): Флаг, указывающий, требуется ли авторизация для использования сервиса.
- `supports_stream` (bool): Флаг, указывающий, поддерживает ли провайдер потоковую передачу ответов.
- `models` (list): Список моделей, доступных через провайдера.

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, webdriver: WebDriver = None, user_data_dir: str = None, headless: bool = True, **kwargs) -> CreateResult`:  Функция, отвечающая за отправку запроса к модели Poe и получение ответа.

**Внутренние функции**:

- `element_send_text(element, text)`:  Вспомогательная функция для вставки текста в элемент веб-страницы.
- `format_prompt(messages)`: Форматирует входные сообщения в подходящий формат для отправки в модель.

**Как работает класс**:

1. **Инициализация**:  При создании объекта `Poe` происходит инициализация необходимых атрибутов.
2. **Обработка запроса**:  Метод `create_completion` принимает следующие параметры:
    - `model`:  Идентификатор модели, с которой необходимо взаимодействовать.
    - `messages`: Список сообщений, необходимых для создания контекста.
    - `stream`: Флаг, указывающий, требуется ли потоковая передача ответа.
    - `proxy`:  Прокси-сервер, если требуется.
    - `webdriver`:  Экземпляр Selenium WebDriver.
    - `user_data_dir`: Путь к директории с данными пользователя для WebDriver.
    - `headless`: Флаг, указывающий, запускать ли WebDriver в headless режиме.
3. **Отправка запроса**:  WebDriver открывает веб-страницу Poe, вводит текст запроса в текстовое поле и отправляет запрос.
4. **Получение ответа**:  Метод `create_completion` использует Selenium WebDriver для ожидания ответа от модели. Он получает ответ в виде потока текста и возвращает его как `CreateResult`.
5. **Потоковая передача**:  Если флаг `stream` установлен в `True`, метод `create_completion` возвращает поток текста, позволяя получить части ответа по мере его формирования.

**Примеры**:

```python
# Создание инстанса драйвера (пример с Chrome)
driver = Driver(Chrome)

# Пример отправки запроса к модели GPT-3.5-Turbo
messages = [
    {"role": "user", "content": "Привет!"},
]

result = Poe.create_completion(
    model="gpt-3.5-turbo",
    messages=messages,
    stream=True,
    webdriver=driver
)

# Вывод ответа
for chunk in result:
    print(chunk, end="")
```

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
        user_data_dir: str = None,
        headless: bool = True,
        **kwargs
    ) -> CreateResult:
        """
        Отправляет запрос к модели Poe и получает ответ.

        Args:
            model (str): Идентификатор модели, с которой необходимо взаимодействовать.
            messages (Messages): Список сообщений, необходимых для создания контекста.
            stream (bool): Флаг, указывающий, требуется ли потоковая передача ответа.
            proxy (str, optional): Прокси-сервер, если требуется. По умолчанию `None`.
            webdriver (WebDriver, optional): Экземпляр Selenium WebDriver. По умолчанию `None`.
            user_data_dir (str, optional): Путь к директории с данными пользователя для WebDriver. По умолчанию `None`.
            headless (bool, optional): Флаг, указывающий, запускать ли WebDriver в headless режиме. По умолчанию `True`.
            **kwargs: Дополнительные аргументы.

        Returns:
            CreateResult: Результат создания ответа.

        Raises:
            ValueError: Если модель не поддерживается.
            RuntimeError: Если текстовое поле для ввода не найдено (возможно, пользователь не авторизован).
        """
        if not model:
            model = "gpt-3.5-turbo"
        elif model not in models:
            raise ValueError(f"Model are not supported: {model}")
        prompt = format_prompt(messages)

        session = WebDriverSession(webdriver, user_data_dir, headless, proxy=proxy)
        with session as driver:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
    window._message = window._last_message = "";
    window._message_finished = false;
    class ProxiedWebSocket extends WebSocket {\n
    constructor(url, options) {\n
        super(url, options);\n
        this.addEventListener("message", (e) => {\n
            const data = JSON.parse(JSON.parse(e.data)["messages"][0])["payload"]["data"];\n
            if ("messageAdded" in data) {\n
                if (data["messageAdded"]["author"] != "human") {\n
                    window._message = data["messageAdded"]["text"];\n
                    if (data["messageAdded"]["state"] == "complete") {\n
                        window._message_finished = true;\n
                    }\n                }\n            }\n        });\n
    }\n    }\n    window.WebSocket = ProxiedWebSocket;\n    """
            })

            try:
                driver.get(f"{cls.url}/{models[model]['name']}")
                wait = WebDriverWait(driver, 10 if headless else 240)
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[class^='GrowingTextArea']")))
            except:
                # Reopen browser for login
                if not webdriver:
                    driver = session.reopen()
                    driver.get(f"{cls.url}/{models[model]['name']}")
                    wait = WebDriverWait(driver, 240)
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[class^='GrowingTextArea']")))
                else:
                    raise RuntimeError("Prompt textarea not found. You may not be logged in.")

            element_send_text(driver.find_element(By.CSS_SELECTOR, "footer textarea[class^='GrowingTextArea']"), prompt)
            driver.find_element(By.CSS_SELECTOR, "footer button[class*='ChatMessageSendButton']").click()

            script = """
if(window._message && window._message != window._last_message) {
    try {
        return window._message.substring(window._last_message.length);
    } finally {
        window._last_message = window._message;
    }
} else if(window._message_finished) {
    return null;
} else {
    return '';
}
"""
            while True:
                chunk = driver.execute_script(script)
                if chunk:
                    yield chunk
                elif chunk != "":
                    break
                else:
                    time.sleep(0.1)