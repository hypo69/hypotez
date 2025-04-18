# Модуль `Myshell`

## Обзор

Модуль `Myshell` предоставляет асинхронный интерфейс для взаимодействия с сервисом Myshell AI. Он позволяет генерировать текст на основе предоставленных сообщений, используя различные модели, такие как `samantha`, `gpt-3.5-turbo` и `gpt-4`. Модуль использует вебсокеты для асинхронной потоковой передачи данных, обеспечивая эффективное взаимодействие с API Myshell.

## Подробней

Этот модуль предназначен для использования в асинхронных приложениях, требующих взаимодействия с большими языковыми моделями через API Myshell. Он инкапсулирует логику подключения к вебсокету, отправки запросов и обработки ответов, предоставляя удобный интерфейс для генерации текста.

## Классы

### `Myshell`

**Описание**: Класс `Myshell` является асинхронным провайдером, который наследует от `AsyncGeneratorProvider` и обеспечивает взаимодействие с API Myshell.

**Принцип работы**:
Класс использует асинхронные вебсокеты для отправки сообщений и получения потоковых ответов от API Myshell. Он поддерживает различные модели и предоставляет методы для генерации подписей и идентификаторов посетителей, необходимых для аутентификации и авторизации запросов.

**Аттрибуты**:
- `url` (str): URL для подключения к сервису Myshell (`https://app.myshell.ai/chat`).
- `working` (bool): Флаг, указывающий на работоспособность провайдера (по умолчанию `False`).
- `supports_gpt_35_turbo` (bool): Флаг, указывающий на поддержку модели `gpt-3.5-turbo` (по умолчанию `True`).
- `supports_gpt_4` (bool): Флаг, указывающий на поддержку модели `gpt-4` (по умолчанию `True`).

**Методы**:
- `create_async_generator`: Асинхронный генератор для создания потока текстовых ответов от Myshell.

## Функции

### `create_async_generator`

```python
@classmethod
async def create_async_generator(
    cls,
    model: str,
    messages: Messages,
    proxy: str = None,
    timeout: int = 90,
    **kwargs
) -> AsyncResult:
    """Создает асинхронный генератор для взаимодействия с API Myshell.

    Args:
        cls (type): Ссылка на класс.
        model (str): Идентификатор модели для использования (например, `samantha`, `gpt-3.5-turbo`, `gpt-4`).
        messages (Messages): Список сообщений для отправки в API.
        proxy (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
        timeout (int, optional): Время ожидания ответа от сервера в секундах. По умолчанию `90`.
        **kwargs: Дополнительные аргументы.

    Returns:
        AsyncResult: Асинхронный генератор, выдающий текстовые фрагменты ответа от API Myshell.

    Raises:
        ValueError: Если указанная модель не поддерживается.
        RuntimeError: Если получен неожиданный тип сообщения от сервера.

    """
```

**Назначение**: Создает асинхронный генератор, который взаимодействует с API Myshell для получения потоковых текстовых ответов на основе предоставленных сообщений и выбранной модели.

**Параметры**:
- `cls` (type): Ссылка на класс.
- `model` (str): Идентификатор модели для использования (например, `samantha`, `gpt-3.5-turbo`, `gpt-4`).
- `messages` (Messages): Список сообщений для отправки в API.
- `proxy` (str, optional): URL прокси-сервера для использования. По умолчанию `None`.
- `timeout` (int, optional): Время ожидания ответа от сервера в секундах. По умолчанию `90`.
- `**kwargs`: Дополнительные аргументы.

**Возвращает**:
- `AsyncResult`: Асинхронный генератор, выдающий текстовые фрагменты ответа от API Myshell.

**Вызывает исключения**:
- `ValueError`: Если указанная модель не поддерживается.
- `RuntimeError`: Если получен неожиданный тип сообщения от сервера.

**Как работает функция**:

1. **Определение идентификатора бота**:
   - Если `model` не указана, используется модель `samantha`.
   - Если `model` есть в списке поддерживаемых моделей, используется соответствующий идентификатор.
   - Если `model` не поддерживается, вызывается исключение `ValueError`.
2. **Генерация идентификатора посетителя**:
   - Генерируется `visitor_id` на основе `user_agent`.
3. **Установка соединения с WebSocket**:
   - Устанавливается асинхронное соединение с WebSocket API Myshell.
   - Отправляется приветственное сообщение и сообщение с идентификатором посетителя.
4. **Отправка сообщения чата**:
   - Форматируется текст сообщения на основе списка сообщений (`messages`).
   - Генерируется подпись (`signature`) для сообщения.
   - Отправляется сообщение чата через WebSocket.
