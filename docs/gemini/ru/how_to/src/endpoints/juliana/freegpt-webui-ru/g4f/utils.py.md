## Как использовать блок кода `get_cookies`
=========================================================================================

Описание
-------------------------
Блок кода `get_cookies` позволяет получить куки из всех браузеров, установленных на устройстве. Функция принимает имя домена и опционально имя куки (setName) и имя браузера (setBrowser). Если имя куки задано, функция возвращает словарь с именем куки и её значением. Если имя куки не задано, функция возвращает словарь с именами всех куки и их значениями.

Шаги выполнения
-------------------------
1. Функция определяет список браузеров, для которых она может получить куки. Список браузеров включает в себя: Chrome, Safari, Firefox, Edge, Opera, Brave, Opera GX и Vivaldi. 
2. Если имя браузера задано, функция ищет куки в заданном браузере.
3. Если имя браузера не задано, функция ищет куки во всех браузерах.
4. Для каждого браузера функция получает список всех куки для заданного домена.
5. Для каждой куки функция проверяет, есть ли она уже в словаре cookies. Если нет, она добавляет куки в словарь. 
6. Если имя куки задано, функция возвращает словарь с именем куки и её значением.
7. Если имя куки не задано, функция возвращает словарь с именами всех куки и их значениями.


Пример использования
-------------------------

```python
from src.endpoints.juliana.freegpt-webui-ru.g4f.utils import Utils

# Получение всех куки для домена example.com
all_cookies = Utils.get_cookies(domain='example.com')
print(all_cookies)

# Получение куки с именем session_id для домена example.com
session_id_cookie = Utils.get_cookies(domain='example.com', setName='session_id')
print(session_id_cookie)

# Получение всех куки для домена example.com в браузере Chrome
chrome_cookies = Utils.get_cookies(domain='example.com', setBrowser='chrome')
print(chrome_cookies)
```