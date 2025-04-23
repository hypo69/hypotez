### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Модуль предоставляет функции для работы с URL, такие как извлечение параметров запроса, проверка валидности URL и сокращение URL с использованием сервиса TinyURL.

Шаги выполнения
-------------------------
1. **Извлечение параметров URL**: Функция `extract_url_params(url: str) -> dict | None` извлекает параметры запроса из URL. Она принимает URL в качестве строки, парсит его и возвращает словарь, содержащий параметры и их значения. Если URL не содержит параметров, функция возвращает `None`.
2. **Проверка валидности URL**: Функция `is_url(text: str) -> bool` проверяет, является ли переданная строка валидным URL. Для проверки используется библиотека `validators`. Если строка является валидным URL, функция возвращает `True`, иначе `False`.
3. **Сокращение URL**: Функция `url_shortener(long_url: str) -> str | None` сокращает длинный URL с использованием сервиса TinyURL. Она отправляет запрос к API TinyURL и возвращает сокращенный URL. В случае ошибки функция возвращает `None`.

Пример использования
-------------------------

```python
from src.utils.url import extract_url_params, is_url, url_shortener

# Пример использования функции extract_url_params
url = "https://www.example.com/path?param1=value1&param2=value2"
params = extract_url_params(url)
if params:
    print("Параметры URL:", params)
# Функция возвращает: {'param1': 'value1', 'param2': 'value2'}
else:
    print("URL не содержит параметров.")

# Пример использования функции is_url
url_to_check = "https://www.example.com"
if is_url(url_to_check):
    print(f"{url_to_check} является валидным URL.")
else:
    print(f"{url_to_check} не является валидным URL.")

# Пример использования функции url_shortener
long_url = "https://www.example.com/very/long/path/to/resource"
short_url = url_shortener(long_url)
if short_url:
    print("Сокращенный URL:", short_url)
else:
    print("Не удалось сократить URL.")