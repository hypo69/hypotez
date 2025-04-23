### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет утилиты для извлечения кукисов из различных веб-браузеров. Он использует библиотеку `browser_cookie3` для доступа к кукисам браузеров, таких как Chrome, Safari, Firefox, Edge, Opera, Brave, Opera GX и Vivaldi. Класс `Utils` содержит список поддерживаемых браузеров и метод `get_cookies` для получения кукисов для определенного домена.

Шаги выполнения
-------------------------
1. **Определение класса `Utils`**: Класс содержит статический список `browsers`, включающий функции для доступа к кукисам различных браузеров.
2. **Метод `get_cookies`**:
   - Принимает домен (`domain`), имя конкретного кукиса (`setName`, необязательный) и название конкретного браузера (`setBrowser`, необязательный).
   - Инициализирует пустой словарь `cookies` для хранения кукисов.
   - Если `setBrowser` указан, пытается получить кукисы только из указанного браузера.
   - Если `setBrowser` не указан, пытается получить кукисы из всех поддерживаемых браузеров.
   - Для каждого браузера перебирает кукисы, извлеченные для указанного домена, и добавляет их в словарь `cookies`, избегая дублирования.
   - Если `setName` указан, возвращает словарь, содержащий только указанный кукис. Если кукис не найден, выводит сообщение об ошибке и завершает программу.
   - Если `setName` не указан, возвращает словарь со всеми найденными кукисами.
   - Обрабатывает исключения, которые могут возникнуть при доступе к кукисам браузера.

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
domain = 'example.com'
cookies = Utils.get_cookies(domain)
print(cookies)

# Пример получения конкретного кукиса:
cookie_name = 'sessionid'
session_cookie = Utils.get_cookies(domain, setName=cookie_name)
print(session_cookie)

# Пример получения кукисов только из Chrome:
chrome_cookies = Utils.get_cookies(domain, setBrowser='chrome')
print(chrome_cookies)