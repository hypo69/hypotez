### Как использовать класс `PlaywrightExecutor`
=========================================================================================

Описание
-------------------------
Класс `PlaywrightExecutor` предназначен для управления браузером с использованием Playwright и выполнения различных действий с веб-элементами на странице. Он позволяет запускать и останавливать браузер, выполнять поиск элементов, получать их атрибуты, делать скриншоты и выполнять события, такие как клики или ввод текста.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создайте экземпляр класса `PlaywrightExecutor`, указав тип браузера (по умолчанию 'chromium').
2. **Запуск браузера**: Вызовите асинхронный метод `start()` для запуска браузера и создания новой страницы.
3. **Выполнение действий**: Используйте метод `execute_locator()` для выполнения действий с веб-элементами на странице, указав локатор элемента и другие параметры.
4. **Остановка браузера**: Вызовите асинхронный метод `stop()` для закрытия браузера и остановки экземпляра Playwright.

Пример использования
-------------------------

```python
import asyncio
from src.webdriver.playwright.executor import PlaywrightExecutor

async def main():
    # 1. Инициализация класса
    executor = PlaywrightExecutor(browser_type='firefox')

    try:
        # 2. Запуск браузера
        await executor.start()

        # 3. Выполнение действий
        # Определение локатора для поля ввода
        locator = {
            "by": "XPATH",
            "selector": "//input[@name='q']",
            "attribute": None,
            "event": "type(playwright)",
            "if_list": None,
            "use_mouse": False,
            "mandatory": True,
            "timeout": 10,
            "timeout_for_event": "presence_of_element_located",
            "locator_description": "Поле ввода для поиска"
        }
        
        # Выполнение ввода текста в поле
        await executor.execute_locator(locator)
        
        # Определение локатора для кнопки поиска
        locator = {
            "by": "XPATH",
            "selector": "//input[@name='btnK']",
            "attribute": None,
            "event": "click()",
            "if_list": "first",
            "use_mouse": False,
            "mandatory": True,
            "timeout": 10,
            "timeout_for_event": "presence_of_element_located",
            "locator_description": "Кнопка поиска"
        }

        # Выполнение клика на кнопку
        await executor.execute_locator(locator)

        # Небольшая пауза для отображения результатов
        await asyncio.sleep(2)

    finally:
        # 4. Остановка браузера
        await executor.stop()

if __name__ == "__main__":
    asyncio.run(main())