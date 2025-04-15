### **Системные инструкции для обработки кода проекта `hypotez`**

=========================================================================================

Описание функциональности и правил для генерации, анализа и улучшения кода. Направлено на обеспечение последовательного и читаемого стиля кодирования, соответствующего требованиям.

---

### **Основные принципы**

#### **1. Общие указания**:
- Соблюдай четкий и понятный стиль кодирования.
- Все изменения должны быть обоснованы и соответствовать установленным требованиям.

#### **2. Комментарии**:
- Используй `#` для внутренних комментариев.
- Документация всех функций, методов и классов должна следовать такому формату: 
    ```python
        def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:
            """ 
            Args:
                param (str): Описание параметра `param`.
                param1 (Optional[str | dict | str], optional): Описание параметра `param1`. По умолчанию `None`.
    
            Returns:
                dict | None: Описание возвращаемого значения. Возвращает словарь или `None`.
    
            Raises:
                SomeError: Описание ситуации, в которой возникает исключение `SomeError`.

            Ехаmple:
                >>> function('param', 'param1')
                {'param': 'param1'}
            """
    ```
- Комментарии и документация должны быть четкими, лаконичными и точными.

#### **3. Форматирование кода**:
- Используй одинарные кавычки. `a:str = 'value'`, `print('Hello World!')`;
- Добавляй пробелы вокруг операторов. Например, `x = 5`;
- Все параметры должны быть аннотированы типами. `def function(param: str, param1: Optional[str | dict | str] = None) -> dict | None:`;
- Не используй `Union`. Вместо этого используй `|`.

#### **4. Логирование**:
- Для логгирования Всегда Используй модуль `logger` из `src.logger.logger`.
- Ошибки должны логироваться с использованием `logger.error`.
Пример:
    ```python
        try:
            ...
        except Exception as ex:
            logger.error('Error while processing data', ех, exc_info=True)
    ```
#### **5 Не используй `Union[]` в коде. Вместо него используй `|`
Например:
```python
x: str | int ...
```




---

### **Основные требования**:

#### **1. Формат ответов в Markdown**:
- Все ответы должны быть выполнены в формате **Markdown**.

#### **2. Формат комментариев**:
- Используй указанный стиль для комментариев и документации в коде.
- Пример:

```python
from typing import Generator, Optional, List
from pathlib import Path


def read_text_file(
    file_path: str | Path,
    as_list: bool = False,
    extensions: Optional[List[str]] = None,
    chunk_size: int = 8192,
) -> Generator[str, None, None] | str | None:
    """
    Считывает содержимое файла (или файлов из каталога) с использованием генератора для экономии памяти.

    Args:
        file_path (str | Path): Путь к файлу или каталогу.
        as_list (bool): Если `True`, возвращает генератор строк.
        extensions (Optional[List[str]]): Список расширений файлов для чтения из каталога.
        chunk_size (int): Размер чанков для чтения файла в байтах.

    Returns:
        Generator[str, None, None] | str | None: Генератор строк, объединенная строка или `None` в случае ошибки.

    Raises:
        Exception: Если возникает ошибка при чтении файла.

    Example:
        >>> from pathlib import Path
        >>> file_path = Path('example.txt')
        >>> content = read_text_file(file_path)
        >>> if content:
        ...    print(f'File content: {content[:100]}...')
        File content: Example text...
    """
    ...
```
- Всегда делай подробные объяснения в комментариях. Избегай расплывчатых терминов, 
- таких как *«получить»* или *«делать»*. Вместо этого используйте точные термины, такие как *«извлечь»*, *«проверить»*, *«выполнить»*.
- Вместо: *«получаем»*, *«возвращаем»*, *«преобразовываем»* используй имя объекта *«функция получае»*, *«переменная возвращает»*, *«код преобразовывает»* 
- Комментарии должны непосредственно предшествовать описываемому блоку кода и объяснять его назначение.

#### **3. Пробелы вокруг операторов присваивания**:
- Всегда добавляйте пробелы вокруг оператора `=`, чтобы повысить читаемость.
- Примеры:
  - **Неправильно**: `x=5`
  - **Правильно**: `x = 5`

#### **4. Использование `j_loads` или `j_loads_ns`**:
- Для чтения JSON или конфигурационных файлов замените стандартное использование `open` и `json.load` на `j_loads` или `j_loads_ns`.
- Пример:

```python
# Неправильно:
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Правильно:
data = j_loads('config.json')
```

#### **5. Сохранение комментариев**:
- Все существующие комментарии, начинающиеся с `#`, должны быть сохранены без изменений в разделе «Улучшенный код».
- Если комментарий кажется устаревшим или неясным, не изменяйте его. Вместо этого отметьте его в разделе «Изменения».

