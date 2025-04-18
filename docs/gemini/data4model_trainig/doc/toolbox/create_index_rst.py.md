# Модуль для создания index.rst

## Обзор

Этот модуль предназначен для автоматического создания файла `index.rst` в директории `docs`, который используется для генерации документации Sphinx. Модуль рекурсивно обходит указанную директорию, находит все Python-файлы и добавляет их в `index.rst` в формате `toctree`.

## Подробнее

Модуль выполняет следующие действия:

1. Рекурсивно обходит все поддиректории, начиная с указанной.
2. Ищет все файлы с расширением `.py`.
3. Создает файл `index.rst` в директории `docs`.
4. Записывает в `index.rst` директиву `toctree`, которая указывает Sphinx на необходимость включения найденных Python-файлов в документацию.
5. Логирует процесс создания `index.rst` и добавления файлов.

## Функции

### `create_index_rst`

```python
def create_index_rst(start_dir: str) -> None:
    """Рекурсивно обходит все поддиректории, начиная с указанной, считывает все *.py файлы
    и создает файл index.rst в директории `docs`, в котором перечислены все эти файлы в формате toctree.
    Логирует процесс в течение всего времени.

    Args:
        start_dir (str): Корневая директория, с которой начинается обход.

    Returns:
        None

    Example:
        >>> create_index_rst(os.getcwd())
    """
    ...
```

**Назначение**:
Функция `create_index_rst` предназначена для автоматического создания файла `index.rst`, используемого Sphinx для построения документации проекта.

**Параметры**:
- `start_dir` (str): Путь к корневой директории, с которой начинается обход файловой системы.

**Возвращает**:
- `None`: Функция ничего не возвращает.

**Как работает функция**:
1.  Функция принимает путь к начальной директории (`start_dir`).
2.  Определяет путь к директории `docs` и файлу `index.rst`.
3.  Создает директорию `docs`, если она не существует.
4.  Открывает файл `index.rst` для записи.
5.  Записывает в файл директивы `toctree`, необходимые для Sphinx.
6.  Рекурсивно обходит все поддиректории, начиная с `start_dir`.
7.  Для каждой поддиректории находит все файлы с расширением `.py`.
8.  Для каждого найденного Python-файла формирует относительный путь и добавляет его в файл `index.rst`.
9.  Логирует информацию о процессе создания `index.rst` и добавления файлов.
10. В случае возникновения ошибок логирует информацию об ошибке и прекращает выполнение.

**Примеры**:

```python
create_index_rst(os.getcwd())
```

## Запуск

```python
if __name__ == "__main__":
    create_index_rst(Path(header.__root__, 'src'))
```

При запуске этого скрипта будет вызвана функция `create_index_rst`, которая создаст файл `index.rst` в директории `docs`, содержащий список всех Python-файлов, найденных в директории `src` и ее поддиректориях.