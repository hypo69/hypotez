Этот документ предоставляет обзор всех вебдрайверов, доступных в проекте, их настроек и опций. Каждый вебдрайвер имеет свои параметры, которые можно настроить в соответствующих файлах JSON.

# Вебдрайверы и их настройки

&nbsp;&nbsp;&nbsp;&nbsp;Этот документ содержит описание всех вебдрайверов, доступных в проекте, их настроек и опций. Каждый вебдрайвер предоставляет возможности для автоматизации браузеров и сбора данных.

---

## Оглавление

1. [Firefox WebDriver](#1-firefox-webdriver)
2. [Chrome WebDriver](#2-chrome-webdriver)
3. [Edge WebDriver](#3-edge-webdriver)
4. [Playwright Crawler](#4-playwright-crawler)
5. [BeautifulSoup и XPath Parser](#5-beautifulsoup-и-xpath-parser)
6. [Заключение](#заключение)

---

## 1. Firefox WebDriver

### Описание
&nbsp;&nbsp;&nbsp;&nbsp;Firefox WebDriver предоставляет функциональность для работы с браузером Firefox. Он поддерживает настройку пользовательских профилей, прокси, user-agent и других параметров.

### Настройки
- **profile_name**: Имя пользовательского профиля Firefox.
- **geckodriver_version**: Версия geckodriver.
- **firefox_version**: Версия Firefox.
- **user_agent**: Пользовательский агент.
- **proxy_file_path**: Путь к файлу с прокси.
- **options**: Список опций для Firefox (например, `["--kiosk", "--headless"]`).

### Пример конфигурации (`firefox.json`)
```json
{
  "options": ["--kiosk", "--headless"],
  "profile_directory": {
    "os": "%LOCALAPPDATA%\\\\Mozilla\\\\Firefox\\\\Profiles\\\\default",
    "internal": "webdriver\\\\firefox\\\\profiles\\\\default"
  },
  "executable_path": {
    "firefox_binary": "bin\\\\webdrivers\\\\firefox\\\\ff\\\\core-127.0.2\\\\firefox.exe",
    "geckodriver": "bin\\\\webdrivers\\\\firefox\\\\gecko\\\\33\\\\geckodriver.exe"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  },
  "proxy_enabled": false
}
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Firefox WebDriver обеспечивает управление браузером Firefox для автоматизации задач, таких как тестирование веб-приложений или сбор данных. Он позволяет настраивать различные параметры браузера, включая профиль пользователя, прокси-сервер, строку User-Agent и другие опции.

Шаги выполнения
-------------------------
1. **Установка Firefox WebDriver**: Убедитесь, что у вас установлены Firefox и Geckodriver (необходимый для управления Firefox).
2. **Настройка конфигурационного файла**: Создайте или отредактируйте файл `firefox.json` с необходимыми параметрами, такими как опции запуска, пути к исполняемым файлам и заголовки.
3. **Инициализация WebDriver**: Используйте WebDriver для запуска Firefox с указанными настройками.

Пример использования
-------------------------

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

# Функция для загрузки конфигурации из JSON файла
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

# Загрузка конфигурации из файла firefox.json
config = load_config('firefox.json')

# Настройка опций Firefox
options = Options()
for option in config['options']:
    options.add_argument(option)

# Установка пути к исполняемым файлам
executable_path = config['executable_path']
firefox_binary = executable_path['firefox_binary']
geckodriver = executable_path['geckodriver']

# Инициализация WebDriver с указанными параметрами
driver = webdriver.Firefox(
    executable_path=geckodriver,
    firefox_binary=firefox_binary,
    options=options
)

# Пример использования: открытие веб-страницы
driver.get("https://www.example.com")

# Дальнейшие действия по автоматизации или сбору данных
# ...

# Закрытие браузера после завершения
driver.quit()
```

---

## 2. Chrome WebDriver

### Описание
Chrome WebDriver предоставляет функциональность для работы с браузером Google Chrome. Он поддерживает настройку профилей, user-agent, прокси и других параметров.

### Настройки
- **profile_name**: Имя пользовательского профиля Chrome.
- **chromedriver_version**: Версия chromedriver.
- **chrome_version**: Версия Chrome.
- **user_agent**: Пользовательский агент.
- **proxy_file_path**: Путь к файлу с прокси.
- **options**: Список опций для Chrome (например, `["--headless", "--disable-gpu"]`).

### Пример конфигурации (`chrome.json`)
```json
{
  "options": ["--headless", "--disable-gpu"],
  "profile_directory": {
    "os": "%LOCALAPPDATA%\\\\Google\\\\Chrome\\\\User Data\\\\Default",
    "internal": "webdriver\\\\chrome\\\\profiles\\\\default"
  },
  "executable_path": {
    "chrome_binary": "bin\\\\webdrivers\\\\chrome\\\\125.0.6422.14\\\\chrome.exe",
    "chromedriver": "bin\\\\webdrivers\\\\chrome\\\\125.0.6422.14\\\\chromedriver.exe"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  },
  "proxy_enabled": false
}
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Chrome WebDriver обеспечивает взаимодействие с браузером Google Chrome для автоматизации задач, таких как тестирование веб-приложений или сбор данных. Он позволяет настраивать различные параметры браузера, включая профиль пользователя, прокси-сервер, строку User-Agent и другие опции.

Шаги выполнения
-------------------------
1. **Установка Chrome WebDriver**: Убедитесь, что у вас установлены Chrome и Chromedriver (необходимый для управления Chrome).
2. **Настройка конфигурационного файла**: Создайте или отредактируйте файл `chrome.json` с необходимыми параметрами, такими как опции запуска, пути к исполняемым файлам и заголовки.
3. **Инициализация WebDriver**: Используйте WebDriver для запуска Chrome с указанными настройками.

Пример использования
-------------------------

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

# Функция для загрузки конфигурации из JSON файла
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

# Загрузка конфигурации из файла chrome.json
config = load_config('chrome.json')

# Настройка опций Chrome
options = Options()
for option in config['options']:
    options.add_argument(option)

# Установка пути к исполняемым файлам
executable_path = config['executable_path']
chrome_binary = executable_path['chrome_binary']
chromedriver = executable_path['chromedriver']

# Инициализация WebDriver с указанными параметрами
driver = webdriver.Chrome(
    executable_path=chromedriver,
    chrome_binary=chrome_binary,
    options=options
)

# Пример использования: открытие веб-страницы
driver.get("https://www.example.com")

# Дальнейшие действия по автоматизации или сбору данных
# ...

# Закрытие браузера после завершения
driver.quit()
```

---

## 3. Edge WebDriver

### Описание
Edge WebDriver предоставляет функциональность для работы с браузером Microsoft Edge. Он поддерживает настройку профилей, user-agent, прокси и других параметров.

### Настройки
- **profile_name**: Имя пользовательского профиля Edge.
- **edgedriver_version**: Версия edgedriver.
- **edge_version**: Версия Edge.
- **user_agent**: Пользовательский агент.
- **proxy_file_path**: Путь к файлу с прокси.
- **options**: Список опций для Edge (например, `["--headless", "--disable-gpu"]`).

### Пример конфигурации (`edge.json`)
```json
{
  "options": ["--headless", "--disable-gpu"],
  "profiles": {
    "os": "%LOCALAPPDATA%\\\\Microsoft\\\\Edge\\\\User Data\\\\Default",
    "internal": "webdriver\\\\edge\\\\profiles\\\\default"
  },
  "executable_path": {
    "edge_binary": "bin\\\\webdrivers\\\\edge\\\\123.0.2420.97\\\\edge.exe",
    "edgedriver": "bin\\\\webdrivers\\\\edge\\\\123.0.2420.97\\\\msedgedriver.exe"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  },
  "proxy_enabled": false
}
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Edge WebDriver обеспечивает взаимодействие с браузером Microsoft Edge для автоматизации задач, таких как тестирование веб-приложений или сбор данных. Он позволяет настраивать различные параметры браузера, включая профиль пользователя, прокси-сервер, строку User-Agent и другие опции.

Шаги выполнения
-------------------------
1. **Установка Edge WebDriver**: Убедитесь, что у вас установлены Edge и Edgedriver (необходимый для управления Edge).
2. **Настройка конфигурационного файла**: Создайте или отредактируйте файл `edge.json` с необходимыми параметрами, такими как опции запуска, пути к исполняемым файлам и заголовки.
3. **Инициализация WebDriver**: Используйте WebDriver для запуска Edge с указанными настройками.

Пример использования
-------------------------

```python
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
import json

# Функция для загрузки конфигурации из JSON файла
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

# Загрузка конфигурации из файла edge.json
config = load_config('edge.json')

# Настройка опций Edge
options = EdgeOptions()
options.use_chromium = True
for option in config['options']:
    options.add_argument(option)

# Установка пути к исполняемым файлам
executable_path = config['executable_path']
edge_binary = executable_path['edge_binary']
edgedriver = executable_path['edgedriver']

# Инициализация WebDriver с указанными параметрами
driver = Edge(
    executable_path=edgedriver,
    capabilities = {"ms:edgeOptions": {'binary': edge_binary}},
    options=options
)

# Пример использования: открытие веб-страницы
driver.get("https://www.example.com")

# Дальнейшие действия по автоматизации или сбору данных
# ...

# Закрытие браузера после завершения
driver.quit()
```

---

## 4. Playwright Crawler

### Описание
Playwright Crawler предоставляет функциональность для автоматизации браузеров с использованием библиотеки Playwright. Он поддерживает настройку прокси, user-agent, размера окна и других параметров.

### Настройки
- **max_requests**: Максимальное количество запросов.
- **headless**: Режим безголового запуска браузера.
- **browser_type**: Тип браузера (`chromium`, `firefox`, `webkit`).
- **user_agent**: Пользовательский агент.
- **proxy**: Настройки прокси-сервера.
- **viewport**: Размер окна браузера.
- **timeout**: Тайм-аут для запросов.
- **ignore_https_errors**: Игнорирование ошибок HTTPS.

### Пример конфигурации (`playwrid.json`)
```json
{
  "max_requests": 10,
  "headless": true,
  "browser_type": "chromium",
  "options": ["--disable-dev-shm-usage", "--no-sandbox"],
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
  "proxy": {
    "enabled": false,
    "server": "http://proxy.example.com:8080",
    "username": "user",
    "password": "password"
  },
  "viewport": {
    "width": 1280,
    "height": 720
  },
  "timeout": 30000,
  "ignore_https_errors": false
}
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Playwright Crawler автоматизирует браузеры, используя библиотеку Playwright, для выполнения задач, таких как сбор данных или тестирование. Он позволяет настраивать различные параметры браузера, включая прокси-сервер, строку User-Agent, размеры окна просмотра и другие опции.

Шаги выполнения
-------------------------
1. **Установка Playwright**: Установите библиотеку Playwright с помощью `pip install playwright` и необходимые браузеры с помощью `playwright install`.
2. **Настройка конфигурационного файла**: Создайте или отредактируйте файл `playwrid.json` с необходимыми параметрами, такими как максимальное количество запросов, режим без головы, настройки прокси и т. д.
3. **Инициализация Playwright**: Используйте Playwright для запуска браузера с указанными настройками.

Пример использования
-------------------------

```python
from playwright.sync_api import sync_playwright
import json

# Функция для загрузки конфигурации из JSON файла
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

# Загрузка конфигурации из файла playwrid.json
config = load_config('playwrid.json')

# Настройка прокси
proxy = None
if config['proxy']['enabled']:
    proxy = {
        'server': config['proxy']['server'],
        'username': config['proxy']['username'],
        'password': config['proxy']['password']
    }

# Запуск Playwright
with sync_playwright() as p:
    browser_type = config['browser_type']
    if browser_type == 'chromium':
        browser = p.chromium.launch(headless=config['headless'], proxy=proxy, args=config['options'])
    elif browser_type == 'firefox':
        browser = p.firefox.launch(headless=config['headless'], proxy=proxy, args=config['options'])
    elif browser_type == 'webkit':
        browser = p.webkit.launch(headless=config['headless'], proxy=proxy, args=config['options'])
    else:
        raise ValueError(f"Unknown browser type: {browser_type}")

    page = browser.new_page(
        viewport=config['viewport'],
        user_agent=config['user_agent'],
        ignore_https_errors=config['ignore_https_errors']
    )
    page.goto("https://www.example.com", timeout=config['timeout'])

    # Дальнейшие действия по автоматизации или сбору данных
    # ...

    browser.close()
```

---

## 5. BeautifulSoup и XPath Parser

### Описание
Модуль для парсинга HTML-контента с использованием BeautifulSoup и XPath. Он позволяет извлекать данные из локальных файлов или веб-страниц.

### Настройки
- **default_url**: URL по умолчанию для загрузки HTML.
- **default_file_path**: Путь к файлу по умолчанию.
- **default_locator**: Локатор по умолчанию для извлечения элементов.
- **logging**: Настройки логирования.
- **proxy**: Настройки прокси-сервера.
- **timeout**: Тайм-аут для запросов.
- **encoding**: Кодировка для чтения файлов или запросов.

### Пример конфигурации (`bs.json`)
```json
{
  "default_url": "https://example.com",
  "default_file_path": "file://path/to/your/file.html",
  "default_locator": {
    "by": "ID",
    "attribute": "element_id",
    "selector": "//*[@id='element_id']"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/bs.log"
  },
  "proxy": {
    "enabled": false,
    "server": "http://proxy.example.com:8080",
    "username": "user",
    "password": "password"
  },
  "timeout": 10,
  "encoding": "utf-8"
}
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
BeautifulSoup и XPath Parser позволяют извлекать информацию из HTML-контента, будь то локальные файлы или веб-страницы. BeautifulSoup используется для парсинга HTML, а XPath — для навигации и выбора элементов в структуре документа.

Шаги выполнения
-------------------------
1. **Установка BeautifulSoup и lxml**: Установите необходимые библиотеки с помощью `pip install beautifulsoup4 lxml`.
2. **Настройка конфигурационного файла**: Создайте или отредактируйте файл `bs.json` с необходимыми параметрами, такими как URL или путь к файлу, локаторы элементов и настройки прокси.
3. **Инициализация и парсинг**: Используйте BeautifulSoup для парсинга HTML и XPath для извлечения нужных элементов.

Пример использования
-------------------------

```python
from bs4 import BeautifulSoup
import requests
import json

# Функция для загрузки конфигурации из JSON файла
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

# Загрузка конфигурации из файла bs.json
config = load_config('bs.json')

# Функция для загрузки HTML-контента
def load_html(config):
    if config['default_url']:
        response = requests.get(config['default_url'], timeout=config['timeout'])
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.content, response.encoding
    elif config['default_file_path']:
        with open(config['default_file_path'], 'r', encoding=config['encoding']) as f:
            return f.read(), config['encoding']
    else:
        raise ValueError("Не указан ни URL, ни путь к файлу")

# Загрузка HTML-контента
html_content, encoding = load_html(config)

# Парсинг HTML с использованием BeautifulSoup
soup = BeautifulSoup(html_content, 'lxml', from_encoding=encoding)

# Извлечение элемента с использованием XPath
locator = config['default_locator']
if locator['by'] == 'ID':
    element = soup.find(id=locator['attribute'])
elif locator['by'] == 'XPATH':
    element = soup.select_one(locator['selector'])
else:
    raise ValueError(f"Unknown locator type: {locator['by']}")

# Вывод результата
if element:
    print(element.text)
else:
    print("Элемент не найден")
```