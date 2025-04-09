# Модуль MetaAIAccount

## Обзор

Модуль `MetaAIAccount` предоставляет класс `MetaAIAccount`, который является подклассом класса `MetaAI`. Этот класс предназначен для работы с моделями Meta AI, требующими аутентификации через аккаунт.

## Подробнее

Модуль содержит функциональность для создания асинхронного генератора, который взаимодействует с моделями Meta AI, используя cookies для аутентификации. Это позволяет получать ответы от моделей Meta AI в асинхронном режиме, обрабатывая данные частями.

## Классы

### `MetaAIAccount`

**Описание**: Класс `MetaAIAccount` предназначен для работы с моделями Meta AI, требующими аутентификации через аккаунт.

**Наследует**:
- `MetaAI`: Класс `MetaAIAccount` наследует функциональность от класса `MetaAI`, расширяя его для работы с аутентифицированными моделями Meta AI.

**Атрибуты**:
- `needs_auth` (bool): Указывает, требуется ли аутентификация для использования данного класса. Всегда `True` для `MetaAIAccount`.
- `parent` (str): Имя родительского класса. Всегда `"MetaAI"` для `MetaAIAccount`.
- `image_models` (list): Список моделей изображений, поддерживаемых классом. Всегда `["meta"]` для `MetaAIAccount`.

**Методы**:
- `create_async_generator`: Создает асинхронный генератор для взаимодействия с моделями Meta AI.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    cookies: Cookies = None,
    **kwargs
) -> AsyncResult:
    """
    Создает асинхронный генератор для взаимодействия с моделями Meta AI.

    Args:
        cls: Ссылка на класс.
        model (str): Название модели.
        messages (Messages): Список сообщений для отправки в модель.
        proxy (str, optional): Прокси-сервер для использования. По умолчанию `None`.
        cookies (Cookies, optional): Cookies для аутентификации. По умолчанию `None`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий ответы от модели Meta AI.
    """
```

**Назначение**: Создает асинхронный генератор для получения ответов от моделей Meta AI, используя cookies для аутентификации.

**Параметры**:
- `cls`: Ссылка на класс.
- `model` (str): Название модели.
- `messages` (Messages): Список сообщений для отправки в модель.
- `proxy` (str, optional): Прокси-сервер для использования. По умолчанию `None`.
- `cookies` (Cookies, optional): Cookies для аутентификации. Если `None`, пытается получить cookies из домена ".meta.ai". По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий ответы от модели Meta AI.

**Как работает функция**:

1. **Получение Cookies**:
   - Если `cookies` не предоставлены, функция пытается получить их для домена ".meta.ai".

2. **Создание Генератора**:
   - Создается экземпляр класса `MetaAIAccount` с использованием прокси (если предоставлен).
   - Вызывается метод `prompt` для получения ответа от модели Meta AI.

3. **Асинхронная Генерация**:
   - Асинхронно перебираются чанки ответа, полученные от модели, и выдаются через генератор.

```
Получение Cookies --> Создание экземпляра класса MetaAIAccount --> Вызов метода prompt --> Асинхронная генерация
```

**Примеры**:

```python
# Пример использования create_async_generator
messages = [{"role": "user", "content": "Hello, Meta AI!"}]
async for chunk in MetaAIAccount.create_async_generator(model="meta", messages=messages):
    print(chunk, end="")
```
```python
# Пример использования create_async_generator с cookies и прокси
messages = [{"role": "user", "content": "Hello, Meta AI!"}]
cookies = {"cookie_name": "cookie_value"}
async for chunk in MetaAIAccount.create_async_generator(model="meta", messages=messages, proxy="http://proxy:8080", cookies=cookies):
    print(chunk, end="")