# Модуль `src.utils.xls`

## Обзор

Модуль `src.utils.xls` предоставляет функциональность для конвертации файлов Excel (`.xls`) в формат JSON и обратно. Он позволяет читать данные из Excel файлов, преобразовывать их в JSON, а также сохранять JSON данные в Excel файлы. Модуль поддерживает работу с несколькими листами в Excel файле и обеспечивает обработку ошибок.

## Подробнее

Этот модуль предназначен для упрощения обмена данными между форматами Excel и JSON. Он использует библиотеку `pandas` для работы с Excel файлами и библиотеку `json` для работы с JSON данными. Модуль предоставляет две основные функции: `read_xls_as_dict` для чтения данных из Excel файла и `save_xls_file` для сохранения JSON данных в Excel файл.

## Функции

### `read_xls_as_dict`

```python
def read_xls_as_dict(
    xls_file: str,
    json_file: str = None,
    sheet_name: Union[str, int] = None
) -> Union[Dict, List[Dict], bool]:
    """
    Читает Excel файл и конвертирует его в JSON. Опционально конвертирует конкретный лист и сохраняет результат в JSON файл.
    Обрабатывает ошибки.

    Args:
        xls_file (str): Путь к Excel файлу.
        json_file (str, optional): Путь для сохранения JSON файла. По умолчанию `None`.
        sheet_name (Union[str, int], optional): Имя или индекс листа Excel для конвертации. Если `None`, конвертируются все листы. По умолчанию `None`.

    Returns:
        Union[Dict, List[Dict], bool]: Если `sheet_name` указан как `None`, возвращается словарь, где ключи - имена листов, а значения - списки словарей.
                                        Если `sheet_name` указан, возвращается список словарей.
                                        Возвращает `False` в случае ошибки.

    Raises:
        FileNotFoundError: Если Excel файл не найден.
        Exception: Если возникает ошибка при чтении или обработке Excel файла.

    Как работает функция:
    - Проверяет, существует ли указанный Excel файл. Если файл не существует, функция регистрирует ошибку и возвращает `False`.
    - Использует `pandas` для чтения Excel файла.
    - Если `sheet_name` не указан, функция читает все листы в Excel файле. Для каждого листа:
        - Читает данные с листа в DataFrame.
        - Преобразует DataFrame в список словарей, где каждый словарь представляет строку.
        - Сохраняет список словарей в словарь `data_dict`, где ключ - имя листа.
    - Если `sheet_name` указан, функция читает только указанный лист в Excel файле.
        - Читает данные с листа в DataFrame.
        - Преобразует DataFrame в список словарей, где каждый словарь представляет строку.
        - Возвращает список словарей.
    - Если указан `json_file`, функция сохраняет полученные данные в JSON файл.
    - В случае возникновения ошибок при чтении или обработке листов, функция регистрирует ошибку и возвращает `False`.

    Примеры:
        Чтение всех листов из Excel файла:
        ```python
        data = read_xls_as_dict('input.xlsx')
        if data:
            print(data)
        ```

        Чтение определенного листа из Excel файла и сохранение в JSON файл:
        ```python
        data = read_xls_as_dict('input.xlsx', 'output.json', 'Sheet1')
        if data:
            print(data)
        ```
    """
    try:
        xls_file_path:Path = Path(xls_file) #  создается объект Path для представления пути к файлу Excel
        if not xls_file_path.exists(): # выполняется проверка существования файла по указанному пути
            logging.error(f"Excel file not found: {xls_file}") # если файл не существует, в лог записывается сообщение об ошибке
            return False  # Indicate failure # функция возвращает False, указывая на неудачное выполнение

        xls:pd.ExcelFile = pd.ExcelFile(xls_file) #  создается объект ExcelFile для работы с Excel файлом

        if sheet_name is None: # проверяется, указано ли имя листа для чтения
            data_dict:dict = {} # инициализируется словарь для хранения данных из Excel файла
            for sheet in xls.sheet_names: # начинается перебор всех листов в Excel файле
                try:
                    df:pd.DataFrame = pd.read_excel(xls, sheet_name=sheet) #  выполняется чтение данных из текущего листа в DataFrame
                    data_dict[sheet]:list = df.to_dict(orient='records') # DataFrame преобразуется в словарь, где ключи - имена листов, а значения - списки записей (строк)
                except Exception as ex: # обрабатываются возможные исключения при чтении и обработке данных листа
                    logging.error(f"Error processing sheet '{sheet}': {ex}") # в лог записывается сообщение об ошибке с указанием имени листа и текста ошибки
                    return False # функция возвращает False, указывая на неудачное выполнение

        else:
            try:
                df:pd.DataFrame = pd.read_excel(xls, sheet_name=sheet_name) #  выполняется чтение данных из указанного листа в DataFrame
                data_dict:list = df.to_dict(orient='records') # DataFrame преобразуется в список словарей (записей)
            except Exception as ex: #  обрабатываются возможные исключения при чтении и обработке данных листа
                logging.error(f"Error processing sheet '{sheet_name}': {ex}") #  в лог записывается сообщение об ошибке с указанием имени листа и текста ошибки
                return False # функция возвращает False, указывая на неудачное выполнение


        if json_file: # проверяется, указан ли путь к файлу для сохранения данных в формате JSON
            with open(json_file, 'w', encoding='utf-8') as f: # открывается файл для записи данных в формате JSON
                json.dump(data_dict, f, ensure_ascii=False, indent=4) # данные из словаря data_dict записываются в файл в формате JSON с отступами для удобочитаемости
                logging.info(f"JSON data saved to {json_file}") # в лог записывается сообщение об успешном сохранении данных в JSON файл

        return data_dict # функция возвращает словарь с данными из Excel файла

    except FileNotFoundError as ex: # обрабатывается исключение, если файл не найден
        logging.error(f"File not found: {ex}") # в лог записывается сообщение об ошибке, указывающее, что файл не найден
        return False # функция возвращает False, указывая на неудачное выполнение
    except Exception as ex: # обрабатываются все остальные исключения, которые могут возникнуть в процессе выполнения функции
        logging.error(f"An error occurred: {ex}") #  в лог записывается сообщение об ошибке
        return False # функция возвращает False, указывая на неудачное выполнение

### `save_xls_file`

```python
def save_xls_file(data: Dict[str, List[Dict]], file_path: str) -> bool:
    """Сохраняет JSON данные в Excel файл. Обрабатывает ошибки."""
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for sheet_name, rows in data.items():
                df:pd.DataFrame = pd.DataFrame(rows) #  для каждого листа создается DataFrame из списка словарей
                df.to_excel(writer, sheet_name=sheet_name, index=False) # DataFrame записывается в Excel файл на соответствующий лист без индексов
                logging.info(f"Sheet '{sheet_name}' saved to {file_path}") # в лог записывается сообщение об успешном сохранении листа

        return True # функция возвращает True, указывая на успешное выполнение
    except Exception as ex: # обрабатываются возможные исключения при записи данных в Excel файл
        logging.error(f"Error saving Excel file: {ex}") # в лог записывается сообщение об ошибке с указанием текста ошибки
        return False # функция возвращает False, указывая на неудачное выполнение

    Args:
        data (Dict[str, List[Dict]]): Данные для сохранения, где ключи - имена листов, а значения - списки словарей.
        file_path (str): Путь для сохранения Excel файла.

    Returns:
        bool: `True`, если данные успешно сохранены, `False` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при создании или записи Excel файла.

    Как работает функция:
    - Открывает Excel файл для записи с использованием `pd.ExcelWriter` и движка `xlsxwriter`.
    - Перебирает все листы и соответствующие им данные в словаре `data`.
    - Для каждого листа создает DataFrame из списка словарей.
    - Записывает DataFrame в Excel файл на соответствующий лист без индексов.
    - В случае возникновения ошибок при создании или записи Excel файла, функция регистрирует ошибку и возвращает `False`.

    Примеры:
        Сохранение JSON данных в Excel файл:
        ```python
        data_to_save = {'Sheet1': [{'column1': 'value1', 'column2': 'value2'}]}
        success = save_xls_file(data_to_save, 'output.xlsx')
        if success:
            print("Successfully saved to output.xlsx")
        ```
    """
    try:
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer: #  открывается Excel файл для записи данных с использованием движка xlsxwriter
            for sheet_name, rows in data.items(): # начинается перебор всех листов и соответствующих им данных
                df:pd.DataFrame = pd.DataFrame(rows) #  для каждого листа создается DataFrame из списка словарей
                df.to_excel(writer, sheet_name=sheet_name, index=False) # DataFrame записывается в Excel файл на соответствующий лист без индексов
                logging.info(f"Sheet '{sheet_name}' saved to {file_path}") # в лог записывается сообщение об успешном сохранении листа
        return True # функция возвращает True, указывая на успешное выполнение
    except Exception as ex: # обрабатываются возможные исключения при записи данных в Excel файл
        logging.error(f"Error saving Excel file: {ex}") # в лог записывается сообщение об ошибке с указанием текста ошибки
        return False # функция возвращает False, указывая на неудачное выполнение