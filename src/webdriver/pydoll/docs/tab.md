
# `Tab` Class Reference

Класс `Tab` — это основной и наиболее важный интерфейс для автоматизации веб-страницы. Он управляет одной вкладкой браузера через Chrome DevTools Protocol (CDP), позволяя выполнять навигацию, манипулировать DOM, выполнять JavaScript, обрабатывать события, отслеживать сетевую активность и многое другое.

**Важно:** Класс `Tab` наследует всю функциональность от `FindElementsMixin`, предоставляя мощные методы для поиска элементов на странице, такие как `find` и `query`.

---

## Свойства

| Свойство                              | Тип      | Описание                                                                            |
| :------------------------------------ | :------- | :---------------------------------------------------------------------------------- |
| `current_url`                         | `str`    | Текущий URL страницы, включая перенаправления. (асинхронное)                      |
| `page_source`                         | `str`    | Полный HTML-код текущей страницы в реальном времени. (асинхронное)                  |
| `page_events_enabled`                 | `bool`   | `True`, если включены события домена `Page` (загрузка, диалоги).                    |
| `network_events_enabled`              | `bool`   | `True`, если включены события домена `Network` (запросы, ответы).                   |
| `fetch_events_enabled`                | `bool`   | `True`, если включен перехват запросов через домен `Fetch`.                         |
| `dom_events_enabled`                  | `bool`   | `True`, если включены события домена `DOM` (изменения структуры документа).         |
| `runtime_events_enabled`              | `bool`   | `True`, если включены события домена `Runtime`.                                     |
| `intercept_file_chooser_dialog_enabled` | `bool`   | `True`, если активен перехват диалоговых окон выбора файлов.                       |

---

## Методы поиска элементов (из `FindElementsMixin`)

Эти методы позволяют находить один или несколько `WebElement` на странице.

### `find(...)`

Находит элемент(ы) по комбинации HTML-атрибутов. Удобен для простых и читаемых поисковых запросов.

- **Параметры:**
  - `id`, `class_name`, `name`, `tag_name`, `text` (`Optional[str]`): Атрибуты для поиска.
  - `timeout` (`int`): Время ожидания элемента в секундах (0 - без ожидания).
  - `find_all` (`bool`): `True` для поиска всех элементов, `False` для первого.
  - `raise_exc` (`bool`): `True` для вызова исключения, если ничего не найдено.
  - `**attributes`: Дополнительные атрибуты (например, `aria_label="Close"`).

- **Возвращаемое значение:**

| `find_all` | `raise_exc` | Тип                                 | Описание                                                   |
| :--------- | :---------- | :---------------------------------- | :--------------------------------------------------------- |
| `False`    | `True`      | `WebElement`                        | Находит первый элемент, иначе вызывает исключение.         |
| `False`    | `False`     | `Optional[WebElement]`              | Находит первый элемент, иначе возвращает `None`.           |
| `True`     | `True`      | `list[WebElement]`                  | Находит все элементы, иначе вызывает исключение.           |
| `True`     | `False`     | `Optional[list[WebElement]]`        | Находит все элементы, возвращает список (может быть пустым).|

- **Примеры:**
  ```python
  # Найти кнопку по ID
  submit_button = await tab.find(id='submit-button')
  # Найти все ссылки с определенным классом, подождать до 5 секунд
  links = await tab.find(tag_name='a', class_name='external-link', find_all=True, timeout=5)
  ```

### `query(...)`

Находит элемент(ы) с помощью "сырого" CSS-селектора или XPath-выражения.

- **Параметры:**
  - `expression` (`str`): CSS-селектор или XPath-выражение.
- **Возвращаемое значение:** Аналогично методу `find`.

- **Примеры:**
  ```python
  # Поиск по CSS
  main_content = await tab.query('#main .article > p')
  # Поиск по XPath
  login_form = await tab.query('//form[@id="loginForm"]')
  ```
---

## Навигация

### `go_to(url: str, timeout: int = 300)`
Переходит по указанному URL и ожидает полной загрузки страницы.
- **Вызывает:** `PageLoadTimeout` при превышении времени ожидания.

