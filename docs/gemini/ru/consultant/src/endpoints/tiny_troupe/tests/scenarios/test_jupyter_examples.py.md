### **Анализ кода модуля `test_jupyter_examples.py`**

## \file /hypotez/src/endpoints/tiny_troupe/tests/scenarios/test_jupyter_examples.py

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
  - Использование `pytest.mark.parametrize` для параметризации тестов.
  - Четкое разделение на функции для получения списка ноутбуков и выполнения тестов.
  - Обработка исключений при выполнении ноутбуков.
  - Сохранение выполненной версии ноутбука.
- **Минусы**:
  - Отсутствие аннотаций типов.
  - Пути в `sys.path.insert` заданы строками, что может быть менее надежным.
  - Отсутствие логирования.
  - Некоторые комментарии неинформативны.

**Рекомендации по улучшению:**

1.  **Добавить аннотации типов:**

    - Добавить аннотации типов для всех переменных и возвращаемых значений функций. Это улучшит читаемость и облегчит отладку.
2.  **Использовать `Path` для путей:**

    - Вместо `os.path.join` и строковых путей использовать `pathlib.Path` для большей гибкости и надежности.
3.  **Логирование:**

    - Добавить логирование для более информативного вывода.
4.  **Улучшить комментарии и добавить docstring:**

    - Добавить docstring к функциям и классам.
    - Сделать комментарии более конкретными.
5.  **Обработка ошибок:**

    - Использовать `logger.error` для логирования ошибок.
    - Использовать `ex` вместо `e` в блоках `except`.
6.  **Удалить избыточные `sys.path.insert`:**

    - Оставить только необходимые `sys.path.insert`.

**Оптимизированный код:**

```python
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pytest
import sys
from typing import List
from pathlib import Path

# Путь к модулю logger
from src.logger import logger

# Убеждаемся, что пакет импортируется из родительской директории, а не из установки Python
sys.path.insert(0, '../../tinytroupe/')
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

import conftest


# Устанавливаем папку, содержащую ноутбуки
NOTEBOOK_FOLDER: Path = Path(os.path.dirname(__file__)) / "../../examples/"

# Устанавливаем таймаут для долго выполняющихся ноутбуков
TIMEOUT: int = 600

KERNEL_NAME: str = "python3"


def get_notebooks(folder: Path) -> List[Path]:
    """
    Получает все Jupyter notebook файлы из указанной папки.

    Args:
        folder (Path): Путь к папке.

    Returns:
        List[Path]: Список путей к notebook файлам.
    
    Example:
        >>> folder = Path('./examples')
        >>> notebooks = get_notebooks(folder)
        >>> print(notebooks)
        [PosixPath('examples/notebook1.ipynb'), PosixPath('examples/notebook2.ipynb')]
    """
    notebooks: List[Path] = [
        Path(os.path.join(folder, f))
        for f in os.listdir(folder)
        if f.endswith(".ipynb") and not ".executed." in f and not ".local." in f
    ]
    return notebooks


@pytest.mark.parametrize("notebook_path", get_notebooks(NOTEBOOK_FOLDER))
def test_notebook_execution(notebook_path: Path) -> None:
    """
    Выполняет Jupyter notebook и проверяет, что не возникает исключений.

    Args:
        notebook_path (Path): Путь к notebook файлу.

    Raises:
        pytest.fail: Если notebook вызывает исключение.

    Example:
        >>> test_notebook_execution(Path('./examples/notebook1.ipynb'))
        Executing notebook: ./examples/notebook1.ipynb with kernel: python3
        Notebook ./examples/notebook1.ipynb executed successfully.
        Executed notebook saved as: ./examples/notebook1.executed.local.ipynb
    """
    if conftest.test_examples:
        try:
            with open(notebook_path, "r", encoding="utf-8") as nb_file:
                notebook = nbformat.read(nb_file, as_version=4)
                logger.info(f"Executing notebook: {notebook_path} with kernel: {KERNEL_NAME}")
                ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=KERNEL_NAME)

                ep.preprocess(notebook, {'metadata': {'path': str(NOTEBOOK_FOLDER)}})
                logger.info(f"Notebook {notebook_path} executed successfully.")

        except Exception as ex:
            logger.error(f"Notebook {notebook_path} raised an exception: {ex}", ex, exc_info=True)
            pytest.fail(f"Notebook {notebook_path} raised an exception: {ex}")

        finally:
            # сохраняем копию выполненного notebook
            output_path: str = str(notebook_path).replace(".ipynb", ".executed.local.ipynb")
            try:
                with open(output_path, "w", encoding="utf-8") as out_file:
                    nbformat.write(notebook, out_file)
                logger.info(f"Executed notebook saved as: {output_path}")
            except Exception as ex:
                logger.error(f"Error saving executed notebook: {ex}", ex, exc_info=True)

    else:
        logger.info(f"Skipping notebooks executions for {notebook_path}.")