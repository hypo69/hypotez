# Модуль Koala для работы с gpt4free

## Обзор

Модуль `Koala` предоставляет асинхронтный генератор для взаимодействия с API Koala.sh, который позволяет использовать различные модели, включая `gpt-4o-mini`. Этот модуль предназначен для интеграции в gpt4free, обеспечивая возможность общаться с Koala.sh через асинхронные запросы.

## Подробней

Модуль `Koala` является асинхронным провайдером, который использует `aiohttp` для выполнения HTTP-запросов к API Koala.sh. Он поддерживает передачу истории сообщений для поддержания контекста разговора. Модуль предназначен для интеграции в систему `gpt4free`.

## Классы

### `Koala`

**Описание**: Класс `Koala` реализует асинхронный генератор для взаимодействия с API Koala.sh.

   **Наследует**:
   - `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных провайдеров, работающих с генераторами.
   - `ProviderModelMixin`: Предоставляет функциональность для работы с моделями провайдера.

   **Атрибуты**:
   - `url` (str): URL Koala.sh.
   - `api_endpoint` (str): URL API для взаимодействия с Koala.sh.
   - `working` (bool): Указывает, работает ли провайдер в данный момент.
   - `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений.
   - `default_model` (str): Модель, используемая по умолчанию, если не указана другая.

   **Методы**:
   - `create_async_generator`: Создает асинхронный генератор для обмена сообщениями с Koala.sh.
   - `_parse_event_stream`: Статический метод для обработки потока событий, возвращаемого API Koala.sh.

   **Принцип работы**:
   - Класс `Koala` использует асинхронные запросы для взаимодействия с API Koala.sh. Он формирует запросы на основе истории сообщений и модели, указанной пользователем. Полученные ответы обрабатываются как поток событий, который затем преобразуется в асинхронный генератор.

   **Методы**:
   - `create_async_generator`:
      - **Назначение**: Создает асинхронный генератор для обмена сообщениями с Koala.sh.
   - `_parse_event_stream`:
      - **Назначение**: Разбирает поток событий ответа и преобразует его в асинхронный генератор.

## Функции

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: Optional[str] = None,
        connector: Optional[BaseConnector] = None,
        **kwargs: Any
    ) -> AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]:
        """
        Создает асинхронный генератор для обмена сообщениями с Koala.sh.

        Args:
            model (str): Название модели для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
            connector (Optional[BaseConnector], optional): Aiohttp коннектор. По умолчанию `None`.
            **kwargs (Any): Дополнительные аргументы.

        Returns:
            AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]: Асинхронный генератор, возвращающий ответы от Koala.sh.

        Raises:
            Exception: Возникает, если происходит ошибка при подключении или обработке запроса.
        """
        ...
