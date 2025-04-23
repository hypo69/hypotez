Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой скрипт установки (`setup.py`) для библиотеки `g4f` (gpt4free). Он автоматизирует процесс сборки, распространения и установки пакета, определяя зависимости, дополнительные компоненты и точки входа. Скрипт также включает метаданные, такие как имя пакета, версия, автор, описание и ссылки на репозиторий.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**:
   - Импортируются модули `codecs`, `os` и функции `find_packages`, `setup` из библиотеки `setuptools`.
   ```python
   import codecs
   import os
   from setuptools import find_packages, setup
   ```
   *Код импортирует необходимые модули для работы с файловой системой, кодировками и сборки пакета.*

2. **Определение абсолютного пути к директории скрипта**:
   - С помощью `os.path.abspath(os.path.dirname(__file__))` определяется абсолютный путь к директории, в которой находится файл `setup.py`.
   ```python
   here = os.path.abspath(os.path.dirname(__file__))
   ```
   *Код получает абсолютный путь к текущей директории.*

3. **Чтение содержимого файла README.md**:
   - Открывается файл `README.md` в кодировке UTF-8 и считывается его содержимое, которое присваивается переменной `long_description`.
   ```python
   with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
       long_description = '\n' + fh.read()
   ```
   *Код считывает описание пакета из файла README.md.*

4. **Замена текста в `long_description`**:
   - Заменяются определенные строки в `long_description`, чтобы корректно отображать ссылки на изображения и документы в репозитории GitHub.
   ```python
   long_description = long_description.replace("[!NOTE]", "")
   long_description = long_description.replace("(docs/images/", "(https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/images/")
   long_description = long_description.replace("(docs/", "(https://github.com/xtekky/gpt4free/blob/main/docs/")
   ```
   *Код заменяет ссылки на ресурсы в описании пакета.*

5. **Определение основных зависимостей**:
   - Создается список `INSTALL_REQUIRE`, содержащий названия основных пакетов, от которых зависит библиотека `g4f`.
   ```python
   INSTALL_REQUIRE = [
       "requests",
       "aiohttp",
       "brotli",
       "pycryptodome",
       "nest_asyncio",
   ]
   ```
   *Код определяет основные зависимости, необходимые для установки пакета.*

6. **Определение дополнительных зависимостей**:
   - Создается словарь `EXTRA_REQUIRE`, содержащий списки дополнительных пакетов, которые могут быть установлены в зависимости от потребностей пользователя. Например, для поддержки GUI, API, поиска и т.д.
   ```python
   EXTRA_REQUIRE = {
       'all': [
           "curl_cffi>=0.6.2",
           "certifi",
           "browser_cookie3",
           "duckduckgo-search>=5.0",
           "beautifulsoup4",
           "platformdirs",
           "aiohttp_socks",
           "pillow",
           "cairosvg",
           "werkzeug", "flask",
           "fastapi",
           "uvicorn",
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
           "duckduckgo-search>=5.0",
           "beautifulsoup4",
           "aiohttp_socks",
           "pillow",
           "werkzeug", "flask",
           "fastapi",
           "uvicorn",
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
   *Код определяет дополнительные зависимости для различных компонентов пакета.*

7. **Определение краткого описания пакета**:
   - Строка `DESCRIPTION` содержит краткое описание библиотеки.
   ```python
   DESCRIPTION = (
       'The official gpt4free repository | various collection of powerful language models'
   )
   ```
   *Код задает краткое описание для пакета.*

8. **Настройка и запуск установки**:
   - Функция `setup` из `setuptools` вызывается для настройки и запуска процесса установки. Передаются различные параметры, такие как имя пакета, версия, автор, описание, зависимости и т.д.
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
   *Код запускает процесс установки пакета с указанными параметрами.*

Пример использования
-------------------------

Чтобы использовать данный скрипт для установки библиотеки `g4f`, выполните следующие шаги:

1.  Сохраните код в файл `setup.py` в корневой директории проекта.
2.  Откройте терминал и перейдите в корневую директорию проекта.
3.  Выполните команду `python setup.py install` для установки библиотеки с основными зависимостями.
4.  Для установки дополнительных зависимостей используйте команду `python setup.py install --extras-require all` (или замените `all` на нужную категорию, например, `gui`, `api`, и т.д.).

```python
# Пример использования setup.py для установки библиотеки g4f
# python setup.py install
# python setup.py install --extras-require all