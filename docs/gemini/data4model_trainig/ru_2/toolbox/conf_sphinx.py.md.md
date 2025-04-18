# Модуль конфигурации Sphinx

## Обзор

Этот модуль предназначен для настройки генерации документации Sphinx для проекта `hypotez`. Он загружает параметры проекта из файла `settings.json`, устанавливает тему оформления, исключает ненужные файлы и папки из сборки документации и подключает обработчик для фильтрации членов документации.

## Подробнее

Модуль выполняет следующие задачи:

1.  Загружает основные параметры проекта (название, авторские права, автора, версию релиза) из файла `settings.json`. Если файл не найден или содержит ошибки, используются значения по умолчанию.
2.  Определяет расширения Sphinx, используемые для генерации документации, такие как `sphinx.ext.autodoc` для автоматического создания документации из docstring'ов.
3.  Указывает пути к шаблонам и статическим файлам, а также определяет файлы и папки, которые следует исключить из процесса сборки документации.
4.  Настраивает тему оформления документации.
5.  Добавляет путь к исходному коду проекта, чтобы Sphinx мог найти и использовать docstring'и для автоматической генерации документации.
6.  Определяет функцию `skip_files` для фильтрации членов документации на основе их имени. Это позволяет исключить из документации элементы, которые не должны быть включены (например, члены, имена которых содержат определенные шаблоны).
7.  Подключает функцию `skip_files` к событию `autodoc-skip-member`, чтобы она вызывалась при обработке каждого члена документации.

## Переменные модуля

-   `project` (str): Название проекта.
-   `copyright` (str): Информация об авторских правах.
-   `author` (str): Автор проекта.
-   `release` (str): Версия релиза проекта.
-   `extensions` (list): Список расширений Sphinx, используемых для генерации документации.
-   `templates_path` (list): Список путей к директориям с шаблонами.
-   `exclude_patterns` (list): Список шаблонов файлов и папок, которые следует исключить из сборки документации.
-   `available_themes` (dict): Словарь доступных тем оформления документации.
-   `html_theme` (str): Выбранная тема оформления документации.
-   `html_static_path` (list): Список путей к директориям со статическими файлами.

## Функции

### `skip_files`

```python
def skip_files(app, what, name, obj, skip, options):\n    """\n    Функция-обработчик события \'autodoc-skip-member\'.\n    Используется для игнорирования членов документации, соответствующих определённым шаблонам.\n\n    Args:\n        app: Объект приложения Sphinx\n        what: Тип документации (например, \'module\', \'class\', \'exception\', \'function\', \'method\', \'attribute\')\n        name: Имя члена документации\n        obj: Объект члена документации\n        skip: Логическое значение, указывающее, следует ли пропустить этот член по умолчанию\n        options: Опции автодокументации\n\n    Returns:\n        bool: True, если член должен быть пропущен; иначе возвращает значение `skip`\n    """
    ...
```

**Назначение**: Определяет, следует ли пропускать определенный член документации при автоматической генерации.

**Параметры**:

*   `app`: Объект приложения Sphinx.
*   `what` (str): Тип документации (например, `'module'`, `'class'`, `'exception'`, `'function'`, `'method'`, `'attribute'`).
*   `name` (str): Имя члена документации.
*   `obj` (object): Объект члена документации.
*   `skip` (bool): Логическое значение, указывающее, следует ли пропустить этот член по умолчанию.
*   `options` (dict): Опции автодокументации.

**Возвращает**:

*   `bool`: `True`, если член должен быть пропущен; иначе возвращает значение `skip`.

**Как работает функция**:

Функция проверяет, содержит ли имя члена круглые скобки или соответствует ли оно другим заданным шаблонам. Если имя соответствует одному из шаблонов, функция возвращает `True`, указывая Sphinx пропустить этот член документации. В противном случае функция возвращает исходное значение `skip`, позволяя Sphinx принять решение о пропуске члена на основе других правил.

**Примеры**:

```python
# Пример использования функции skip_files в Sphinx:
# В conf.py:
# def setup(app):
#     app.connect('autodoc-skip-member', skip_files)

# Это приведет к тому, что функция skip_files будет вызываться для каждого члена документации,
# и члены, имена которых соответствуют заданным шаблонам, будут исключены из документации.
```

### `setup`

```python
def setup(app):\n    """\n    Функция настройки, которая подключает функцию `skip_files` к событию `autodoc-skip-member`.\n\n    Args:\n        app: Объект приложения Sphinx\n    """
    ...
```

**Назначение**: Подключает функцию `skip_files` к событию `autodoc-skip-member` в Sphinx.

**Параметры**:

*   `app`: Объект приложения Sphinx.

**Как работает функция**:

Функция использует метод `connect` объекта приложения Sphinx для подключения функции `skip_files` к событию `autodoc-skip-member`. Это означает, что функция `skip_files` будет вызываться каждый раз, когда Sphinx обрабатывает член документации и решает, следует ли его пропустить.

**Примеры**:

```python
# Пример использования функции setup в Sphinx:
# В conf.py:
# def setup(app):
#     app.connect('autodoc-skip-member', skip_files)

# Это приведет к тому, что функция skip_files будет вызываться для каждого члена документации,
# и члены, имена которых соответствуют заданным шаблонам, будут исключены из документации.