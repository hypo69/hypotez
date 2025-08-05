## Как использовать модуль `Firefox`
=========================================================================================

Описание
-------------------------
Модуль `Firefox` расширяет стандартный `selenium.webdriver.Firefox` функциональностью, 
такой как управление профилями, режим киоска, а также настройками прокси.

Шаги выполнения
-------------------------
1. **Импортируй модуль `Firefox`:**
    ```python
    from src.webdriver.firefox import Firefox 
    ```

2. **Создай экземпляр класса `Firefox`:**
    - **Обязательный аргумент:** 
        - `profile_name` (необязательный) - имя профиля Firefox. 
    - **Необязательные аргументы:**
        - `geckodriver_version` - версия GeckoDriver.
        - `firefox_version` - версия Firefox.
        - `user_agent` - строка User-Agent. Если не задано, будет использоваться случайный User-Agent.
        - `proxy_file_path` - путь к файлу с прокси-серверами.
        - `options` - список дополнительных опций для Firefox.
        - `window_mode` - режим окна браузера (например, "windowless", "kiosk").

3. **Используй методы WebDriver для управления браузером:**
    - `get(url)`: переходит на заданный URL.
    - `quit()`: закрывает браузер.

Пример использования
-------------------------

```python
from src.webdriver.firefox import Firefox 

if __name__ == "__main__":
    browser = Firefox(
        profile_name="custom_profile", 
        window_mode="kiosk"
    ) 
    browser.get("https://www.example.com") 
    browser.quit() 
```

## Конфигурационные настройки
-------------------------

- **`firefox.json`**: файл конфигурации для настроек Firefox.
    - `executable_path.geckodriver`: путь к исполняемому файлу GeckoDriver.
    - `executable_path.firefox_binary`: путь к исполняемому файлу Firefox.
    - `profile_directory.default`: источник профиля - "os" (системный) или "internal" (встроенный).
    - `profile_directory.os`: путь к системному профилю.
    - `profile_directory.internal`: путь к встроенному профилю.
    - `options`: список дополнительных опций для Firefox.
    - `headers`: словарь пользовательских заголовков.
    - `proxy_enabled`: флаг, указывающий на использование прокси.

## Методы класса `Firefox`
-------------------------

**`__init__(self, profile_name: Optional[str] = None, geckodriver_version: Optional[str] = None, firefox_version: Optional[str] = None, user_agent: Optional[str] = None, proxy_file_path: Optional[str] = None, options: Optional[List[str]] = None, window_mode: Optional[str] = None, *args, **kwargs) -> None`**

* Инициализирует WebDriver Firefox с пользовательскими настройками.

**`set_proxy(self, options: Options) -> None`**

* Настраивает настройки прокси из словаря.

**`_payload(self) -> None`**

* Загружает исполнителей для локаторов и скриптов JavaScript.


## Дополнительные замечания
-------------------------

- **Профили**:
    - Если `profile_name` не задан, WebDriver использует стандартный профиль Firefox.
    - Если `profile_name` задан, WebDriver будет использовать указанный профиль.
- **Режим киоска**:
    - `window_mode="kiosk"` позволяет запускать Firefox в режиме полного экрана.
- **Прокси**:
    - `proxy_enabled` должен быть установлен в `True`, чтобы включить прокси.
    - `proxy_file_path` указывает на файл JSON, содержащий список прокси-серверов.
- **Опции**:
    - Список `options` позволяет задавать дополнительные опции для Firefox.
- **User-Agent**:
    - Если `user_agent` не задан, WebDriver будет использовать случайный User-Agent.
- **Ошибка запуска WebDriver**:
    - Если WebDriver не запускается, проверьте, что Firefox и GeckoDriver установлены и доступны.
    - Также убедитесь, что настройки прокси и другие конфигурационные параметры верны.