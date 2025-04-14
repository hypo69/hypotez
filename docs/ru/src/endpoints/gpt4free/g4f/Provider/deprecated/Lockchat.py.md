# Модуль Lockchat

## Обзор

Модуль `Lockchat` предоставляет класс для взаимодействия с Lockchat API, предлагая поддержку потоковой передачи данных и моделей GPT-3.5 Turbo и GPT-4. Он позволяет отправлять запросы на создание завершений чата и обрабатывать потоковые ответы.

## Подробней

Этот модуль является частью устаревшей функциональности (`deprecated`) в проекте `hypotez`, что подразумевает его возможное удаление или замену в будущем. Модуль предназначен для обеспечения совместимости с Lockchat API, но рекомендуется рассмотреть альтернативные решения, если они доступны.

## Классы

### `Lockchat`

**Описание**: Класс `Lockchat` предоставляет интерфейс для взаимодействия с Lockchat API.

**Наследует**:
- `AbstractProvider`: Наследует от абстрактного класса `AbstractProvider`, предоставляющего базовую структуру для провайдеров API.

**Атрибуты**:
- `url` (str): URL-адрес API Lockchat. По умолчанию "http://supertest.lockchat.app".
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных. Всегда `True`.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo. Всегда `True`.
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модель GPT-4. Всегда `True`.

**Методы**:
- `create_completion`: Создает запрос на завершение чата и возвращает результат в потоковом режиме.

## Функции

### `create_completion`

```python
@staticmethod
def create_completion(
    model: str,
    messages: list[dict[str, str]],
    stream: bool, **kwargs: Any) -> CreateResult:
    """ Функция создает запрос на завершение чата к API Lockchat и обрабатывает потоковый ответ.

    Args:
        model (str): Имя используемой модели.
        messages (list[dict[str, str]]): Список сообщений для чата.
        stream (bool): Указывает, следует ли использовать потоковый режим.
        **kwargs (Any): Дополнительные аргументы, такие как температура.

    Returns:
        CreateResult: Генератор токенов из ответа API.

    Raises:
        requests.exceptions.HTTPError: Если HTTP запрос завершается с ошибкой.

    Внутренние функции:
        Отсутствуют.

    Как работает функция:
    1. Извлекает значение температуры из `kwargs` или использует значение по умолчанию 0.7.
    2. Формирует полезную нагрузку (payload) с температурой, сообщениями, моделью и параметром потоковой передачи.
    3. Определяет заголовки, включая User-Agent.
    4. Отправляет POST-запрос к API Lockchat с полезной нагрузкой и заголовками, устанавливая stream=True для потоковой передачи.
    5. Перебирает строки в потоковом ответе.
    6. Если обнаружена ошибка модели (например, `The model: gpt-4 does not exist`), выводит сообщение об ошибке и повторяет вызов `create_completion`.
    7. Если строка содержит "content", извлекает контент из JSON, декодирует его и извлекает текст из поля "content".
    8. Возвращает (yield) каждый извлеченный токен.

    ASCII flowchart:

    Начало
    │
    Получение параметров (temperature, model, messages, stream)
    │
    Создание payload (словарь с данными для запроса)
    │
    Создание headers (заголовки запроса)
    │
    Отправка POST запроса к Lockchat API (http://supertest.lockchat.app/v1/chat/completions)
    │
    Обработка потокового ответа
    │
    Проверка на наличие ошибок в ответе
    │
    Извлечение контента из JSON
    │
    Выдача токена (yield token)
    │
    Конец
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
```

**Параметры**:
- `model` (str): Имя используемой модели.
- `messages` (list[dict[str, str]]): Список сообщений для чата.
- `stream` (bool): Указывает, следует ли использовать потоковый режим.
- `**kwargs` (Any): Дополнительные аргументы, такие как температура.

**Возвращает**:
- `CreateResult`: Генератор токенов из ответа API.

**Вызывает исключения**:
- `requests.exceptions.HTTPError`: Если HTTP запрос завершается с ошибкой.

**Примеры**:

```python
# Пример использования create_completion
model = "gpt-3.5-turbo"
messages = [{"role": "user", "content": "Hello, how are you?"}]
stream = True
kwargs = {"temperature": 0.5}

# Вызов функции и итерация по результатам
result = Lockchat.create_completion(model, messages, stream, **kwargs)
for token in result:
    print(token)