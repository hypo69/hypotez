## Как использовать класс AliRequests
=========================================================================================

Описание
-------------------------
Класс `AliRequests`  предназначен для работы с API AliExpress. Он использует библиотеку `requests` для отправки запросов и хранит файлы `cookies` из браузера для авторизации. 

Шаги выполнения
-------------------------
1. **Инициализация класса:**
   - Создается экземпляр класса `AliRequests` с указанием типа браузера (`webdriver_for_cookies`)  для загрузки `cookies`.
   -  `cookies` загружаются из файла, находящегося в директории `src/utils/cookies/aliexpress.com/chrome/cookie`
   - Загруженные `cookies` добавляются в объект `requests.Session`  в качестве `self.cookies_jar`.
   - При каждом вызове `make_get_request`  обновляются `cookies` в `requests.Session`
   -  В методе `_refresh_session_cookies`  обновляется  `JSESSIONID`  и `cookies`  в `requests.Session`.
2. **Загрузка файлов `cookies`:**
   -  Функция `_load_webdriver_cookies_file`  загружает  `cookies` из файла с помощью `pickle.load`  и добавляет их в  `self.cookies_jar`.
   -  `cookies`  сохраняются в  `self.cookies_jar`  с помощью `RequestsCookieJar.set`.
   -  `cookies`  добавленные в  `self.cookies_jar`  используются при каждом вызове `make_get_request`.
3. **Обновление `cookies`:**
   -  `_refresh_session_cookies`  делает GET-запрос к  `https://portals.aliexpress.com`  и обновляет  `cookies`  в `self.cookies_jar`.
   - `_handle_session_id`  ищет  `JSESSIONID`  в  `cookies`  и обновляет его в `self.cookies_jar`.
4. **Отправка GET-запроса:**
   - `make_get_request`  отправляет GET-запрос к указанному  URL  с помощью `requests.Session.get`.
   - `headers`  и  `cookies`  используются для отправки запроса.
   - После успешной отправки запроса  `_handle_session_id`  обновляет  `JSESSIONID`  в `self.cookies_jar`.
5. **Сокращение ссылок:**
   - `short_affiliate_link`  сокращает ссылку с помощью  `https://portals.aliexpress.com/affiportals/web/link_generator.htm`  и возвращает  `requests.Response`  объект.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.alirequests import AliRequests

# Инициализация класса
ali_requests = AliRequests(webdriver_for_cookies='chrome')

# Отправка GET-запроса
url = 'https://www.aliexpress.com/wholesale?SearchText=phone+case'
response = ali_requests.make_get_request(url)

# Сокращение ссылки
link_url = 'https://www.aliexpress.com/item/1005002558149163.html'
short_link_response = ali_requests.short_affiliate_link(link_url)

# Обработка ответа
if response:
    print(f"Статус ответа: {response.status_code}")
    print(f"Текст ответа: {response.text}")
else:
    print("Ошибка при отправке запроса")

if short_link_response:
    print(f"Сокращенная ссылка: {short_link_response.url}")
else:
    print("Ошибка при сокращении ссылки")

```