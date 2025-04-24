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
import header # Импортируем модуль header
from header import __root__ # Импортируем __root__ из header
# from src import gs # Закомментировано, т.к. не используется напрямую в генераторе
# from src.endpoints.hypo69.code_assistant import CodeAssistant # Закомментировано, т.к. не используется
# Импортируем вашу функцию j_loads
from src.utils.jjson import j_loads 
from src.logger import logger


class Config:
    # Используем импортированный __root__
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
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
        return # Завершаем генератор

    # 2. Получаем итератор путей к JSON файлам
    json_file_paths = dialogs_dir.glob('*.json')
    
    found_files = False # Флаг для проверки, были ли найдены файлы

    # 3. Итерируемся по путям к файлам
    for file_path in json_file_paths:
        found_files = True 
        # logger.debug(f"Обработка файла: {file_path.name}") 

        # 4. Загружаем содержимое ОДНОГО файла с помощью j_loads
        loaded_data = j_loads(file_path) 

        # 5. Проверяем результат загрузки (Falsy check)
        if not loaded_data:
            # j_loads должен был залогировать ошибку внутри себя.
            logger.warning(f"Пропуск файла из-за ошибки загрузки или пустого содержимого: {file_path.name}")
            continue 

        # 6. Нормализуем данные к списку для единообразной обработки
        items_to_process = []
        if isinstance(loaded_data, dict):
            items_to_process.append(loaded_data)
        elif isinstance(loaded_data, list):
             items_to_process = loaded_data
        else:
            logger.warning(f"Неожиданный тип данных ({type(loaded_data)}) после j_loads для файла: {file_path.name}")
            continue

        # 7. Итерируемся по элементам (диалогам?) из файла
        for item_index, item in enumerate(items_to_process):
            if isinstance(item, dict):
                try:
                    # Безопасно извлекаем 'chunks'
                    chunked_prompt = item.get('chunkedPrompt')
                    if isinstance(chunked_prompt, dict):
                        chunks = chunked_prompt.get('chunks')
                        if isinstance(chunks, list):
                            # 8. Генерируем каждый chunk
                            for chunk_index, chunk in enumerate(chunks):
                                yield chunk
                                
                except Exception as e: 
                    logger.error(f"Неожиданная ошибка при извлечении chunks из элемента {item_index} файла {file_path.name}: {e}", exc_info=False) 
            else:
                logger.warning(f"Элемент {item_index} в файле {file_path.name} не является словарем (тип: {type(item)}), пропускается.")

    # Логируем, если ни одного файла не было найдено
    if not found_files:
         logger.warning(f"В директории {dialogs_dir} не найдено *.json файлов.")


# --- Пример использования генератора ---
# Этот блок выполняется, только если скрипт запускается напрямую.
if __name__ == "__main__":
    
    # Проверяем, что Config.DIALOGS_DIR существует перед запуском
    if not Config.DIALOGS_DIR.exists():
         logger.error(f"Директория для диалогов не существует: {Config.DIALOGS_DIR}")
         logger.error("Пожалуйста, убедитесь, что путь в Config правильный и директория создана.")
         exit(1) # Выход, если директория не существует

    logger.info(f"--- Запуск генератора yield_dialog_chunks из {Config.DIALOGS_DIR} ---")
    chunk_count = 0
    all_chunks_received = []
    try:
        # Итерируемся по генератору
        for i, chunk_item in enumerate(yield_dialog_chunks()):
            logger.info(f"Получен Chunk {i+1}: {str(chunk_item)[:150]}...") 
            all_chunks_received.append(chunk_item)
            chunk_count += 1
            # if chunk_count >= 10: # Ограничение для отладки
            #    logger.info("Достигнуто ограничение вывода.")
            #    break 

    except Exception as e:
         logger.exception(f"Произошла ошибка во время итерации по генератору: {e}")

    logger.info(f"--- Генератор завершил работу ---")
    logger.info(f"Всего получено чанков: {chunk_count}")
    # logger.debug(f"Все полученные чанки: {all_chunks_received}") 
