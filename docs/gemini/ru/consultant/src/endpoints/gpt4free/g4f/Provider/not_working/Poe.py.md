### **Анализ кода модуля `Poe.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование `WebDriver` для взаимодействия с веб-страницей.
    - Поддержка стриминга ответов.
    - Наличие моделей для выбора.
- **Минусы**:
    - Отсутствие аннотаций типов для параметров и возвращаемых значений функций.
    - Использование устаревшего `Union[]` вместо `|`.
    - Недостаточно подробные комментарии и отсутствует документация для класса.
    - Дублирование кода (например, повторный поиск элемента `textarea`).
    - Не обрабатываются все возможные исключения.
    - Не используется модуль `logger` для логирования.

#### **Рекомендации по улучшению**:

1. **Добавить аннотации типов**: Необходимо добавить аннотации типов для всех параметров функций, переменных и возвращаемых значений.

2. **Заменить `Union[]` на `|`**: Использовать современный синтаксис для объединения типов.

3. **Документирование кода**: Добавить docstring для класса `Poe` и всех его методов, включая описание параметров, возвращаемых значений и возможных исключений.

4. **Логирование**: Использовать модуль `logger` для логирования ошибок и других важных событий.

5. **Улучшить обработку исключений**: Добавить более конкретные блоки `except` для обработки различных типов исключений и логировать их с помощью `logger.error`.

6. **Улучшить читаемость**: Разбить длинные строки кода на более короткие для улучшения читаемости.

7. **Избавиться от дублирования кода**: Избегать повторного выполнения одних и тех же действий (например, поиска элемента `textarea`).

8. **Обработка `webdriver`**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

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

#### **Оптимизированный код**:

