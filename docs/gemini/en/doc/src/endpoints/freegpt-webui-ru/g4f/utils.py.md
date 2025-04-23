# Модуль `utils.py`

## Обзор

Модуль `utils.py` содержит утилиты, используемые в проекте `hypotez`. В частности, он предоставляет функциональность для извлечения файлов cookie из различных браузеров. Модуль включает класс `Utils` с методом `get_cookies`, который позволяет получить файлы cookie для определенного домена.

## Более подробно

Модуль предназначен для автоматического получения файлов cookie из установленных в системе браузеров. Это может быть полезно для автоматизации задач, требующих аутентификации, например, для парсинга данных с веб-сайтов.

## Классы

### `Utils`

**Описание**: Класс, содержащий утилиты для работы с файлами cookie браузеров.

**Атрибуты**:
- `browsers (list)`: Список функций из модуля `browser_cookie3`, представляющих различные браузеры.

**Методы**:
- `get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict`: Метод для получения файлов cookie из браузеров.

## Методы класса

### `get_cookies`

```python
def get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict:
    """
    Функция извлекает файлы cookie для указанного домена из поддерживаемых браузеров.

    Args:
        domain (str): Домен, для которого требуется извлечь файлы cookie.
        setName (str, optional): Имя конкретного cookie, который нужно извлечь. По умолчанию `None`.
        setBrowser (str, optional): Название конкретного браузера, из которого нужно извлечь файлы cookie. По умолчанию `False`.

    Returns:
        dict: Словарь, содержащий извлеченные файлы cookie.

    Raises:
        ValueError: Если указанное имя cookie (`setName`) не найдено ни в одном браузере.

    Как работает функция:
    - Инициализирует пустой словарь `cookies` для хранения извлеченных файлов cookie.
    - Если указан параметр `setBrowser`, функция пытается извлечь файлы cookie только из указанного браузера.
    - Если `setBrowser` не указан, функция перебирает все браузеры в списке `Utils.browsers` и пытается извлечь файлы cookie из каждого.
    - Для каждого браузера функция вызывает соответствующую функцию из `browser_cookie3` для получения файлов cookie для указанного домена.
    - Если в процессе извлечения файлов cookie возникает исключение, оно игнорируется.
    - Если указан параметр `setName`, функция пытается вернуть только cookie с указанным именем.
    - Если cookie с указанным именем не найден, функция выводит сообщение об ошибке и завершает работу.
    - Если `setName` не указан, функция возвращает все извлеченные файлы cookie в виде словаря.

    Примеры:
    - Получение всех файлов cookie для домена "example.com":
        >>> Utils.get_cookies("example.com")
        {'cookie1': 'value1', 'cookie2': 'value2'}

    - Получение конкретного cookie с именем "my_cookie" для домена "example.com":
        >>> Utils.get_cookies("example.com", setName="my_cookie")
        {'my_cookie': 'my_value'}

    - Получение файлов cookie только из браузера Chrome для домена "example.com":
        >>> Utils.get_cookies("example.com", setBrowser="chrome")
        {'cookie1': 'value1', 'cookie2': 'value2'}
    """
    cookies: dict = {}
    
    if setBrowser != False:
        for browser in Utils.browsers:
            if browser.__name__ == setBrowser:
                try:
                    for c in browser(domain_name=domain):
                        if c.name not in cookies:
                            cookies = cookies | {c.name: c.value} 
                
                except Exception as ex:
                    pass
    
    else:
        for browser in Utils.browsers:
            try:
                for c in browser(domain_name=domain):
                    if c.name not in cookies:
                        cookies = cookies | {c.name: c.value} 
            
            except Exception as ex:
                pass
    
    if setName:
        try:
            return {setName: cookies[setName]}
        
        except ValueError:
            print(f'Error: could not find {setName} cookie in any browser.')
            exit(1)
    
    else:
        return cookies
```

## Параметры класса

- `browsers`: Список функций для работы с cookie разных браузеров.
    - `browser_cookie3.chrome`: Функция для извлечения cookie из браузера Chrome.
    - `browser_cookie3.safari`: Функция для извлечения cookie из браузера Safari.
    - `browser_cookie3.firefox`: Функция для извлечения cookie из браузера Firefox.
    - `browser_cookie3.edge`: Функция для извлечения cookie из браузера Edge.
    - `browser_cookie3.opera`: Функция для извлечения cookie из браузера Opera.
    - `browser_cookie3.brave`: Функция для извлечения cookie из браузера Brave.
    - `browser_cookie3.opera_gx`: Функция для извлечения cookie из браузера Opera GX.
    - `browser_cookie3.vivaldi`: Функция для извлечения cookie из браузера Vivaldi.

## Примеры

Пример использования класса `Utils` для получения файлов cookie:

```python
import browser_cookie3

class Utils:
    browsers = [
        browser_cookie3.chrome,
        browser_cookie3.safari,
        browser_cookie3.firefox,
        browser_cookie3.edge,
        browser_cookie3.opera,
        browser_cookie3.brave,
        browser_cookie3.opera_gx,
        browser_cookie3.vivaldi,
    ]

    def get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict:
        cookies: dict = {}
        
        if setBrowser != False:
            for browser in Utils.browsers:
                if browser.__name__ == setBrowser:
                    try:
                        for c in browser(domain_name=domain):
                            if c.name not in cookies:
                                cookies = cookies | {c.name: c.value} 
                    
                    except Exception as ex:
                        pass
        
        else:
            for browser in Utils.browsers:
                try:
                    for c in browser(domain_name=domain):
                        if c.name not in cookies:
                            cookies = cookies | {c.name: c.value} 
            
            except Exception as ex:
                pass
        
        if setName:
            try:
                return {setName: cookies[setName]}
            
            except ValueError:
                print(f'Error: could not find {setName} cookie in any browser.')
                exit(1)
        
        else:
            return cookies

# Пример получения всех файлов cookie для домена "example.com"
cookies = Utils.get_cookies("example.com")
print(cookies)

# Пример получения конкретного cookie с именем "my_cookie" для домена "example.com"
my_cookie = Utils.get_cookies("example.com", setName="my_cookie")
print(my_cookie)

# Пример получения файлов cookie только из браузера Chrome для домена "example.com"
chrome_cookies = Utils.get_cookies("example.com", setBrowser="chrome")
print(chrome_cookies)