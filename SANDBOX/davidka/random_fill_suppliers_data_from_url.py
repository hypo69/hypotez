## \file /sandbox/davidka/random_fill_suppliers_data_from_url.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для обхода существующих файлов JSON поставщиков, поиска записей
с пустым полем 'text' и заполнения его HTML-содержимым, полученным
с соответствующего URL с помощью веб-драйвера.
=====================================================================
Скрипт итерирует по файлам в `Config.data_by_supplier_dir`. Для каждого
файла он находит *первый* ключ (URL), у которого значение поля 'text'
является пустым. Затем он использует `driver.fetch_html` для получения
HTML этого URL и обновляет поле 'text' в файле. Обрабатывается только
одна запись на файл за один запуск скрипта для этой записи.

```rst
 .. module:: sandbox.davidka.random_fill_suppliers_data_from_url
```
"""

from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import threading

# Стандартные импорты проекта
import header
from header import __root__
# from src import gs # Не используется в этом модуле
from src.utils.jjson import j_loads, j_dumps
from src.utils.file import recursively_yield_file_path
from src.logger import logger

# --- Импорты WebDriver ---
from src.webdriver.driver import Driver
from src.webdriver.firefox import Firefox
# -------------------------
from SANDBOX.davidka.graber import extract_page_data

class Config:
    """Класс конфигурации скрипта."""
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    # Директория с файлами поставщиков (результат работы crawl_suppliers...)
    data_by_supplier_dir: Path = Path("F:/llm/data_by_supplier")
    # Убедимся, что директория существует
    data_by_supplier_dir.mkdir(parents=True, exist_ok=True)
    # Настройка для драйвера
    HEADLESS_MODE: bool = True # Пример: используется в __main__


# --- Механизм блокировки файлов ---
_locks: Dict[Path, threading.Lock] = {}
_lock_guard = threading.Lock()

def _get_lock(file_path: Path) -> threading.Lock:
    """
    Возвращает или создает объект блокировки для указанного пути файла.

    Args:
        file_path (Path): Путь к файлу.

    Returns:
        threading.Lock: Объект блокировки для данного файла.
    """
    with _lock_guard:
        if file_path not in _locks:
            _locks[file_path] = threading.Lock()
        return _locks[file_path]
# ----------------------------------


# ==============================================================================
# Функция обработки одного файла поставщика для заполнения поля 'text'
# ==============================================================================
def process_supplier_file_for_text(
    supplier_file_path: Path,
    driver: Driver
) -> bool:
    """
    Обрабатывает один файл JSON поставщика: находит первую запись с пустым
    полем 'text', получает HTML для соответствующего URL и обновляет поле 'text'.

    Args:
        supplier_file_path (Path): Путь к файлу JSON поставщика.
        driver (Driver): Инстанс веб-драйвера для получения HTML.

    Returns:
        bool: True, если файл был успешно прочитан, обновлен и записан,
              False в случае любой ошибки или если не найдено записей для обновления.
    """
    # Объявление переменных
    file_lock: threading.Lock = _get_lock(supplier_file_path)
    loaded_data: Optional[Dict[str, Any]] = None
    url_key_to_update: Optional[str] = None
    value_to_process: Optional[Dict[str, Any]] = None # Словарь для ключа с пустым текстом
    current_text: Any = None
    html_content: Optional[str] = None
    modified: bool = False
    write_success: bool = False
    # Переменные для цикла
    url_key: str
    value: Any

    logger.debug(f"Начало обработки файла: {supplier_file_path}")

    with file_lock: # Захват блокировки для файла
        # 1. Чтение файла
        try:
            loaded_data:dict = j_loads(supplier_file_path)
            if not loaded_data:
                logger.warning(f"Функция j_loads не вернула данные или файл пуст: {supplier_file_path}. Пропуск.")
                return False # Не удалось прочитать
            if not isinstance(loaded_data, dict):
                 logger.error(f"Ожидался словарь, но j_loads вернул {type(loaded_data)} из {supplier_file_path}. Пропуск.")
                 return False
        except Exception as ex:
            logger.error(f"Непредвиденная ошибка при загрузке {supplier_file_path}: {ex}", ex, exc_info=True)
            return False # Ошибка чтения

        # 2. Поиск первой записи с пустым 'text'
        url_key_to_update = None
        value_to_process = None # Сброс перед циклом
        for url_key, value in loaded_data.items():
            # Проверяем, что значение является словарем
            if isinstance(value, dict):
                # Сохраняем ссылку на словарь значения, если он найден
                current_value_dict = value
                current_text = current_value_dict.get('text') # Безопасно получаем значение text
                # Проверяем, что текст "пустой" (None, "", или строка из пробелов)
                if current_text is None or not str(current_text).strip():
                    url_key_to_update = url_key
                    value_to_process = current_value_dict # Сохраняем ссылку на найденный словарь
                    logger.info(f"Найдена запись для обновления 'text' в {supplier_file_path}: URL='{url_key_to_update}'")
                    break # Нашли первую, выходим из цикла по ключам
            else:
                logger.warning(f"Значение для ключа '{url_key}' в файле {supplier_file_path} не является словарем ({type(value)}). Пропускаем проверку 'text'.")
                continue # Переходим к следующему ключу

        # Если не нашли ключ для обновления, выходим
        if not url_key_to_update or value_to_process is None:
            logger.info(f"В файле {supplier_file_path} не найдено записей с пустым полем 'text'. Обновление не требуется.")
            return False # Ничего не обновлено

        # 3. Вызвать функцию driver.fetch_html(url)
        html_content = None # Сброс перед вызовом
        logger.debug(f"Запрос HTML для URL: {url_key_to_update}")
        try:
            # Вызов метода драйвера для получения HTML
            html_content = driver.fetch_html(url_key_to_update)
            # Проверка результата fetch_html
            if not html_content:
                 logger.error(f"Метод driver.fetch_html не вернул контент для URL '{url_key_to_update}'. Поле 'text' не будет обновлено.")
                 return False # HTML не получен
        except Exception as ex:
            logger.error(f"Исключение при вызове driver.fetch_html для URL '{url_key_to_update}': {ex}", ex, exc_info=True)
            # Решаем не обновлять файл, если получение HTML вызвало исключение
            return False

        # 4. Результат поместить в поле 'text'
        value_to_process:dict = extract_page_data(html_content, url_key_to_update) # Извлекаем данные из HTML)
        if isinstance(value_to_process, dict):
            value_to_process['text'] = html_content # Обновляем поле 'text' в найденном словаре
            modified = True
            logger.info(f"Поле 'text' для URL '{url_key_to_update}' в {supplier_file_path} будет обновлено полученным HTML.")
        else:
             # Эта ситуация маловероятна, если код выше корректен
             logger.error(f"Критическая ошибка: value_to_process для ключа '{url_key_to_update}' не является словарем перед обновлением поля 'text'.")
             return False

        # 5. Записать измененные данные обратно в файл
        if modified:
            logger.debug(f"Попытка записи обновленных данных в {supplier_file_path}...")
            write_success = False # Сброс перед записью
            try:
                # Используем порядок: <что>, <куда>
                write_success = j_dumps(loaded_data, supplier_file_path)
                if write_success:
                    logger.info(f"Файл {supplier_file_path} успешно обновлен.")
                    return True # Успешное обновление
                else:
                     # j_dumps должен был залогировать ошибку
                     logger.error(f"Функция j_dumps сообщила об ошибке при записи файла {supplier_file_path}")
                     return False # Ошибка записи
            except Exception as ex:
                logger.error(f"Непредвиденная ошибка при записи {supplier_file_path}: {ex}", ex, exc_info=True)
                return False # Ошибка записи
        else:
             # Сюда не должны попасть, если html_content не был None
             logger.debug("Изменений для записи не было (HTML не получен?).")
             return False # Файл не был обновлен

    # Блокировка освобождается здесь
    return False # Если вышли из 'with' без успешного return True


# ==============================================================================
# Основной блок выполнения скрипта
# ==============================================================================
if __name__ == '__main__':
    # --- Объявление переменных ---
    driver_instance: Optional[Driver] = None # Инициализируем как None для finally
    processed_files_count: int = 0
    updated_files_count: int = 0
    error_files_count: int = 0 # Счетчик для ошибок во время цикла
    total_files_scanned: int = 0
    supplier_file: Path
    update_result: bool = False
    # -----------------------------

    logger.info(f"--- Начало работы скрипта {Path(__file__).name} ---")
    logger.info(f"Поиск файлов поставщиков в: {Config.data_by_supplier_dir}")

    # --- Инициализация драйвера ---
    try:
        logger.info(f"Инициализация драйвера типа: {Firefox.__name__}")
        # Используем класс браузера и передаем режим из Config
        driver_instance = Driver(Firefox, headless=Config.HEADLESS_MODE)
        logger.info("Драйвер успешно инициализирован.")

        logger.info("Начало обхода файлов поставщиков...")
        # Итерация по файлам JSON в директории поставщиков
        for supplier_file in recursively_yield_file_path(Config.data_by_supplier_dir, '*.json'):
            total_files_scanned += 1
            try:
                # Вызов функции обработки для каждого файла
                update_result = process_supplier_file_for_text(supplier_file, driver_instance)
                if update_result:
                    updated_files_count += 1
                # Не считаем как ошибку файла, если он просто не требовал обновления
                processed_files_count +=1 # Считаем каждый файл, до которого дошла обработка

            except Exception as loop_ex:
                # Ловим ошибки, возникшие при обработке *одного* файла, чтобы продолжить цикл
                logger.error(f"Ошибка при обработке файла {supplier_file}: {loop_ex}", exc_info=True)
                error_files_count += 1
                continue # Переходим к следующему файлу

    except Exception as ex:
        # Ловим критические ошибки (например, инициализация драйвера, ошибка в recursively_yield_file_path)
        logger.critical(f"Критическая ошибка во время выполнения: {ex}", exc_info=True)
        # Статистика может быть неполной в этом случае
    finally:
        # Гарантированное закрытие драйвера
        if driver_instance: # Проверяем, был ли драйвер успешно создан
            logger.info("Завершение работы драйвера...")
            try:
                driver_instance.quit()
            except Exception as ex:
                logger.error(f"Ошибка при закрытии драйвера: {ex}", ex, exc_info=True)

    logger.info(f"--- Обработка файлов завершена ---")
    logger.info(f"Статистика:")
    logger.info(f" - Всего просканировано файлов: {total_files_scanned}")
    logger.info(f" - Файлов обработано (попытка чтения/поиска): {processed_files_count}")
    logger.info(f" - Файлов успешно обновлено (найдена запись и записан HTML): {updated_files_count}")
    logger.info(f" - Ошибок при обработке отдельных файлов (в цикле): {error_files_count}")
    logger.info(f"--- Работа скрипта {Path(__file__).name} завершена ---")