### `refresh(...)`
Перезагружает текущую страницу и ожидает ее полной загрузки.
- **Вызывает:** `PageLoadTimeout` при превышении времени ожидания.

---
## Взаимодействие со страницей и контентом

### `take_screenshot(path: Optional[str] = None, ..., as_base64: bool = False)`
Делает скриншот видимой части страницы.
- **Параметры:**
  - `path`: Путь для сохранения файла (формат определяется расширением: `.png`, `.jpeg`, `.webp`).
  - `as_base64`: Если `True`, возвращает скриншот как строку Base64.
- **Возвращает:** `str` (Base64), если `as_base64=True`, иначе `None`.

### `print_to_pdf(path: str, ..., as_base64: bool = False)`
Сохраняет текущую страницу как PDF-файл.

### `execute_script(script: str, element: Optional[WebElement] = None)`
Выполняет JavaScript в контексте страницы.
- **Вариант 1: `execute_script(script)`** - выполняет скрипт в глобальном контексте.
- **Вариант 2: `execute_script(script, element)`** - выполняет скрипт в контексте элемента, где он доступен через `argument`.
- **Примеры:**
  ```python
  # Получить user agent
  user_agent = await tab.execute_script("return navigator.userAgent;")
  # Прокрутить элемент в видимую область
  el = await tab.find(id='footer')
  await tab.execute_script("argument.scrollIntoView();", el)
  ```
---

## Управление Cookies

### `get_cookies()`
Возвращает список всех cookie, доступных странице.

### `set_cookies(cookies: list[CookieParam])`
Устанавливает один или несколько cookie.

### `delete_all_cookies()`
Удаляет все cookie в текущем контексте браузера.

---

## Обработка диалоговых окон

**Примечание:** Требуется предварительно включить события `await tab.enable_page_events()`.

### `has_dialog()`
Проверяет, открыто ли диалоговое окно (`alert`, `confirm`, `prompt`).

### `get_dialog_message()`
Возвращает текст из открытого диалогового окна.
- **Вызывает:** `NoDialogPresent`, если диалога нет.

### `handle_dialog(accept: bool, prompt_text: Optional[str] = None)`
Принимает (`accept=True`) или отклоняет (`accept=False`) диалоговое окно.
- **`prompt_text`**: Текст для ввода в `prompt`.

---

## Работа с IFrame

### `get_frame(frame: WebElement)`
Возвращает новый экземпляр `Tab` для взаимодействия с содержимым `iframe`.
- **Параметры:** `frame` - `WebElement`, представляющий тег `<iframe>`.

---

## Сеть и перехват запросов

**Примечание:** Требуется предварительно включить соответствующий домен событий (`Network` или `Fetch`).

### `enable_network_events()` / `enable_fetch_events()`
Включают отслеживание или перехват сетевых запросов.

### `get_network_response_body(request_id: str)`
Получает тело ответа для запроса по его ID.

### `get_network_logs(filter: Optional[str] = None)`
Получает список сетевых логов, опционально фильтруя по URL.

### `continue_request(...)` / `fail_request(...)` / `fulfill_request(...)`
Управляют перехваченными запросами (продолжить, оборвать или подменить ответ).

---

## Обработка событий

### `on(event_name: str, callback: Callable, temporary: bool = False)`
Регистрирует функцию-обработчик для событий CDP.
- **`event_name`**: Имя события (например, `Page.loadEventFired`).
- **`callback`**: Функция, которая будет вызвана.
- **`temporary`**: `True`, если обработчик нужно удалить после первого срабатывания.

---

## Высокоуровневая автоматизация (Контекстные менеджеры)

### `expect_file_chooser(files: Union[str, Path, list])`
Контекстный менеджер, который автоматически обрабатывает диалог выбора файлов.
```python
async with tab.expect_file_chooser("/path/to/image.jpg"):
    await tab.click("#upload-button") # Этот клик откроет диалог
# Файл будет автоматически выбран
```

### `expect_and_bypass_cloudflare_captcha(...)`
Контекстный менеджер, который временно включает автоматический обход капчи Cloudflare Turnstile для блока кода.

---

## Управление вкладкой

### `close()`
Закрывает текущую вкладку браузера. Экземпляр `Tab` после этого становится недействительным.