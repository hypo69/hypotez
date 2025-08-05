# hypotez/src/endpoints/gpt4free/setup.py

## Обзор

Файл `setup.py`  содержит скрипт для настройки и установки пакета Python `gpt4free`. Он используется для определения зависимостей, метаданных пакета и точек входа. 

##  Подробнее

Этот файл содержит информацию о том, как устанавливать пакет `gpt4free`, включая:

- **Зависимости**:  Список библиотек Python, от которых зависит проект `gpt4free`. 
- **Метаданные**:  Информация о пакете, такая как имя, версия, автор, описание, ключевые слова и классификаторы. 
- **Точки входа**:  Определение точки входа для запуска командной строки.

##  Функции

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
        'g4f': [
            'g4f/interference/*',
            'g4f/gui/client/*',
            'g4f/gui/server/*',
            'g4f/Provider/npm/*',
            'g4f/local/models/*'
        ]
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRE,
    extras_require=EXTRA_REQUIRE,
    entry_points={
        'console_scripts': [
            'g4f=g4f.cli:main',
        ],
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

**Назначение**:  Функция `setup`  используется для  конфигурации и установки пакета Python `gpt4free`. Она принимает множество параметров, которые определяют характеристики и поведение пакета при установке. 

**Параметры**: 

- **name**: Имя пакета.
- **version**: Версия пакета.
- **author**: Автор пакета.
- **author_email**: Электронная почта автора.
- **description**: Краткое описание пакета.
- **long_description**: Подробное описание пакета.
- **long_description_content_type**: Тип содержимого подробного описания.
- **packages**: Список пакетов, которые будут установлены.
- **package_data**:  Словарь, содержащий данные, которые должны быть включены в пакет. 
- **include_package_data**:  Флаг, указывающий, нужно ли включать данные из пакета. 
- **install_requires**:  Список зависимостей, которые должны быть установлены вместе с пакетом.
- **extras_require**:  Словарь, содержащий дополнительные зависимости, которые могут быть установлены.
- **entry_points**:  Определение точек входа для запуска командной строки. 
- **url**:  Ссылка на репозиторий GitHub.
- **project_urls**:  Словарь, содержащий ссылки на репозиторий GitHub и отслеживание ошибок. 
- **keywords**:  Список ключевых слов, связанных с пакетом.
- **classifiers**:  Список классификаторов, которые описывают пакет.

**Как работает функция**:  Функция `setup`  собирает всю информацию о пакете, включая зависимости, метаданные и точки входа, и использует ее для создания  файла `setup.py`, который используется  установщиком  Python (pip) для установки пакета.

**Примеры**:

```python
from setuptools import setup

setup(
    name='my_package',  # Имя пакета
    version='1.0.0',  # Версия пакета
    author='John Doe',  # Автор
    description='My amazing package',  # Краткое описание
    # ... другие параметры
)
```

##  Параметры класса

### `INSTALL_REQUIRE`

- **Описание**:  Список основных зависимостей, которые должны быть установлены вместе с пакетом `gpt4free`.
- **Примеры**: 

```python
INSTALL_REQUIRE = [
    "requests",
    "aiohttp",
    "brotli",
    "pycryptodome",
    "nest_asyncio",
]
```

### `EXTRA_REQUIRE`

- **Описание**:  Словарь, содержащий  дополнительные зависимости, которые могут быть установлены  вместе с пакетом `gpt4free`.  Включает  разные варианты  зависмостей для  разных  функциональностей: `slim`, `image`, `webview`, `api`, `gui`, `search`, `local`  и `files`. 

- **Примеры**: 

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

### `DESCRIPTION`

- **Описание**:  Краткое описание пакета `gpt4free`.
- **Примеры**: 

```python
DESCRIPTION = (
    'The official gpt4free repository | various collection of powerful language models'
)
```

##  Примеры

```python
from setuptools import setup

setup(
    name='my_package',
    version='1.0.0',
    # ... другие параметры
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
        ],
    },
)
```

**Пример установки пакета с дополнительными зависимостями**: 

```bash
pip install my_package[dev]