# Модуль Lockchat

## Обзор

Модуль `Lockchat` предоставляет класс `Lockchat`, который является провайдером для работы с API Lockchat. Он поддерживает потоковую передачу данных и модели `gpt-3.5-turbo` и `gpt-4`.

## Подробней

Модуль предназначен для интеграции с сервисом Lockchat, предоставляющим доступ к моделям GPT через свой API. Он позволяет отправлять запросы на создание завершений (completions) и получать ответы в потоковом режиме.

## Классы

### `Lockchat(AbstractProvider)`

**Описание**: Класс `Lockchat` является провайдером для работы с API Lockchat. Он наследуется от `AbstractProvider`.

**Наследует**: `AbstractProvider`

**Атрибуты**:
- `url` (str): URL API Lockchat. По умолчанию `"http://supertest.lockchat.app"`.
- `supports_stream` (bool): Поддержка потоковой передачи данных. Установлено в `True`.
- `supports_gpt_35_turbo` (bool): Поддержка модели `gpt-3.5-turbo`. Установлено в `True`.
- `supports_gpt_4` (bool): Поддержка модели `gpt-4`. Установлено в `True`.

**Методы**:
- `create_completion`: Создает запрос на завершение текста.

### `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

**Описание**: Метод `create_completion` отправляет запрос к API Lockchat для создания завершения текста на основе предоставленных сообщений.

**Параметры**:
- `model` (str): Идентификатор модели, которую следует использовать (например, `gpt-3.5-turbo` или `gpt-4`).
- `messages` (list[dict[str, str]]): Список сообщений для отправки в API. Каждое сообщение представляет собой словарь с ключами `"role"` и `"content"`.
- `stream` (bool): Флаг, указывающий, следует ли возвращать ответ в потоковом режиме.
- `**kwargs` (Any): Дополнительные параметры, такие как `temperature`.

**Возвращает**:
- `CreateResult`: Генератор, выдающий текстовые токены из ответа API.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если HTTP-запрос завершается с ошибкой.

**Как работает функция**:

1. **Подготовка параметров**:
   - Извлекается значение температуры из `kwargs` или используется значение по умолчанию `0.7`.
   - Формируется полезная нагрузка (`payload`) для запроса, включающая `temperature`, `messages`, `model` и `stream`.
   - Определяются заголовки (`headers`) для запроса, включая `user-agent`.

2. **Отправка запроса**:
   - Отправляется `POST`-запрос к API Lockchat по адресу `http://supertest.lockchat.app/v1/chat/completions` с использованием библиотеки `requests`.
   - Устанавливается `stream=True` для получения ответа в потоковом режиме.

3. **Обработка ответа**:
   - Вызывается метод `response.raise_for_status()` для проверки статуса ответа HTTP и возбуждения исключения в случае ошибки.
   - Итерируется по строкам ответа, полученным с помощью `response.iter_lines()`.
   - Проверяется наличие сообщения об ошибке `"The model: \`gpt-4\` does not exist"` в токене. Если ошибка обнаружена, функция повторно вызывает сама себя с теми же параметрами.
   - Если токен содержит `"content"`, он декодируется из JSON и извлекается содержимое сообщения.
   - Извлекается текст из поля `content` в JSON-ответе и передается через генератор.

**Примеры**:

```python
# Пример вызова функции create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True
temperature = 0.8

result = Lockchat.create_completion(model=model, messages=messages, stream=stream, temperature=temperature)
for token in result:
    print(token)
```

```python
# Пример вызова функции create_completion с обработкой исключений
model = "gpt-4"
messages = [{"role": "user", "content": "Write a poem about the sea."}]
stream = True

try:
    result = Lockchat.create_completion(model=model, messages=messages, stream=stream)
    for token in result:
        print(token)
except requests.exceptions.HTTPError as ex:
    print(f"Error: {ex}")
```
```python
# Пример определения функции create_completion
class Lockchat(AbstractProvider):
    url: str              = "http://supertest.lockchat.app"
    supports_stream       = True
    supports_gpt_35_turbo = True
    supports_gpt_4        = True

    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        """ Функция отправляет запрос к API Lockchat для создания завершения текста на основе предоставленных сообщений.

        Args:
            model (str): Идентификатор модели, которую следует использовать (например, `gpt-3.5-turbo` или `gpt-4`).
            messages (list[dict[str, str]]): Список сообщений для отправки в API. Каждое сообщение представляет собой словарь с ключами "role" и "content".
            stream (bool): Флаг, указывающий, следует ли возвращать ответ в потоковом режиме.
            **kwargs (Any): Дополнительные параметры, такие как `temperature`.

        Returns:
            CreateResult: Генератор, выдающий текстовые токены из ответа API.

        Raises:
            requests.exceptions.HTTPError: Если HTTP-запрос завершается с ошибкой.
        """
        temperature = float(kwargs.get("temperature", 0.7))
        payload = {
            "temperature": temperature,
            "messages"   : messages,
            "model"      : model,
            "stream"     : True,
        }

        headers = {
            "user-agent": "ChatX/39 CFNetwork/1408.0.4 Darwin/22.5.0",
        }
        response = requests.post("http://supertest.lockchat.app/v1/chat/completions",
                                 json=payload, headers=headers, stream=True)

        response.raise_for_status()
        for token in response.iter_lines():
            if b"The model: `gpt-4` does not exist" in token:
                print("error, retrying...")

                Lockchat.create_completion(
                    model       = model,
                    messages    = messages,
                    stream      = stream,
                    temperature = temperature,
                    **kwargs)

            if b"content" in token:
                token = json.loads(token.decode("utf-8").split("data: ")[1])
                token = token["choices"][0]["delta"].get("content")

                if token:
                    yield (token)