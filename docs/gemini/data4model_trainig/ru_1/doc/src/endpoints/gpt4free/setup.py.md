# Модуль setup.py

## Обзор

Модуль `setup.py` используется для сборки, распространения и установки пакета `g4f` (gpt4free). Он определяет метаданные пакета, зависимости и точки входа.

## Подробней

Этот файл является стандартным скриптом установки Python, используемым `setuptools`. Он определяет различные аспекты пакета, такие как имя, версия, автор, описание, зависимости и другие метаданные. Этот файл позволяет упаковать код в распространяемый формат, который можно установить с помощью `pip`.

## Функции

### `setup`

```python
setup(
    name='g4f',
    version=os.environ.get("G4F_VERSION"),
    author='Tekky',
    author_email='<support@g4f.ai>',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    package_data={
        'g4f': ['g4f/interference/*', 'g4f/gui/client/*', 'g4f/gui/server/*', 'g4f/Provider/npm/*', 'g4f/local/models/*']
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    entry_points={
        'console_scripts': ['g4f=g4f.cli:main'],
    },
    url='https://github.com/xtekky/gpt4free',  # Link to your GitHub repository
    project_urls={
        'Source Code': 'https://github.com/xtekky/gpt4free',  # GitHub link
        'Bug Tracker': 'https://github.com/xtekky/gpt4free/issues',  # Link to issue tracker
    },
    keywords=[
        'python',
        'chatbot',
        'reverse-engineering',
        'openai',
        'chatbots',
        'gpt',
        'language-model',
        'gpt-3',
        'gpt3',
        'openai-api',
        'gpt-4',
        'gpt4',
        'chatgpt',
        'chatgpt-api',
        'openai-chatgpt',
        'chatgpt-free',
        'chatgpt-4',
        'chatgpt4',
        'chatgpt4-api',
        'free',
        'free-gpt',
        'gpt4free',
        'g4f',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
)
```

**Назначение**: Функция `setup` из `setuptools` используется для настройки процесса установки пакета.

**Параметры**:

-   `name` (str): Имя пакета (`g4f`).
-   `version` (str): Версия пакета, полученная из переменной окружения `G4F_VERSION`.
-   `author` (str): Автор пакета (`Tekky`).
-   `author_email` (str): Электронный адрес автора (`<support@g4f.ai>`).
-   `description` (str): Краткое описание пакета (`DESCRIPTION`).
-   `long_description` (str): Развернутое описание пакета, взятое из файла `README.md`.
-   `long_description_content_type` (str): Тип контента для `long_description` (`text/markdown`).
-   `packages` (list): Список пакетов, которые будут включены в дистрибутив, найденные с помощью `find_packages()`.
-   `package_data` (dict): Дополнительные файлы, которые будут включены в пакет.
-   `include_package_data` (bool): Если `True`, включает все файлы, соответствующие правилам `package_data`.
-   `install_requires` (list): Список зависимостей, необходимых для установки пакета.
-   `extras_require` (dict): Дополнительные группы зависимостей.
-   `entry_points` (dict): Определяет точки входа для консольных скриптов.
-   `url` (str): URL репозитория GitHub.
-   `project_urls` (dict): Словарь URL-ов проекта, таких как репозиторий и трекер ошибок.
-   `keywords` (list): Список ключевых слов, связанных с пакетом.
-   `classifiers` (list): Список классификаторов, описывающих пакет.

**Возвращает**:

-   `None`

**Вызывает исключения**:

-   `OSError`: Если не удается открыть и прочитать файл `README.md`.

**Как работает функция**:

1.  Определяет метаданные пакета, такие как имя, версию, автора и описание.
2.  Загружает развернутое описание из файла `README.md` и выполняет замены в тексте.
3.  Находит все пакеты в текущей директории с помощью `find_packages()`.
4.  Указывает дополнительные файлы, которые должны быть включены в пакет, в `package_data`.
5.  Определяет зависимости, необходимые для установки пакета, в `install_requires` и `extras_require`.
6.  Определяет точку входа для консольного скрипта `g4f`, который запускает функцию `main` из модуля `g4f.cli`.
7.  Указывает URL-ы проекта, такие как репозиторий и трекер ошибок.
8.  Указывает ключевые слова, связанные с пакетом.
9.  Указывает классификаторы, описывающие пакет.

**Примеры**:

```python
setup(
    name='g4f',
    version='1.0.0',
    author='Tekky',
    author_email='<support@g4f.ai>',
    description='The official gpt4free repository',
    long_description='Проект для бесплатного использования GPT',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests', 'aiohttp'],
    entry_points={
        'console_scripts': ['g4f=g4f.cli:main'],
    },
    url='https://github.com/xtekky/gpt4free',
)
```

## Переменные

-   `here` (str): Абсолютный путь к директории, в которой находится файл `setup.py`.
-   `long_description` (str): Содержимое файла `README.md`, используемое в качестве длинного описания пакета.
-   `INSTALL_REQUIRE` (list): Список основных зависимостей пакета.
-   `EXTRA_REQUIRE` (dict): Словарь дополнительных зависимостей пакета, разделенных по категориям.
-   `DESCRIPTION` (str): Краткое описание пакета.

## Файлы

-   `README.md`: Файл с развернутым описанием пакета в формате Markdown.