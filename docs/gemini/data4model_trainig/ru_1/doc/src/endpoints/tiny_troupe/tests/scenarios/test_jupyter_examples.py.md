# Документация для модуля `test_jupyter_examples.py`

## Обзор

Модуль `test_jupyter_examples.py` предназначен для автоматического тестирования Jupyter Notebook, расположенных в директории `examples` проекта `hypotez`. Он выполняет каждую тетрадь и проверяет, не возникает ли в процессе выполнения исключений. Если тесты примеров включены через `conftest.py`, то модуль также сохраняет копию выполненной тетради.

## Подробнее

Этот модуль использует библиотеки `nbformat` и `nbconvert` для работы с Jupyter Notebook. `nbformat` используется для чтения и записи файлов notebook, а `nbconvert` - для выполнения кода в notebook. `pytest` используется для организации и запуска тестов.

Модуль добавляет в `sys.path` директории `../../tinytroupe/`, `../../` и `..\` для корректного импорта пакетов из родительских директорий.

## Функции

### `get_notebooks`

```python
def get_notebooks(folder: str) -> list[str]:
    """
    Извлекает все файлы Jupyter notebook из указанной папки.

    Args:
        folder (str): Путь к папке, в которой расположены файлы notebook.

    Returns:
        list[str]: Список путей к файлам notebook, которые соответствуют критериям (имеют расширение ".ipynb" и не содержат ".executed." или ".local." в имени).

    Пример:
        >>> notebooks = get_notebooks("/path/to/notebooks")
        >>> print(notebooks)
        ['/path/to/notebooks/example.ipynb', '/path/to/notebooks/another_example.ipynb']
    """
    ...
```

**Назначение**: Функция `get_notebooks` получает список всех файлов Jupyter notebook (`.ipynb`) из указанной папки, исключая те, которые содержат в имени `.executed.` или `.local.`.

**Параметры**:
- `folder` (str): Путь к директории, в которой расположены файлы Jupyter notebook.

**Возвращает**:
- `list[str]`: Список полных путей к файлам Jupyter notebook, найденным в указанной директории и соответствующим критериям.

**Как работает функция**:
1. Функция использует `os.listdir(folder)` для получения списка всех файлов и поддиректорий в указанной папке.
2. Затем она фильтрует этот список, оставляя только те элементы, которые удовлетворяют следующим условиям:
   - Имеют расширение `.ipynb`.
   - Не содержат в имени подстроки `.executed.` или `.local.`.
3. Для каждого файла, прошедшего фильтрацию, функция формирует полный путь с помощью `os.path.join(folder, f)`.
4. Функция возвращает список полных путей к файлам notebook.

**Примеры**:

Предположим, что в папке `/path/to/notebooks` находятся следующие файлы:
- `example.ipynb`
- `example.executed.local.ipynb`
- `another_example.ipynb`
- `text_file.txt`

Вызов функции:
```python
notebooks = get_notebooks("/path/to/notebooks")
print(notebooks)
```

Вывод:
```
['/path/to/notebooks/example.ipynb', '/path/to/notebooks/another_example.ipynb']
```

### `test_notebook_execution`

```python
@pytest.mark.parametrize("notebook_path", get_notebooks(NOTEBOOK_FOLDER))
def test_notebook_execution(notebook_path: str) -> None:
    """
    Выполняет Jupyter notebook и проверяет, не возникает ли исключений.

    Args:
        notebook_path (str): Путь к файлу notebook.

    Returns:
        None

    Raises:
        pytest.fail: Если при выполнении notebook возникает исключение.

    Пример:
        >>> test_notebook_execution("/path/to/notebooks/example.ipynb")
    """
    ...
```

**Назначение**: Функция `test_notebook_execution` выполняет Jupyter notebook и проверяет, не возникает ли при этом каких-либо исключений. Если исключение возникает, тест завершается неудачей. Если выполнение тестов примеров включено через `conftest.test_examples`, функция также сохраняет копию выполненной тетради.

**Параметры**:
- `notebook_path` (str): Путь к файлу Jupyter notebook, который нужно выполнить.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция проверяет, включены ли тесты примеров через `conftest.test_examples`.
2. Если тесты примеров включены:
   - Открывает файл notebook в режиме чтения с кодировкой UTF-8.
   - Читает содержимое файла, используя `nbformat.read`, и преобразует его в объект notebook версии 4.
   - Создает экземпляр класса `ExecutePreprocessor` с заданным таймаутом (`TIMEOUT`) и названием ядра (`KERNEL_NAME`).
   - Пытается выполнить notebook, используя метод `ep.preprocess`. При этом передается сам объект notebook и словарь с метаданными, содержащий путь к папке с notebook.
   - Если в процессе выполнения возникает исключение, функция вызывает `pytest.fail` с сообщением об ошибке, содержащим путь к notebook и текст исключения.
   - В блоке `finally` (который выполняется всегда, независимо от того, возникло исключение или нет) функция формирует путь для сохранения выполненного notebook, заменяя `.ipynb` на `.executed.local.ipynb`.
   - Открывает файл для записи с кодировкой UTF-8 и сохраняет выполненный notebook, используя `nbformat.write`.
3. Если тесты примеров не включены, функция выводит сообщение о том, что выполнение notebook пропущено.

**Примеры**:

Предположим, что нужно выполнить notebook, расположенный по пути `/path/to/notebooks/example.ipynb`.

Вызов функции:
```python
test_notebook_execution("/path/to/notebooks/example.ipynb")
```

В зависимости от результата выполнения notebook, функция либо завершится успешно, либо вызовет `pytest.fail` в случае возникновения исключения. В любом случае, выполненная копия notebook будет сохранена по пути `/path/to/notebooks/example.executed.local.ipynb` (если `conftest.test_examples` имеет значение `True`).

## Параметры модуля

- `NOTEBOOK_FOLDER` (str): Путь к директории, содержащей примеры Jupyter Notebook для тестирования.
- `TIMEOUT` (int): Максимальное время выполнения одного notebook в секундах.
- `KERNEL_NAME` (str): Название ядра Jupyter, используемого для выполнения тестов.