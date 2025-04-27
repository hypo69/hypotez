# \file browser_use.py
# -*- coding: utf-8 -*-

"""
Модуль, предоставляющий класс BrowserController для управления веб-браузером
с использованием Selenium.
"""

import time
from typing import Optional

# --- Selenium Imports ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)

from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox

# --- WebDriver Manager ---
# Автоматически скачивает и управляет chromedriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


import header
from src.logger import logger

class BrowserController:
    """
    Класс для управления веб-браузером (Chrome) с использованием Selenium.
    Предоставляет методы для навигации, поиска, скрапинга и взаимодействия.
    """
    DEFAULT_WAIT_TIMEOUT = 10 # Секунд для ожидания элементов

    def __init__(self, headless: bool = True):
        """
        Инициализирует WebDriver для Chrome.

        Args:
            headless (bool): Запускать ли браузер в "безголовом" режиме (без GUI).
                             True по умолчанию для автоматизации.
        """
        self.driver: Optional[webdriver.Chrome] = None
        options = ChromeOptions()
        if headless:
            logger.info("Настройка Chrome для запуска в headless режиме.")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu") # Часто нужен для headless
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("user-agent=Mozilla/5.0...") # Пример User Agent

        try:
            logger.info("Инициализация Chrome WebDriver...")
            # WebDriverManager автоматически скачает/обновит драйвер
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("Chrome WebDriver успешно инициализирован.")
        except WebDriverException as ex:
             # Используем ваш формат логгера
             logger.error("Критическая ошибка: Не удалось инициализировать Chrome WebDriver.", ex, exc_info=True)
        except Exception as ex:
             logger.error("Неожиданная ошибка при инициализации Chrome WebDriver.", ex, exc_info=True)


    def _check_driver(self) -> bool:
        """ Проверяет, был ли драйвер успешно инициализирован. """
        if self.driver is None:
            # Используем ваш формат
            logger.error("Драйвер браузера не был инициализирован.", None, exc_info=False)
            return False
        return True

    def search(self, query: str, search_engine_url: str = "https://www.google.com") -> str:
        """ Выполняет поиск в указанной поисковой системе. """
        if not self._check_driver(): return "Ошибка: Драйвер браузера недоступен."

        logger.info(f"[Browser Action] Поиск: '{query}' на {search_engine_url}")
        try:
            self.driver.get(search_engine_url)
            wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIMEOUT)
            # Ищем поле поиска (пробуем разные селекторы)
            search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='q'], input[name='q']")))
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            # Ждем загрузки результатов
            wait.until(EC.presence_of_element_located((By.ID, "search")))
            # time.sleep(1) # Пауза не рекомендуется, лучше ждать конкретный элемент

            # Извлекаем текст с результатами
            results_text = self.driver.find_element(By.TAG_NAME, 'body').text
            max_len = 2500 # Ограничиваем длину
            if len(results_text) > max_len:
                logger.debug(f"Результаты поиска обрезаны до {max_len} символов.", exc_info=False)
                results_text = results_text[:max_len] + "..."

            return f"Результаты поиска по запросу '{query}':\n{results_text}"

        except TimeoutException as ex:
             logger.error(f"Timeout",ex)

