# Модуль тестирования провайдеров GPT4Free

## Обзор

Модуль `test_providers.py` предназначен для тестирования доступных провайдеров, используемых в проекте `hypotez` для взаимодействия с API GPT4Free. Он проверяет работоспособность каждого провайдера, а также его потребность в авторизации.

## Подробней

Модуль использует `concurrent.futures` для параллельного запуска тестов для всех доступных провайдеров. 
В файле `src/endpoints/gpt4free/etc/testing/test_providers.py` используются следующие провайдеры:

```python
_ = [
    'BaseProvider',
    'AsyncProvider',
    'AsyncGeneratorProvider',
    'RetryProvider'
]
```
Они определены в `src/endpoints/gpt4free/Provider.py`
В тесте используется `ChatCompletion.create` для проверки работоспособности.
Если провайдер работает без авторизации - тест выполняется.

## Функции

### `test_provider`

**Назначение**: Проверка работоспособности провайдера.

**Параметры**:

- `provider`:  Название провайдера (строка).

**Возвращает**:

- `tuple`:  Кортеж, содержащий `ChatCompletion` объект (если тест прошел успешно) и название провайдера, или `None` в случае ошибки.

**Вызывает исключения**:

- `Exception`:  В случае ошибки при тестировании провайдера.

**Как работает функция**:

- Проверяет, доступен ли провайдер, и не требуется ли авторизация. 
- Если провайдер доступен и не требуется авторизация, функция создает `ChatCompletion` объект с использованием  `ChatCompletion.create` и возвращает его вместе с названием провайдера.
- В противном случае возвращает `None`.

**Примеры**:

```python
>>> test_provider('AsyncGeneratorProvider')
('AsyncGeneratorProvider', <ChatCompletion object>)

>>> test_provider('BaseProvider')
None
```


## Примеры 

```python
from g4f.Provider import __all__, ProviderUtils
from g4f import ChatCompletion
import concurrent.futures

_ = [
    'BaseProvider',
    'AsyncProvider',
    'AsyncGeneratorProvider',
    'RetryProvider'
]

def test_provider(provider):
    """
    Проверка работоспособности провайдера.
    
    Args:
        provider (str):  Название провайдера (строка).
    
    Returns:
        tuple:  Кортеж, содержащий `ChatCompletion` объект (если тест прошел успешно) и название провайдера, или `None` в случае ошибки.
    
    Raises:
        Exception:  В случае ошибки при тестировании провайдера.
    
    Example:
        >>> test_provider('AsyncGeneratorProvider')
        ('AsyncGeneratorProvider', <ChatCompletion object>)

        >>> test_provider('BaseProvider')
        None
    """
    try:
        provider = (ProviderUtils.convert[provider])
        if provider.working and not provider.needs_auth:
            print('testing', provider.__name__)
            completion = ChatCompletion.create(model='gpt-3.5-turbo', 
                                            messages=[{"role": "user", "content": "hello"}], provider=provider)
            return completion, provider.__name__
    except Exception as e:
        #print(f'Failed to test provider: {provider} | {e}\')
        return None

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(test_provider, provider)
        for provider in __all__
        if provider not in _
    ]
    for future in concurrent.futures.as_completed(futures):
        if result := future.result():
            print(f'{result[1]} | {result[0]}')