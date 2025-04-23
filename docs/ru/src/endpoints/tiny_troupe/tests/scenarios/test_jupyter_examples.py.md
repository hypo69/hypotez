# Модуль тестирования примеров Jupyter Notebook
## Обзор
Модуль `test_jupyter_examples.py` предназначен для автоматического тестирования Jupyter Notebook, расположенных в указанной директории (`../../examples/`). Он использует `pytest` для запуска тестов и проверяет, что ни один из Notebook не вызывает исключений во время выполнения.

## Подробнее
Этот модуль выполняет следующие действия:
1. **Находит Notebook**: Ищет все файлы с расширением `.ipynb` в заданной директории.
2. **Выполняет Notebook**: Запускает каждый найденный Notebook, используя ядро `python3`.
3. **Проверяет на ошибки**: Фиксирует все исключения, возникающие во время выполнения Notebook.
4. **Сохраняет результаты**: Сохраняет копию выполненного Notebook с добавлением `.executed.local.ipynb` к имени файла.

Этот модуль важен для проверки работоспособности примеров использования кода в формате Jupyter Notebook.

## Функции

### `get_notebooks`

```python
def get_notebooks(folder: str) -> list[str]:
    """
    Извлекает все файлы Jupyter notebook из указанной папки.

    Args:
        folder (str): Путь к папке, содержащей notebook.

    Returns:
        list[str]: Список путей ко всем файлам Jupyter notebook в папке.

    
        Функция проходит по всем файлам в указанной папке и возвращает список тех,
        которые заканчиваются на ".ipynb", но не содержат ".executed." или ".local." в имени.
    """
```

### `test_notebook_execution`

```python
@pytest.mark.parametrize("notebook_path", get_notebooks(NOTEBOOK_FOLDER))
def test_notebook_execution(notebook_path: str) -> None:
    """
    Выполняет Jupyter notebook и проверяет, что не возникает исключений.

    Args:
        notebook_path (str): Путь к файлу Jupyter notebook.

    
        Функция открывает notebook, выполняет его с помощью `ExecutePreprocessor`,
        и проверяет, не возникло ли исключений. Если исключение возникло, тест завершается неудачно.
        В любом случае сохраняется копия выполненного notebook.
    """
```

## Параметры

- `NOTEBOOK_FOLDER` (str): Путь к директории, содержащей примеры Jupyter Notebook. По умолчанию - `"../../examples/"`.
- `TIMEOUT` (int): Максимальное время выполнения notebook в секундах. По умолчанию - `600`.
- `KERNEL_NAME` (str): Имя ядра Jupyter, используемого для выполнения notebook. По умолчанию - `"python3"`.

## Пример
Запуск тестов для Jupyter Notebook:

```bash
pytest test_jupyter_examples.py