5. **Получение и обработка сообщений**:
   - Циклически принимаются сообщения из WebSocket.
   - Если сообщение является пингом, отправляется ответ.
   - Если сообщение является сообщением чата, извлекается и выдается текст.
   - Если получен неожиданный тип сообщения, вызывается исключение `RuntimeError`.

**Внутренние функции**: Нет

**ASCII схема работы функции**:

```
    [Начало]
        ↓
    [Определение bot_id]
        ↓
    [Генерация visitor_id]
        ↓
    [Установка WebSocket соединения]
        ↓
    [Отправка приветственного сообщения]
        ↓
    [Отправка сообщения чата]
        ↓
    [Получение сообщения]
        ↓
    [Проверка типа сообщения]
        ├── [Пинг] --> [Отправка ответа]
        ├── [Сообщение чата] --> [Извлечение текста] --> [Выдача текста]
        └── [Неожиданный тип сообщения] --> [Вызов RuntimeError]
        ↓
    [Конец]
```

**Примеры**:

```python
# Пример использования create_async_generator
import asyncio
from typing import List, Dict, AsyncGenerator, Optional

async def main():
    model = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = [{"role": "user", "content": "Hello, Myshell!"}]

    generator: AsyncGenerator[str, None] = await Myshell.create_async_generator(model=model, messages=messages)
    
    async for message in generator:
        print(message, end="")

    print()

if __name__ == "__main__":
    asyncio.run(main())
```

### `generate_timestamp`

```python
def generate_timestamp() -> str:
    """Генерирует временную метку для использования в API Myshell.

    Returns:
        str: Сгенерированная временная метка в виде строки.
    """
```

**Назначение**: Генерирует временную метку, используемую для подписи запросов к API Myshell.

**Параметры**: Нет

**Возвращает**:
- `str`: Сгенерированная временная метка в виде строки.

**Как работает функция**:

1. **Получение текущего времени**:
   - Получается текущее время в миллисекундах.
2. **Преобразование и вычисление контрольной суммы**:
   - Вычисляется контрольная сумма на основе цифр текущего времени.
3. **Формирование временной метки**:
   - Объединяются преобразованное время и контрольная сумма в строку.

**Внутренние функции**: Нет

**ASCII схема работы функции**:

```
    [Начало]
        ↓
    [Получение текущего времени (мс)]
        ↓
    [Вычисление контрольной суммы]
        ↓
    [Формирование временной метки]
        ↓
    [Возврат временной метки]
        ↓
    [Конец]
```

**Примеры**:

```python
# Пример использования generate_timestamp
timestamp = generate_timestamp()
print(f"Generated timestamp: {timestamp}")
```

### `generate_signature`

```python
def generate_signature(text: str):
    """Генерирует подпись для запроса к API Myshell.

    Args:
        text (str): Текст запроса для подписи.

    Returns:
        dict: Словарь, содержащий подпись, временную метку и версию.
    """
```

**Назначение**: Генерирует подпись для запроса к API Myshell, обеспечивая аутентификацию и целостность запроса.

**Параметры**:
- `text` (str): Текст запроса, который будет подписан.

**Возвращает**:
- `dict`: Словарь, содержащий подпись (`signature`), временную метку (`timestamp`) и версию (`version`).

**Как работает функция**:

1. **Генерация временной метки**:
   - Вызывается функция `generate_timestamp()` для получения временной метки.
2. **Формирование данных для подписи**:
   - Объединяются версия, текст запроса, временная метка и секретный ключ.
3. **Вычисление MD5 хеша**:
   - Вычисляется MD5 хеш от полученных данных.
4. **Инвертирование подписи**:
   - Инвертируется полученная подпись.
5. **Формирование словаря с результатами**:
   - Создается словарь, содержащий подпись, временную метку и версию.

**Внутренние функции**: Нет

**ASCII схема работы функции**:

```
    [Начало]
        ↓
    [Генерация временной метки]
        ↓
    [Формирование данных для подписи]
        ↓
    [Вычисление MD5 хеша]
        ↓
    [Инвертирование подписи]
        ↓
    [Формирование словаря с результатами]
        ↓
    [Возврат словаря]
        ↓
    [Конец]
```

**Примеры**:

```python
# Пример использования generate_signature
text = "Hello, Myshell!"
signature_data = generate_signature(text)
print(f"Signature data: {signature_data}")
```

### `xor_hash`

```python
def xor_hash(B: str):
    """Вычисляет XOR хеш строки.

    Args:
        B (str): Строка для вычисления хеша.

    Returns:
        str: XOR хеш строки в шестнадцатеричном формате.
    """
```