```python
"""
Модуль для взаимодействия с Poe
=================================

Модуль содержит класс :class:`Poe`, который используется для взаимодействия с Poe.com 
через WebDriver для обхода защиты.

Пример использования
----------------------

>>> poe = Poe()
>>> completion = poe.create_completion(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'Hello'}], stream=True)
>>> for chunk in completion:
...     print(chunk, end='')
"""
from __future__ import annotations

import time
from typing import AsyncGenerator, Generator, List, Optional, Dict
from pathlib import Path

from src.logger import logger

from ...typing import CreateResult, Messages
from ..base_provider import AbstractProvider
from ..helper import format_prompt
from src.webdriver import Driver, Chrome, Firefox, Playwright

models = {
    "meta-llama/Llama-2-7b-chat-hf": {"name": "Llama-2-7b"},
    "meta-llama/Llama-2-13b-chat-hf": {"name": "Llama-2-13b"},
    "meta-llama/Llama-2-70b-chat-hf": {"name": "Llama-2-70b"},
    "codellama/CodeLlama-7b-Instruct-hf": {"name": "Code-Llama-7b"},
    "codellama/CodeLlama-13b-Instruct-hf": {"name": "Code-Llama-13b"},
    "codellama/CodeLlama-34b-Instruct-hf": {"name": "Code-Llama-34b"},
    "gpt-3.5-turbo": {"name": "GPT-3.5-Turbo"},
    "gpt-3.5-turbo-instruct": {"name": "GPT-3.5-Turbo-Instruct"},
    "gpt-4": {"name": "GPT-4"},
    "palm": {"name": "Google-PaLM"},
}


class Poe(AbstractProvider):
    """
    Класс для взаимодействия с Poe.com через WebDriver.
    """

    url: str = "https://poe.com"
    working: bool = False
    needs_auth: bool = True
    supports_stream: bool = True
    models: List[str] = list(models.keys())

    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: Optional[str] = None,
        webdriver: Optional[Driver] = None,
        user_data_dir: Optional[str] = None,
        headless: bool = True,
        **kwargs,
    ) -> CreateResult:
        """
        Создает запрос к Poe и возвращает результат.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг стриминга.
            proxy (Optional[str], optional): Прокси-сервер. По умолчанию None.
            webdriver (Optional[Driver], optional): Объект WebDriver. По умолчанию None.
            user_data_dir (Optional[str], optional): Путь к каталогу пользовательских данных. По умолчанию None.
            headless (bool, optional): Флаг headless-режима. По умолчанию True.
            **kwargs: Дополнительные аргументы.

        Returns:
            CreateResult: Результат запроса.

        Raises:
            ValueError: Если модель не поддерживается.
            RuntimeError: Если не найден элемент textarea для ввода текста.
        """
        if not model:
            model = "gpt-3.5-turbo"
        elif model not in models:
            raise ValueError(f"Model are not supported: {model}")

        prompt: str = format_prompt(messages)

        session = WebDriverSession(webdriver, user_data_dir, headless, proxy=proxy)
        with session as driver:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            try:
                driver.execute_cdp_cmd(
                    "Page.addScriptToEvaluateOnNewDocument",
                    {
                        "source": """
            window._message = window._last_message = "";
            window._message_finished = false;
            class ProxiedWebSocket extends WebSocket {
            constructor(url, options) {
                super(url, options);
                this.addEventListener("message", (e) => {
                    const data = JSON.parse(JSON.parse(e.data)["messages"][0])["payload"]["data"];
                    if ("messageAdded" in data) {
                        if (data["messageAdded"]["author"] != "human") {
                            window._message = data["messageAdded"]["text"];
                            if (data["messageAdded"]["state"] == "complete") {
                                window._message_finished = true;
                            }
                        }
                    }
                });
            }
            }
            window.WebSocket = ProxiedWebSocket;
            """,
                    },
                )
            except Exception as ex:
                logger.error("Error while executing cdp command", ex, exc_info=True)
                raise

            try:
                driver.get(f"{cls.url}/{models[model]['name']}")
                wait = WebDriverWait(driver, 10 if headless else 240)
                wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "textarea[class^='GrowingTextArea']")
                    )
                )
            except Exception as ex:
                logger.error(
                    "Error while waiting for textarea", ex, exc_info=True
                )
                # Reopen browser for login
                if not webdriver:
                    driver = session.reopen()
                    driver.get(f"{cls.url}/{models[model]['name']}")
                    wait = WebDriverWait(driver, 240)
                    wait.until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "textarea[class^='GrowingTextArea']")
                        )
                    )
                else:
                    raise RuntimeError(
                        "Prompt textarea not found. You may not be logged in."
                    )

            textarea = driver.find_element(
                By.CSS_SELECTOR, "footer textarea[class^='GrowingTextArea']"
            )
            element_send_text(textarea, prompt)
            driver.find_element(
                By.CSS_SELECTOR, "footer button[class*='ChatMessageSendButton']"
            ).click()

            script: str = """
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
                try:
                    chunk: str = driver.execute_script(script)
                    if chunk:
                        yield chunk
                    elif chunk != "":
                        break
                    else:
                        time.sleep(0.1)
                except Exception as ex:
                    logger.error("Error while executing script", ex, exc_info=True)
                    break

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


def element_send_text(element: WebDriver, text: str) -> None:
    """
    Sends text to an element using JavaScript to bypass potential Selenium issues.

    Args:
        element (WebDriver): The web element to send text to.
        text (str): The text to send.
    """
    try:
        element.send_keys(text)
    except Exception as ex:
        logger.error('Error while sending keys to element', ex, exc_info=True)

class WebDriverSession:
    """
    Управляет сессией WebDriver, обеспечивая повторное использование и переоткрытие драйвера.
    """

    def __init__(self, webdriver: Optional[Driver] = None, user_data_dir: Optional[str] = None, headless: bool = True, proxy: Optional[str] = None):
        """
        Инициализирует сессию WebDriver.

        Args:
            webdriver (Optional[Driver], optional): Существующий объект WebDriver для повторного использования. Defaults to None.
            user_data_dir (Optional[str], optional): Каталог пользовательских данных браузера. Defaults to None.
            headless (bool, optional): Запускать ли браузер в headless-режиме. Defaults to True.
            proxy (Optional[str], optional): URL прокси-сервера. Defaults to None.
        """
        self.webdriver = webdriver
        self.user_data_dir = user_data_dir
        self.headless = headless
        self.proxy = proxy
        self.driver = None  # Initialize driver to None

    def __enter__(self) -> WebDriver:
        """
        Входит в контекстный менеджер, возвращая WebDriver.

        Returns:
            WebDriver: Объект WebDriver для использования.
        """
        if self.webdriver:
            self.driver = self.webdriver  # Use existing webdriver if provided
        else:
            # Initialize a new WebDriver instance
            options = {}
            if self.user_data_dir:
                options["user_data_dir"] = self.user_data_dir
            if self.headless:
                options["headless"] = self.headless
            if self.proxy:
                options["proxy"] = self.proxy
            self.driver = Driver(Chrome, **options).driver # тут мы задаем Chrome по умолчанию
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Выходит из контекстного менеджера, закрывая WebDriver, если он был создан внутри контекста.

        Args:
            exc_type: Тип исключения (если есть).
            exc_val: Значение исключения (если есть).
            exc_tb: Трассировка исключения (если есть).
        """
        if not self.webdriver and self.driver:
            try:
                self.driver.quit()
            except Exception as ex:
                logger.error('Error while quiting driver', ex, exc_info=True)

    def reopen(self) -> WebDriver:
        """
        Переоткрывает браузер, создавая новый WebDriver с теми же параметрами.

        Returns:
            WebDriver: Новый объект WebDriver.
        """
        try:
            if self.driver:
                self.driver.quit()  # Ensure the current driver is closed
        except Exception as ex:
            logger.error('Error while quiting driver', ex, exc_info=True)
        # Initialize a new WebDriver instance
        options = {}
        if self.user_data_dir:
            options["user_data_dir"] = self.user_data_dir
        if self.headless:
            options["headless"] = self.headless
        if self.proxy:
            options["proxy"] = self.proxy
        self.driver = Driver(Chrome, **options).driver # тут мы задаем Chrome по умолчанию
        return self.driver