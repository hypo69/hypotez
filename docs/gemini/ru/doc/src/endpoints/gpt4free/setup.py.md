# Модуль setup.py

## Обзор

Файл `setup.py` используется для сборки, распространения и установки пакета `g4f` (gpt4free). Он содержит метаданные о пакете, такие как имя, версия, автор, описание, зависимости и другие.

## Подробней

Этот файл является стандартным файлом `setup.py` для проектов Python, использующих `setuptools`. Он определяет, как пакет должен быть установлен и какие зависимости необходимы для его работы. В частности, он указывает зависимости, дополнительные компоненты (например, для работы с изображениями или веб-интерфейсом), точки входа для консольных скриптов и URL-адреса проекта.

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

**Назначение**: Функция `setup` из библиотеки `setuptools` используется для настройки процесса сборки, установки и распространения Python-пакета.

**Параметры**:
- `name` (str): Имя пакета (`g4f`).
- `version` (str): Версия пакета, извлекается из переменной окружения `G4F_VERSION`.
- `author` (str): Имя автора пакета (`Tekky`).
- `author_email` (str): Email автора пакета (`<support@g4f.ai>`).
- `description` (str): Краткое описание пакета (значение переменной `DESCRIPTION`).
- `long_description_content_type` (str): Тип контента для длинного описания (`text/markdown`).
- `long_description` (str): Длинное описание пакета, загруженное из файла `README.md`.
- `packages` (list): Список пакетов, которые необходимо включить, определяется функцией `find_packages()`.
- `package_data` (dict): Дополнительные файлы, которые нужно включить в пакет.
- `include_package_data` (bool): Флаг, указывающий, нужно ли включать данные пакета.
- `install_requires` (list): Список обязательных зависимостей для установки пакета (значение `INSTALL_REQUIRE`).
- `extras_require` (dict): Словарь дополнительных зависимостей, разделенных по категориям (значение `EXTRA_REQUIRE`).
- `entry_points` (dict): Определяет точки входа для консольных скриптов.
- `url` (str): URL-адрес репозитория GitHub.
- `project_urls` (dict): Словарь URL-адресов проекта, таких как репозиторий исходного кода и трекер ошибок.
- `keywords` (list): Список ключевых слов, связанных с пакетом.
- `classifiers` (list): Список классификаторов, описывающих различные аспекты пакета.

**Возвращает**:
- `None`

**Вызывает исключения**:
- Функция `setup` может вызывать различные исключения в зависимости от ошибок конфигурации или проблем с зависимостями.

**Как работает функция**:
- Функция `setup` принимает различные аргументы, описывающие пакет, его зависимости, метаданные и другие параметры.
- Она использует эти параметры для настройки процесса сборки, установки и распространения пакета.
- Функция `find_packages()` автоматически определяет все пакеты в проекте.
- Параметр `package_data` указывает, какие дополнительные файлы следует включить в пакет при установке.
- Параметр `install_requires` определяет список обязательных зависимостей, которые будут установлены вместе с пакетом.
- Параметр `extras_require` позволяет определить дополнительные зависимости, которые могут быть установлены отдельно.
- Параметр `entry_points` определяет точки входа для консольных скриптов, что позволяет запускать скрипты из командной строки.
- Остальные параметры содержат метаданные о пакете, такие как имя, версия, автор, описание и URL-адреса проекта.

**Примеры**:

```python
setup(
    name='g4f',
    version='1.0.0',
    author='Tekky',
    author_email='<support@g4f.ai>',
    description='The official gpt4free repository',
    long_description='...',
    packages=find_packages(),
    install_requires=['requests', 'aiohttp'],
    entry_points={
        'console_scripts': ['g4f=g4f.cli:main'],
    },
    url='https://github.com/xtekky/gpt4free',
)
```

В этом примере показана минимальная конфигурация для функции `setup`, включающая имя, версию, автора, описание, список пакетов и обязательные зависимости.

## Переменные

- `here` (str): Абсолютный путь к директории, содержащей файл `setup.py`.
- `long_description` (str): Длинное описание пакета, загруженное из файла `README.md` и обработанное для удаления определенных элементов и замены путей к изображениям.
- `INSTALL_REQUIRE` (list): Список обязательных зависимостей для установки пакета.
- `EXTRA_REQUIRE` (dict): Словарь дополнительных зависимостей, разделенных по категориям (например, `all`, `slim`, `image`, `webview`, `api`, `gui`, `search`, `local`, `files`).
- `DESCRIPTION` (str): Краткое описание пакета.