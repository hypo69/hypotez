# `Tab` Class Reference

Класс `Tab` — это основной интерфейс для автоматизации веб-страницы. Он управляет одной вкладкой браузера через Chrome DevTools Protocol (CDP), позволяя выполнять навигацию, манипулировать DOM, выполнять JavaScript, обрабатывать события, отслеживать сетевую активность и многое другое.

Экземпляры `Tab` управляются как синглтоны на основе `target_id`, гарантируя, что для каждой вкладки браузера существует только один объект `Tab`.

**Примечание по поиску элементов:** Этот класс наследуется от `FindElementsMixin`, что предоставляет ему методы для поиска элементов в DOM, такие как `find_element`, `find_elements`, `wait_for_element`, `find_or_wait_element` и другие.

---

## Свойства

### `page_events_enabled`
Определяет, включены ли события домена `Page` в CDP (загрузка, навигация, диалоги и т.д.).
- **Тип:** `bool`

### `network_events_enabled`
Определяет, включены ли события домена `Network` в CDP (запросы, ответы и т.д.).
- **Тип:** `bool`

### `fetch_events_enabled`
Определяет, включены ли события домена `Fetch` в CDP для перехвата запросов.
- **Тип:** `bool`

### `dom_events_enabled`
Определяет, включены ли события домена `DOM` в CDP (изменения в структуре документа).
- **Тип:** `bool`

### `runtime_events_enabled`
Определяет, включены ли события домена `Runtime` в CDP.
- **Тип:** `bool`

### `intercept_file_chooser_dialog_enabled`
Определяет, активен ли перехват диалоговых окон выбора файлов.
- **Тип:** `bool`

### `current_url`
Возвращает текущий URL страницы. Это свойство отражает перенаправления и навигацию на стороне клиента.
- **Тип:** `str`

### `page_source`
Возвращает полный HTML-код текущей страницы, отражающий живое состояние DOM.
- **Тип:** `str`

---

## Методы

### `enable_page_events()`
Включает события домена `Page` в CDP (загрузка, навигация, диалоги и т.д.). Необходимо для работы с диалогами и отслеживания событий загрузки.

### `enable_network_events()`
Включает события домена `Network` в CDP. Необходимо для отслеживания сетевых запросов, получения тел ответов и логов.

### `enable_fetch_events(handle_auth=False, resource_type=None, request_stage=None)`
Включает домен `Fetch` для перехвата сетевых запросов. Перехваченные запросы должны быть явно продолжены (`continue_request`), отклонены (`fail_request`) или выполнены (`fulfill_request`), иначе они зависнут.
- **Параметры:**
  - `handle_auth` (`bool`): Перехватывать ли запросы аутентификации.
  - `resource_type` (`Optional[ResourceType]`): Фильтровать перехватываемые запросы по типу ресурса (например, `ResourceType.DOCUMENT`).
  - `request_stage` (`Optional[RequestStage]`): На каком этапе перехватывать (запрос или ответ).

### `enable_dom_events()`
Включает события домена `DOM`, позволяя отслеживать изменения в структуре документа.

### `enable_runtime_events()`
Включает события домена `Runtime`, которые могут быть полезны для отладки и мониторинга выполнения JavaScript.

### `enable_intercept_file_chooser_dialog()`
Включает перехват диалоговых окон выбора файлов для автоматизации загрузки файлов. Для удобства используйте контекстный менеджер `expect_file_chooser`.

### `enable_auto_solve_cloudflare_captcha(custom_selector=None, time_before_click=2, time_to_wait_captcha=5)`
Включает автоматический обход капчи Cloudflare Turnstile. Метод устанавливает слушателя на событие загрузки страницы, который ищет и пытается решить капчу.
- **Параметры:**
  - `custom_selector` (`Optional[tuple[By, str]]`): Пользовательский селектор для поиска элемента капчи. По умолчанию ищет по классу `cf-turnstile`.
  - `time_before_click` (`int`): Задержка в секундах перед кликом по капче.
  - `time_to_wait_captcha` (`int`): Время ожидания появления капчи на странице.

### `disable_page_events()`
Отключает события домена `Page`.

### `disable_network_events()`
Отключает события домена `Network`.

### `disable_fetch_events()`
Отключает перехват запросов (домен `Fetch`).

### `disable_dom_events()`
Отключает события домена `DOM`.

### `disable_runtime_events()`
Отключает события домена `Runtime`.

### `disable_intercept_file_chooser_dialog()`
Отключает перехват диалоговых окон выбора файлов.

### `disable_auto_solve_cloudflare_captcha()`
Отключает автоматический обход капчи Cloudflare, удаляя ранее установленный слушатель событий.

### `close()`
Закрывает текущую вкладку браузера. После вызова этого метода экземпляр `Tab` становится недействительным.

