Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет утилиту для извлечения кукисов из различных веб-браузеров, установленных в системе. Он использует библиотеку `browser_cookie3` для доступа к кукисам браузеров, таких как Chrome, Safari, Firefox, Edge, Opera, Brave, Opera GX и Vivaldi. Функция `get_cookies` позволяет получить все кукисы для определенного домена или конкретный кукис по имени.

Шаги выполнения
-------------------------
1. **Импорт библиотек**: Импортируется библиотека `browser_cookie3` для работы с кукисами браузеров.
2. **Определение класса `Utils`**:
   - Создается класс `Utils`, который содержит список поддерживаемых браузеров и метод `get_cookies`.
   - Список `browsers` содержит функции для доступа к кукисам различных браузеров.
3. **Функция `get_cookies`**:
   - Принимает домен (`domain`), имя конкретного кукиса (`setName`, опционально) и имя браузера (`setBrowser`, опционально) в качестве аргументов.
   - Инициализирует пустой словарь `cookies` для хранения кукисов.
   - Если указан конкретный браузер (`setBrowser != False`):
     - Перебирает список браузеров и, если имя браузера совпадает с указанным, пытается извлечь кукисы для заданного домена.
     - Если браузер выдает исключение, оно игнорируется.
   - Если браузер не указан (`setBrowser == False`):
     - Перебирает все браузеры в списке и пытается извлечь кукисы для заданного домена.
     - Если браузер выдает исключение, оно игнорируется.
   - Если указано имя конкретного кукиса (`setName`):
     - Пытается вернуть только этот кукис из словаря `cookies`.
     - Если кукис с указанным именем не найден, выводит сообщение об ошибке и завершает программу.
   - Если имя кукиса не указано (`setName == None`):
     - Возвращает все кукисы, найденные для данного домена.

Пример использования
-------------------------

```python
import browser_cookie3

class Utils:
    browsers = [
        browser_cookie3.chrome,   # 62.74% market share
        browser_cookie3.safari,   # 24.12% market share
        browser_cookie3.firefox,  #  4.56% market share
        browser_cookie3.edge,     #  2.85% market share
        browser_cookie3.opera,    #  1.69% market share
        browser_cookie3.brave,    #  0.96% market share
        browser_cookie3.opera_gx, #  0.64% market share
        browser_cookie3.vivaldi,  #  0.32% market share
    ]

    def get_cookies(domain: str, setName: str = None, setBrowser: str = False) -> dict:
        cookies = {}

        if setBrowser != False:
            for browser in Utils.browsers:
                if browser.__name__ == setBrowser:
                    try:
                        for c in browser(domain_name=domain):
                            if c.name not in cookies:
                                cookies = cookies | {c.name: c.value}

                    except Exception as e:
                        pass

        else:
            for browser in Utils.browsers:
                try:
                    for c in browser(domain_name=domain):
                        if c.name not in cookies:
                            cookies = cookies | {c.name: c.value}

                except Exception as e:
                    pass

        if setName:
            try:
                return {setName: cookies[setName]}

            except ValueError:
                print(f'Error: could not find {setName} cookie in any browser.')
                exit(1)

        else:
            return cookies

# Пример использования:
# Получение всех кукисов для домена "example.com"
cookies = Utils.get_cookies("example.com")
print(cookies)

# Получение конкретного кукиса "sessionid" для домена "example.com"
session_cookie = Utils.get_cookies("example.com", setName="sessionid")
print(session_cookie)

# Получение кукисов только из браузера Chrome
chrome_cookies = Utils.get_cookies("example.com", setBrowser="chrome")
print(chrome_cookies)