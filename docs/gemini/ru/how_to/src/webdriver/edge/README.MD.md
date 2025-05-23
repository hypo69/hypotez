## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой документацию для модуля `src.webdriver.edge`, который предоставляет кастомную реализацию WebDriver для браузера Microsoft Edge. Он использует Selenium и настраивается с помощью файла `edge.json`.

Шаги выполнения
-------------------------
1. **Определение зависимостей**: Убедитесь, что установлены необходимые библиотеки Python: Selenium, Fake User Agent и драйвер Edge WebDriver (msedgedriver.exe).
2. **Настройка конфигурации**: В файле `edge.json` вы найдете настройки, такие как опции командной строки для Edge, пути к профилям, путь к исполняемому файлу драйвера, а также HTTP-заголовки.
3. **Инициализация WebDriver**: Импортируйте класс `Edge` из модуля `src.webdriver.edge` и создайте экземпляр класса. Вы можете указать кастомный user-agent и опции командной строки при инициализации.
4. **Взаимодействие с браузером**: Используйте методы класса `Edge` (например, `get()`, `quit()`) для взаимодействия с веб-страницами.

Пример использования
-------------------------

```python
from src.webdriver.edge import Edge

# Инициализация Edge WebDriver с кастомным user-agent и опциями
browser = Edge(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", options=["--headless", "--disable-gpu"])

# Открытие веб-сайта
browser.get("https://www.example.com")

# Закрытие браузера
browser.quit()
```

## Дополнительные сведения

- Модуль `src.webdriver.edge` использует паттерн "Singleton".
- Все ошибки и предупреждения регистрируются в логах с помощью `logger` из `src.logger`.
- `edge.json` содержит различные настройки, такие как опции командной строки, профили, пути к исполняемому файлу драйвера и заголовки HTTP.
- `Edge` WebDriver поддерживает несколько профилей, позволяя использовать разные настройки для тестирования.