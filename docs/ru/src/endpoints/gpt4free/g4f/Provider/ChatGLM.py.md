# Модуль `ChatGLM`

## Обзор

Модуль `ChatGLM` предоставляет асинхронную интеграцию с сервисом ChatGLM, позволяя генерировать текст на основе предоставленных сообщений. Он поддерживает потоковую передачу ответов и использует API ChatGLM для взаимодействия.

## Подробнее

Этот модуль является частью проекта `hypotez` и предназначен для работы с сервисом ChatGLM. Он использует `aiohttp` для асинхронных HTTP-запросов и предоставляет функциональность для генерации текста на основе входных сообщений. Модуль поддерживает потоковую передачу ответов, что позволяет получать текст по частям в режиме реального времени.

## Классы

### `ChatGLM`

**Описание**: Класс `ChatGLM` реализует асинхронный генератор для взаимодействия с API ChatGLM.

**Наследует**:
- `AsyncGeneratorProvider`: Предоставляет базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Добавляет поддержку выбора модели.

**Атрибуты**:
- `url` (str): URL сервиса ChatGLM (`https://chatglm.cn`).
- `api_endpoint` (str): URL API для отправки запросов (`https://chatglm.cn/chatglm/mainchat-api/guest/stream`).
- `working` (bool): Флаг, указывающий, что провайдер работает (True).
- `supports_stream` (bool): Флаг, указывающий, что провайдер поддерживает потоковую передачу (True).
- `supports_system_message` (bool): Флаг, указывающий, что провайдер не поддерживает системные сообщения (False).
- `supports_message_history` (bool): Флаг, указывающий, что провайдер не поддерживает историю сообщений (False).
- `default_model` (str): Модель, используемая по умолчанию (`glm-4`).
- `models` (List[str]): Список поддерживаемых моделей (по умолчанию содержит только `default_model`).

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
        """Создает асинхронный генератор для взаимодействия с API ChatGLM.

        Args:
            model (str): Имя используемой модели.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Адрес прокси-сервера. По умолчанию `None`.
            **kwargs: Дополнительные аргументы.

        Yields:
            str: Части сгенерированного текста.
            FinishReason: Причина завершения генерации.

        Raises:
            Exception: Если возникает ошибка при взаимодействии с API ChatGLM.

        """
```

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Адрес прокси-сервера. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий части сгенерированного текста и причину завершения.

**Как работает функция**:

1. **Генерация `device_id`**: Генерируется уникальный идентификатор устройства (`device_id`) на основе UUID.

2. **Формирование `headers`**: Создаются заголовки HTTP-запроса, включая `User-Agent`, `Content-Type` и `X-Device-Id`.

3. **Создание `ClientSession`**: Инициализируется асинхронная сессия `aiohttp.ClientSession` с заданными заголовками.

4. **Формирование `data`**: Подготавливаются данные для отправки в теле запроса, включая идентификатор ассистента, сообщения и метаданные.

5. **Отправка `POST`-запроса**: Отправляется асинхронный `POST`-запрос к API-endpoint ChatGLM с использованием `session.post`.

6. **Обработка ответа**: 
   - Читаются чанки из ответа сервера.
   - Декодируются чанки из байтов в `utf-8`.
   - Извлекается `json_data` из декодированного чанка, если он начинается с `'data: '`.
   - Извлекается `content` из `json_data` и извлекается `text_content` из `content`.
   - Вычисляется `text`, как разница между полным `text_content` и уже выданным `yield_text`.
   - Если `text` не пустой, то он выдаётся через `yield`.
   - Обновляется `yield_text` на длину выданного `text`.
   - Если `json_data` содержит `status` равный `'finish'`, то выдаётся `FinishReason("stop")`.

```mermaid
graph TD
    A[Генерация device_id] --> B(Формирование headers);
    B --> C{Создание ClientSession};
    C --> D{Формирование data};
    D --> E{Отправка POST-запроса};
    E --> F{Чтение чанков из ответа};
    F --> G{Декодирование чанка};
    G --> H{Извлечение json_data};
    H --> I{Извлечение content из json_data};
    I --> J{Извлечение text_content из content};
    J --> K{Вычисление text};
    K --> L{Если text не пустой?};
    L -- Да --> M{Выдача text через yield};
    M --> N{Обновление yield_text};
    L -- Нет --> O{Проверка status в json_data};
    O -- status == 'finish' --> P{Выдача FinishReason("stop")};
```

**Примеры**:

```python
# Пример вызова функции create_async_generator
async def example():
    model = "glm-4"
    messages = [
        {"role": "user", "content": "Hello"}
    ]
    async for chunk in ChatGLM.create_async_generator(model=model, messages=messages):
        print(chunk)
```
```python
# Пример вызова функции create_async_generator c прокси
async def example_with_proxy():
    model = "glm-4"
    messages = [
        {"role": "user", "content": "Hello"}
    ]
    proxy = "http://your_proxy:8080"
    async for chunk in ChatGLM.create_async_generator(model=model, messages=messages, proxy=proxy):
        print(chunk)