```

   **Параметры**:
   - `model` (str): Название модели для использования.
   - `messages` (Messages): Список сообщений для отправки.
   - `proxy` (Optional[str], optional): Прокси-сервер для использования. По умолчанию `None`.
   - `connector` (Optional[BaseConnector], optional): Aiohttp коннектор. По умолчанию `None`.
   - `**kwargs` (Any): Дополнительные аргументы.

   **Возвращает**:
   - `AsyncGenerator[Dict[str, Union[str, int, float, List[Dict[str, Any]], None]], None]`: Асинхронный генератор, возвращающий ответы от Koala.sh.

   **Вызывает исключения**:
   - `Exception`: Возникает, если происходит ошибка при подключении или обработке запроса.

   **Как работает функция**:

   1. **Инициализация**: Функция получает параметры, такие как модель, сообщения, прокси и коннектор. Если модель не указана, используется модель по умолчанию `gpt-4o-mini`.
   2. **Формирование заголовков**: Создаются заголовки для HTTP-запроса, включая `User-Agent`, `Accept`, `Referer` и другие необходимые параметры.
   3. **Создание сессии**: Используется `aiohttp.ClientSession` для управления HTTP-соединением. При необходимости используется прокси и/или коннектор.
   4. **Подготовка данных**: Формируются данные для отправки в API, включая входной текст, историю ввода и вывода сообщений, а также название модели.
   5. **Отправка запроса**: Отправляется POST-запрос к API Koala.sh с подготовленными данными.
   6. **Обработка ответа**: Полученный ответ обрабатывается с помощью асинхронного генератора `_parse_event_stream`, который извлекает данные из потока событий.
   7. **Возврат генератора**: Функция возвращает асинхронный генератор, который позволяет получать ответы от API Koala.sh по мере их поступления.

   **Внутренние функции**: Нет внутренних функций

   **ASCII flowchart**:

   ```
   Начало
     ↓
   Проверка модели (если не указана, используется gpt-4o-mini)
     ↓
   Формирование заголовков
     ↓
   Создание асинхронной сессии (с прокси и коннектором, если указаны)
     ↓
   Подготовка данных для запроса (входной текст, история сообщений, модель)
     ↓
   Отправка POST-запроса к API Koala.sh
     ↓
   Обработка ответа с помощью _parse_event_stream
     ↓
   Возврат асинхронного генератора
     ↓
   Конец
   ```

   **Примеры**:

   ```python
   # Пример использования create_async_generator
   import asyncio
   from typing import List, Dict, Any

   async def main():
       messages: List[Dict[str, str]] = [
           {"role": "user", "content": "Привет, как дела?"},
           {"role": "assistant", "content": "Привет! У меня все хорошо, спасибо!"},
           {"role": "user", "content": "Расскажи что-нибудь интересное."},
       ]

       async for chunk in Koala.create_async_generator(model="gpt-4o-mini", messages=messages):
           print(chunk)

   if __name__ == "__main__":
       asyncio.run(main())
   ```

### `_parse_event_stream`

```python
    @staticmethod
    async def _parse_event_stream(response: ClientResponse) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Разбирает поток событий ответа и преобразует его в асинхронный генератор.

        Args:
            response (ClientResponse): Объект ответа от API Koala.sh.

        Returns:
            AsyncGenerator[Dict[str, Any], None]: Асинхронный генератор, возвращающий данные из потока событий.
        """
        ...
```

   **Параметры**:
   - `response` (ClientResponse): Объект ответа от API Koala.sh.

   **Возвращает**:
   - `AsyncGenerator[Dict[str, Any], None]`: Асинхронный генератор, возвращающий данные из потока событий.

   **Как работает функция**:

   1. **Итерация по чанкам**: Функция асинхронно итерируется по чанкам, полученным из ответа `response.content`.
   2. **Проверка префикса**: Для каждого чанка проверяется, начинается ли он с префикса `b"data: "`.
   3. **Извлечение данных**: Если чанк начинается с указанного префикса, извлекаются данные, начиная с 6-го байта (после `data: `).
   4. **Декодирование JSON**: Извлеченные данные декодируются из JSON-формата с помощью `json.loads`.
   5. **Возврат данных**: Декодированные данные возвращаются через асинхронный генератор.

   **Внутренние функции**: Нет внутренних функций

   **ASCII flowchart**:

   ```
   Начало
     ↓
   Итерация по чанкам в response.content
     ↓
   Проверка, начинается ли чанк с "data: "
     ├──-> Да: Извлечение данных после "data: "
     │      ↓
     │   Декодирование JSON
     │      ↓
     │   Выдача данных через генератор
     │      ↓
     └──-> Нет: Переход к следующему чанку
     ↓
   Конец
   ```

   **Примеры**:

   ```python
   # Пример использования _parse_event_stream
   import asyncio
   from aiohttp import ClientSession
   from typing import AsyncGenerator, Dict, Any

   async def fetch_data() -> AsyncGenerator[Dict[str, Any], None]:
       async with ClientSession() as session:
           async with session.get("https://example.com/api/stream") as response:  # Замените URL на реальный endpoint
               async for item in Koala._parse_event_stream(response):
                   yield item

   async def main():
       async for data in fetch_data():
           print(data)

   if __name__ == "__main__":
       asyncio.run(main())
   ```