### `get_frame(frame: WebElement)`
Возвращает новый объект `Tab` для взаимодействия с содержимым `iframe`.
- **Параметры:**
  - `frame` (`WebElement`): Веб-элемент, представляющий тег `<iframe>`.
- **Возвращает:**
  - `IFrame` (псевдоним `Tab`): Новый экземпляр `Tab`, настроенный для работы с `iframe`.
- **Вызывает:**
  - `NotAnIFrame`: Если переданный элемент не является `iframe`.
  - `InvalidIFrame`: Если у `iframe` отсутствует атрибут `src`.
  - `IFrameNotFound`: Если целевая вкладка для `iframe` не найдена.

### `get_cookies()`
Получает все cookie, доступные с текущей страницы.
- **Возвращает:**
  - `list[Cookie]`: Список объектов cookie.

### `get_network_response_body(request_id: str)`
Получает тело ответа для указанного сетевого запроса.
- **Параметры:**
  - `request_id` (`str`): ID запроса, который можно получить из сетевых событий.
- **Возвращает:**
  - `str`: Тело ответа.
- **Вызывает:**
  - `NetworkEventsNotEnabled`: Если сетевые события не были предварительно включены.

### `get_network_logs(filter: Optional[str] = None)`
Получает собранные сетевые логи.
- **Параметры:**
  - `filter` (`Optional[str]`): Строка для фильтрации логов по URL запроса.
- **Возвращает:**
  - `list[NetworkLog]`: Список логов сетевой активности.
- **Вызывает:**
  - `NetworkEventsNotEnabled`: Если сетевые события не были предварительно включены.

### `set_cookies(cookies: list[CookieParam])`
Устанавливает один или несколько cookie для текущего домена.
- **Параметры:**
  - `cookies` (`list[CookieParam]`): Список словарей с параметрами cookie. Обязательные поля: `name` и `value`.

### `delete_all_cookies()`
Удаляет все cookie из текущего контекста браузера.

### `go_to(url: str, timeout: int = 300)`
Переходит по указанному URL и ожидает полной загрузки страницы. Если URL совпадает с текущим, страница будет перезагружена.
- **Параметры:**
  - `url` (`str`): Целевой URL.
  - `timeout` (`int`): Максимальное время ожидания загрузки страницы в секундах.
- **Вызывает:**
  - `PageLoadTimeout`: Если страница не загрузилась в течение указанного времени.

### `refresh(ignore_cache: bool = False, script_to_evaluate_on_load: Optional[str] = None)`
Перезагружает текущую страницу и ожидает ее полной загрузки.
- **Параметры:**
  - `ignore_cache` (`bool`): Если `True`, кеш браузера будет проигнорирован.
  - `script_to_evaluate_on_load` (`Optional[str]`): JavaScript-код, который будет выполнен после загрузки страницы.
- **Вызывает:**
  - `PageLoadTimeout`: Если страница не загрузилась в течение установленного времени.

### `take_screenshot(path: Optional[str] = None, quality: int = 100, as_base64: bool = False)`
Делает скриншот текущей видимой области страницы.
- **Параметры:**
  - `path` (`Optional[str]`): Путь для сохранения файла. Расширение (`.png`, `.jpeg`, `.webp`) определяет формат.
  - `quality` (`int`): Качество изображения (0-100) для форматов `jpeg` и `webp`.
  - `as_base64` (`bool`): Если `True`, возвращает скриншот в виде строки Base64 вместо сохранения в файл.
- **Возвращает:**
  - `Optional[str]`: Строка Base64, если `as_base64=True`, иначе `None`.
- **Вызывает:**
  - `InvalidFileExtension`: Если расширение файла не поддерживается.
  - `ValueError`: Если `path` не указан и `as_base64=False`.

### `print_to_pdf(path: str, ..., as_base64: bool = False)`
Сохраняет текущую страницу в формате PDF.
- **Параметры:**
  - `path` (`str`): Путь для сохранения PDF-файла.
  - `landscape` (`bool`): Альбомная ориентация.
  - `display_header_footer` (`bool`): Отображать ли колонтитулы.
  - `print_background` (`bool`): Печатать ли фоновые изображения и цвета.
  - `scale` (`float`): Масштаб (от 0.1 до 2.0).
  - `as_base64` (`bool`): Если `True`, возвращает PDF в виде строки Base64.
- **Возвращает:**
  - `Optional[str]`: Строка Base64, если `as_base64=True`, иначе `None`.

### `has_dialog()`
Проверяет, открыто ли в данный момент диалоговое окно JavaScript (`alert`, `confirm`, `prompt`).
- **Примечание:** Требуется, чтобы события страницы были включены (`enable_page_events`).
- **Возвращает:**
  - `bool`: `True`, если диалог открыт.

### `get_dialog_message()`
Возвращает текст из текущего диалогового окна.
- **Возвращает:**
  - `str`: Сообщение диалога.
- **Вызывает:**
  - `NoDialogPresent`: Если диалоговое окно отсутствует.

