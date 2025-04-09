### **Анализ кода модуля `Poe.py`**

=========================================================================================

Модуль `Poe.py` предназначен для взаимодействия с Poe.com с использованием Selenium WebDriver. Он позволяет отправлять запросы к различным моделям, таким как Llama-2 и GPT, и получать ответы.

**Качество кода**:

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Использование WebDriver для автоматизации взаимодействия с веб-сайтом.
    - Поддержка стриминга ответов.
    - Наличие списка поддерживаемых моделей.
- **Минусы**:
    - Отсутствие аннотаций типов.
    - Жёстко заданные значения таймаутов.
    - Повторяющийся код (например, при поиске `textarea`).
    - Использование `WebDriver` напрямую, а не через обертку `Driver` из `src.webdirver`.
    - Отсутствие обработки исключений для конкретных ошибок Selenium.
    - Не все строки документированы.

**Рекомендации по улучшению**:

1.  **Добавить аннотации типов**:

    - Для всех переменных, аргументов функций и возвращаемых значений необходимо добавить аннотации типов.

2.  **Использовать `j_loads` или `j_loads_ns`**:

    - Если используются JSON-файлы для конфигурации, заменить стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.

3.  **Рефакторинг и улучшения**:

    - Избавиться от дублирования кода при поиске элемента `textarea`.
    - Использовать более гибкие настройки таймаутов, возможно, через параметры конфигурации.
    - Добавить обработку конкретных исключений Selenium, чтобы более точно диагностировать проблемы.
    - Переработать логику повторного открытия браузера для входа, чтобы она была более надежной.

4.  **Документация**:

    - Добавить docstring для класса `Poe` с описанием его назначения.
    - Добавить docstring для каждой внутренней функции и метода.

5.  **Использовать `logger`**:

    - Добавить логирование для отладки и мониторинга работы кода.

6.  **Использовать webdriver из проекта `hypotez`**:
    - Использовать `from src.webdirver import Driver, Chrome, Firefox, Playwright`

**Оптимизированный код**:

```python
from __future__ import annotations

import time
from typing import Generator, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.logger import logger
from ..base_provider import AbstractProvider
from ..helper import format_prompt
from ...typing import CreateResult, Messages

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
    Класс для взаимодействия с Poe.com.

    Этот класс позволяет отправлять запросы к различным моделям через Poe.com
    с использованием Selenium WebDriver.
    """

    url: str = "https://poe.com"
    working: bool = False
    needs_auth: bool = True
    supports_stream: bool = True

    models: set[str] = models.keys()

    @classmethod
    def create_completion(
        cls,
        model: str,
        messages: Messages,
        stream: bool,
        proxy: Optional[str] = None,
        webdriver: Optional[WebDriver] = None,
        user_data_dir: Optional[str] = None,
        headless: bool = True,
        **kwargs,
    ) -> CreateResult:
        """
        Создает запрос к Poe.com и возвращает ответ.

        Args:
            model (str): Имя модели для использования.
            messages (Messages): Список сообщений для отправки.
            stream (bool): Флаг, указывающий, нужно ли возвращать ответ в виде потока.
            proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию None.
            webdriver (Optional[WebDriver], optional): Инстанс WebDriver для использования. По умолчанию None.
            user_data_dir (Optional[str], optional): Путь к каталогу пользовательских данных браузера. По умолчанию None.
            headless (bool, optional): Флаг, указывающий, нужно ли запускать браузер в headless-режиме. По умолчанию True.

        Returns:
            CreateResult: Результат выполнения запроса.

        Raises:
            ValueError: Если указанная модель не поддерживается.
            RuntimeError: Если не удается найти поле ввода текста.
        """
        if not model:
            model = "gpt-3.5-turbo"
        elif model not in models:
            raise ValueError(f"Model are not supported: {model}")
        prompt: str = format_prompt(messages)

        session = WebDriverSession(webdriver, user_data_dir, headless, proxy=proxy)
        with session as driver:
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
            """
                    },
                )

                driver.get(f"{cls.url}/{models[model]['name']}")
                wait: WebDriverWait = WebDriverWait(driver, 10 if headless else 240)
                wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "textarea[class^='GrowingTextArea']")
                    )
                )
            except Exception as ex:
                logger.error("Error during initial page load", ex, exc_info=True)
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

            element_send_text(
                driver.find_element(
                    By.CSS_SELECTOR, "footer textarea[class^='GrowingTextArea']"
                ),
                prompt,
            )
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
                chunk: Optional[str] = driver.execute_script(script)
                if chunk:
                    yield chunk
                elif chunk != "":
                    break
                else:
                    time.sleep(0.1)