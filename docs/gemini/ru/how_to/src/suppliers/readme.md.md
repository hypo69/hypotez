## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот набор модулей предназначен для автоматизации взаимодействия с веб-браузерами (в первую очередь, Firefox) с использованием Selenium WebDriver и для сбора (парсинга/граббинга) структурированных данных со страниц товаров на сайтах поставщиков.

Шаги выполнения
-------------------------
1. **Инициализация WebDriver:**
    - Импортируйте необходимые классы из модулей `src.webdriver`.
    - Создайте экземпляр `Firefox` с конфигурацией из `firefox.json` (или переопределите параметры, например, `window_mode`).
    - Получите экземпляр `driver`, содержащий стандартные методы Selenium и дополнительные утилиты.
2. **Взаимодействие с веб-страницами:**
    - Используйте методы `driver` для перехода по URL (`get_url`), прокрутки (`scroll`), ожидания (`wait`), получения HTML (`fetch_html`) и т.д.
3. **Взаимодействие с элементами (`ExecuteLocator`):**
    - Создайте локатор (словарь или `SimpleNamespace`) с описанием элемента (селектор, стратегия поиска, действие, таймаут, атрибут).
    - Используйте `driver.execute_locator` (асинхронный метод) для поиска элемента и выполнения действия (клик, ввод текста, получение атрибута, скриншот и т.д.).
4. **Сбор данных (`Graber`):**
    - Получите экземпляр `Graber` (класс-наследник для конкретного поставщика) с помощью `get_graber_by_supplier_prefix` или `get_graber_by_supplier_url`.
    - Вызовите `grab_page_async` для сбора данных с текущей страницы товара, указав нужные поля.
    - Дополнительно можно воспользоваться `process_supplier_scenarios_async` для автоматического сбора данных по сценариям поставщика (из директории `scenarios/`).
5. **Логирование:**
    - Используйте логгер (`src/logger/logger.py`) для отслеживания процесса работы, предупреждений и ошибок.
6. **Закрытие WebDriver:**
    - После завершения работы вызовите `driver.quit()` для освобождения ресурсов.

Пример использования
-------------------------

```python
import asyncio
from src.webdriver.firefox import Firefox
from src.logger.logger import logger
from src.suppliers.get_graber_by_supplier import get_graber_by_supplier_prefix
from src.suppliers.graber import ProductFields

# 1. Инициализация WebDriver
try:
    driver = Firefox(window_mode="kiosk")
    logger.info("Драйвер Firefox успешно запущен.")
except Exception as e:
    logger.critical(f"Не удалось инициализировать драйвер Firefox: {e}")
    exit()

# 4. Использование Системы Сбора Данных
supplier = "ksp"
lang_id = 2

# Получаем экземпляр грабера для KSP
graber = get_graber_by_supplier_prefix(driver, supplier, lang_index=lang_id)

if graber:
    logger.info(f"Грабер для \'{supplier}\' получен.")

    async def run_supplier_processing():
        # Запускаем обработку всех сценариев из папки scenarios/ для ksp
        results = await graber.process_supplier_scenarios_async(supplier_prefix=supplier, id_lang=lang_id)
        if results:
            logger.info(f"Обработка сценариев для \'{supplier}\' завершена. Собрано {len(results)} товаров.")
        else:
            logger.error(f"Ошибка при обработке сценариев для \'{supplier}\'.")

    # Запуск
    asyncio.run(run_supplier_processing())

else:
    logger.error(f"Не удалось получить грабер для поставщика \'{supplier}\'.")

# Закрытие WebDriver
driver.quit()
```