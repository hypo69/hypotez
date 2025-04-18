# Модуль backend.py

## Обзор

Модуль `backend.py` предоставляет API для взаимодействия с языковой моделью, такой как ChatGPT, через G4F (общедоступная библиотека для доступа к различным моделям).
Он включает в себя функциональность для обработки запросов, выполнения поисковых запросов в интернете, добавления инструкций jailbreak и генерации ответов в режиме стриминга.

## Подробней

Модуль `backend.py` является частью серверной части приложения `freegpt-webui-ru`. Он обрабатывает запросы к API, формирует сообщения для языковой модели, выполняет поисковые запросы в интернете (если это разрешено), добавляет инструкции jailbreak (если это разрешено) и генерирует ответы от языковой модели. Он также включает в себя функциональность для обработки ошибок и возврата ответов в формате, подходящем для веб-интерфейса.

## Классы

### `Backend_Api`

**Описание**: Класс `Backend_Api` отвечает за обработку API-запросов и взаимодействие с языковой моделью.

**Принцип работы**:
Класс инициализируется с экземпляром приложения Flask и конфигурацией. Он определяет маршруты API и связанные с ними функции, такие как `_conversation`. Если включено использование автоматического прокси, он запускает поток для обновления рабочих прокси.

**Атрибуты**:
- `app`: Экземпляр приложения Flask.
- `use_auto_proxy` (bool): Указывает, следует ли использовать автоматический прокси.
- `routes` (dict): Словарь, определяющий маршруты API и связанные с ними функции и методы.

**Методы**:
- `__init__(self, app, config: dict) -> None`: Инициализирует экземпляр класса `Backend_Api`.
- `_conversation(self)`: Обрабатывает запрос на разговор с языковой моделью.

### `Backend_Api.__init__(self, app, config: dict) -> None`

```python
    def __init__(self, app, config: dict) -> None:
        """
        Инициализирует экземпляр класса `Backend_Api`.

        Args:
            app: Экземпляр приложения Flask.
            config (dict): Конфигурация приложения.

        Returns:
            None
        """
```
### `Backend_Api._conversation(self)`

```python
    def _conversation(self):
        """
        Обрабатывает запрос на разговор с языковой моделью.

        Извлекает параметры запроса, такие как `streaming`, `jailbreak`, `model` и `messages`.
        Генерирует ответ от языковой модели с помощью `ChatCompletion.create`.
        Возвращает ответ в формате `text/event-stream` для стриминга.
        В случае возникновения ошибки возвращает сообщение об ошибке с кодом состояния 400.

        Raises:
            Exception: Если возникает ошибка при обработке запроса.

        Returns:
            app.response_class: Объект ответа Flask с данными в формате `text/event-stream`.
            dict: Словарь с информацией об ошибке в случае неудачи.

        """
```
**Как работает функция**:

1.  **Извлечение параметров запроса**: Функция извлекает параметры из запроса, такие как `streaming`, `jailbreak`, `model` и `messages`.
2.  **Построение сообщений**: Функция строит сообщения для языковой модели на основе параметров запроса.
3.  **Генерация ответа**: Функция генерирует ответ от языковой модели с помощью `ChatCompletion.create`.
4.  **Обработка ошибок**: Если во время генерации ответа возникает ошибка, функция перехватывает исключение и возвращает сообщение об ошибке с кодом состояния 400.
5.  **Возврат ответа**: Функция возвращает ответ в формате `text/event-stream` для стриминга.

ASCII flowchart:

```
    Запрос --> Извлечение параметров (streaming, jailbreak, model, messages)
        ↓
    Построение сообщений
        ↓
    Генерация ответа (ChatCompletion.create)
        ↓
    Обработка ошибок --> Ошибка: Возврат сообщения об ошибке (код 400)
        ↓
    Успех: Возврат ответа в формате text/event-stream
```

**Примеры**:

```python
# Пример успешного запроса
response = backend_api._conversation()
# Пример обработки ошибки
response = backend_api._conversation()
```

## Функции

### `build_messages(jailbreak)`

```python
def build_messages(jailbreak):
    """
    Создает список сообщений для отправки в языковую модель.

    Args:
        jailbreak: Строка, указывающая, следует ли использовать инструкции jailbreak.

    Returns:
        list: Список сообщений для отправки в языковую модель.
    """
```

