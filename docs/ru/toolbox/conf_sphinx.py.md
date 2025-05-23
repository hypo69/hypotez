# Документация для модуля `conf.py`

## Обзор

Модуль `conf.py` используется для конфигурации генерации документации Sphinx для проекта `hypotez`. Он определяет настройки проекта, такие как имя, авторские права, версия релиза, а также указывает на используемые расширения Sphinx, пути к шаблонам и статическим файлам. Кроме того, модуль содержит функции для фильтрации файлов, которые следует исключить из документации.

## Подробней

Этот модуль является центральным местом для настройки процесса генерации документации с использованием Sphinx. Он загружает основные параметры проекта из файла `settings.json` и определяет различные параметры, такие как пути к шаблонам и темам оформления документации. Также, модуль предоставляет функцию `skip_files` для исключения определенных файлов или элементов из документации на основе заданных критериев. Функция `setup` подключает функцию `skip_files` к событию `autodoc-skip-member` в Sphinx.

## Переменные модуля

- `project` (str): Название проекта.
- `copyright` (str): Информация об авторских правах.
- `author` (str): Автор проекта.
- `release` (str): Версия релиза проекта.
- `extensions` (list): Список расширений Sphinx, используемых для генерации документации.
- `templates_path` (list): Список путей к каталогам с шаблонами Sphinx.
- `exclude_patterns` (list): Список шаблонов файлов и каталогов, которые следует исключить из процесса генерации документации.
- `available_themes` (dict): Словарь доступных тем оформления Sphinx.
- `default_theme` (str): Тема оформления, используемая по умолчанию.
- `html_static_path` (list): Список путей к каталогам со статическими файлами, такими как CSS и изображения.

## Функции

### `skip_files`

```python
def skip_files(app, what, name, obj, skip, options):
    """
    Функция-обработчик события 'autodoc-skip-member'.
    Используется для игнорирования членов документации, соответствующих определённым шаблонам.

    Args:
        app: Объект приложения Sphinx
        what: Тип документации (например, 'module', 'class', 'exception', 'function', 'method', 'attribute')
        name: Имя члена документации
        obj: Объект члена документации
        skip: Логическое значение, указывающее, следует ли пропустить этот член по умолчанию
        options: Опции автодокументации

    Returns:
        bool: True, если член должен быть пропущен; иначе возвращает значение `skip`
    """
```

**Назначение**: Определяет, следует ли исключить определенный элемент (например, функцию или класс) из сгенерированной документации Sphinx.

**Параметры**:
- `app`: Объект приложения Sphinx.
- `what` (str): Тип элемента документации (например, `'module'`, `'class'`, `'exception'`, `'function'`, `'method'`, `'attribute'`).
- `name` (str): Имя элемента документации.
- `obj`: Объект элемента документации.
- `skip` (bool): Значение, указывающее, следует ли пропустить элемент по умолчанию.
- `options` (dict): Опции автодокументации.

**Возвращает**:
- `bool`: `True`, если элемент следует пропустить; в противном случае возвращает значение `skip`.

**Как работает функция**:
Функция проверяет, соответствует ли имя элемента определенным шаблонам, например, содержит ли имя круглые скобки или соответствует другим заданным шаблонам. Если соответствие обнаружено, функция возвращает `True`, указывая Sphinx исключить этот элемент из документации. В противном случае возвращается исходное значение `skip`, позволяя Sphinx принять решение о включении или исключении элемента.

**Примеры**:
```python
# Пример использования (внутри Sphinx):
# В конфигурационном файле conf.py:

def skip_files(app, what, name, obj, skip, options):
    if name == 'some_private_function':
        return True
    return skip

# В данном случае, функция 'some_private_function' будет исключена из документации.
```

### `setup`

```python
def setup(app):
    """
    Функция настройки, которая подключает функцию `skip_files` к событию `autodoc-skip-member`.

    Args:
        app: Объект приложения Sphinx
    """
```

**Назначение**: Подключает функцию `skip_files` к событию `autodoc-skip-member` в Sphinx.

**Параметры**:
- `app`: Объект приложения Sphinx.

**Как работает функция**:
Функция использует метод `connect` объекта приложения Sphinx для подключения функции `skip_files` к событию `autodoc-skip-member`. Это позволяет функции `skip_files` быть вызванной каждый раз, когда Sphinx решает, следует ли пропустить определенный элемент документации.

**Примеры**:
```python
# Пример использования (внутри Sphinx):
# В конфигурационном файле conf.py:

def setup(app):
    app.connect('autodoc-skip-member', skip_files)

# В данном случае, функция skip_files будет вызвана для каждого элемента документации,
# и она сможет определить, следует ли его пропустить.
```

## Дополнительные переменные

- `_project_name` (str):  Название проекта, извлеченное из файла `settings.json`.
- `_copyright` (str):  Информация об авторских правах, извлеченная из файла `settings.json`.
- `_release` (str):  Версия релиза проекта, извлеченная из файла `settings.json`.
- `_author` (str):  Автор проекта, извлеченный из файла `settings.json`.

## Как работает модуль

1.  **Загрузка конфигурации**: В начале модуля происходит загрузка основных параметров проекта из файла `../src/settings.json`. Если файл не найден или содержит ошибки JSON, используются значения по умолчанию.
2.  **Определение переменных**: На основе загруженных данных и значений по умолчанию определяются основные переменные, такие как название проекта, авторские права, автор и версия релиза.
3.  **Настройка Sphinx**: Определяются основные параметры Sphinx, такие как используемые расширения, пути к шаблонам и статическим файлам, а также шаблоны исключений.
4.  **Функция `skip_files`**: Эта функция определяет, какие файлы следует исключить из документации на основе заданных критериев.
5.  **Функция `setup`**: Эта функция подключает функцию `skip_files` к событию `autodoc-skip-member` в Sphinx, активируя механизм исключения файлов из документации.

## Примеры

Пример конфигурации `settings.json`:

```json
{
  "project_name": "hypotez",
  "copyright": "2024, hypo69",
  "release": "1.0.0",
  "author": "hypo69"
}
```

Пример использования в `conf.py`:

```python
# conf.py
import os
import sys
import fnmatch

sys.path.insert(0, os.path.abspath('..'))

project = 'hypotez'
copyright = '2024, hypo69'
author = 'hypo69'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
]

def skip_files(app, what, name, obj, skip, options):
    if fnmatch.fnmatch(name, '*test*'):
        return True
    return skip

def setup(app):
    app.connect('autodoc-skip-member', skip_files)
```
В этом примере все файлы, содержащие в имени `test`, будут исключены из сгенерированной документации.