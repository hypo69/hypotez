# Модуль Lockchat

## Обзор

Модуль `Lockchat` предоставляет реализацию класса `Lockchat`, который реализует интерфейс `AbstractProvider` для работы с API Lockchat. 

## Подробнее

Модуль `Lockchat` предназначен для взаимодействия с API сервиса Lockchat, который предоставляет доступ к моделям генерации текста, в том числе GPT-3.5 Turbo и GPT-4. 

Класс `Lockchat` наследует от `AbstractProvider` и реализует метод `create_completion`, отвечающий за отправку запросов к API и получение результатов. 

## Классы

### `class Lockchat`

**Описание**: Класс `Lockchat` реализует интерфейс `AbstractProvider` для работы с API Lockchat.

**Наследует**: `AbstractProvider`

**Атрибуты**:

- `url` (str): URL-адрес API Lockchat.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных.
- `supports_gpt_35_turbo` (bool): Указывает, поддерживает ли провайдер модель GPT-3.5 Turbo.
- `supports_gpt_4` (bool): Указывает, поддерживает ли провайдер модель GPT-4.

**Методы**:

- `create_completion(model: str, messages: list[dict[str, str]], stream: bool, **kwargs: Any) -> CreateResult`

## Методы класса

### `create_completion`

```python
    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:

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

**Назначение**: Метод `create_completion` отправляет запрос к API Lockchat для генерации текста.

**Параметры**:

- `model` (str): Имя модели, которую нужно использовать для генерации текста (например, `gpt-3.5-turbo` или `gpt-4`).
- `messages` (list[dict[str, str]]): Список сообщений, используемых для контекста генерации текста. 
- `stream` (bool): Флаг, указывающий на использование потоковой передачи данных.
- `kwargs` (Any): Дополнительные параметры для запроса API.

**Возвращает**:

- `CreateResult`: Результат генерации текста.

**Вызывает исключения**:

- `requests.exceptions.HTTPError`: Если запрос к API Lockchat не удался.

**Как работает функция**:

1. Метод `create_completion` создает запрос к API Lockchat с использованием библиотеки `requests`.
2. В запросе передается payload с информацией о модели, сообщениях, температуре и флагом `stream`.
3. Метод `response.raise_for_status()` проверяет наличие ошибок в ответе.
4. Функция iter_lines() итерационно обрабатывает ответ, извлекая блоки текста и возвращая их.

**Примеры**:

```python
# Инициализация провайдера
lockchat_provider = Lockchat()

# Запрос к API для генерации текста
messages = [
    {"role": "user", "content": "Привет! Как дела?"},
]
result = lockchat_provider.create_completion(
    model="gpt-3.5-turbo", 
    messages=messages, 
    stream=True
)

# Получение результата
for token in result:
    print(token)