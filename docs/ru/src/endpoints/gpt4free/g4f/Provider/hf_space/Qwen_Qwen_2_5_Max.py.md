# Модуль Qwen_Qwen_2_5_Max

## Обзор

Модуль `Qwen_Qwen_2_5_Max` предоставляет класс для взаимодействия с моделью Qwen Qwen-2.5-Max через API Hugging Face Space. Он поддерживает асинхронную генерацию текста с использованием потоковой передачи данных.

## Подробнее

Этот модуль позволяет использовать модель Qwen Qwen-2.5-Max для генерации текста. Он отправляет запросы к API Hugging Face Space и возвращает результаты в асинхронном режиме. Модуль поддерживает потоковую передачу данных, что позволяет получать результаты по частям.

## Классы

### `Qwen_Qwen_2_5_Max`

**Описание**: Класс для взаимодействия с моделью Qwen Qwen-2.5-Max.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера ("Qwen Qwen-2.5-Max").
- `url` (str): URL Hugging Face Space ("https://qwen-qwen2-5-max-demo.hf.space").
- `api_endpoint` (str): URL API для присоединения к очереди ("https://qwen-qwen2-5-max-demo.hf.space/gradio_api/queue/join?").
- `working` (bool): Указывает, работает ли провайдер (True).
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу (True).
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения (True).
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений (False).
- `default_model` (str): Модель по умолчанию ("qwen-qwen2-5-max").
- `model_aliases` (dict): Псевдонимы моделей ({"qwen-2-5-max": default_model}).
- `models` (list): Список моделей (list(model_aliases.keys())).

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для получения ответов от модели.

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
        """Создает асинхронный генератор для получения ответов от модели.

        Args:
            model (str): Имя модели.
            messages (Messages): Список сообщений для отправки модели.
            proxy (str, optional): URL прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответы модели.

        Raises:
            aiohttp.ClientError: При ошибках HTTP-запроса.
            json.JSONDecodeError: При ошибках декодирования JSON.

        """
```

#### Внутренние функции:

##### `generate_session_hash`

```python
        def generate_session_hash():
            """Генерирует уникальный хеш сессии.

            Returns:
                str: Уникальный хеш сессии.
            """
```

**Как работает функция**:

1.  **Генерация уникального идентификатора**: Функция использует `uuid.uuid4()` для создания уникального идентификатора.
2.  **Форматирование идентификатора**: Из полученного UUID удаляются дефисы (`-`) и извлекаются две части: первые 8 и первые 4 символа.
3.  **Объединение частей**: Обе части объединяются в строку, которая и является хешем сессии.

```ascii
    UUID generate  ->  Remove hyphens  ->  Extract parts (8 and 4 chars)  ->  Concatenate parts  ->  Session hash
```

**Примеры**:

```python
# Пример использования функции generate_session_hash
session_hash = generate_session_hash()
print(session_hash)  # Пример: 'a1b2c3d4e5f6'
```

**Описание**:

Эта функция генерирует уникальный хеш сессии, который используется для идентификации сессии при взаимодействии с API.

#### Описание работы `create_async_generator`

1.  **Генерация хеша сессии**: Вызывается функция `generate_session_hash()` для создания уникального идентификатора сессии.
2.  **Подготовка заголовков**: Формируются заголовки для HTTP-запросов, включая `User-Agent`, `Accept`, `Referer` и другие.
3.  **Подготовка промпта**: Извлекаются системные сообщения из списка `messages` и объединяются в строку `system_prompt`. Если системные сообщения отсутствуют, устанавливается значение по умолчанию "You are a helpful assistant.".
4.  **Формирование полезной нагрузки (payload)**: Создается словарь `payload_join`, содержащий промпт, системный промпт и хеш сессии.
5.  **Отправка запроса на присоединение**: Отправляется POST-запрос к `cls.api_endpoint` с заголовками и полезной нагрузкой. Полученный `event_id` используется для дальнейших запросов.
6.  **Подготовка запроса на получение данных**: Формируются URL и заголовки для запроса на получение данных в формате `text/event-stream`.
7.  **Отправка запроса на получение данных**: Отправляется GET-запрос к `url_data` с заголовками и параметрами.
8.  **Обработка потока данных**: Читаются данные из потока, декодируются и обрабатываются.
    *   Если строка начинается с `data: `, извлекается JSON-данные.
    *   Проверяется наличие сообщения `process_generating` для получения фрагментов текста.
    *   Фрагменты текста добавляются к полной строке ответа `full_response` и возвращаются через `yield`.
    *   Проверяется наличие сообщения `process_completed` для получения полного ответа.
    *   Извлекается окончательный ответ `final_full_response`, очищается от дубликатов и возвращается через `yield`.
9.  **Обработка ошибок**: В случае ошибки декодирования JSON, информация об ошибке логируется с использованием `debug.log`.

```ascii
    Generate session hash -> Prepare headers -> Prepare prompt -> Form payload -> Send join request -> Get event_id
    -> Prepare data stream request -> Send data stream request
    -> Process stream data:
        -> Check 'data:' prefix -> Extract JSON data
        -> Check 'process_generating' message -> Extract text fragments -> Yield fragments
        -> Check 'process_completed' message -> Extract final response -> Clean response -> Yield remaining response
    -> Handle JSONDecodeError -> Log error
```

**Примеры**:

```python
# Пример использования create_async_generator
model = "qwen-2-5-max"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke."}
]

async def main():
    async for fragment in Qwen_Qwen_2_5_Max.create_async_generator(model=model, messages=messages):
        print(fragment, end="")

# Запуск примера
# asyncio.run(main())
```
```python
# Пример использования create_async_generator
model = "qwen-2-5-max"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Напиши небольшой стих о весне."}
]

async def main():
    async for fragment in Qwen_Qwen_2_5_Max.create_async_generator(model=model, messages=messages):
        print(fragment, end="")

# Запуск примера
# asyncio.run(main())
```

## Функции

В данном модуле нет отдельных функций, не являющихся методами класса.