### `handle_dialog(accept: bool, prompt_text: Optional[str] = None)`
Обрабатывает текущее диалоговое окно JavaScript.
- **Параметры:**
  - `accept` (`bool`): `True` для принятия (OK, Confirm), `False` для отмены (Cancel).
  - `prompt_text` (`Optional[str]`): Текст для ввода в диалоговое окно `prompt`.
- **Вызывает:**
  - `NoDialogPresent`: Если диалоговое окно отсутствует.

### `execute_script(script: str, element: Optional[WebElement] = None)`
Выполняет JavaScript-код в контексте страницы.
- **Вариант 1: Глобальное выполнение**
  - `execute_script(script: str)`
  - Выполняет скрипт в глобальном контексте.
- **Вариант 2: Выполнение в контексте элемента**
  - `execute_script(script: str, element: WebElement)`
  - Выполняет скрипт, где `element` доступен внутри скрипта через ключевое слово `argument`.
- **Параметры:**
  - `script` (`str`): JavaScript-код для выполнения.
  - `element` (`Optional[WebElement]`): Элемент, который будет контекстом выполнения (`argument`).
- **Вызывает:**
  - `InvalidScriptWithElement`: Если в скрипте есть `argument`, но элемент не передан.
- **Примеры:**
  ```python
  # Получить заголовок страницы
  title = await tab.execute_script("return document.title;")

  # Кликнуть по элементу
  button = await tab.find_element(By.ID, "my-button")
  await tab.execute_script("argument.click();", button)

  # Изменить значение поля ввода
  input_field = await tab.find_element(By.ID, "my-input")
  await tab.execute_script('argument.value = "Новый текст";', input_field)
  ```

### `continue_request(request_id: str, ...)`
Продолжает выполнение перехваченного сетевого запроса. Можно изменить параметры запроса.
- **Параметры:**
  - `request_id` (`str`): ID перехваченного запроса.
  - `url`, `method`, `post_data`, `headers`: Новые параметры запроса.

### `fail_request(request_id: str, error_reason: NetworkErrorReason)`
Отклоняет перехваченный сетевой запрос с указанной ошибкой.
- **Параметры:**
  - `request_id` (`str`): ID перехваченного запроса.
  - `error_reason` (`NetworkErrorReason`): Причина сбоя (например, `NetworkErrorReason.BLOCKED_BY_CLIENT`).

### `fulfill_request(request_id: str, response_code: int, ...)`
Подменяет ответ для перехваченного запроса, предоставляя свои данные.
- **Параметры:**
  - `request_id` (`str`): ID перехваченного запроса.
  - `response_code` (`int`): HTTP-код ответа (например, 200).
  - `response_headers`, `body`, `response_phrase`: Пользовательские данные ответа.

### `expect_file_chooser(files: Union[str, Path, list])`
Контекстный менеджер для автоматической обработки диалога выбора файлов.
- **Параметры:**
  - `files`: Путь к одному файлу или список путей к файлам для загрузки.
- **Пример:**
  ```python
  async with tab.expect_file_chooser("/path/to/my/file.txt"):
      # Этот клик должен открыть диалог выбора файла
      await tab.click("#upload-button")
  # Файл будет автоматически выбран
  ```

### `expect_and_bypass_cloudflare_captcha(...)`
Контекстный менеджер для временного включения автоматического обхода капчи Cloudflare. Удобен для операций, которые могут вызвать появление капчи.
- **Параметры:**
  - Аналогичны `enable_auto_solve_cloudflare_captcha`.
- **Пример:**
  ```python
  async with tab.expect_and_bypass_cloudflare_captcha():
      await tab.go_to("https://example.com/protected-page")
      # Капча, если появится, будет обработана автоматически
  ```

### `on(event_name: str, callback: Callable, temporary: bool = False)`
Регистрирует асинхронный или синхронный колбэк для прослушивания событий CDP.
- **Параметры:**
  - `event_name` (`str`): Имя события CDP (например, `Page.loadEventFired`, `Network.requestWillBeSent`).
  - `callback` (`Callable`): Функция, которая будет вызвана при возникновении события. Она получит словарь с данными события в качестве аргумента.
  - `temporary` (`bool`): Если `True`, колбэк будет удален после первого вызова.
- **Возвращает:**
  - `int`: ID колбэка, который можно использовать для его удаления вручную.
- **Примечание:** Соответствующий домен событий (`Page`, `Network` и т.д.) должен быть включен заранее.
- **Пример:**
  ```python
  async def on_request(event):
      print(f"Request sent to: {event['params']['request']['url']}")

  await tab.enable_network_events()
  callback_id = await tab.on("Network.requestWillBeSent", on_request)

  # ... ваш код ...

  # Позже можно удалить колбэк, если он не временный
  # await tab._connection_handler.remove_callback(callback_id)
  ```