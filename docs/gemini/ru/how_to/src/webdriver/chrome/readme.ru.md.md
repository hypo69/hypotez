## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет кастомную реализацию Chrome WebDriver с использованием Selenium. Он интегрирует настройки конфигурации из файла `chrome.json`, такие как user-agent и настройки профиля браузера, для обеспечения гибких и автоматизированных взаимодействий с браузером.

Шаги выполнения
-------------------------
1. **Установка зависимостей**: Убедитесь, что у вас установлены Python 3.x, Selenium, Fake User Agent и WebDriver бинарник для Chrome (например, `chromedriver`).
2. **Установка библиотек Python**:
   ```bash
   pip install selenium fake_useragent
   ```
3. **Конфигурация `chrome.json`**: Настройте файл `chrome.json` с необходимыми параметрами, такими как `options`, `disabled_options`, `profile_directory`, `binary_location` и `headers`.
4. **Инициализация Chrome WebDriver**: Импортируйте класс `Chrome` из `src.webdriver.chrome` и инициализируйте его с нужными параметрами.
5. **Использование WebDriver**: Используйте методы `Chrome` WebDriver для открытия веб-сайтов, выполнения действий и закрытия браузера.

Пример использования
-------------------------

```python
from src.webdriver.chrome import Chrome

# Инициализация Chrome WebDriver с настройками user-agent и пользовательскими опциями
browser = Chrome(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", options=["--headless", "--disable-gpu"])

# Открытие веб-сайта
browser.get("https://www.example.com")

# Закрытие браузера
browser.quit()
```

Этот пример показывает, как инициализировать Chrome WebDriver с пользовательским user-agent и опциями, открыть веб-сайт и закрыть браузер. Класс `Chrome` автоматически загружает настройки из файла `chrome.json` и использует их для конфигурации WebDriver.