## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет кастомную реализацию Chrome WebDriver, использующую Selenium.
Он интегрирует настройки, определенные в файле `chrome.json`, такие как user-agent и настройки профиля браузера,
чтобы обеспечить гибкие и автоматизированные взаимодействия с браузером.

Шаги выполнения
-------------------------
1. **Инициализация**: Импортируйте класс `Chrome` из модуля `src.webdriver.chrome`.
2. **Настройка**: Создайте экземпляр класса `Chrome`, передав в качестве аргументов необходимые настройки.
    - `user_agent`: Строка user-agent, которую будет использовать браузер.
    - `options`: Список дополнительных опций для WebDriver.
3. **Открытие веб-страницы**: Используйте метод `get()` экземпляра `Chrome` для открытия веб-страницы.
4. **Взаимодействие с браузером**: После открытия веб-страницы вы можете взаимодействовать с ней, используя методы класса `Chrome`
   или Selenium для выполнения действий, таких как клики, ввод текста, получение данных и т. д.
5. **Закрытие браузера**: Используйте метод `quit()` экземпляра `Chrome` для закрытия браузера.

Пример использования
-------------------------

```python
from src.webdriver.chrome import Chrome

# Инициализация Chrome WebDriver с настройками user-agent и кастомными опциями
browser = Chrome(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", options=["--headless", "--disable-gpu"])

# Открытие веб-страницы
browser.get("https://www.example.com")

# Взаимодействие с браузером 
# (например, получение заголовка страницы)
title = browser.title

# Закрытие браузера
browser.quit()
```

## Дополнительные сведения
-------------------------
### Синглтон
Класс `Chrome` реализует шаблон проектирования `Синглтон`. Это означает, что создается только один экземпляр `Chrome` WebDriver.
При повторном вызове конструктора будет возвращаться тот же экземпляр.
### Логирование
Класс `Chrome` использует `logger` из `src.logger` для логирования ошибок, предупреждений и общей информации.
Все проблемы, возникающие во время инициализации, настройки или выполнения, будут записаны в лог-файлы для удобства отладки.
### Файл конфигурации `chrome.json`
Файл `chrome.json` содержит настройки для Chrome WebDriver.
#### Структура `chrome.json`
```json
{
  "options": {
    "log-level": "5",
    "disable-dev-shm-usage": "",
    "remote-debugging-port": "0",
    "arguments": [ "--kiosk", "--disable-gpu" ]
  },
  "disabled_options": { "headless": "" },
  "profile_directory": {
    "os": "%LOCALAPPDATA%\\\\Google\\\\Chrome\\\\User Data",
    "internal": "webdriver\\\\chrome\\\\profiles\\\\default",
    "testing": "%LOCALAPPDATA%\\\\Google\\\\Chrome for Testing\\\\User Data"
  },
  "binary_location": {
    "os": "C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe",
    "exe": "bin\\\\webdrivers\\\\chrome\\\\125.0.6422.14\\\\chromedriver.exe",
    "binary": "bin\\\\webdrivers\\\\chrome\\\\125.0.6422.14\\\\win64-125.0.6422.14\\\\chrome-win64\\\\chrome.exe",
    "chromium": "bin\\\\webdrivers\\\\chromium\\\\chrome-win\\\\chrome.exe"
  },
  "headers": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive"
  },
  "proxy_enabled": false
}
```

#### Описание полей конфигурации
- **options**: Словарь параметров Chrome для изменения поведения браузера.
- **disabled_options**: Опции, которые явно отключены.
- **profile_directory**: Пути к каталогам данных пользователя Chrome для разных сред.
- **binary_location**: Пути к различным двоичным файлам Chrome.
- **headers**: Настраиваемые HTTP-заголовки, используемые в запросах браузера.
- **proxy_enabled**: Логическое значение, указывающее, использовать ли прокси-сервер для WebDriver.

## Лицензия
-------------------------
Этот проект лицензирован по лицензии MIT. См. файл [LICENSE](../../LICENSE) для получения более подробной информации.