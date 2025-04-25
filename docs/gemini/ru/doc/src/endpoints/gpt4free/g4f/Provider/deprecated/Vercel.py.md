# Модуль Vercel

## Обзор

Модуль предоставляет класс `Vercel`, который реализует интерфейс `AbstractProvider` для взаимодействия с API Vercel. `Vercel` позволяет создавать запросы к API Vercel для генерации текста с использованием различных моделей, таких как GPT-3.5-turbo и GPT-4.

## Подробнее

Этот модуль использует API Vercel для генерации текста. API Vercel предоставляет доступ к различным моделям искусственного интеллекта, включая GPT-3.5-turbo, GPT-4 и другие. Модуль `Vercel` предоставляет возможность создавать запросы к API Vercel с помощью метода `create_completion`, передавая в качестве аргумента модель, сообщения и другие параметры, необходимые для генерации текста.

## Классы

### `class Vercel`

**Описание**: Класс реализует интерфейс `AbstractProvider` для взаимодействия с API Vercel.

**Атрибуты**:

- `url`: URL-адрес API Vercel.
- `working`: Флаг, указывающий, работает ли провайдер (по умолчанию `False`).
- `supports_message_history`: Флаг, указывающий, поддерживает ли провайдер историю сообщений (по умолчанию `True`).
- `supports_gpt_35_turbo`: Флаг, указывающий, поддерживает ли провайдер модель GPT-3.5-turbo (по умолчанию `True`).
- `supports_stream`: Флаг, указывающий, поддерживает ли провайдер потоковую передачу (по умолчанию `True`).

**Методы**:

- `create_completion(model: str, messages: Messages, stream: bool, proxy: str = None, **kwargs) -> CreateResult`

**Назначение**: Создает запрос к API Vercel для генерации текста.

**Параметры**:

- `model`: Имя модели, используемой для генерации текста.
- `messages`: Список сообщений, которые будут переданы в модель.
- `stream`: Флаг, указывающий, нужно ли использовать потоковую передачу.
- `proxy`: Прокси-сервер, который будет использоваться для запросов к API Vercel.
- `**kwargs`: Дополнительные параметры для API Vercel.

**Возвращает**:

- `CreateResult`: Результат запроса к API Vercel.

**Вызывает исключения**:

- `MissingRequirementsError`: Если отсутствуют необходимые библиотеки.
- `ValueError`: Если модель не поддерживается.

**Как работает**:

- Проверяет, установлены ли необходимые библиотеки.
- Проверяет, поддерживается ли указанная модель.
- Формирует заголовок HTTP-запроса.
- Формирует JSON-данные для запроса.
- Отправляет запрос к API Vercel.
- Обрабатывает ответ API Vercel и возвращает результат.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vercel import Vercel

# Создание инстанса провайдера Vercel
vercel_provider = Vercel()

# Создание запроса для генерации текста
response = vercel_provider.create_completion(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Привет!"},
    ],
    stream=False,
)

# Печать результата
print(response.text)
```

## Функции

### `get_anti_bot_token() -> str`

**Назначение**: Получает токен для защиты от ботов API Vercel.

**Как работает**:

- Отправляет запрос к API Vercel для получения токена.
- Декодирует полученные данные.
- Преобразует данные в строку токена.
- Возвращает токен.

**Пример**:

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Vercel import get_anti_bot_token

token = get_anti_bot_token()
print(token)
```


## Параметры класса

- `model_info`: Словарь, содержащий информацию о моделях, поддерживаемых API Vercel.

**Пример**:

```python
# Получение информации о модели GPT-3.5-turbo
model_info = Vercel.model_info['gpt-3.5-turbo']
print(model_info)
```