#### **6. Обработка `...` в коде**:
- Оставляйте `...` как указатели в коде без изменений.
- Не документируйте строки с `...`.
```

#### **7. Аннотации**
Для всех переменных должны быть определены аннотации типа. 
Для всех функций все входные и выходные параметры аннотириваны
Для все параметров должны быть аннотации типа.


### **8. webdriver**
В коде используется webdriver. Он импртируется из модуля `webdriver` проекта `hypotez`
```python
from src.webdirver import Driver, Chrome, Firefox, Playwright, ...
driver = Driver(Firefox)

Пoсле чего может использоваться как

close_banner = {
  "attribute": null,
  "by": "XPATH",
  "selector": "//button[@id = 'closeXButton']",
  "if_list": "first",
  "use_mouse": false,
  "mandatory": false,
  "timeout": 0,
  "timeout_for_event": "presence_of_element_located",
  "event": "click()",
  "locator_description": "Закрываю pop-up окно, если оно не появилось - не страшно (`mandatory`:`false`)"
}

result = driver.execute_locator(close_banner)
```

### Анализ кода `hypotez/src/endpoints/bots/telegram/webhooks.py`

#### 1. Блок-схема

```mermaid
graph LR
    A[Начало: Прием HTTP запроса от Telegram] --> B{Обработка запроса telegram_webhook};
    B --> C[Запуск асинхронной функции telegram_webhook_async];
    C --> D{Извлечение данных из запроса};
    D --> E{Асинхронная обработка application};
    E --> F{Декодирование JSON из запроса};
    F -- Успешно --> G{Создание объекта Update};
    G --> H{Обработка обновления application.process_update(update)};
    H --> I[Отправка HTTP ответа 200];
    F -- Ошибка JSONDecodeError --> J[Логирование ошибки JSON];
    J --> K[Отправка HTTP ответа 400];
    E -- Exception --> L[Логирование общей ошибки];
    L --> M[Отправка HTTP ответа 500];
    I --> Z[Конец обработки];
    K --> Z;
    M --> Z;
```

**Примеры для логических блоков:**

*   **A**: Пользователь отправил сообщение боту в Telegram. Telegram отправляет HTTP POST запрос на настроенный webhook URL.
*   **B**: Функция `telegram_webhook` принимает HTTP запрос и экземпляр `Application` Telegram бота.
*   **C**: Асинхронная функция `telegram_webhook_async` обрабатывает запрос.
*   **D**: Извлечение данных из тела запроса для дальнейшей обработки.
*   **E**: `application` - это контекстный менеджер, обеспечивающий правильную инициализацию и завершение работы `Application` Telegram бота.
*   **F**: Если запрос содержит некорректный JSON, выбрасывается исключение `json.JSONDecodeError`.
*   **G**: Создается объект `Update` из JSON данных, используя метод `de_json`.
*   **H**: `application.process_update(update)` обрабатывает полученное обновление (сообщение, команду и т.д.).
*   **I**: В случае успешной обработки, отправляется HTTP ответ со статусом 200.
*   **J**: В случае ошибки декодирования JSON, логируется ошибка.
*   **K**: Отправляется HTTP ответ со статусом 400 и описанием ошибки.
*   **L**: В случае любой другой ошибки при обработке, она логируется.
*   **M**: Отправляется HTTP ответ со статусом 500 и описанием ошибки.

#### 2. Диаграмма

```mermaid
graph TD
    A[Прием HTTP запроса] --> B(telegram_webhook);
    B --> C(telegram_webhook_async);
    C --> D{request.json()};
    D --> E{Update.de_json()};
    E --> F{application.process_update()};
    F --> G[Response(status_code=200)];
    D -- Ошибка --> H[logger.error("Error decoding JSON")];
    H --> I[Response(status_code=400)];
    F -- Ошибка --> J[logger.error("Error processing webhook")];
    J --> K[Response(status_code=500)];
    G --> L[Завершение];
    I --> L;
    K --> L;
    classDef important fill:#f9f,stroke:#333,stroke-width:2px;
    class B,C important
