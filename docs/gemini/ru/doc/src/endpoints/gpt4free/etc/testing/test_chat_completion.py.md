# Тестирование API gpt4free

## Обзор

Файл `test_chat_completion.py` предназначен для тестирования работы API `gpt4free` через библиотеку `g4f`. Файл содержит код, который отправляет запросы к API с разными параметрами, а затем выводит результаты.

## Подробней

Файл расположен в `/hypotez/src/endpoints/gpt4free/etc/testing/test_chat_completion.py`. Он содержит два тестовых сценария, один из которых выполняется синхронно, а второй асинхронно. 

## Функции

### `test_chat_completion.py`

**Описание**:  Этот файл содержит два тестовых сценария, которые отправляют запросы к API `gpt4free` с использованием библиотеки `g4f` и выводит полученные ответы.

**Параметры**: 
- `model`: Указывает модель, которая будет использоваться для генерации ответов. По умолчанию используется стандартная модель `g4f.models.default`.
- `messages`: Список сообщений, отправляемых в API. 
- `stream`: Флаг, указывающий, нужно ли использовать потоковую передачу данных. 
- `provider`: Указывает провайдера API (например, Bing). 

**Возвращает**: 
-  Этот файл не возвращает значения. Он печатает результаты запросов в консоль.

**Примеры**:

```python
print("create:", end=" ", flush=True)
for response in g4f.ChatCompletion.create(
    model=g4f.models.default,
    #provider=g4f.Provider.Bing,
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True
):
    print(response, end="", flush=True)
print()

```

**Внутренние функции**:

### `run_async()`

**Описание**: Асинхронная функция, которая отправляет запрос к API `gpt4free` с использованием библиотеки `g4f`.

**Параметры**: 
- `model`: Указывает модель, которая будет использоваться для генерации ответов. По умолчанию используется стандартная модель `g4f.models.default`.
- `messages`: Список сообщений, отправляемых в API. 
- `provider`: Указывает провайдера API (например, Bing). 

**Возвращает**: 
-  Возвращает результат запроса.

**Пример**:

```python
async def run_async():
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        #provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": "hello!"}],
    )
    print("create_async:", response)
```

##  Примеры 

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f, asyncio

print("create:", end=" ", flush=True)
for response in g4f.ChatCompletion.create(
    model=g4f.models.default,
    #provider=g4f.Provider.Bing,
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True
):
    print(response, end="", flush=True)
print()

async def run_async():
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        #provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": "hello!"}],
    )
    print("create_async:", response)

asyncio.run(run_async())