## \file /sandbox/davidka/build_hypotez_train_data_from_files.py
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для сбора датасета для обучения модели 
=====================================================


Пример использования:
```python
# Ваш словарь (пример структуры "instruction/input/output")
my_record = {
  "instruction": "Определи тональность следующего отзыва.",
  "input": "Обслуживание было отличным, но еда не понравилась.",
  "output": "смешанная"
}

# Другой словарь (пример структуры "prompt/completion")
my_other_record = {
    "prompt": "Переведи на французский: 'Добрый вечер'",
    "completion": "Bonsoir"
}

# Путь к файлу, куда будем записывать
output_file = 'my_finetuning_data.jsonl'

# Записываем первый словарь
append_dict_to_jsonl(my_record, output_file)

# Записываем второй словарь (он добавится на новую строку)
append_dict_to_jsonl(my_other_record, output_file)

print(f"Данные записаны в файл: {output_file}")

# --- Проверка содержимого файла (опционально) ---
try:
    with open(output_file, 'r', encoding='utf-8') as f:
        print("\nСодержимое файла:")
        print(f.read())
except FileNotFoundError:
    print(f"Файл {output_file} не найден.")
```
```rst
.. module:: sandbox.davidka.build_hypotez_train_data_from_files
```
"""
from pathlib import Path
from typing import Generator, Any, Dict, List, Optional, Union # Добавлены аннотации


import header 
from header import __root__ 
from src import gs
from src.utils.jjson import j_loads, j_dumps 
from src.utils.file import save_text_file
from src.utils.string.ai_string_utils import string_for_train 
from src.utils.printer import pprint as print
from src.logger import logger


class Config:
    # Используем импортированный __root__
    ENDPOINT: Path = __root__ / 'SANDBOX' / 'davidka'
    DIALOGS_DIR: Path = ENDPOINT / 'dialogs with gemini from Google AI studio'
    output_file: Path = ENDPOINT / 'code_train_data' / f'dialogs_{gs.now}.jsonl'

def yield_dialog_chunks() -> Generator[Any, None, None]:
    """
    Генератор, который находит JSON файлы в директории Config.DIALOGS_DIR,
    читает каждый файл по отдельности с помощью j_loads, 
    извлекает из него списки 'chunks' и выдает (yields) каждый 'chunk'.

    Returns:
        Generator[Any, None, None]: Генератор, выдающий элементы ('chunks'). 
                                     Тип 'chunk' предполагается Any, т.к. не указан.
    
    Yields:
        Any: Следующий 'chunk' из найденных файлов.
    """
    
    dialogs_dir: Path = Config.DIALOGS_DIR
    json_file_paths: Generator[Path, None, None] 
    found_files: bool = False
    file_path: Path
    loaded_data: Union[Dict, List, None] # j_loads возвращает dict или list, или {} (Falsy)
    items_to_process: List[Dict] 
    item_index: int
    item: Dict # Предполагаем, что элементы в items_to_process - словари
    chunked_prompt: Optional[Dict]
    chunks: Optional[List]
    chunk_index: int
    chunk: Any
    ex: Exception

    # 1. Проверка, существует ли директория
    if not dialogs_dir.is_dir():
        logger.error(f'Директория не найдена: {dialogs_dir}')
        return # Завершение генератора

    # 2. Получение итератора путей к JSON файлам
    json_file_paths = dialogs_dir.glob('*.json')
    
    # 3. Итерация по путям к файлам
    for file_path in json_file_paths:
        found_files = True 
        # logger.debug(f'Обработка файла: {file_path.name}') 

        # 4. Загрузка содержимого ОДНОГО файла с помощью j_loads
        loaded_data = j_loads(file_path) 

        # 5. Проверка результата загрузки (Falsy check)
        if not loaded_data:
            # j_loads должен был залогировать ошибку внутри себя.
            logger.warning(f'Пропуск файла из-за ошибки загрузки или пустого содержимого: {file_path.name}')
            continue # Переход к следующему файлу

        # 6. Нормализация данных к списку для единообразной обработки
        items_to_process = []
        if isinstance(loaded_data, dict):
            items_to_process.append(loaded_data)
        elif isinstance(loaded_data, list):
             # Фильтрация, чтобы убедиться, что обрабатываем только словари из списка
             original_length: int = len(loaded_data)
             items_to_process = [d for d in loaded_data if isinstance(d, dict)]
             if len(items_to_process) != original_length:
                 logger.warning(f'Некоторые элементы в списке файла {file_path.name} не являются словарями и были проигнорированы.')
        else:
            logger.warning(f'Неожиданный тип данных ({type(loaded_data)}) после j_loads для файла: {file_path.name}')
            continue # Переход к следующему файлу

        # 7. Итерация по элементам (диалогам?) из файла
        for item_index, item in enumerate(items_to_process):
            try:
                # Безопасное извлечение 'chunks'
                chunked_prompt = item.get('chunkedPrompt')
                if isinstance(chunked_prompt, dict):
                    chunks = chunked_prompt.get('chunks')
                    if isinstance(chunks, list):
                        # 8. Генерация каждого chunk
                        for chunk_index, chunk in enumerate(chunks):
                            yield chunk
                            
            except Exception as ex: 
                # Обработка ошибки с использованием переменной ex
                logger.error(f'Неожиданная ошибка при извлечении chunks из элемента {item_index} файла {file_path.name}', ex, exc_info=False) 

    # Логирование, если ни одного файла не было найдено
    if not found_files:
         logger.warning(f'В директории {dialogs_dir} не найдено *.json файлов.')


def append_dict_to_jsonl(data_dict, file_path: Path | str = '') -> bool:
  """
  Добавляет Python-словарь как новую строку в JSONL файл.

  Args:
    data_dict (dict): Словарь для записи.
    file_path (str): Путь к JSONL файлу.
  """
  file_path = file_path if file_path else Config.output_file
  return True is j_dumps(data_dict, file_path, ensure_ascii=False) 
 


if __name__ == "__main__":
    # Объявление переменных в начале блока
    chunk_count: int = 0
    all_chunks_received: List[Any] = []
    i: int
    chunk_item: Any
    ex: Exception
    tarin_dict:dict = {}


    try:
        # Итерация по генератору
        for i, chunk_item in enumerate(yield_dialog_chunks()):
            #logger.info(f'Получен Chunk {i+1}: {str(chunk_item)[:150]}...')
            if "role" in chunk_item and "text" in chunk_item:

                role_value = chunk_item["role"]
                text_value = chunk_item["text"]

                question:str = ''
                if role_value == "user":
                    chunk_item["text"] = string_for_train(text_value)
                    
                elif role_value == "model":
                    chunk_item["output"] = string_for_train(text_value)
                    tarin_dict.update({'text_input':chunk_item["text"],'output':chunk_item["output"]})

           
            all_chunks_received.append( chunk_item)
            chunk_count += 1
            if chunk_count >= 10: # Ограничение для отладки
               logger.info('Достигнуто ограничение вывода.')
               Config.output_file = Config.output_file.with_name(f'dialogs_{gs.now}.jsonl')
               j_dumps(tarin_dict, Config.ENDPOINT/'code_train_data'/f'train_from_ai_studio_{gs.now}.jsonl')
               chunk_count = 0
               ...

            ...

    except Exception as ex: # Обработка ошибки с использованием переменной ex
         logger.error('Произошла ошибка во время итерации по генератору', ex, exc_info=True) 
         ...

    logger.info('--- Генератор завершил работу ---')
    logger.info(f'Всего получено чанков: {chunk_count}')
    # logger.debug(f'Все полученные чанки: {all_chunks_received}') 
