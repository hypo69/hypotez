# Модуль `EasyChat`

## Обзор

Модуль `EasyChat` предоставляет интерфейс для взаимодействия с сервисом EasyChat для создания завершений текста на основе предоставленных сообщений. Он поддерживает потоковую передачу ответов и использует модель `gpt-3.5-turbo`.

## Более детально

Этот модуль предназначен для интеграции с сервисом EasyChat, который предоставляет API для генерации текста на основе моделей машинного обучения. Модуль содержит класс `EasyChat`, который наследуется от `AbstractProvider` и реализует метод `create_completion` для отправки запросов к API EasyChat и получения ответов.

## Классы

### `EasyChat`

**Описание**: Класс для взаимодействия с сервисом EasyChat.

**Наследуется**:
- `AbstractProvider`: Абстрактный базовый класс для провайдеров.

**Атрибуты**:
- `url` (str): URL-адрес сервиса EasyChat. По умолчанию `"https://free.easychat.work"`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу ответов. По умолчанию `True`.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`. По умолчанию `True`.
- `working` (bool): Указывает, работает ли провайдер. По умолчанию `False`.

**Принцип работы**:
1. Класс `EasyChat` инициализируется с URL-адресом сервиса EasyChat и флагами поддержки потоковой передачи и модели `gpt-3.5-turbo`.
2. Метод `create_completion` отправляет POST-запрос к API EasyChat с предоставленными сообщениями и параметрами.
3. Если `stream` установлен в `True`, ответы передаются потоком. В противном случае возвращается полный ответ.

## Методы класса

### `create_completion`

```python
    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        """ Функция отправляет запрос к API EasyChat и возвращает завершение текста.

        Args:
            model (str): Имя используемой модели.
            messages (list[dict[str, str]]): Список сообщений для отправки.
            stream (bool): Указывает, следует ли использовать потоковую передачу ответов.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            CreateResult: Результат создания завершения текста.

        Raises:
            Exception: Если возникает ошибка при отправке запроса или получении ответа.

        Как работает функция:
        - Функция выбирает случайный активный сервер из списка.
        - Функция формирует заголовки запроса, включая информацию о браузере и типе контента.
        - Функция формирует JSON-данные запроса, включая сообщения, параметры модели и флаги.
        - Функция создает сессию requests и отправляет POST-запрос к API EasyChat.
        - Если статус код ответа не 200, выбрасывается исключение.
        - Если `stream` установлен в `False`, функция возвращает содержимое первого сообщения из списка `choices`.
        - Если `stream` установлен в `True`, функция итерируется по чанкам ответа и возвращает содержимое каждого чанка, содержащего "content".
        """
```
**Примеры**:
```python
# Пример вызова функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
stream = False
kwargs = {"temperature": 0.7}

result = EasyChat.create_completion(model, messages, stream, **kwargs)
for chunk in result:
    print(chunk)
```

## Параметры класса
### `create_completion`

- `model` (str): Имя используемой модели.
- `messages` (list[dict[str, str]]): Список сообщений для отправки.
- `stream` (bool): Указывает, следует ли использовать потоковую передачу ответов.
- `**kwargs` (Any): Дополнительные аргументы, такие как `temperature`, `presence_penalty`, `frequency_penalty` и `top_p`.

## Примеры

```python
# Пример использования класса EasyChat
from src.endpoints.gpt4free.g4f.Provider.deprecated.EasyChat import EasyChat

model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, world!"}]
stream = False
kwargs = {"temperature": 0.7}

result = EasyChat.create_completion(model, messages, stream, **kwargs)
for chunk in result:
    print(chunk)