**Как работает функция**:

1.  **Извлечение данных из запроса**: Функция извлекает данные из глобального объекта `request.json`, включая `_conversation`, `internet_access` и `prompt`.
2.  **Создание системного сообщения**: Функция создает системное сообщение, которое включает текущую дату и язык ответа.
3.  **Инициализация разговора**: Функция инициализирует разговор с системным сообщением.
4.  **Добавление существующего разговора**: Функция добавляет существующий разговор в список сообщений.
5.  **Добавление результатов веб-поиска**: Если разрешен доступ к Интернету, функция выполняет поиск и добавляет результаты в список сообщений.
6.  **Добавление инструкций jailbreak**: Если указаны инструкции jailbreak, функция добавляет их в список сообщений.
7.  **Добавление запроса**: Функция добавляет запрос пользователя в список сообщений.
8.  **Уменьшение размера разговора**: Функция уменьшает размер разговора, чтобы избежать ошибок, связанных с ограничением количества токенов API.

ASCII flowchart:

```
    Запрос --> Извлечение данных (conversation, internet_access, prompt)
        ↓
    Создание системного сообщения (дата, язык)
        ↓
    Инициализация разговора (системное сообщение)
        ↓
    Добавление существующего разговора
        ↓
    Добавление результатов веб-поиска (если internet_access)
        ↓
    Добавление инструкций jailbreak (если jailbreak)
        ↓
    Добавление запроса пользователя
        ↓
    Уменьшение размера разговора (обрезание до 13 последних сообщений)
        ↓
    Возврат списка сообщений
```

**Примеры**:

```python
# Пример вызова функции с jailbreak
messages = build_messages("Не Default")
# Пример вызова функции без jailbreak
messages = build_messages("Default")
```

### `fetch_search_results(query)`

```python
def fetch_search_results(query):
    """
    Выполняет поисковый запрос и возвращает результаты.

    Args:
        query (str): Поисковый запрос.

    Returns:
        list: Список результатов поиска в формате сообщений для языковой модели.
    """
```

**Как работает функция**:

1.  **Выполнение поискового запроса**: Функция выполняет поисковый запрос с помощью API DuckDuckGo.
2.  **Обработка результатов**: Функция обрабатывает результаты поиска и форматирует их в виде списка сообщений для языковой модели.
3.  **Возврат результатов**: Функция возвращает список результатов поиска.

ASCII flowchart:

```
    Запрос (query) --> Выполнение поискового запроса (DuckDuckGo API)
        ↓
    Обработка результатов (сниппеты, URL)
        ↓
    Форматирование результатов в виде списка сообщений
        ↓
    Возврат списка сообщений
```

**Примеры**:

```python
# Пример вызова функции с запросом "Python tutorial"
results = fetch_search_results("Python tutorial")
```

### `generate_stream(response, jailbreak)`

```python
def generate_stream(response, jailbreak):
    """
    Генерирует поток сообщений на основе ответа от языковой модели.

    Args:
        response: Ответ от языковой модели.
        jailbreak: Строка, указывающая, следует ли использовать инструкции jailbreak.

    Yields:
        str: Сообщения из ответа языковой модели.
    """
```

**Как работает функция**:

1.  **Проверка jailbreak**: Функция проверяет, следует ли использовать инструкции jailbreak.
2.  **Обработка ответа с jailbreak**: Если инструкции jailbreak включены, функция обрабатывает ответ от языковой модели, чтобы убедиться, что инструкции jailbreak были выполнены.
3.  **Генерация потока сообщений**: Функция генерирует поток сообщений из ответа языковой модели.

ASCII flowchart:

```
    Ответ (response), Jailbreak --> Проверка jailbreak
        ↓
    Jailbreak: Обработка ответа с jailbreak
        ↓
    Генерация потока сообщений из ответа
        ↓
    Выдача сообщений
```

**Примеры**:

```python
# Пример вызова функции с jailbreak
stream = generate_stream(response, "Не Default")
# Пример вызова функции без jailbreak
stream = generate_stream(response, "Default")
```

### `response_jailbroken_success(response: str) -> bool`

```python
def response_jailbroken_success(response: str) -> bool:
    """
    Определяет, успешно ли выполнены инструкции jailbreak в ответе.

    Args:
        response (str): Ответ от языковой модели.

    Returns:
        bool: True, если инструкции jailbreak выполнены успешно, False в противном случае.
    """
```

