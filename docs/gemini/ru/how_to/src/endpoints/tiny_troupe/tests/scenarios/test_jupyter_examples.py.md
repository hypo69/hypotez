### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для автоматического тестирования Jupyter Notebooks. Он выполняет каждый notebook, расположенный в указанной директории, и проверяет, что в процессе выполнения не возникает исключений. После выполнения notebook сохраняется его копия с отметкой о выполнении.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `os`, `nbformat`, `ExecutePreprocessor` и `pytest`.
2. **Настройка путей**:
   - `sys.path.insert(0, '../../tinytroupe/')` и другие аналогичные строки добавляют директории в `sys.path`, чтобы обеспечить импорт пакетов из родительских директорий.
   - `NOTEBOOK_FOLDER` устанавливается в путь к директории с примерами Jupyter Notebooks.
3. **Определение функции `get_notebooks(folder)`**: Эта функция извлекает список всех файлов Jupyter Notebook (`.ipynb`) из указанной директории, исключая файлы, содержащие в имени `.executed.` или `.local.`.
4. **Параметризация тестов**:
   - `@pytest.mark.parametrize("notebook_path", get_notebooks(NOTEBOOK_FOLDER))` используется для параметризации тестов, чтобы каждый notebook из списка, возвращенного `get_notebooks`, был протестирован отдельно.
5. **Функция `test_notebook_execution(notebook_path)`**:
   - Проверяет, включены ли тесты примеров (`if conftest.test_examples:`).
   - Открывает notebook, используя `nbformat.read()`.
   - Инициализирует `ExecutePreprocessor` с заданным таймаутом и именем ядра.
   - Выполняет notebook, используя `ep.preprocess()`.
   - В случае возникновения исключения во время выполнения теста, тест завершается с ошибкой.
   - Сохраняет выполненную копию notebook с добавлением `.executed.local.` в имя файла.
   - Выводит сообщение о сохранении выполненного notebook.
   - Если тесты примеров не включены, выводится сообщение о пропуске выполнения notebook.

Пример использования
-------------------------

```python
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pytest

import sys
sys.path.insert(0, '../../tinytroupe/')
sys.path.insert(0, '../../')
sys.path.insert(0, '..')

import conftest

# Директория, содержащая notebooks
NOTEBOOK_FOLDER = os.path.join(os.path.dirname(__file__), "../../examples/")

# Таймаут для выполнения notebooks
TIMEOUT = 600

KERNEL_NAME = "python3"

def get_notebooks(folder):
    """Функция извлекает Jupyter notebooks из указанной директории."""
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".ipynb") and not ".executed." in f and not ".local." in f
    ]

@pytest.mark.parametrize("notebook_path", get_notebooks(NOTEBOOK_FOLDER))
def test_notebook_execution(notebook_path):
    """Функция выполняет Jupyter notebook и проверяет отсутствие исключений."""

    if conftest.test_examples:
        with open(notebook_path, "r", encoding="utf-8") as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)
            print(f"Выполняется notebook: {notebook_path} с ядром: {KERNEL_NAME}")
            ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=KERNEL_NAME)

            try:
                ep.preprocess(notebook, {'metadata': {'path': NOTEBOOK_FOLDER}})
                print(f"Notebook {notebook_path} успешно выполнен.")

            except Exception as e:
                pytest.fail(f"Notebook {notebook_path} вызвал исключение: {e}")
            
            finally:
                # сохранение копии выполненного notebook
                output_path = notebook_path.replace(".ipynb", ".executed.local.ipynb")
                with open(output_path, "w", encoding="utf-8") as out_file:
                    nbformat.write(notebook, out_file)
                
                print(f"Выполненный notebook сохранен как: {output_path}")
    else:
        print(f"Пропуск выполнения notebooks для {notebook_path}.")