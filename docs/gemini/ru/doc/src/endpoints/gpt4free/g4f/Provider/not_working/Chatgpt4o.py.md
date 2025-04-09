# Модуль для взаимодействия с Chatgpt4o
==========================================

Модуль предоставляет асинхронный класс `Chatgpt4o`, который используется для взаимодействия с моделью gpt-4o-mini-2024-07-18 через API chatgpt4o.one.

## Обзор

Этот модуль позволяет отправлять запросы к модели `gpt-4o-mini-2024-07-18` через веб-сайт `chatgpt4o.one`. Он включает в себя функциональность для получения идентификатора поста и nonce, необходимых для аутентификации запросов.

## Подробнее

Модуль `Chatgpt4o` является асинхронным провайдером, предназначенным для интеграции с API `chatgpt4o.one`. Он автоматически извлекает необходимые параметры аутентификации, такие как `post_id` и `nonce`, и использует их для отправки запросов.

## Классы

### `Chatgpt4o`

**Описание**: Класс для взаимодействия с моделью `gpt-4o-mini-2024-07-18` через API `chatgpt4o.one`.

**Наследует**:
- `AsyncProvider`: Обеспечивает асинхронную отправку запросов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL веб-сайта `chatgpt4o.one`.
- `working` (bool): Флаг, указывающий на работоспособность провайдера.
- `_post_id` (str): Идентификатор поста, необходимый для аутентификации запросов.
- `_nonce` (str): Nonce, необходимый для аутентификации запросов.
- `default_model` (str): Модель, используемая по умолчанию (`gpt-4o-mini-2024-07-18`).
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь с псевдонимами моделей.

**Методы**:
- `create_async()`: Асинхронный метод для создания запроса к модели.

## Функции

### `create_async`

```python
    @classmethod
    async def create_async(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        timeout: int = 120,
        cookies: dict = None,
        **kwargs
    ) -> str:
        """ Асинхронно отправляет запрос к API chatgpt4o.one и возвращает результат.

        Args:
            model (str): Модель для использования.
            messages (Messages): Список сообщений для отправки.
            proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
            timeout (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
            cookies (dict, optional): Cookies для отправки с запросом. По умолчанию `None`.
            **kwargs: Дополнительные параметры.

        Returns:
            str: Ответ от API.

        Raises:
            RuntimeError: Если не удается найти `post_id` или `nonce`, или если ответ не содержит поле `data`.
        """
```

**Назначение**: Асинхронно отправляет запрос к API `chatgpt4o.one` и возвращает результат.

**Параметры**:
- `model` (str): Модель для использования.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания запроса в секундах. По умолчанию 120.
- `cookies` (dict, optional): Cookies для отправки с запросом. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `str`: Ответ от API.

**Вызывает исключения**:
- `RuntimeError`: Если не удается найти `post_id` или `nonce`, или если ответ не содержит поле `data`.

**Как работает функция**:

1. **Подготовка заголовков**: Определяются заголовки HTTP-запроса, включая `User-Agent`, `Referer` и другие необходимые параметры.
2. **Создание сессии**: Создается асинхронная сессия с использованием `StreamSession` для выполнения HTTP-запросов.
3. **Получение `post_id` и `nonce`**: Если `post_id` или `nonce` не установлены, функция выполняет GET-запрос к главной странице `chatgpt4o.one` для извлечения этих параметров из HTML-кода страницы.
4. **Форматирование запроса**: Список сообщений `messages` форматируется в строку запроса с использованием функции `format_prompt`.
5. **Отправка POST-запроса**: Отправляется POST-запрос к API `chatgpt4o.one` с данными, включающими `_wpnonce`, `post_id`, `url`, `action`, `message` и `bot_id`.
6. **Обработка ответа**: Полученный JSON-ответ проверяется на наличие поля `data`, которое содержит результат запроса. Если поле отсутствует, вызывается исключение `RuntimeError`.

```
A: Подготовка заголовков и создание сессии
|
B: Проверка наличия _post_id и _nonce
|
C: GET-запрос к chatgpt4o.one для получения _post_id и _nonce (если необходимо)
|
D: Форматирование запроса prompt = format_prompt(messages)
|
E: Отправка POST-запроса к API chatgpt4o.one
|
F: Обработка JSON-ответа и возврат данных
```

**Примеры**:

```python
import asyncio
from typing import List, Dict

from g4f.Provider.not_working.Chatgpt4o import Chatgpt4o
from g4f.typing import Message

async def main():
    messages: List[Message] = [{"role": "user", "content": "Hello, how are you?"}]
    model: str = "gpt-4o-mini-2024-07-18"
    result: str = await Chatgpt4o.create_async(model=model, messages=messages)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())