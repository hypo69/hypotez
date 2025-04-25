# Модуль Forefront

## Обзор

Модуль предоставляет класс `Forefront`, который реализует интерфейс `AbstractProvider` для работы с API Forefront. 

## Подробней

Класс `Forefront` реализует функциональность для взаимодействия с API Forefront, который позволяет использовать большие языковые модели (LLM) для различных задач, таких как генерация текста, перевод, и другие. 

## Классы

### `class Forefront`

**Описание**: Класс реализует интерфейс `AbstractProvider` для работы с API Forefront.

**Атрибуты**:

- `url`: URL API Forefront.
- `supports_stream`: Указывает, поддерживает ли API Forefront потоковую обработку ответов.
- `supports_gpt_35_turbo`: Указывает, поддерживает ли API Forefront использование модели `gpt-3.5-turbo`.

**Методы**:

- `create_completion()`: Функция отправляет запрос к API Forefront для получения ответа от LLM.

## Методы класса

### `create_completion()`

```python
    @staticmethod
    def create_completion(
        model: str,
        messages: list[dict[str, str]],
        stream: bool, **kwargs: Any) -> CreateResult:
        
        json_data = {
            "text"          : messages[-1]["content"],
            "action"        : "noauth",
            "id"            : "",
            "parentId"      : "",
            "workspaceId"   : "",
            "messagePersona": "607e41fe-95be-497e-8e97-010a59b2e2c0",
            "model"         : "gpt-4",
            "messages"      : messages[:-1] if len(messages) > 1 else [],
            "internetMode"  : "auto",
        }

        response = requests.post("https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat",
            json=json_data, stream=True)
        
        response.raise_for_status()
        for token in response.iter_lines():
            if b"delta" in token:
                yield json.loads(token.decode().split("data: ")[1])["delta"]
```

**Назначение**: Функция отправляет запрос к API Forefront для получения ответа от LLM.

**Параметры**:

- `model`: Строка, указывающая модель LLM, которую нужно использовать.
- `messages`: Список словарей, содержащий историю общения с LLM.
- `stream`: Булевое значение, указывающее, нужно ли использовать потоковую обработку ответа.
- `**kwargs`: Дополнительные аргументы, передаваемые в API.

**Возвращает**:

- `CreateResult`: Объект `CreateResult`, содержащий ответ от LLM.

**Как работает функция**:

- Функция `create_completion` создает словарь `json_data`, который содержит параметры запроса к API Forefront.
- `json_data` включает информацию о модели LLM, сообщениях, истории общения и других параметрах.
- Функция отправляет POST-запрос к API Forefront с использованием `requests.post`.
- `response.raise_for_status` проверяет статус ответа и вызывает исключение, если статус не является успешным.
- Функция использует `response.iter_lines` для итерации по строкам ответа.
- Если строка содержит `delta`, функция извлекает и декодирует данные и возвращает их.

**Примеры**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Forefront import Forefront

# Создание инстанса класса Forefront
forefront = Forefront()

# Пример запроса с одним сообщением
messages = [{"role": "user", "content": "Привет! Как дела?"}]
response = forefront.create_completion(model="gpt-4", messages=messages, stream=True)

# Итерация по ответам
for token in response:
    print(token)

# Пример запроса с несколькими сообщениями
messages = [
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Хорошо, а у тебя?"},
    {"role": "user", "content": "Тоже хорошо. Спасибо."},
]
response = forefront.create_completion(model="gpt-4", messages=messages, stream=True)

# Итерация по ответам
for token in response:
    print(token)
```

## Параметры класса

- `url`: URL API Forefront.
- `supports_stream`: Указывает, поддерживает ли API Forefront потоковую обработку ответов.
- `supports_gpt_35_turbo`: Указывает, поддерживает ли API Forefront использование модели `gpt-3.5-turbo`.