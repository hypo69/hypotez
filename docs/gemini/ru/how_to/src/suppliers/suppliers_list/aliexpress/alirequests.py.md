### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `AliRequests`, который используется для выполнения HTTP-запросов к AliExpress с использованием библиотеки `requests`. Он включает в себя функциональность для управления cookies, обновления сессий и создания коротких партнерских ссылок.

Шаги выполнения
-------------------------
1. **Инициализация класса `AliRequests`**:
   - При создании экземпляра класса `AliRequests` происходит инициализация сессии `requests.Session()`, устанавливаются заголовки User-Agent и вызывается метод `_load_webdriver_cookies_file()` для загрузки cookies из файла, специфичного для указанного веб-драйвера.

2. **Загрузка cookies из файла**:
   - Метод `_load_webdriver_cookies_file()` пытается загрузить cookies из файла, расположенного в директории `gs.dir_cookies/aliexpress.com/{webdriver_for_cookies}/cookie`.
   - Cookies загружаются из файла, используя `pickle.load()`, и устанавливаются в `self.cookies_jar`.
   - После успешной загрузки вызывается метод `self._refresh_session_cookies()` для обновления cookies сессии.

3. **Обновление cookies сессии**:
   - Метод `_refresh_session_cookies()` выполняет GET-запрос к `https://portals.aliexpress.com` для обновления cookies сессии.
   - Если `self.cookies_jar` не пуст, cookies передаются в запросе.
   - После выполнения запроса вызывается метод `self._handle_session_id()` для обработки JSESSIONID.

4. **Обработка JSESSIONID**:
   - Метод `_handle_session_id()` проверяет наличие cookie с именем `JSESSIONID` в переданных cookies.
   - Если `JSESSIONID` найден и его значение отличается от текущего `self.session_id`, он обновляет `self.session_id` и устанавливает cookie в `self.cookies_jar`.

5. **Выполнение GET-запроса**:
   - Метод `make_get_request()` выполняет GET-запрос к указанному URL с использованием `requests.Session()`.
   - Cookies из `self.cookies_jar` добавляются в сессию перед выполнением запроса.
   - После выполнения запроса вызывается метод `self._handle_session_id()` для обработки JSESSIONID.
   - В случае успеха возвращает объект `requests.Response`, иначе возвращает `False`.

6. **Получение короткой партнерской ссылки**:
   - Метод `short_affiliate_link()` генерирует короткую партнерскую ссылку на основе переданного URL.
   - Использует метод `self.make_get_request()` для выполнения GET-запроса к AliExpress API.

Пример использования
-------------------------

```python
from src.suppliers.suppliers_list.aliexpress.alirequests import AliRequests

# Инициализация класса AliRequests
ali_requests = AliRequests(webdriver_for_cookies='chrome')

# URL для выполнения GET-запроса
url = 'https://aliexpress.com/some/path'

# Выполнение GET-запроса
response = ali_requests.make_get_request(url)

if response:
    print(f"Запрос выполнен успешно. Статус код: {response.status_code}")
    # Обработка данных из ответа
    data = response.text
else:
    print("Запрос не удался.")

# URL для получения короткой партнерской ссылки
link_url = 'https://aliexpress.com/product/1234567890'

# Получение короткой партнерской ссылки
short_link_response = ali_requests.short_affiliate_link(link_url)

if short_link_response:
    print(f"Короткая партнерская ссылка получена. Статус код: {short_link_response.status_code}")
    # Обработка данных из ответа
    short_link = short_link_response.url
    print(f"Короткая ссылка: {short_link}")
else:
    print("Не удалось получить короткую партнерскую ссылку.")