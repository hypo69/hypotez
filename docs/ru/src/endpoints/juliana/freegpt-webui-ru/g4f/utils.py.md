# Модуль `utils`

## Обзор

Модуль `utils` предназначен для получения cookies из различных браузеров для заданного домена.

## Подробнее

Модуль содержит класс `Utils` с методом `get_cookies`, который позволяет извлекать cookies из поддерживаемых браузеров. Он использует библиотеку `browser_cookie3` для доступа к cookies браузеров. Модуль полезен для автоматизации задач, требующих аутентификации через cookies, например, для парсинга веб-страниц или тестирования веб-приложений.

## Классы

### `Utils`

**Описание**: Класс `Utils` предоставляет статический метод для получения cookies из различных браузеров.

**Атрибуты**:
- `browsers (list)`: Список функций из `browser_cookie3`, представляющих различные браузеры.

**Методы**:
- `get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict`: Получает cookies для заданного домена из указанных или всех поддерживаемых браузеров.

## Методы класса

### `get_cookies`

```python
def get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict:
    """ Функция извлекает cookies для заданного домена из различных браузеров.

    Args:
        domain (str): Домен, для которого требуется извлечь cookies.
        setName (str, optional): Имя конкретной cookie, которую нужно извлечь. По умолчанию `None`, что означает извлечение всех cookies для домена.
        setBrowser (str, optional): Имя конкретного браузера, из которого нужно извлечь cookies. Если `False`, cookies извлекаются из всех поддерживаемых браузеров. По умолчанию `False`.

    Returns:
        dict: Словарь, содержащий извлеченные cookies. Ключами словаря являются имена cookies, а значениями - их значения.
             Если указано `setName`, возвращается словарь только с этой cookie.
             Если cookie с указанным именем не найдена, функция выводит сообщение об ошибке и завершает работу.

    Raises:
        ValueError: Если указанное имя cookie (`setName`) не найдено ни в одном из браузеров.
        Exception: Обрабатываются исключения, которые могут возникнуть при доступе к cookies браузеров.

    
    - Инициализирует пустой словарь `cookies` для хранения извлеченных cookies.
    - Если указан параметр `setBrowser`, функция пытается получить cookies только из указанного браузера.
    - Если параметр `setBrowser` не указан, функция перебирает все поддерживаемые браузеры и пытается получить cookies из каждого.
    - Для каждого браузера функция перебирает все cookies, найденные для заданного домена, и добавляет их в словарь `cookies`, если их там еще нет.
    - Если указан параметр `setName`, функция пытается вернуть словарь, содержащий только cookie с указанным именем. Если cookie не найдена, выводится сообщение об ошибке и происходит выход из программы.
    - Если параметр `setName` не указан, функция возвращает словарь со всеми найденными cookies.

    Примеры:
        >>> # Получение всех cookies для домена "example.com"
        >>> cookies = Utils.get_cookies("example.com")
        >>> print(cookies)
        {'cookie1': 'value1', 'cookie2': 'value2', ...}

        >>> # Получение cookie с именем "sessionid" для домена "example.com"
        >>> cookies = Utils.get_cookies("example.com", setName="sessionid")
        >>> print(cookies)
        {'sessionid': '1234567890'}

        >>> # Получение cookies только из браузера Chrome для домена "example.com"
        >>> cookies = Utils.get_cookies("example.com", setBrowser="chrome")
        >>> print(cookies)
        {'cookie1': 'value1', 'cookie2': 'value2', ...}
    """
    cookies = {}

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

        except ValueError as ex:
            print(f'Error: could not find {setName} cookie in any browser.')
            exit(1)

    else:
        return cookies
```

## Параметры класса

- `browsers (list)`: Список функций для получения cookies из разных браузеров. Содержит функции:
  - `browser_cookie3.chrome`: Для получения cookies из браузера Chrome.
  - `browser_cookie3.safari`: Для получения cookies из браузера Safari.
  - `browser_cookie3.firefox`: Для получения cookies из браузера Firefox.
  - `browser_cookie3.edge`: Для получения cookies из браузера Edge.
  - `browser_cookie3.opera`: Для получения cookies из браузера Opera.
  - `browser_cookie3.brave`: Для получения cookies из браузера Brave.
  - `browser_cookie3.opera_gx`: Для получения cookies из браузера Opera GX.
  - `browser_cookie3.vivaldi`: Для получения cookies из браузера Vivaldi.