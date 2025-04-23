# Документация для модуля `FastGpt.py`

## Обзор

Модуль `FastGpt.py` предоставляет реализацию провайдера `FastGpt` для работы с API `chat9.fastgpt.me`. Он позволяет отправлять запросы на создание завершений текста, поддерживает потоковую передачу ответов и предназначен для использования с моделями, совместимыми с `gpt-3.5-turbo`.

## Подробнее

Модуль содержит класс `FastGpt`, который наследуется от `AbstractProvider` и реализует метод `create_completion` для взаимодействия с API `FastGpt`. Класс определяет URL, указывает на необходимость аутентификации, поддерживает потоковую передачу и совместимость с `gpt-3.5-turbo`.

## Классы

### `FastGpt`

**Описание**: Класс `FastGpt` предоставляет методы для взаимодействия с API `chat9.fastgpt.me` для генерации текста.
**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL API `chat9.fastgpt.me`. Значение по умолчанию: `'https://chat9.fastgpt.me/'`.
- `working` (bool): Указывает, работает ли провайдер. Значение по умолчанию: `False`.
- `needs_auth` (bool): Указывает, требуется ли аутенентификация. Значение по умолчанию: `False`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу. Значение по умолчанию: `True`.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`. Значение по умолчанию: `True`.
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модель `gpt-4`. Значение по умолчанию: `False`.

**Методы**:
- `create_completion`: Метод для создания запроса на завершение текста.

## Методы класса

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool, **kwargs: Any) -> CreateResult:
    """ Функция создает запрос к API для генерации текста на основе предоставленных параметров.
    Args:
        model (str): Идентификатор используемой модели.
        messages (list[dict[str, str]]): Список сообщений для контекста генерации.
        stream (bool): Флаг, указывающий на необходимость потоковой передачи.
        **kwargs (Any): Дополнительные параметры запроса.

    Returns:
        CreateResult: Результат запроса к API.

    Как работает функция:
    - Функция `create_completion` принимает параметры, необходимые для создания запроса к API `FastGpt`.
    - Определяются заголовки запроса, включая `authority`, `accept`, `content-type` и другие.
    - Формируется JSON-тело запроса с сообщениями, моделью, параметрами температуры, штрафами и другими настройками.
    - Выбирается случайный поддомен из списка `['jdaen979ew', 'chat9']`.
    - Отправляется POST-запрос к API `FastGpt` с использованием библиотеки `requests`.
    - Если потоковая передача включена, функция итерируется по строкам ответа и извлекает содержимое (`content`) из каждой строки.
    - Извлеченное содержимое передается как токен с использованием `yield`.
    - В случае ошибок в процессе обработки ответа, они игнорируются.

    Пример:
        Пример вызова функции:

        model = "gpt-3.5-turbo"
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        stream = True
        kwargs = {"temperature": 0.7}
        result = FastGpt.create_completion(model=model, messages=messages, stream=stream, **kwargs)
        for token in result:
            print(token)
    """
```

## Параметры класса `FastGpt`
- `url` (str): URL API `chat9.fastgpt.me`. Значение по умолчанию: `'https://chat9.fastgpt.me/'`.
- `working` (bool): Указывает, работает ли провайдер. Значение по умолчанию: `False`.
- `needs_auth` (bool): Указывает, требуется ли аутентификация. Значение по умолчанию: `False`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу. Значение по умолчанию: `True`.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`. Значение по умолчанию: `True`.
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модель `gpt-4`. Значение по умолчанию: `False`.

## Примеры

```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True
kwargs = {"temperature": 0.7}
result = FastGpt.create_completion(model=model, messages=messages, stream=stream, **kwargs)
for token in result:
    print(token)