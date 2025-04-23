# Документация модуля `RubiksAI.py`

## Обзор

Модуль предоставляет асинхронный интерфейс для взаимодействия с API Rubiks AI. Он позволяет генерировать текст на основе предоставленных сообщений, используя различные модели, поддерживаемые Rubiks AI. Модуль поддерживает потоковую передачу ответов, системные сообщения и историю сообщений.

## Более подробная информация

Модуль предназначен для интеграции с другими частями проекта `hypotez`, где требуется использование AI моделей для генерации текста. Он предоставляет удобный интерфейс для отправки запросов к API Rubiks AI и обработки полученных ответов.

## Классы

### `RubiksAI`

**Описание**: Класс предоставляет функциональность для взаимодействия с API Rubiks AI для генерации текста.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает асинхронную генерацию данных.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `label` (str): Метка провайдера, "Rubiks AI".
- `url` (str): URL сайта Rubiks AI, "https://rubiks.ai".
- `api_endpoint` (str): URL API endpoint Rubiks AI, "https://rubiks.ai/search/api/".
- `working` (bool): Указывает, работает ли провайдер, `True`.
- `supports_stream` (bool): Указывает, поддерживает ли провайдер потоковую передачу, `True`.
- `supports_system_message` (bool): Указывает, поддерживает ли провайдер системные сообщения, `True`.
- `supports_message_history` (bool): Указывает, поддерживает ли провайдер историю сообщений, `True`.
- `default_model` (str): Модель, используемая по умолчанию, `gpt-4o-mini`.
- `models` (List[str]): Список поддерживаемых моделей.
- `model_aliases` (Dict[str, str]): Словарь псевдонимов моделей.

**Принцип работы**:
Класс использует асинхронные запросы для взаимодействия с API Rubiks AI. Он генерирует уникальные идентификаторы (`mid`) и URL-адреса для каждого запроса. Поддерживает потоковую передачу ответов, что позволяет получать ответы по частям.

**Методы**:
- `generate_mid()`: Генерирует уникальный идентификатор сообщения.
- `create_referer()`: Создает URL-адрес Referer с динамическими параметрами.
- `create_async_generator()`: Создает асинхронный генератор для отправки запросов и получения ответов.

## Методы класса

### `generate_mid`

```python
    @staticmethod
    def generate_mid() -> str:
        """
        Генерирует строку 'mid' в формате:
        6 символов - 4 символа - 4 символа - 4 символа - 12 символов
        Пример: 0r7v7b-quw4-kdy3-rvdu-ekief6xbuuq4

        Returns:
            str: Сгенерированная строка 'mid'.
        """
```

### `create_referer`

```python
    @staticmethod
    def create_referer(q: str, mid: str, model: str = '') -> str:
        """
        Создает URL-адрес Referer с динамическими значениями q и mid, используя urlencode для безопасного кодирования параметров.

        Args:
            q (str): Значение параметра q.
            mid (str): Значение параметра mid.
            model (str, optional): Значение параметра model. Defaults to ''.

        Returns:
            str: Сгенерированный URL-адрес Referer.
        """
```

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        web_search: bool = False,
        temperature: float = 0.6,
        **kwargs
    ) -> AsyncResult:
        """
        Создает асинхронный генератор, который отправляет запросы к API Rubiks AI и возвращает ответ.

        Args:
            model (str): Модель для использования в запросе.
            messages (Messages): Сообщения для отправки в качестве запроса.
            proxy (str, optional): URL прокси-сервера, если необходимо.
            web_search (bool, optional): Указывает, следует ли включать источники поиска в ответ. Defaults to False.
            temperature (float, optional): Температура для использования в запросе. Defaults to 0.6.

        Returns:
            AsyncResult: Асинхронный генератор, возвращающий ответ от API.

        Raises:
            Exception: Если возникает ошибка при отправке запроса или обработке ответа.

        Как работает функция:
        - Функция создает URL-адрес Referer с использованием предоставленных параметров.
        - Формирует данные запроса, включающие сообщения, модель, параметры поиска и температуру.
        - Отправляет асинхронный POST-запрос к API Rubiks AI с использованием `ClientSession`.
        - Обрабатывает ответ, извлекая данные из потока событий (`text/event-stream`).
        - Извлекает контент из ответов и возвращает его через генератор.
        - Обрабатывает источники веб-поиска, если они включены.
        """
```

## Примеры

### `generate_mid`
```python
mid = RubiksAI.generate_mid()
print(mid)
# Вывод: Пример: 0r7v7b-quw4-kdy3-rvdu-ekief6xbuuq4
```

### `create_referer`
```python
referer = RubiksAI.create_referer(q='test query', mid='0r7v7b-quw4-kdy3-rvdu-ekief6xbuuq4', model='gpt-4o-mini')
print(referer)
# Вывод: https://rubiks.ai/search/?q=test+query&model=gpt-4o-mini&mid=0r7v7b-quw4-kdy3-rvdu-ekief6xbuuq4
```

### `create_async_generator`
```python
import asyncio
from typing import List, Dict

async def main():
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, how are you?"}]
    generator = await RubiksAI.create_async_generator(model='gpt-4o-mini', messages=messages)
    async for message in generator:
        print(message)

if __name__ == "__main__":
    asyncio.run(main())