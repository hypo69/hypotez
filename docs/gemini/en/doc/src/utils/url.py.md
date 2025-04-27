# Модуль src.utils.string.url
## Обзор
Модуль для работы с URL строками, включая извлечение параметров запроса, проверку на валидность URL и сокращение ссылок.

## Детали
Модуль предоставляет функции для обработки URL-адресов. 
Он использует стандартную библиотеку `urllib.parse` для разбора URL и извлечения параметров, 
а также библиотеку `validators` для проверки валидности URL. 
Для сокращения ссылок используется сервис TinyURL.
## Классы
### `None`
## Функции
### `extract_url_params`
**Цель**: Извлекает параметры из строки URL.

**Параметры**:
- `url` (str): Строка URL для парсинга.

**Возвращает**:
- `dict | None`: Словарь параметров запроса и их значений или `None`, если URL не содержит параметров.

**Пример**:
```python
>>> extract_url_params('https://example.com?param1=value1&param2=value2')
{'param1': 'value1', 'param2': 'value2'}

>>> extract_url_params('https://example.com')
None
```
### `is_url`
**Цель**: Проверяет, является ли переданный текст валидным URL с использованием библиотеки validators.

**Параметры**:
- `text` (str): Строка для проверки.

**Возвращает**:
- `bool`: `True` если строка является валидным URL, иначе `False`.

**Пример**:
```python
>>> is_url('https://example.com')
True

>>> is_url('example.com')
False
```
### `url_shortener`
**Цель**: Сокращает длинный URL с использованием сервиса TinyURL.

**Параметры**:
- `long_url` (str): Длинный URL для сокращения.

**Возвращает**:
- `str | None`: Сокращённый URL или `None`, если произошла ошибка.

**Пример**:
```python
>>> url_shortener('https://www.example.com/very/long/url/with/lots/of/parameters')
'https://tinyurl.com/your-short-url'
```
## Параметры деталей
- `url` (str): Строка URL для парсинга.
- `text` (str): Строка для проверки.
- `long_url` (str): Длинный URL для сокращения.
## Примеры
```python
# Получаем строку URL от пользователя
url = input("Введите URL: ")

# Проверяем валидность URL
if is_url(url):
    params = extract_url_params(url)

    # Выводим параметры
    if params:
        print("Параметры URL:")
        for key, value in params.items():
            print(f"{key}: {value}")
    else:
        print("URL не содержит параметров.")

    # Предлагаем пользователю сократить URL
    shorten = input("Хотите сократить этот URL? (y/n): ").strip().lower()
    if shorten == 'y':
        short_url = url_shortener(url)
        if short_url:
            print(f"Сокращённый URL: {short_url}")
        else:
            print("Ошибка при сокращении URL.")
else:
    print("Введенная строка не является валидным URL.")
```
```python
# Пример использования extract_url_params
url = 'https://www.example.com/search?q=python&lang=ru'
params = extract_url_params(url)
print(f"Параметры URL: {params}") # Вывод: {'q': 'python', 'lang': 'ru'}

# Пример использования is_url
url = 'https://www.example.com'
is_valid = is_url(url)
print(f"URL валиден: {is_valid}") # Вывод: URL валиден: True

# Пример использования url_shortener
long_url = 'https://www.example.com/very/long/url/with/lots/of/parameters'
short_url = url_shortener(long_url)
print(f"Сокращённый URL: {short_url}") # Вывод: Сокращённый URL: https://tinyurl.com/your-short-url
```
```python
>>> url = 'https://www.example.com/search?q=python&lang=ru'
>>> extract_url_params(url)
{'q': 'python', 'lang': 'ru'}

>>> url = 'https://www.example.com'
>>> is_url(url)
True

>>> url = 'example.com'
>>> is_url(url)
False

>>> long_url = 'https://www.example.com/very/long/url/with/lots/of/parameters'
>>> url_shortener(long_url)
'https://tinyurl.com/your-short-url'
```
```python
# Проверка валидности URL
url = 'https://www.example.com/search?q=python&lang=ru'
if is_url(url):
    print(f"URL валиден: {url}")
else:
    print("Введён некорректный URL.")

# Извлечение параметров из URL
params = extract_url_params(url)
if params:
    print("Параметры URL:")
    for key, value in params.items():
        print(f"{key}: {value}")
else:
    print("URL не содержит параметров.")

# Сокращение URL
short_url = url_shortener(url)
if short_url:
    print(f"Сокращённый URL: {short_url}")
else:
    print("Ошибка при сокращении URL.")