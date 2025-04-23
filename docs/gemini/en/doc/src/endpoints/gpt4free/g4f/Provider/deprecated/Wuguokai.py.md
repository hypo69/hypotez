# Module Wuguokai

## Обзор

Модуль предоставляет класс `Wuguokai`, который является провайдером для работы с языковой моделью. Он использует API `chat.wuguokai.xyz` для генерации ответов на основе входных сообщений. Модуль поддерживает модель `gpt-3.5-turbo`.

## Более подробная информация

Этот модуль предназначен для интеграции с сервисом `wuguokai.xyz`, предоставляющим доступ к языковым моделям. Он отправляет запросы к API этого сервиса и обрабатывает ответы для получения сгенерированного текста. В коде реализована функция для создания запросов к API с использованием библиотеки `requests`.

## Классы

### `Wuguokai`

**Описание**: Класс `Wuguokai` является провайдером для работы с API `chat.wuguokai.xyz`.

**Наследует**:
- `AbstractProvider`: Абстрактный класс, определяющий интерфейс для всех провайдеров.

**Атрибуты**:
- `url` (str): URL-адрес сервиса `chat.wuguokai.xyz`.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `working` (bool): Указывает, работает ли провайдер в данный момент.

**Принцип работы**:
Класс `Wuguokai` использует статический метод `create_completion` для отправки запросов к API `chat.wuguokai.xyz` и получения ответов. Запросы формируются на основе входных сообщений, а ответы возвращаются в виде генератора текста.

### Методы класса

#### `create_completion`

```python
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool,
    **kwargs: Any,
) -> CreateResult:
    """Функция отправляет запрос к API wuguokai.xyz и возвращает результат генерации текста.

    Args:
        model (str): Имя используемой модели.
        messages (list[dict[str, str]]): Список сообщений, используемых для формирования запроса.
        stream (bool): Флаг, указывающий, следует ли возвращать результат в виде потока.
        **kwargs (Any): Дополнительные параметры, такие как прокси.

    Returns:
        CreateResult: Результат генерации текста.

    Raises:
        Exception: Если возникает ошибка при выполнении запроса или обработке ответа.

    **Внутренние функции**:
        Отсутствуют

    **Принцип работы**:
    1. Формируются заголовки запроса (`headers`) и данные (`data`) для отправки к API.
    2. Выполняется POST-запрос к API `https://ai-api20.wuguokai.xyz/api/chat-process` с использованием библиотеки `requests`.
    3. Проверяется статус код ответа. Если статус код не равен 200, выбрасывается исключение.
    4. Разделяется текст ответа на части по разделителю "> 若回答失败请重试或多刷新几次界面后重试".
    5. Если разделение успешно, возвращается вторая часть, иначе - первая часть.

    """
```

#### Параметры `create_completion`

- `model` (str): Имя используемой модели.
- `messages` (list[dict[str, str]]): Список сообщений, используемых для формирования запроса.
- `stream` (bool): Флаг, указывающий, следует ли возвращать результат в виде потока.
- `**kwargs` (Any): Дополнительные параметры, такие как прокси.

#### Примеры `create_completion`

```python
# Пример вызова функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
stream = False
kwargs = {"proxy": {}}

result = Wuguokai.create_completion(model, messages, stream, **kwargs)
for item in result:
    print(item)
```
```python
# Пример вызова функции create_completion с прокси
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Как дела?"}]
stream = False
kwargs = {"proxy": {"http": "http://example.com:8080", "https": "https://example.com:8080"}}

result = Wuguokai.create_completion(model, messages, stream, **kwargs)
for item in result:
    print(item)
```