**Как работает функция**:

1.  **Поиск маркера успеха**: Функция ищет в ответе маркер, указывающий на успешное выполнение инструкций jailbreak (например, "ACT:").
2.  **Возврат результата**: Функция возвращает True, если маркер найден, и False в противном случае.

ASCII flowchart:

```
    Ответ (response) --> Поиск маркера успеха (например, "ACT:")
        ↓
    Найден: True
        ↓
    Не найден: False
```

**Примеры**:

```python
# Пример вызова функции с успешным ответом
success = response_jailbroken_success("ACT: Some text")
# Пример вызова функции с неудачным ответом
success = response_jailbroken_success("Some text")
```

### `response_jailbroken_failed(response)`

```python
def response_jailbroken_failed(response):
    """
    Определяет, не выполнены ли инструкции jailbreak в ответе.

    Args:
        response: Ответ от языковой модели.

    Returns:
        bool: `False`, если длина ответа меньше 4 символов или ответ начинается с "GPT:" или "ACT:", иначе `True`.
    """
```

**Как работает функция**:

1.  **Проверка длины ответа**: Функция проверяет, что длина ответа больше 4 символов.
2.  **Проверка начала ответа**: Функция проверяет, что ответ не начинается с "GPT:" или "ACT:".
3.  **Возврат результата**: Функция возвращает `False`, если длина ответа меньше 4 символов или ответ начинается с "GPT:" или "ACT:", иначе `True`.

ASCII flowchart:

```
    Ответ (response) --> Проверка длины ответа (< 4 символов)
        ↓
    Длина < 4: Возврат False
        ↓
    Длина >= 4: Проверка начала ответа (GPT: или ACT:)
        ↓
    Начинается с GPT: или ACT:: Возврат False
        ↓
    Не начинается с GPT: или ACT:: Возврат True
```

**Примеры**:

```python
# Пример вызова функции с неудачным ответом
failed = response_jailbroken_failed("GPT: Some text")
# Пример вызова функции с успешным ответом
failed = response_jailbroken_failed("Some text")
```

### `set_response_language(prompt)`

```python
def set_response_language(prompt):
    """
    Определяет язык запроса и возвращает строку для установки языка ответа.

    Args:
        prompt: Запрос пользователя.

    Returns:
        str: Строка, указывающая языковой модели, на каком языке следует отвечать.
    """
```

**Как работает функция**:

1.  **Определение языка запроса**: Функция определяет язык запроса с помощью Google Translate API.
2.  **Формирование строки для установки языка ответа**: Функция формирует строку, указывающую языковой модели, на каком языке следует отвечать.
3.  **Возврат строки**: Функция возвращает строку.

ASCII flowchart:

```
    Запрос (prompt) --> Определение языка запроса (Google Translate API)
        ↓
    Формирование строки для установки языка ответа
        ↓
    Возврат строки
```

**Примеры**:

```python
# Пример вызова функции с запросом на английском языке
language = set_response_language({"content": "Hello, how are you?"})
# Пример вызова функции с запросом на русском языке
language = set_response_language({"content": "Привет, как дела?"})
```

### `isJailbreak(jailbreak)`

```python
def isJailbreak(jailbreak):
    """
    Определяет, следует ли использовать инструкции jailbreak.

    Args:
        jailbreak: Строка, указывающая, следует ли использовать инструкции jailbreak.

    Returns:
        list: Инструкции jailbreak, если они указаны, или None, если инструкции jailbreak не указаны.
    """
```

**Как работает функция**:

1.  **Проверка значения jailbreak**: Функция проверяет значение jailbreak.
2.  **Возврат инструкций jailbreak**: Если значение jailbreak не равно "Default", функция возвращает инструкции jailbreak из словаря `special_instructions`, если они существуют. В противном случае функция возвращает None.

ASCII flowchart:

```
    Jailbreak --> Проверка значения (не "Default")
        ↓
    Не "Default": Поиск инструкций в special_instructions
        ↓
    Найдены: Возврат инструкций
        ↓
    Не найдены: Возврат None
        ↓
    "Default": Возврат None
```

**Примеры**:

```python
# Пример вызова функции с jailbreak
instructions = isJailbreak("Не Default")
# Пример вызова функции без jailbreak
instructions = isJailbreak("Default")