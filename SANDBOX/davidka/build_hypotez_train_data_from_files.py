## \file /sandbox/davidka/build_hypotez_train_data_from_files.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора датасета для обучения модели 
=====================================================

```rst
.. module:: sandbox.davidka.build_hypotez_train_data_from_files
```
"""
from pathlib import Path
# Импорты из вашего проекта
import header # Предполагаем, что header и __root__ определены правильно
from header import __root__
# from src import gs # Закомментировано, т.к. не используется напрямую в генераторе
# from src.endpoints.hypo69.code_assistant import CodeAssistant # Закомментировано, т.к. не используется
# Импортируем вашу функцию j_loads и logger (если он используется в j_loads)
from src.utils.jjson import j_loads 
# Убедимся, что logger импортирован, если j_loads его использует для вывода ошибок
try:
    from src.logger.logger import logger
except ImportError:
    # Простой fallback, если logger не найден
    import logging
    logger = logging.getLogger(__name__)
    # Настройка базового логгирования, если ваш logger не настроен
    if not logger.hasHandlers():
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.warning("Модуль 'src.logger.logger' не найден или не настроен, используется стандартный logging.")


class Config:
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    # Определим путь к директории с JSON файлами более явно
    DIALOGS_DIR: Path = ENDPOINT / 'dialogs with gemini from Google AI studio'

def yield_dialog_chunks():
    """
    Генератор, который находит JSON файлы в директории Config.DIALOGS_DIR,
    читает каждый файл по отдельности с помощью j_loads, 
    извлекает из него списки 'chunks' и выдает (yields) каждый 'chunk'.
    """
    dialogs_dir = Config.DIALOGS_DIR

    # 1. Проверяем, существует ли директория
    if not dialogs_dir.is_dir():
        logger.error(f"Директория не найдена: {dialogs_dir}")
        return # Завершаем генератор, т.к. нечего читать

    # 2. Получаем итератор путей к JSON файлам в директории
    #    Использование glob напрямую как итератора экономит память, если файлов очень много
    json_file_paths = dialogs_dir.glob('*.json')
    
    found_files = False # Флаг для проверки, были ли найдены файлы

    # 3. Итерируемся по путям к файлам
    for file_path in json_file_paths:
        found_files = True # Отмечаем, что хотя бы один файл найден
        # logger.debug(f"Обработка файла: {file_path.name}") # Раскомментировать для детальной отладки

        # 4. Загружаем содержимое ОДНОГО файла с помощью вашей функции j_loads
        #    j_loads должен вернуть dict или list при успехе, или Falsy ({}) при ошибке.
        loaded_data = j_loads(file_path) 

        # 5. Проверяем результат загрузки (Falsy check - {} считается Falsy)
        if not loaded_data:
            # j_loads должен был залогировать ошибку внутри себя.
            logger.warning(f"Пропуск файла из-за ошибки загрузки или пустого содержимого: {file_path.name}")
            continue # Переходим к следующему файлу

        # 6. Обрабатываем успешно загруженные данные.
        #    Нормализуем данные к списку для единообразной обработки.
        items_to_process = []
        if isinstance(loaded_data, dict):
            # Если файл содержит один JSON-объект
            items_to_process.append(loaded_data)
        elif isinstance(loaded_data, list):
             # Если файл содержит JSON-массив объектов
             items_to_process = loaded_data
        else:
            # На случай, если j_loads вернет что-то неожиданное, но не Falsy
            logger.warning(f"Неожиданный тип данных ({type(loaded_data)}) после j_loads для файла: {file_path.name}")
            continue

        # 7. Итерируемся по элементам (диалогам?) из файла
        for item_index, item in enumerate(items_to_process):
            if isinstance(item, dict):
                try:
                    # Безопасно извлекаем 'chunks', используя .get() для вложенных словарей
                    chunked_prompt = item.get('chunkedPrompt')
                    if isinstance(chunked_prompt, dict):
                        chunks = chunked_prompt.get('chunks')
                        if isinstance(chunks, list):
                            # 8. Если 'chunks' найден и это список, генерируем каждый chunk
                            for chunk_index, chunk in enumerate(chunks):
                                yield chunk
                        # else: # Опционально: логировать, если 'chunks' не список
                        #     if 'chunks' in chunked_prompt:
                        #          logger.warning(f"Ключ 'chunks' в элементе {item_index} файла {file_path.name} не является списком.")
                    # else: # Опционально: логировать, если 'chunkedPrompt' не словарь
                    #     if 'chunkedPrompt' in item:
                    #          logger.warning(f"Ключ 'chunkedPrompt' в элементе {item_index} файла {file_path.name} не является словарем.")
                
                except Exception as e: 
                    # Ловим прочие ошибки при доступе к данным внутри элемента
                    logger.error(f"Неожиданная ошибка при извлечении chunks из элемента {item_index} файла {file_path.name}: {e}", exc_info=False) 
            else:
                # Если элемент в JSON-массиве не является словарем
                logger.warning(f"Элемент {item_index} в файле {file_path.name} не является словарем (тип: {type(item)}), пропускается.")

    # Логируем, если ни одного файла не было найдено (glob вернул пустой итератор)
    if not found_files:
         logger.warning(f"В директории {dialogs_dir} не найдено *.json файлов.")


# --- Пример использования генератора ---
# Этот блок обычно помещают в другое место программы, где реально нужны данные,
# или оставляют для тестирования модуля.
if __name__ == "__main__":
    # --- Предварительные проверки и настройка (для возможности запуска скрипта) ---
    # Убедитесь, что __root__ инициализирован правильно 
    if '__root__' not in globals() or not isinstance(__root__, Path):
         logger.error("Переменная __root__ не определена или имеет неверный тип. Невозможно определить Config.")
         # Попытка определить __root__ для локального запуска (может не совпадать с вашей структурой)
         try:
             current_file_path = Path(__file__).resolve()
             # Пример: если скрипт лежит в /sandbox/davidka/, а __root__ это корень проекта
             __root__ = current_file_path.parent.parent.parent 
             logger.info(f"Установлено предполагаемое значение __root__: {__root__}")
             # Переопределяем Config с новым __root__
             class Config:
                 ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
                 DIALOGS_DIR: Path = ENDPOINT / 'dialogs with gemini from Google AI studio'
         except Exception as e:
             logger.exception(f"Не удалось автоматически определить __root__. Задайте его вручную или запустите из корректного окружения. Ошибка: {e}")
             exit(1) # Выход, если __root__ не установлен

    # --- Запуск генератора и вывод результатов ---
    logger.info(f"--- Запуск генератора yield_dialog_chunks из {Config.DIALOGS_DIR} ---")
    chunk_count = 0
    all_chunks_received = []
    try:
        # Итерируемся по генератору
        for i, chunk_item in enumerate(yield_dialog_chunks()):
            # Здесь вы можете обрабатывать каждый chunk_item
            # Например, печатать его или передавать в другую функцию
            logger.info(f"Получен Chunk {i+1}: {str(chunk_item)[:150]}...") # Печатаем начало чанка
            all_chunks_received.append(chunk_item)
            chunk_count += 1
            # Можно добавить условие для остановки при отладке
            # if chunk_count >= 10:
            #    logger.info("Достигнуто ограничение вывода в 10 чанков.")
            #    break 

    except Exception as e:
         logger.exception(f"Произошла ошибка во время итерации по генератору: {e}")

    logger.info(f"--- Генератор завершил работу ---")
    logger.info(f"Всего получено чанков: {chunk_count}")
    # logger.debug(f"Все полученные чанки: {all_chunks_received}") # Раскомментировать для полного списка чанков

    # Исходный вызов yeld_dialogs() здесь не нужен и был некорректен для генератора
    # yeld_dialogs() 
