# Module `setup.py`

## Обзор

Этот модуль используется для настройки и установки пакета `g4f` (gpt4free). Он определяет зависимости, дополнительные компоненты и другие метаданные, необходимые для установки и распространения пакета.

## Подробнее

Модуль `setup.py` является стандартным файлом для пакетов Python, использующих `setuptools`. Он содержит информацию о пакете, такую как имя, версия, автор, описание, зависимости и точки входа. Этот файл позволяет пользователям легко устанавливать пакет с помощью `pip`.

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

**Описание**: Функция `setup` из библиотеки `setuptools` используется для настройки процесса установки пакета.

**Параметры**:
- `name` (str): Имя пакета (`g4f`).
- `version` (str): Версия пакета, извлекается из переменной окружения `G4F_VERSION`.
- `author` (str): Автор пакета (`Tekky`).
- `author_email` (str): Электронный адрес автора (`<support@g4f.ai>`).
- `description` (str): Краткое описание пакета.
- `long_description_content_type` (str): Тип контента для длинного описания (`text/markdown`).
- `long_description` (str): Длинное описание пакета, извлеченное из файла `README.md`.
- `packages` (list): Список пакетов, которые необходимо включить, определяется с помощью `find_packages()`.
- `package_data` (dict): Дополнительные файлы, которые необходимо включить в пакет.
- `include_package_data` (bool): Если `True`, включает файлы, указанные в `package_data`.
- `install_requires` (list): Список зависимостей, необходимых для установки пакета.
- `extras_require` (dict): Словарь с дополнительными группами зависимостей.
- `entry_points` (dict): Определяет точки входа для консольных скриптов.
- `url` (str): URL репозитория GitHub.
- `project_urls` (dict): Словарь с URL для различных разделов проекта, таких как исходный код и отслеживание ошибок.
- `keywords` (list): Список ключевых слов, связанных с пакетом.
- `classifiers` (list): Список классификаторов, описывающих различные аспекты пакета.

**Как работает функция**:

1. **Чтение метаданных**:
   - Извлекает имя, версию, автора и описание пакета.
   - Читает длинное описание из файла `README.md` и заменяет ссылки на изображения и документацию.
2. **Определение зависимостей**:
   - Указывает обязательные зависимости в списке `INSTALL_REQUIRE`.
   - Определяет дополнительные зависимости в словаре `EXTRA_REQUIRE`, разделенные по категориям.
3. **Настройка пакета**:
   - Использует функцию `find_packages()` для автоматического обнаружения всех пакетов в проекте.
   - Включает дополнительные файлы, такие как шаблоны и статические ресурсы, с помощью параметра `package_data`.
4. **Определение точек входа**:
   - Указывает точку входа для консольного скрипта `g4f` в параметре `entry_points`.
5. **Указание URL и ключевых слов**:
   - Предоставляет URL репозитория и другие ссылки на проект.
   - Определяет ключевые слова для облегчения поиска пакета.
6. **Классификация пакета**:
   - Указывает классификаторы для описания статуса разработки, целевой аудитории, языка программирования и операционных систем.

## Параметры

### `INSTALL_REQUIRE`

```python
INSTALL_REQUIRE = [
    "requests",
    "aiohttp",
    "brotli",
    "pycryptodome",
    "nest_asyncio",
]
```

Список обязательных зависимостей для установки пакета `g4f`.

### `EXTRA_REQUIRE`

```python
EXTRA_REQUIRE = {
    'all': [
        "curl_cffi>=0.6.2",
        "certifi",
        "browser_cookie3",         # get_cookies
        "duckduckgo-search>=5.0",  # internet.search
        "beautifulsoup4",          # internet.search and bing.create_images
        "platformdirs",
        "aiohttp_socks",           # proxy
        "pillow",                  # image
        "cairosvg",                # svg image
        "werkzeug", "flask",       # gui
        "fastapi",                 # api
        "uvicorn",                 # api
        "nodriver",
        "python-multipart",
        "pywebview",
        "plyer",
        "setuptools",
        "pypdf2", # files
        "python-docx",
        "odfpy",
        "ebooklib",
        "openpyxl",
    ],
    'slim': [
        "curl_cffi>=0.6.2",
        "certifi",
        "browser_cookie3",
        "duckduckgo-search>=5.0"  ,# internet.search
        "beautifulsoup4",          # internet.search and bing.create_images
        "aiohttp_socks",           # proxy
        "pillow",                  # image
        "werkzeug", "flask",       # gui
        "fastapi",                 # api
        "uvicorn",                 # api
        "python-multipart",
        "pypdf2", # files
        "python-docx",
    ],
    "image": [
        "pillow",
        "cairosvg",
        "beautifulsoup4"
    ],
    "webview": [
        "pywebview",
        "platformdirs",
        "plyer",
        "cryptography",
    ],
    "api": [
        "loguru", "fastapi",
        "uvicorn",
        "python-multipart",
    ],
    "gui": [
        "werkzeug", "flask",
        "beautifulsoup4", "pillow",
        "duckduckgo-search>=5.0",
    ],
    "search": [
        "beautifulsoup4",
        "pillow",
        "duckduckgo-search>=5.0",
    ],
    "local": [
        "gpt4all"
    ],
    "files": [
        "spacy",
        "beautifulsoup4",
        "pypdf2",
        "python-docx",
        "odfpy",
        "ebooklib",
        "openpyxl",
    ]
}
```

Словарь с группами дополнительных зависимостей. Например, группа `'all'` включает все зависимости, необходимые для полной функциональности, а группа `'slim'` включает только основные зависимости.

### `DESCRIPTION`

```python
DESCRIPTION = (
    'The official gpt4free repository | various collection of powerful language models'
)
```

Краткое описание пакета.

## Примеры

### Установка пакета с обязательными зависимостями

```bash
pip install g4f
```

### Установка пакета со всеми дополнительными зависимостями

```bash
pip install g4f[all]
```

### Установка пакета с зависимостями для работы с изображениями

```bash
pip install g4f[image]
```