# Модуль `Wuguokai.py`

## Обзор

Модуль предоставляет класс `Wuguokai`, который является провайдером для взаимодействия с моделью GPT-3.5 Turbo через API `chat.wuguokai.xyz`.
Модуль использует библиотеку `requests` для выполнения HTTP-запросов и модуль `random` для генерации случайных идентификаторов пользователей.

## Подробней

Модуль `Wuguokai.py` предназначен для интеграции с сервисом `chat.wuguokai.xyz` с целью предоставления доступа к модели GPT-3.5 Turbo. Он содержит класс `Wuguokai`, который наследуется от `AbstractProvider` и реализует метод `create_completion` для отправки запросов к API и получения ответов.
Модуль определяет заголовки HTTP-запроса, формирует данные запроса, включая промпт и идентификатор пользователя, и обрабатывает ответ от API. В случае ошибки HTTP-запроса или некорректного ответа от API, модуль вызывает исключение.

## Классы

### `Wuguokai(AbstractProvider)`

**Описание**:
Класс `Wuguokai` является провайдером для взаимодействия с API `chat.wuguokai.xyz`. Он наследуется от `AbstractProvider` и реализует метод `create_completion` для отправки запросов и получения ответов от API.

**Наследует**:
`AbstractProvider` - базовый класс для всех провайдеров в проекте.

**Атрибуты**:
- `url` (str): URL-адрес API `chat.wuguokai.xyz`.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели GPT-3.5 Turbo.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.

**Методы**:
- `create_completion`: Отправляет запрос к API и возвращает ответ.

### `create_completion`

**Назначение**:
Метод `create_completion` отправляет запрос к API `chat.wuguokai.xyz` и возвращает ответ.

**Параметры**:
- `model` (str): Название модели, которую необходимо использовать.
- `messages` (list[dict[str, str]]): Список сообщений, составляющих контекст запроса.
- `stream` (bool): Флаг, указывающий на необходимость потоковой передачи данных.
- `kwargs` (Any): Дополнительные аргументы, такие как прокси-сервер.

**Возвращает**:
- `CreateResult`: Генератор, возвращающий части ответа от API.

**Вызывает исключения**:
- `Exception`: Если HTTP-запрос завершается с кодом ошибки, отличным от 200.

**Как работает функция**:

1.  **Формирование заголовков**: Определяются заголовки HTTP-запроса, включая `authority`, `accept`, `content-type`, `origin`, `referer` и `user-agent`.
2.  **Формирование данных запроса**: Создается словарь `data`, содержащий промпт, опции и идентификатор пользователя. Промпт формируется с использованием функции `format_prompt`.
3.  **Отправка запроса**: Выполняется POST-запрос к API `https://ai-api20.wuguokai.xyz/api/chat-process` с использованием библиотеки `requests`.
4.  **Обработка ответа**: Ответ от API разделяется на части с использованием разделителя "> 若回答失败请重试或多刷新几次界面后重试".
5.  **Генерация результата**: В случае успешного запроса (код 200) генерируется результат, содержащий части ответа от API. Если длина разделенного ответа больше 1, возвращается `_split[1]`, иначе возвращается `_split[0]`. В случае ошибки выбрасывается исключение.

**Внутренние функции**:
Внутри функции `create_completion` нет внутренних функций.

**ASCII flowchart**:

```
A: Формирование заголовков и данных запроса
↓
B: Отправка POST-запроса к API
↓
C: Проверка статуса ответа (response.status_code == 200)
│
├─── Да ───→ D: Разделение ответа и генерация результата
│           │
└─── Нет ───→ E: Выброс исключения
```

**Примеры**:

```python
# Пример вызова функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
stream = False
kwargs = {"proxy": {"http": "http://proxy.example.com", "https": "https://proxy.example.com"}}

result = Wuguokai.create_completion(model, messages, stream, **kwargs)
for chunk in result:
    print(chunk)
```
```python
# Пример вызова функции create_completion без использования прокси
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Как дела?"}]
stream = False
kwargs = {}

result = Wuguokai.create_completion(model, messages, stream, **kwargs)
for chunk in result:
    print(chunk)
```
```python
# Пример вызова функции create_completion с обработкой исключения
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
stream = False
kwargs = {}

try:
    result = Wuguokai.create_completion(model, messages, stream, **kwargs)
    for chunk in result:
        print(chunk)
except Exception as ex:
    print(f"Error: {ex}")
```