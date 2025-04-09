# Модуль `PerplexityLabs`

## Обзор

Модуль `PerplexityLabs` предоставляет асинхронный интерфейс для взаимодействия с моделями Perplexity AI Labs. Он позволяет отправлять запросы к моделям и получать ответы в виде асинхронного генератора.

## Подробнее

Модуль предназначен для интеграции с Perplexity AI Labs и предоставляет удобный способ отправки запросов к различным моделям, таким как "r1-1776", "sonar-pro", "sonar" и др. Он использует WebSocket для потоковой передачи данных и обеспечивает обработку ошибок и источников в ответах.

## Классы

### `PerplexityLabs`

**Описание**: Класс `PerplexityLabs` реализует асинхронного провайдера для моделей Perplexity AI Labs.

**Наследует**:
- `AsyncGeneratorProvider`: Обеспечивает базовую функциональность для асинхронных генераторов.
- `ProviderModelMixin`: Предоставляет общие методы для работы с моделями.

**Атрибуты**:
- `url` (str): URL для доступа к Perplexity AI Labs (`https://labs.perplexity.ai`).
- `working` (bool): Указывает, работает ли провайдер (всегда `True`).
- `default_model` (str): Модель, используемая по умолчанию (`r1-1776`).
- `models` (List[str]): Список поддерживаемых моделей.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с Perplexity AI Labs.

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
    Создает асинхронный генератор для взаимодействия с Perplexity AI Labs.

    Args:
        cls (PerplexityLabs): Класс PerplexityLabs.
        model (str): Имя используемой модели.
        messages (Messages): Список сообщений для отправки.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        **kwargs: Дополнительные параметры.

    Returns:
        AsyncResult: Асинхронный генератор, возвращающий ответы от модели.

    Raises:
        ResponseError: Если возникает ошибка при обработке ответа.
        RuntimeError: Если возникает неизвестная ошибка.

    """
```

**Назначение**: Создает асинхронный генератор для взаимодействия с Perplexity AI Labs.

**Параметры**:
- `cls` (PerplexityLabs): Класс `PerplexityLabs`.
- `model` (str): Имя используемой модели.
- `messages` (Messages): Список сообщений для отправки.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `**kwargs`: Дополнительные параметры.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, возвращающий ответы от модели.

**Вызывает исключения**:
- `ResponseError`: Если возникает ошибка при обработке ответа.
- `RuntimeError`: Если возникает неизвестная ошибка.

**Как работает функция**:

Функция `create_async_generator` выполняет следующие шаги:

1. **Настройка заголовков**: Устанавливает заголовки HTTP-запроса, включая `Origin` и `Referer`.
2. **Создание сессии**: Инициализирует асинхронную сессию с использованием `StreamSession` для поддержки потоковой передачи данных.
3. **Получение SID**: Отправляет GET-запрос к API для получения идентификатора сессии (SID).
4. **Аутентификация**: Отправляет POST-запрос для аутентификации с JWT.
5. **Подключение к WebSocket**: Устанавливает WebSocket-соединение для обмена сообщениями в реальном времени.
6. **Инициализация WebSocket**: Отправляет probe-сообщения для инициализации соединения.
7. **Отправка сообщения**: Форматирует и отправляет сообщения пользователя в формате JSON.
8. **Получение ответов**: Получает и обрабатывает сообщения от сервера, извлекая данные и флаги завершения.
9. **Обработка ошибок**: Обрабатывает возможные ошибки и возвращает исключения.
10. **Генерация результатов**: Выдает частичные результаты по мере их поступления, а также источники и причину завершения.

```
Начало
  │
  ├─► Установка заголовков и создание сессии (Create session)
  │
  ├─► Получение идентификатора сессии (Get SID)
  │
  ├─► Аутентификация (Authenticate)
  │
  ├─► Подключение к WebSocket (Connect WebSocket)
  │
  ├─► Инициализация WebSocket (Init WebSocket)
  │
  ├─► Отправка сообщения (Send message)
  │
  │   Получение ответов (Receive responses)
  │   │
  │   Проверка на сообщение "2" (Check message "2")
  │   │   └─► Отправка сообщения "3" (Send message "3")
  │   │
  │   Обработка данных (Process data)
  │   │
  │   Извлечение данных и флагов (Extract data)
  │   │
  │   Выдача результатов (Yield results)
  │   │
  │   Обработка ошибок (Handle errors)
  │
  └─► Завершение
```

**Примеры**:

```python
# Пример вызова функции create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

# from g4f.Provider.PerplexityLabs import PerplexityLabs  # Предполагается, что PerplexityLabs уже импортирован
# from g4f.typing import Messages, AsyncResult


async def main():
    model: str = "r1-1776"
    messages: List[Dict[str, str]] = [
        {"role": "user", "content": "Напиши небольшое стихотворение о природе."}
    ]
    proxy: Optional[str] = None

    generator: AsyncGenerator = PerplexityLabs.create_async_generator(
        model=model, messages=messages, proxy=proxy
    )
    
    async for message in generator:
        print(message, end="")

    print()

if __name__ == "__main__":
    asyncio.run(main())
```
Внутренние функции: Нет