# Модуль `Qwen_Qwen_2_72B`

## Обзор

Модуль `Qwen_Qwen_2_72B` предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.72B через API Hugging Face Space. Он поддерживает потоковую передачу данных и системные сообщения, но не поддерживает историю сообщений.

## Подробнее

Этот модуль позволяет отправлять запросы к модели Qwen Qwen-2.72B и получать ответы в асинхронном режиме. Он использует `aiohttp` для выполнения HTTP-запросов и `json` для обработки данных в формате JSON. Модуль также включает в себя функции для форматирования запросов и обработки ответов, чтобы обеспечить совместимость с API Hugging Face Space.

## Классы

### `Qwen_Qwen_2_72B`

**Описание**: Класс `Qwen_Qwen_2_72B` предоставляет методы для взаимодействия с моделью Qwen Qwen-2.72B.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Qwen Qwen-2.72B").
- `url` (str): URL Hugging Face Space ("https://qwen-qwen2-72b-instruct.hf.space").
- `api_endpoint` (str): URL API для присоединения к очереди ("https://qwen-qwen2-72b-instruct.hf.space/queue/join?").
- `working` (bool): Указывает, что провайдер работает (True).
- `supports_stream` (bool): Указывает, что провайдер поддерживает потоковую передачу данных (True).
- `supports_system_message` (bool): Указывает, что провайдер поддерживает системные сообщения (True).
- `supports_message_history` (bool): Указывает, что провайдер не поддерживает историю сообщений (False).
- `default_model` (str): Модель по умолчанию ("qwen-qwen2-72b-instruct").
- `model_aliases` (dict): Псевдонимы моделей ({"qwen-2-72b": default_model}).
- `models` (list): Список моделей (ключи из `model_aliases`).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

## Функции

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
    """Создает асинхронный генератор для получения ответов от модели Qwen Qwen-2.72B.

    Args:
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки модели.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий фрагменты текста от модели.
    """
```

#### Как работает функция:

1. **Генерация уникального хэша сессии**: Функция `generate_session_hash()` генерирует уникальный идентификатор сессии.
2. **Подготовка заголовков и полезной нагрузки**: Формируются HTTP-заголовки и полезная нагрузка (payload) для запроса к API.
3. **Отправка запроса на присоединение**: Отправляется POST-запрос к `cls.api_endpoint` для присоединения к очереди обработки запросов.
4. **Подготовка запроса потока данных**: Формируются URL и заголовки для запроса потока данных.
5. **Отправка запроса потока данных**: Отправляется GET-запрос к `url_data` для получения потока данных с ответом модели.
6. **Обработка потока данных**: В цикле обрабатываются поступающие данные, декодируются и извлекаются фрагменты текста из JSON-ответа.
7. **Извлечение и фильтрация фрагментов**: Извлекаются фрагменты текста, игнорируются дубликаты и фрагменты, соответствующие определенному регулярному выражению.
8. **Завершение обработки**: После получения сообщения о завершении процесса (`process_completed`), извлекается итоговый ответ, очищается от префикса и возвращается оставшаяся часть.
9. **Обработка ошибок JSON**: В случае ошибки парсинга JSON, информация об ошибке логируется.

#### Внутренние функции:

##### `generate_session_hash`
```python
def generate_session_hash():
    """Генерирует уникальный хэш сессии.

    Returns:
        str: Уникальный хэш сессии.
    """
```
Функция генерирует уникальный идентификатор сессии, используя `uuid.uuid4()`. Затем удаляет дефисы и оставляет только первые 12 символов.

#### ASCII flowchart:

```
Генерация session_hash
    ↓
Подготовка headers_join, payload_join
    ↓
Отправка POST запроса к api_endpoint
    ↓
Получение event_id
    ↓
Подготовка headers_data, params_data
    ↓
Отправка GET запроса к url_data
    ↓
Обработка потока данных (цикл по line)
    ├──> Декодирование line
    │   ↓
    │   Если line начинается с 'data: '
    │   ↓
    │   Попытка парсинга JSON
    │   ↓
    │   Если msg == 'process_generating'
    │   ↓
    │   Извлечение и фильтрация fragment
    │   ↓
    │   yield fragment
    │   ↓
    │   Если msg == 'process_completed'
    │   ↓
    │   Извлечение final_full_response
    │   ↓
    │   Очистка и yield final_full_response
    │   ↓
    │   break
    │   ↓
    └──>JSONDecodeError: Логирование ошибки
```

#### Примеры:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict

async def main():
    model: str = "qwen-qwen2-72b-instruct"
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    generator = Qwen_Qwen_2_72B.create_async_generator(model=model, messages=messages)
    
    async for fragment in generator:
        print(fragment, end="")

    print()

if __name__ == "__main__":
    asyncio.run(main())
```