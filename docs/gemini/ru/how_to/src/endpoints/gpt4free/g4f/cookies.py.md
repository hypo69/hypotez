Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для управления cookie-файлами, используемыми в проекте `hypotez`. Он предоставляет функции для загрузки, установки и чтения cookie из различных источников, включая браузеры и файлы. Код также включает конфигурацию для хранения и управления cookie.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
   - Импортируются модули `os`, `time`, `json`.
   - Пытается импортировать `user_config_dir` из `platformdirs` для определения каталога конфигурации пользователя.
   - Пытается импортировать модули для работы с cookie из различных браузеров (`chrome`, `chromium`, `opera`, `brave`, `edge`, `vivaldi`, `firefox`) из библиотеки `browser_cookie3`.
   - Определяется функция `g4f` для загрузки cookie из браузера "g4f", если он существует.
   - Определяется список `browsers`, содержащий функции для загрузки cookie из различных браузеров.
   - Импортируются пользовательские типы данных (`Dict`, `Cookies`) и исключения (`MissingRequirementsError`) из локальных модулей.
   - Импортируется модуль `debug` для логирования.

2. **Настройка конфигурации CookiesConfig**:
   - Создается класс `CookiesConfig` для хранения конфигурации cookie.
   - Определяются атрибуты класса: `cookies` (словарь для хранения cookie по доменам) и `cookies_dir` (каталог для хранения файлов cookie).

3. **Определение списка доменов DOMAINS**:
   - Определяется список `DOMAINS`, содержащий домены, для которых будут загружаться cookie.

4. **Функция get_cookies**:
   - Функция `get_cookies(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False, cache_result: bool = True) -> Dict[str, str]` загружает cookie для заданного домена.
   - Функция проверяет, есть ли cookie для данного домена в кэше (`CookiesConfig.cookies`). Если есть и `cache_result` равен `True`, функция возвращает cookie из кэша.
   - Если cookie в кэше нет или `cache_result` равен `False`, функция вызывает `load_cookies_from_browsers` для загрузки cookie из браузеров.
   - Загруженные cookie сохраняются в кэше (`CookiesConfig.cookies`), если `cache_result` равен `True`.

5. **Функция set_cookies**:
   - Функция `set_cookies(domain_name: str, cookies: Cookies = None) -> None` устанавливает cookie для заданного домена.
   - Если `cookies` передан, функция сохраняет его в `CookiesConfig.cookies`.
   - Если `cookies` не передан, функция удаляет cookie для заданного домена из `CookiesConfig.cookies`, если он там есть.

6. **Функция load_cookies_from_browsers**:
   - Функция `load_cookies_from_browsers(domain_name: str, raise_requirements_error: bool = True, single_browser: bool = False) -> Cookies` загружает cookie из различных браузеров.
   - Если библиотека `browser_cookie3` не установлена и `raise_requirements_error` равен `True`, функция вызывает исключение `MissingRequirementsError`.
   - Функция итерируется по списку браузеров (`browsers`) и пытается загрузить cookie для заданного домена из каждого браузера.
   - Если cookie успешно загружены, они добавляются в словарь `cookies`.
   - Если `single_browser` равен `True`, функция прекращает итерацию после загрузки cookie из первого браузера, вернувшего cookie.
   - Функция обрабатывает исключения, которые могут возникнуть при чтении cookie из браузеров, и логирует ошибки.

7. **Функции set_cookies_dir и get_cookies_dir**:
   - Функция `set_cookies_dir(dir: str) -> None` устанавливает каталог для хранения файлов cookie.
   - Функция `get_cookies_dir() -> str` возвращает текущий каталог для хранения файлов cookie.

8. **Функция read_cookie_files**:
   - Функция `read_cookie_files(dirPath: str = None)` читает cookie из файлов `.har` и `.json`, находящихся в указанном каталоге.
   - Функция проверяет права доступа к указанному каталогу.
   - Функция обходит файлы в указанном каталоге и ищет файлы с расширениями `.har` и `.json`.
   - Для каждого найденного `.har` файла функция пытается загрузить его содержимое как JSON и извлечь cookie из записей HAR.
   - Для каждого найденного `.json` файла функция пытается загрузить его содержимое как JSON и извлечь cookie из JSON.
   - Извлеченные cookie сохраняются в `CookiesConfig.cookies`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f import cookies

# Загрузка cookie для домена "example.com"
domain_name = "example.com"
cookies = cookies.get_cookies(domain_name)
print(f"Cookie для домена {domain_name}: {cookies}")

# Установка cookie для домена "example.com"
new_cookies = {"cookie1": "value1", "cookie2": "value2"}
cookies.set_cookies(domain_name, new_cookies)
print(f"Cookie установлены для домена {domain_name}")

# Чтение cookie из файлов в указанном каталоге
cookies_dir = "./cookies"
cookies.read_cookie_files(cookies_dir)
print(f"Cookie прочитаны из файлов в каталоге {cookies_dir}")

# Получение каталога для хранения файлов cookie
cookies_dir = cookies.get_cookies_dir()
print(f"Каталог для хранения файлов cookie: {cookies_dir}")