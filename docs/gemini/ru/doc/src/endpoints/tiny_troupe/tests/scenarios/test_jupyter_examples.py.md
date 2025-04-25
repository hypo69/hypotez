# Модуль для тестирования примеров Jupyter Notebook
## Обзор
Этот модуль содержит набор тестов для проверки корректности работы примеров Jupyter Notebook, представленных в папке `examples`. 
Он проверяет, что каждый ноутбук может быть успешно запущен без возникновения ошибок. 
## Подробней
Модуль использует библиотеку `nbformat` для чтения и записи ноутбуков, `nbconvert` для выполнения кода в ноутбуках и `pytest` для запуска тестов. 
Он определяет папку с примерами ноутбуков `NOTEBOOK_FOLDER` и задает таймаут для долго выполняющихся ноутбуков `TIMEOUT`. 
## Классы
### `class None`
**Описание**: В этом модуле нет классов.
## Функции
### `get_notebooks`
**Назначение**: Эта функция извлекает список всех файлов Jupyter Notebook из указанной папки. 
**Параметры**:
- `folder` (str): Путь к папке, в которой находятся ноутбуки. 
**Возвращает**:
- list: Список путей к файлам Jupyter Notebook.
**Как работает функция**:
- Функция перебирает все файлы в указанной папке и выбирает только файлы с расширением `.ipynb`, которые не содержат ".executed." и ".local." в имени. 
- Затем функция формирует полный путь к каждому файлу Jupyter Notebook и возвращает список этих путей. 
**Примеры**:
```python
>>> get_notebooks("examples") # Возвращает список путей к файлам Jupyter Notebook в папке "examples"
['examples/example1.ipynb', 'examples/example2.ipynb']
```
### `test_notebook_execution`
**Назначение**: Эта функция запускает Jupyter Notebook и проверяет, что он не вызывает исключений.
**Параметры**:
- `notebook_path` (str): Путь к файлу Jupyter Notebook.
**Возвращает**:
- None
**Вызывает исключения**:
- `pytest.fail`: Если во время выполнения ноутбука возникает исключение.
**Как работает функция**:
- Функция открывает файл Jupyter Notebook и читает его содержимое с помощью `nbformat.read`. 
- Затем функция запускает код в ноутбуке с помощью `ExecutePreprocessor`, задавая таймаут и имя ядра.
- Если во время выполнения ноутбука возникает исключение, функция вызывает `pytest.fail`, чтобы провалить тест.
- Если ноутбук завершается успешно, функция сохраняет копию выполненного ноутбука с расширением ".executed.local.ipynb" в ту же папку.
**Примеры**:
```python
>>> test_notebook_execution("examples/example1.ipynb") # Выполняет Jupyter Notebook "example1.ipynb" и проверяет, что он не вызывает исключений
```
## Параметры
- `NOTEBOOK_FOLDER` (str): Путь к папке, в которой находятся ноутбуки. 
- `TIMEOUT` (int): Таймаут для долго выполняющихся ноутбуков.
- `KERNEL_NAME` (str): Имя ядра, которое будет использоваться для выполнения ноутбуков.
**Примеры**:
```python
>>> NOTEBOOK_FOLDER = "examples" # Задает папку с примерами ноутбуков
>>> TIMEOUT = 600 # Задает таймаут для долго выполняющихся ноутбуков
>>> KERNEL_NAME = "python3" # Задает имя ядра, которое будет использоваться для выполнения ноутбуков
```
## Примеры
```python
>>> import os
>>> import nbformat
>>> from nbconvert.preprocessors import ExecutePreprocessor
>>> import pytest
>>> 
>>> import sys
>>> sys.path.insert(0, '../../tinytroupe/') # ensures that the package is imported from the parent directory, not the Python installation
>>> sys.path.insert(0, '../../') # ensures that the package is imported from the parent directory, not the Python installation
>>> sys.path.insert(0, '..') # ensures that the package is imported from the parent directory, not the Python installation
>>> 
>>> import conftest
>>> 
>>> # Set the folder containing the notebooks
>>> NOTEBOOK_FOLDER = os.path.join(os.path.dirname(__file__), "../../examples/")  # Update this path
>>> 
>>> # Set a timeout for long-running notebooks
>>> TIMEOUT = 600
>>> 
>>> KERNEL_NAME = "python3" #"py310"
>>> 
>>> 
>>> def get_notebooks(folder):
...     """Retrieve all Jupyter notebook files from the specified folder."""
...     return [
...         os.path.join(folder, f)
...         for f in os.listdir(folder)
...         if f.endswith(".ipynb") and not ".executed." in f and not ".local." in f
...     ]
>>> 
>>> @pytest.mark.parametrize("notebook_path", get_notebooks(NOTEBOOK_FOLDER))
>>> def test_notebook_execution(notebook_path):
...     """Execute a Jupyter notebook and assert that no exceptions occur."""
... 
...     if conftest.test_examples:
...         with open(notebook_path, "r", encoding="utf-8") as nb_file:
...             notebook = nbformat.read(nb_file, as_version=4)
...             print(f"Executing notebook: {notebook_path} with kernel: {KERNEL_NAME}")
...             ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=KERNEL_NAME)
... 
...             try:
...                 ep.preprocess(notebook, {'metadata': {'path': NOTEBOOK_FOLDER}})
...                 print(f"Notebook {notebook_path} executed successfully.")
... 
...             except Exception as e:
...                 pytest.fail(f"Notebook {notebook_path} raised an exception: {e}")
...             
...             finally:
...                 # save a copy of the executed notebook
...                 output_path = notebook_path.replace(".ipynb", ".executed.local.ipynb")
...                 with open(output_path, "w", encoding="utf-8") as out_file:
...                     nbformat.write(notebook, out_file)
...                 
...                 print(f"Executed notebook saved as: {output_path}")
...     else:
...         print(f"Skipping notebooks executions for {notebook_path}.")
... 
...