# Модуль `src.utils.xls`

## Обзор

Модуль `src.utils.xls` предоставляет функциональность для конвертации файлов Excel (`.xls`) в формат JSON и обратно. Он предназначен для работы с данными, представленными в формате Excel, и обеспечивает удобный способ их преобразования для использования в других приложениях или системах. Модуль поддерживает чтение данных из Excel-файлов, включая обработку нескольких листов, и сохранение JSON-данных в Excel-файлы.

## Подробней

Модуль содержит две основные функции: `read_xls_as_dict` для чтения данных из Excel-файла и преобразования их в формат JSON, и `save_xls_file` для сохранения данных из JSON-формата в Excel-файл. Он использует библиотеку `pandas` для работы с Excel-файлами и библиотеку `json` для работы с JSON-форматом. Модуль также включает обработку ошибок и логирование для обеспечения надежной работы.

## Функции

### `read_xls_as_dict`

```python
def read_xls_as_dict(
    xls_file: str,
    json_file: str = None,
    sheet_name: Union[str, int] = None
) -> Union[Dict, List[Dict], bool]:
    """
    Читает Excel-файл и конвертирует его в JSON. Опционально, конвертирует указанный лист и сохраняет результат в JSON-файл.
    Обрабатывает ошибки.

    Args:
        xls_file (str): Путь к Excel-файлу.
        json_file (str, optional): Путь для сохранения JSON-файла. По умолчанию `None`.
        sheet_name (Union[str, int], optional): Имя или индекс листа Excel для конвертации. Если `None`, конвертируются все листы. По умолчанию `None`.

    Returns:
        Union[Dict, List[Dict], bool]: Если `sheet_name` указан как `None`, возвращает словарь, где ключи - имена листов, а значения - списки словарей, представляющих строки.
        Если `sheet_name` указан, возвращает список словарей, представляющих строки указанного листа.
        Возвращает `False` в случае ошибки.

    Raises:
        FileNotFoundError: Если Excel-файл не найден.
        Exception: Если возникает ошибка при обработке файла или листа.

    Как работает функция:
    - Функция принимает путь к Excel-файлу, опциональный путь для сохранения JSON-файла и опциональное имя листа для конвертации.
    - Проверяет существование Excel-файла по указанному пути. Если файл не найден, логирует ошибку и возвращает `False`.
    - Использует `pandas.ExcelFile` для открытия Excel-файла.
    - Если `sheet_name` не указан, итерируется по всем листам в Excel-файле.
    - Для каждого листа читает данные с помощью `pandas.read_excel` и преобразует их в список словарей, где каждый словарь представляет строку.
    - Если `sheet_name` указан, читает данные только из указанного листа и преобразует их в список словарей.
    - Если указан `json_file`, сохраняет полученные данные в JSON-файл с использованием `json.dump`.
    - В случае возникновения ошибок в процессе обработки, логирует ошибку и возвращает `False`.

    Примеры:
        >>> data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
        >>> if data:
        ...     print(data)  # Вывод: [{'column1': 'value1', 'column2': 'value2'}, ...]

        >>> data = read_xls_as_dict('input.xlsx')
        >>> if data:
        ...     print(data.keys())  # Вывод: dict_keys(['Sheet1', 'Sheet2', ...])
    """
    try:
        xls_file_path = Path(xls_file)
        if not xls_file_path.exists():
            logging.error(f"Excel file not found: {xls_file}")
            return False  # Indicate failure

        xls = pd.ExcelFile(xls_file)

        if sheet_name is None:
            data_dict = {}
            for sheet in xls.sheet_names:
                try:
                    df = pd.read_excel(xls, sheet_name=sheet)
                    data_dict[sheet] = df.to_dict(orient='records')
                except Exception as ex:
                    logging.error(f"Error processing sheet '{sheet}': {ex}")
                    return False

        else:
            try:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                data_dict = df.to_dict(orient='records')
            except Exception as ex:
                logging.error(f"Error processing sheet '{sheet_name}': {ex}")
                return False


        if json_file:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=4)
                logging.info(f"JSON data saved to {json_file}")

        return data_dict

    except FileNotFoundError as ex:
        logging.error(f"File not found: {ex}")
        return False
    except Exception as ex:
        logging.error(f"An error occurred: {ex}")
        return False

### `save_xls_file`

```python
def save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool:
    """Сохраняет JSON данные в Excel файл. Обрабатывает ошибки."""
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for sheet_name, rows in data.items():
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                logging.info(f"Sheet '{sheet_name}' saved to {file_path}")
        return True
    except Exception as ex:
        logging.error(f"Error saving Excel file: {ex}")
        return False
```

**Назначение**: Сохраняет JSON данные в Excel файл.

**Параметры**:
- `data` (Dict[str, List[Dict]]): Словарь, где ключи - имена листов, а значения - списки словарей, представляющих строки.
- `file_path` (str): Путь для сохранения Excel-файла.

**Возвращает**:
- `bool`: `True`, если данные успешно сохранены в Excel-файл, `False` в случае ошибки.

**Вызывает исключения**:
- `Exception`: Если возникает ошибка при сохранении файла.

**Как работает функция**:
- Функция принимает словарь с данными и путь для сохранения Excel-файла.
- Использует `pandas.ExcelWriter` для создания Excel-файла.
- Итерируется по листам в словаре данных.
- Для каждого листа создает `pandas.DataFrame` из списка словарей.
- Сохраняет DataFrame в Excel-файл с использованием `df.to_excel`.
- В случае возникновения ошибок в процессе сохранения, логирует ошибку и возвращает `False`.

**Примеры**:

```python
data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
success = save_xls_file(data_to_save, 'output.xlsx')
if success:
    print("Successfully saved to output.xlsx")