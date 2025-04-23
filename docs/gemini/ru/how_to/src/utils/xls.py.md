### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код предоставляет функции для конвертации файлов Excel (`.xls`) в формат JSON и наоборот. Он позволяет читать данные из Excel-файлов, преобразовывать их в JSON и сохранять JSON-данные обратно в Excel-файлы, обрабатывая при этом несколько листов.

Шаги выполнения
-------------------------
1. **Чтение Excel-файла и конвертация в JSON:**
   - Функция `read_xls_as_dict(xls_file: str, json_file: str = None, sheet_name: Union[str, int] = None) -> Union[Dict, List[Dict], bool]` читает Excel-файл.
   - Проверяет, существует ли указанный файл.
   - Если `sheet_name` не указан, читает все листы из Excel-файла, конвертирует каждый лист в словарь, где ключи - названия листов, а значения - списки словарей, представляющие строки.
   - Если `sheet_name` указан, читает только указанный лист.
   - При наличии `json_file` сохраняет полученные данные в JSON-файл.
   - Возвращает словарь с данными или `False` в случае ошибки.

2. **Сохранение JSON-данных в Excel-файл:**
   - Функция `save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool` сохраняет JSON-данные в Excel-файл.
   - Создает Excel-файл с использованием `pd.ExcelWriter`.
   - Для каждого листа (sheet_name) в переданных данных создает соответствующий лист в Excel-файле и записывает данные.
   - Возвращает `True` при успешном сохранении или `False` в случае ошибки.

Пример использования
-------------------------

```python
import pandas as pd
import json
from typing import List, Dict, Union
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_xls_as_dict(
    xls_file: str,
    json_file: str = None,
    sheet_name: Union[str, int] = None
) -> Union[Dict, List[Dict], bool]:
    """
    Читает Excel файл и конвертирует его в JSON. Опционально, конвертирует указанный лист и сохраняет результат в JSON файл.
    Обрабатывает ошибки.
    """
    try:
        xls_file_path = Path(xls_file)
        if not xls_file_path.exists():
            logging.error(f"Excel файл не найден: {xls_file}")
            return False  # Обозначает неудачу

        xls = pd.ExcelFile(xls_file)

        if sheet_name is None:
            data_dict = {}
            for sheet in xls.sheet_names:
                try:
                    df = pd.read_excel(xls, sheet_name=sheet)
                    data_dict[sheet] = df.to_dict(orient='records')
                except Exception as e:
                    logging.error(f"Ошибка при обработке листа '{sheet}': {e}")
                    return False

        else:
            try:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                data_dict = df.to_dict(orient='records')
            except Exception as e:
                logging.error(f"Ошибка при обработке листа '{sheet_name}': {e}")
                return False


        if json_file:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=4)
                logging.info(f"JSON данные сохранены в {json_file}")

        return data_dict

    except FileNotFoundError as e:
        logging.error(f"Файл не найден: {e}")
        return False
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        return False


def save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool:
    """Сохраняет JSON данные в Excel файл. Обрабатывает ошибки."""
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for sheet_name, rows in data.items():
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                logging.info(f"Лист '{sheet_name}' сохранен в {file_path}")
        return True
    except Exception as e:
        logging.error(f"Ошибка при сохранении Excel файла: {e}")
        return False

# Пример чтения Excel файла и сохранения в JSON
data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
if data:
    print(data)

# Пример сохранения JSON данных в Excel файл
data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = save_xls_file(data_to_save, 'output.xlsx')
if success:
    print("Успешно сохранено в output.xlsx")