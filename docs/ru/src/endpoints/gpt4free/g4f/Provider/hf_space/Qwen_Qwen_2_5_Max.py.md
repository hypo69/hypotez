# Модуль Qwen_Qwen_2_5_Max
## Обзор

Модуль `Qwen_Qwen_2_5_Max` предоставляет асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5-Max через API Hugging Face Space. Он поддерживает потоковую передачу данных и системные сообщения.

## Подробнее

Этот модуль позволяет взаимодействовать с моделью Qwen Qwen-2.5-Max для генерации текста. Он использует асинхронные запросы для получения данных и поддерживает потоковую передачу результатов. Модуль также позволяет передавать системные сообщения для управления поведением модели.
В проекте `hypotez` этот модуль используется для подключения к конкретному провайдеру модели, в данном случае к `Qwen Qwen-2.5-Max`, обеспечивая стандартизированный интерфейс для взаимодействия с различными языковыми моделями.

## Классы

### `Qwen_Qwen_2_5_Max`

**Описание**: Класс `Qwen_Qwen_2_5_Max` предоставляет функциональность для взаимодействия с моделью Qwen Qwen-2.5-Max через API Hugging Face Space.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую структуру для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями провайдеров.

**Атрибуты**:
- `label` (str): Метка провайдера, `"Qwen Qwen-2.5-Max"`.
- `url` (str): URL Hugging Face Space, `"https://qwen-qwen2-5-max-demo.hf.space"`.
- `api_endpoint` (str): URL API для присоединения к очереди, `"https://qwen-qwen2-5-max-demo.hf.space/gradio_api/queue/join?"`.
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу, `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения, `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений, `False`.
- `default_model` (str): Модель по умолчанию, `"qwen-qwen2-5-max"`.
- `model_aliases` (dict): Алиасы моделей, `{"qwen-2-5-max": default_model}`.
- `models` (list): Список моделей, созданный на основе ключей `model_aliases`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с моделью.

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
    """Создает асинхронный генератор для взаимодействия с моделью Qwen Qwen-2.5-Max.

    Args:
        cls (Qwen_Qwen_2_5_Max): Класс провайдера.
        model (str): Имя модели.
        messages (Messages): Список сообщений для отправки модели.
        proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы модели.

    Raises:
        aiohttp.ClientError: При ошибках, связанных с HTTP-запросами.
        json.JSONDecodeError: При ошибках декодирования JSON.
        Exception: При возникновении непредвиденных ошибок.

    **Внутренние функции**:

    ### `generate_session_hash`
    ```python
    def generate_session_hash():
        """Генерирует уникальный хеш сессии.

        Args:
            Нет.

        Returns:
            str: Уникальный хеш сессии.

        Raises:
            Нет.
        """
    ```

    **Как работает функция `generate_session_hash`**:

    1.  Функция `generate_session_hash` генерирует UUID (универсальный уникальный идентификатор) с помощью модуля `uuid`.
    2.  Из UUID удаляются все дефисы (`-`).
    3.  Из полученной строки берутся первые 8 символов, а затем еще 4 символа из другого UUID, сгенерированного аналогичным образом.
    4.  Результат объединяется и возвращается в виде строки.

    ASCII flowchart:

    ```
    UUID Generation --> Remove Dashes --> Take First 8 Chars --> Take Next 4 Chars --> Concatenate --> Return
    ```

    **Примеры**:

    ```python
    >>> generate_session_hash()
    'a1b2c3d4e5f6'
    ```
    """
```

**Назначение**: Функция `create_async_generator` создает и возвращает асинхронный генератор, который позволяет взаимодействовать с моделью Qwen Qwen-2.5-Max для генерации текста на основе предоставленных сообщений.

**Параметры**:
- `cls` (Qwen_Qwen_2_5_Max): Класс провайдера.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений, отправляемых в модель.
- `proxy` (str, optional): URL прокси-сервера для использования при подключении. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы, которые могут быть переданы в функцию.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, который выдает ответы модели.

**Вызывает исключения**:
- `aiohttp.ClientError`: Возникает при проблемах с HTTP-запросами.
- `json.JSONDecodeError`: Возникает при ошибках декодирования JSON.
- `Exception`: Возникает при любых других непредвиденных исключениях.

**Как работает функция**:

1.  **Генерация хеша сессии**: Сначала генерируется уникальный хеш сессии с использованием внутренней функции `generate_session_hash`.
2.  **Подготовка заголовков**: Формируются заголовки HTTP-запроса, включая User-Agent, Accept и Referer.
3.  **Форматирование промпта**: Извлекаются системные сообщения из списка сообщений и подготавливается промпт для модели.
4.  **Подготовка полезной нагрузки**: Создается полезная нагрузка (payload) для отправки в API, включая промпт, системное сообщение и хеш сессии.
5.  **Отправка запроса на присоединение**: Отправляется POST-запрос к API для присоединения к очереди. Получается `event_id` из ответа.
6.  **Подготовка запроса потока данных**: Формируются URL и заголовки для запроса потока данных.
7.  **Отправка запроса потока данных**: Отправляется GET-запрос для получения потока данных.
8.  **Обработка потока данных**: Построчно читается поток данных, декодируется каждая строка и обрабатывается JSON-ответ.
9.  **Извлечение и выдача фрагментов**: Из JSON-ответа извлекаются фрагменты текста, удаляются дубликаты и они выдаются как части ответа.
10. **Проверка завершения**: Проверяется, завершен ли процесс генерации. Если да, извлекается итоговый ответ, очищается от префикса и выдается оставшаяся часть.

ASCII flowchart:

```
    Generate Session Hash --> Prepare Headers --> Format Prompt --> Prepare Payload -->
    |
    POST to API (Join Queue) --> Get event_id --> Prepare Data Stream Request -->
    |
    GET Data Stream --> Read Line by Line --> Decode --> Process JSON -->
    |
    Extract Fragments --> Remove Duplicates --> Yield Fragments --> Check Completion -->
    |
    Extract Final Response --> Clean Up --> Yield Remaining Part --> End
```

**Примеры**:

```python
# Пример вызова функции create_async_generator
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

async def main():
    generator = await Qwen_Qwen_2_5_Max.create_async_generator(
        model="qwen-2-5-max",
        messages=messages
    )
    async for fragment in generator:
        print(fragment, end="")

# Запуск примера (только в асинхронной среде)
# import asyncio
# asyncio.run(main())