**Назначение**: Вычисляет XOR хеш заданной строки. Используется для генерации идентификатора посетителя.

**Параметры**:
- `B` (str): Строка, для которой вычисляется хеш.

**Возвращает**:
- `str`: XOR хеш строки в шестнадцатеричном формате.

**Как работает функция**:

1. **Инициализация**:
   - Создается пустой список `r` для хранения байтов строки.
   - Инициализируется переменная `i` нулем, которая будет накапливать XOR хеш.
2. **Итерация по строке**:
   - Для каждого символа в строке `B` выполняется:
     - Получается код символа (ASCII).
     - Код символа добавляется в начало списка `r`.
     - Если в списке `r` становится 4 или более элементов, вычисляется XOR с накопленным значением `i`, и список `r` очищается.
3. **Обработка оставшихся байтов**:
   - Если после итерации в списке `r` остались байты, вычисляется XOR с накопленным значением `i`.
4. **Преобразование в шестнадцатеричный формат**:
   - Преобразуется накопленное значение `i` в шестнадцатеричный формат и возвращается.

**Внутренние функции**:
- `o(e, t)`: Вычисляет XOR значения `e` с накопленным значением из списка `t`.

**ASCII схема работы функции**:

```
    [Начало]
        ↓
    [Инициализация]
        ↓
    [Итерация по строке]
        ├── [Получение кода символа]
        ├── [Добавление кода в список r]
        └── [Если len(r) >= 4] --> [Вычисление XOR] --> [Очистка списка r]
        ↓
    [Обработка оставшихся байтов]
        ↓
    [Преобразование в шестнадцатеричный формат]
        ↓
    [Конец]
```

**Примеры**:

```python
# Пример использования xor_hash
text = "example_string"
hash_value = xor_hash(text)
print(f"XOR hash: {hash_value}")
```

### `performance`

```python
def performance() -> str:
    """Генерирует строку производительности на основе текущего времени.

    Returns:
        str: Строка производительности в шестнадцатеричном формате.
    """
```

**Назначение**: Генерирует строку, отражающую производительность, на основе текущего времени.

**Параметры**: Нет

**Возвращает**:
- `str`: Строка производительности в шестнадцатеричном формате.

**Как работает функция**:

1. **Получение текущего времени**:
   - Получается текущее время в миллисекундах.
2. **Определение количества итераций**:
   - Подсчитывается количество итераций, пока время не изменится.
3. **Преобразование в шестнадцатеричный формат**:
   - Преобразуются время и количество итераций в шестнадцатеричный формат.
4. **Объединение результатов**:
   - Объединяются преобразованные значения и возвращаются.

**Внутренние функции**: Нет

**ASCII схема работы функции**:

```
    [Начало]
        ↓
    [Получение текущего времени (мс)]
        ↓
    [Определение количества итераций]
        ↓
    [Преобразование в шестнадцатеричный формат]
        ↓
    [Объединение результатов]
        ↓
    [Конец]
```

**Примеры**:

```python
# Пример использования performance
performance_string = performance()
print(f"Performance string: {performance_string}")
```

### `generate_visitor_id`

```python
def generate_visitor_id(user_agent: str) -> str:
    """Генерирует идентификатор посетителя на основе user agent.

    Args:
        user_agent (str): User agent пользователя.

    Returns:
        str: Сгенерированный идентификатор посетителя.
    """
```

**Назначение**: Генерирует уникальный идентификатор посетителя на основе user agent, который используется для отслеживания и аутентификации.

**Параметры**:
- `user_agent` (str): User agent пользователя.

**Возвращает**:
- `str`: Сгенерированный идентификатор посетителя.

**Как работает функция**:

1. **Генерация компонентов идентификатора**:
   - Генерируется строка производительности с помощью функции `performance()`.
   - Генерируется случайное шестнадцатеричное число.
   - Вычисляется хеш user agent с помощью функции `xor_hash()`.
   - Генерируется строка, представляющая разрешение экрана (1080 * 1920).
2. **Объединение компонентов**:
   - Объединяются все компоненты в строку, разделенную дефисами.

**Внутренние функции**: Нет

**ASCII схема работы функции**:

```
    [Начало]
        ↓
    [Генерация строки производительности]
        ↓
    [Генерация случайного числа]
        ↓
    [Вычисление хеша user agent]
        ↓
    [Генерация строки разрешения экрана]
        ↓
    [Объединение компонентов]
        ↓
    [Конец]
```

**Примеры**:

```python
# Пример использования generate_visitor_id
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
visitor_id = generate_visitor_id(user_agent)
print(f"Visitor ID: {visitor_id}")