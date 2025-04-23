# Модуль `Qwen_Qwen_2_5`

## Обзор

Модуль предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5 через Hugging Face Space. Он поддерживает потоковую передачу ответов, системные сообщения и предоставляет возможности для работы с моделью Qwen.

## Подробнее

Модуль предназначен для интеграции с API Qwen Qwen-2.5, размещенным на Hugging Face Space. Он использует `aiohttp` для асинхронных запросов и предоставляет удобный интерфейс для генерации текста на основе предоставленных сообщений. Модуль также включает обработку ошибок и отладку с использованием модуля `debug`.

## Классы

### `Qwen_Qwen_2_5`

**Описание**: Класс реализует асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера (Qwen Qwen-2.5).
- `url` (str): URL Hugging Face Space.
- `api_endpoint` (str): URL API для отправки запросов.
- `working` (bool): Указывает, работает ли провайдер.
- `supports_stream` (bool): Поддержка потоковой передачи.
- `supports_system_message` (bool): Поддержка системных сообщений.
- `supports_message_history` (bool): Поддержка истории сообщений.
- `default_model` (str): Модель по умолчанию (qwen-qwen2-5).
- `model_aliases` (dict): Псевдонимы моделей.
- `models` (list): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator()`: Создает асинхронный генератор для генерации текста.

## Методы класса

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для генерации текста на основе предоставленных сообщений.

    Args:
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для генерации текста.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий сгенерированный текст.

    Raises:
        aiohttp.ClientError: Если возникает ошибка при подключении к API.
        json.JSONDecodeError: Если не удается декодировать JSON из ответа API.

    Внутренние функции:
    - generate_session_hash(): Генерация уникального идентификатора сессии.
    
    - Генерирует уникальный хеш сессии с помощью `uuid.uuid4()`.
    """
```

#### Описание работы функции `create_async_generator`

1. **Генерация хеша сессии**:
   - Вызывается внутренняя функция `generate_session_hash()` для создания уникального идентификатора сессии, который используется для взаимодействия с API.

2. **Подготовка заголовков**:
   - Определяются заголовки (`headers_join`) для HTTP-запроса, включая User-Agent, Accept, Referer и другие.

3. **Подготовка промпта**:
   - Извлекаются системные сообщения из списка `messages` и объединяются в `system_prompt`. Если системные сообщения отсутствуют, используется стандартное сообщение.
   - Форматируется основной промт (`prompt`) из оставшихся сообщений.

4. **Подготовка полезной нагрузки (payload)**:
   - Создается словарь `payload_join` с данными для отправки в API, включая промт, системный промт и хеш сессии.

5. **Отправка запроса и обработка ответа**:
   - Используется `aiohttp.ClientSession()` для отправки асинхронного POST-запроса к `cls.api_endpoint` с заголовками и полезной нагрузкой.
   - Извлекается `event_id` из JSON-ответа.

6. **Подготовка запроса потока данных**:
   - Формируются URL (`url_data`), заголовки (`headers_data`) и параметры (`params_data`) для запроса потока данных.

7. **Получение и обработка потока данных**:
   - Отправляется GET-запрос к `url_data` для получения потока данных.
   - Итерируется по каждой строке в ответе:
     - Декодируется строка из UTF-8.
     - Если строка начинается с `'data: '`, извлекается JSON-данные.
     - Проверяется наличие стадии генерации (`'msg' == 'process_generating'`) и извлекаются фрагменты текста из `json_data['output']['data'][1]`.
     - Фрагменты текста добавляются к `full_response` и генерируются (`yield fragment`).
     - Проверяется завершение процесса (`'msg' == 'process_completed'`) и извлекается окончательный текст ответа.
     - Оставшаяся часть текста (`final_text`) генерируется, если она отличается от `full_response`.

8. **Обработка ошибок**:
   - Если возникает `json.JSONDecodeError`, логируется сообщение об ошибке.

#### Внутренняя функция `generate_session_hash`

```python
def generate_session_hash():
    """Generate a unique session hash."""
    return str(uuid.uuid4()).replace('-', '')[:10]
```

**Назначение**:
Функция `generate_session_hash` генерирует уникальный хеш сессии.

**Как работает функция**:
- Функция генерирует UUID (Universally Unique Identifier) с помощью `uuid.uuid4()`.
- Удаляет все дефисы из UUID, заменяя их на пустую строку.
- Возвращает первые 10 символов полученной строки.

**Пример**:

```python
session_hash = generate_session_hash()
print(session_hash)  # Вывод: случайная строка длиной 10 символов, например, "a1b2c3d4e5"
```

## Примеры

```python
# Пример использования create_async_generator
import asyncio
from src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5 import Qwen_Qwen_2_5

async def main():
    model = "qwen-2.5"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Как тебя зовут?"}
    ]

    generator = await Qwen_Qwen_2_5.create_async_generator(model=model, messages=messages)
    async for fragment in generator:
        print(fragment, end="")

if __name__ == "__main__":
    asyncio.run(main())