```

**Объяснение зависимостей:**

*   `fastapi.Request`: Используется для получения входящего HTTP запроса.
*   `fastapi.Response`: Используется для отправки HTTP ответа.
*   `telegram.Update`: Используется для представления обновления (сообщения, команды и т.д.) от Telegram.
*   `telegram.ext.Application`: Используется для управления ботом Telegram.
*   `src.logger.logger`: Используется для логирования ошибок и отладочной информации.
*   `json`: Используется для работы с JSON-данными.
*   `asyncio`: Используется для асинхронного выполнения кода.

#### 3. Объяснение

**Импорты:**

*   `import asyncio`: Модуль для поддержки асинхронного программирования. Позволяет выполнять несколько задач одновременно.
*   `from fastapi import Request, Response`: Импортирует классы `Request` и `Response` из библиотеки `fastapi`. `Request` используется для получения данных входящего HTTP запроса, `Response` - для отправки HTTP ответа.
*   `from telegram import Update`: Импортирует класс `Update` из библиотеки `telegram`. `Update` представляет собой обновление, полученное от Telegram (например, новое сообщение).
*   `from telegram.ext import Application`: Импортирует класс `Application` из библиотеки `telegram.ext`. `Application` используется для управления Telegram ботом.
*   `import json`: Модуль для работы с данными в формате JSON.
*   `from src.logger import logger`: Импортирует объект `logger` из модуля `src.logger.logger`. Используется для логирования ошибок и отладочной информации.

**Функции:**

*   `telegram_webhook(request: Request, application: Application)`:
    *   **Аргументы:**
        *   `request (Request)`: Объект HTTP запроса от FastAPI.
        *   `application (Application)`: Объект `Application` из библиотеки `telegram.ext`.
    *   **Возвращаемое значение:** Нет явного возвращаемого значения.
    *   **Назначение:** Функция-обертка, запускающая асинхронную функцию `telegram_webhook_async` в синхронном контексте с помощью `asyncio.run`.
    *   **Пример:** `telegram_webhook(request, application)`
*   `async def telegram_webhook_async(request: Request, application: Application)`:
    *   **Аргументы:**
        *   `request (Request)`: Объект HTTP запроса от FastAPI.
        *   `application (Application)`: Объект `Application` из библиотеки `telegram.ext`.
    *   **Возвращаемое значение:** `Response`
    *   **Назначение:** Асинхронная функция, обрабатывающая входящий HTTP запрос от Telegram. Извлекает JSON из запроса, создает объект `Update` и обрабатывает его с помощью `application.process_update`. В случае успеха возвращает HTTP ответ со статусом 200. В случае ошибки логирует ошибку и возвращает HTTP ответ с кодом 400 или 500.
    *   **Пример:**
        ```python
        async def handle_telegram_message(request: Request, application: Application):
            try:
                data = await request.json()
                async with application:
                    update = Update.de_json(data, application.bot)
                    await application.process_update(update)
                return Response(status_code=200)
            except json.JSONDecodeError as ex:
                logger.error(f'Error decoding JSON: {ex}')
                return Response(status_code=400, content=f'Invalid JSON: {ex}')
            except Exception as ex:
                logger.error(f'Error processing webhook: {type(ex)} - {ex}')
                return Response(status_code=500, content=f'Error processing webhook: {ex}')

        ```

**Переменные:**

*   `request (Request)`: Объект HTTP запроса, содержащий данные от Telegram.
*   `application (Application)`: Объект `Application`, представляющий Telegram бота.
*   `data (dict)`: Словарь, полученный после декодирования JSON из тела запроса.
*   `update (Update)`: Объект `Update`, представляющий обновление от Telegram.
*   `ex (json.JSONDecodeError, Exception)`: Объект исключения, возникшего при обработке запроса.

**Потенциальные ошибки и области для улучшения:**

*   Функция `telegram_webhook` запускает асинхронную функцию `telegram_webhook_async` с помощью `asyncio.run`. Это блокирует event loop FastAPI, что может негативно сказаться на производительности. Рекомендуется использовать `await` для запуска `telegram_webhook_async` непосредственно в FastAPI handler.
*   Не хватает обработки конкретных типов исключений при обработке `application.process_update(update)`. Желательно добавить обработку исключений, специфичных для библиотеки `telegram`.
*   Не хватает валидации входящего запроса. Необходимо проверять, что запрос действительно пришел от Telegram, чтобы избежать несанкционированного доступа.

**Цепочка взаимосвязей с другими частями проекта:**

*   `src.logger.logger`: Используется для логирования ошибок и отладочной информации. Это позволяет отслеживать проблемы, возникающие при обработке webhook запросов.
*   Данный модуль является частью endpoints для обработки запросов от Telegram, что является внешним интерфейсом для взаимодействия с ботом.

```mermaid
flowchart TD
    Start --> TelegramWebhook[<code>telegram_webhook</code><br>Обработка HTTP запроса от Telegram]
    TelegramWebhook --> TelegramWebhookAsync[<code>telegram_webhook_async</code><br>Асинхронная обработка запроса]
    TelegramWebhookAsync --> RequestJson[<code>request.json()</code><br>Получение JSON из запроса]
    RequestJson -- Успех --> UpdateDeJson[<code>Update.de_json()</code><br>Создание объекта Update]
    UpdateDeJson --> ApplicationProcessUpdate[<code>application.process_update()</code><br>Обработка обновления]
    ApplicationProcessUpdate --> Response200[<code>Response(status_code=200)</code><br>Успешный ответ]
    RequestJson -- Ошибка JSONDecodeError --> LoggerErrorJSON[<code>logger.error("Error decoding JSON")</code><br>Логирование ошибки JSON]
    LoggerErrorJSON --> Response400[<code>Response(status_code=400)</code><br>Ошибка в запросе]
    ApplicationProcessUpdate -- Ошибка Exception --> LoggerErrorWebhook[<code>logger.error("Error processing webhook")</code><br>Логирование ошибки webhook]
    LoggerErrorWebhook --> Response500[<code>Response(status_code=500)</code><br>Ошибка сервера]
    Response200 --> End
    Response400 --> End
    Response500 --> End
    End[Конец обработки]