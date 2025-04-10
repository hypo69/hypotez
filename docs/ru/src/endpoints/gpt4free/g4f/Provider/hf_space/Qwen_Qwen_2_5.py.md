# Модуль `Qwen_Qwen_2_5`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с моделью Qwen Qwen-2.5, размещенной на платформе Hugging Face Space. Он включает в себя функциональность для отправки запросов к API, получения потоковых ответов и обработки этих ответов для извлечения полезной информации.

## Подробнее

Модуль предназначен для интеграции с другими частями проекта `hypotez`, обеспечивая возможность использования модели Qwen Qwen-2.5 для генерации текста. Он поддерживает потоковую передачу данных, что позволяет получать ответы в режиме реального времени.

## Классы

### `Qwen_Qwen_2_5`

**Описание**: Класс `Qwen_Qwen_2_5` предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5.

**Принцип работы**:
1.  **Инициализация**: Класс инициализируется с указанием модели, сообщений и прокси-сервера (опционально).
2.  **Генерация уникального идентификатора сессии**: Для каждого запроса генерируется уникальный идентификатор сессии `session_hash`.
3.  **Формирование заголовков и полезной нагрузки**: Заголовки и полезная нагрузка формируются для отправки запросов к API.
4.  **Отправка запроса на подключение**: Отправляется запрос на подключение к API для получения `event_id`.
5.  **Отправка запроса на получение данных**: Отправляется запрос на получение потоковых данных.
6.  **Обработка потоковых данных**: Потоковые данные обрабатываются для извлечения сгенерированного текста.
7.  **Генерация фрагментов текста**: Фрагменты сгенерированного текста передаются через асинхронный генератор.

**Наследует**:

*   `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
*   `ProviderModelMixin`: Предоставляет методы для работы с моделями.

**Атрибуты**:

*   `label` (str): Метка провайдера ("Qwen Qwen-2.5").
*   `url` (str): URL платформы Hugging Face Space ("https://qwen-qwen2-5.hf.space").
*   `api_endpoint` (str): URL API для подключения ("https://qwen-qwen2-5.hf.space/queue/join").
*   `working` (bool): Указывает, работает ли провайдер (True).
*   `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу данных (True).
*   `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (True).
*   `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (False).
*   `default_model` (str): Модель по умолчанию ("qwen-qwen2-5").
*   `model_aliases` (dict): Алиасы моделей ({"qwen-2.5": default_model}).
*   `models` (list): Список моделей (ключи `model_aliases`).

**Методы**:

*   `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

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
    """
    Создает асинхронный генератор для получения ответов от модели Qwen Qwen-2.5.

    Args:
        model (str): Имя модели для использования.
        messages (Messages): Список сообщений для отправки модели.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий фрагменты текста ответа модели.
    """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5 и получения потоковых ответов.

**Параметры**:

*   `cls` (Qwen_Qwen_2_5): Ссылка на класс.
*   `model` (str): Имя модели для использования.
*   `messages` (Messages): Список сообщений для отправки модели.
*   `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
*   `**kwargs`: Дополнительные аргументы.

**Возвращает**:

*   `AsyncResult`: Асинхронный генератор, выдающий фрагменты текста ответа модели.

**Как работает функция**:

1.  **Генерация идентификатора сессии**: Генерируется уникальный идентификатор сессии `session_hash` с помощью внутренней функции `generate_session_hash`.
2.  **Подготовка заголовков**: Формируются заголовки `headers_join` для запроса на подключение к API.
3.  **Формирование системного промпта**: Извлекается и объединяется системный промпт из списка сообщений. Если системный промпт отсутствует, используется значение по умолчанию.
4.  **Формирование промпта**: Формируется промпт `prompt` из списка сообщений.
5.  **Подготовка полезной нагрузки**: Формируется полезная нагрузка `payload_join` для запроса на подключение к API.
6.  **Отправка запроса на подключение**: Отправляется POST-запрос к `cls.api_endpoint` с заголовками `headers_join` и полезной нагрузкой `payload_join`. Полученный `event_id` извлекается из ответа.
7.  **Подготовка заголовков и параметров для потока данных**: Формируются заголовки `headers_data` и параметры `params_data` для запроса на получение потоковых данных.
8.  **Отправка запроса на получение потока данных**: Отправляется GET-запрос к `url_data` с заголовками `headers_data` и параметрами `params_data`.
9.  **Обработка потоковых данных**: Построчно обрабатывается ответ от сервера. Каждая строка декодируется и проверяется на наличие префикса `data: `.
10. **Извлечение JSON**: Если строка начинается с `data: `, извлекается JSON-объект из строки.
11. **Обработка этапов генерации**: Проверяется наличие ключа `msg` со значением `process_generating` в JSON-объекте. Если ключ присутствует, извлекаются данные из ключа `output` и генерируются фрагменты текста.
12. **Обработка завершения**: Проверяется наличие ключа `msg` со значением `process_completed` в JSON-объекте. Если ключ присутствует, извлекается финальный текст ответа и генерируется оставшаяся часть текста.
13. **Обработка ошибок JSON**: Если происходит ошибка при декодировании JSON, регистрируется сообщение об ошибке.

**Внутренние функции**:

### `generate_session_hash`

```python
def generate_session_hash():
    """Generate a unique session hash."""
    return str(uuid.uuid4()).replace('-', '')[:10]
```

**Назначение**: Генерирует уникальный идентификатор сессии.

**Как работает функция**:

1.  Генерирует UUID (Universally Unique Identifier) с помощью `uuid.uuid4()`.
2.  Преобразует UUID в строку с помощью `str()`.
3.  Удаляет все дефисы из строки с помощью `replace('-', '')`.
4.  Возвращает первые 10 символов строки.

**Примеры**:

```python
# Пример вызова функции create_async_generator
import asyncio
from typing import AsyncGenerator, List, Dict

from g4f.Provider.hf_space.Qwen_Qwen_2_5 import Qwen_Qwen_2_5

async def main():
    model = "qwen-2.5"
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    async def process_generator(generator: AsyncGenerator[str, None]):
        async for fragment in generator:
            print(fragment, end="")
        print()

    generator = Qwen_Qwen_2_5.create_async_generator(model=model, messages=messages)
    if generator:
        await process_generator(await generator)

if __name__ == "__main__":
    asyncio.run(main())

# Пример с прокси сервером
import asyncio
from typing import AsyncGenerator, List, Dict

from g4f.Provider.hf_space.Qwen_Qwen_2_5 import Qwen_Qwen_2_5

async def main():
    model = "qwen-2.5"
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    proxy = "http://your_proxy:8080"  # Замените на ваш прокси-сервер

    async def process_generator(generator: AsyncGenerator[str, None]):
        async for fragment in generator:
            print(fragment, end="")
        print()

    generator = Qwen_Qwen_2_5.create_async_generator(model=model, messages=messages, proxy=proxy)
    if generator:
        await process_generator(await generator)

if __name__ == "__main__":
    asyncio.run(main())
```

**ASCII схема работы функции `create_async_generator`**:

```
Начало
  ↓
Генерация session_hash
  ↓
Подготовка headers_join и payload_join
  ↓
Отправка POST запроса к API (получение event_id)
  ↓
Подготовка headers_data и params_data
  ↓
Отправка GET запроса к API (получение потока данных)
  ↓
Обработка каждой строки потока данных
  ├── data: присутствует? 
  │   └── ДА: Извлечение JSON
  │        ├── msg == process_generating?
  │        │   └── ДА: Извлечение и генерация фрагмента текста
  │        │   └── НЕТ: msg == process_completed?
  │        │        └── ДА: Извлечение и генерация остатка текста
  │        │        └── НЕТ: Пропуск
  │        └── НЕТ: Обработка ошибки JSON
  └── НЕТ: Пропуск
  ↓
Конец