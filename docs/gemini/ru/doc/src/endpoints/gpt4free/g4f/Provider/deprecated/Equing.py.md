# Модуль `Equing.py`

## Обзор

Модуль `Equing.py` представляет собой реализацию провайдера `Equing` для работы с сервисом `next.eqing.tech`. Он поддерживает потоковую передачу данных и модель `gpt-3.5-turbo`, но не поддерживает `gpt-4`. Модуль предназначен для создания и обработки запросов к API `openai` для получения ответов от чат-бота.

## Подробней

Модуль содержит класс `Equing`, который наследуется от `AbstractProvider`. Он определяет URL, поддерживает потоковую передачу и указывает, какие модели `GPT` поддерживаются. Основная функциональность заключается в методе `create_completion`, который отправляет запросы к API `next.eqing.tech` и возвращает результаты.

## Классы

### `Equing(AbstractProvider)`

**Описание**:
Класс `Equing` предоставляет реализацию для взаимодействия с API `next.eqing.tech`. Он наследует функциональность от `AbstractProvider` и адаптирует ее для конкретных требований `Equing API`.

**Наследует**:
`AbstractProvider` - абстрактный базовый класс для провайдеров, определяющий интерфейс для работы с различными API.

**Атрибуты**:
- `url` (str): URL-адрес сервиса `next.eqing.tech`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `supports_stream` (bool): Флаг, указывающий на поддержку потоковой передачи данных.
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo`.
- `supports_gpt_4` (bool): Флаг, указывающий на поддержку модели `gpt-4`.

**Методы**:
- `create_completion`: Статический метод для создания запроса на завершение текста.

## Методы класса

### `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

```python
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        """
        Создает запрос к API next.eqing.tech для получения ответа от чат-бота.

        Args:
            model (str): Идентификатор используемой модели.
            messages (list[dict[str, str]]): Список сообщений для передачи в запросе.
            stream (bool): Флаг, указывающий на необходимость потоковой передачи данных.
            **kwargs (Any): Дополнительные аргументы, такие как температура, штрафы и т.д.

        Returns:
            CreateResult: Результат запроса, который может быть как потоком данных, так и полным ответом.

        Raises:
            requests.exceptions.RequestException: В случае ошибки при выполнении запроса.
            json.JSONDecodeError: В случае ошибки при декодировании JSON ответа.

        Как работает функция:
        1. Формирует заголовки запроса, включая информацию о браузере, типе контента и источнике запроса.
        2. Подготавливает JSON-данные для отправки, включая сообщения, модель, параметры температуры и штрафов.
        3. Отправляет POST-запрос к API next.eqing.tech с указанными заголовками и данными.
        4. Если stream=False, возвращает содержимое ответа в формате JSON.
        5. Если stream=True, итерируется по содержимому ответа, декодирует JSON и извлекает текст для генерации.
        """
        ...
```

**Параметры**:
- `model` (str): Идентификатор модели, которую необходимо использовать для генерации ответа.
- `messages` (list[dict[str, str]]): Список сообщений, отправляемых в запросе. Каждое сообщение представлено в виде словаря, содержащего роли и содержимое.
- `stream` (bool): Флаг, указывающий, следует ли использовать потоковую передачу данных.
- `**kwargs` (Any): Дополнительные параметры, такие как `temperature`, `presence_penalty`, `frequency_penalty` и `top_p`, которые позволяют настраивать поведение модели.

**Возвращает**:
- `CreateResult`: В зависимости от значения параметра `stream`, возвращает либо генератор токенов (если `stream=True`), либо полный ответ от API (если `stream=False`).

**Примеры**:

Пример 1: Создание запроса без потоковой передачи:

```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = False
result = Equing.create_completion(model=model, messages=messages, stream=stream)
for r in result:
    print(r)
```

Пример 2: Создание запроса с потоковой передачей:

```python
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Tell me a joke."}]
stream = True
result = Equing.create_completion(model=model, messages=messages, stream=stream, temperature=0.7)
for r in result:
    print(r, end="")
```
```

## Параметры класса

- `url` (str): URL-адрес, используемый для доступа к API `next.eqing.tech`.
- `working` (bool): Указывает, работает ли провайдер в данный момент.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель `gpt-3.5-turbo`.
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модель `gpt-4`.