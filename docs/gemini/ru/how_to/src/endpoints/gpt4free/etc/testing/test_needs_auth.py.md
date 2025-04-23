### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предназначен для тестирования различных провайдеров GPT-4 Free API, таких как H2o, You, HuggingChat, OpenAssistant, Bing и Bard. Он выполняет запросы к этим провайдерам как асинхронно, так и с использованием потоковой передачи (stream) и без нее, замеряя время выполнения каждого запроса. Дополнительно, демонстрируется пример использования аутентификации для провайдера Bing.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
   - Импортируются библиотеки `sys`, `pathlib`, `asyncio`.
   - Добавляется путь к родительской директории для импорта модуля `g4f` и `testing.log_time`.
   - Импортируются `g4f`, `log_time`, `log_time_async`, `log_time_yield`.

2. **Определение списка провайдеров**:
   - Создается список `_providers`, содержащий различные провайдеры, такие как `H2o`, `You`, `HuggingChat`, `OpenAssistant`, `Bing` и `Bard`.

3. **Определение тестового запроса**:
   - Определяется строка `_instruct` с тестовым запросом "Hello, are you GPT 4?".

4. **Функция для потоковой передачи (stream) с аутентификацией для Bing**:
   - Выполняется запрос к провайдеру Bing с использованием потоковой передачи и аутентификации.
   - Измеряется время выполнения запроса с помощью `log_time_yield`.
   - Выводится ответ в консоль.

5. **Асинхронная функция `run_async`**:
   - Создается список асинхронных задач для каждого провайдера в списке `_providers`.
   - Каждая задача отправляет запрос `_instruct` к соответствующему провайдеру.
   - Используется `asyncio.gather` для параллельного выполнения всех задач.
   - Выводятся ответы и имена провайдеров.
   - Измеряется общее время выполнения асинхронных запросов.

6. **Функция `run_stream` для потоковой передачи**:
   - Для каждого провайдера выполняется запрос с использованием потоковой передачи.
   - Ответы выводятся в консоль по мере поступления.
   - Измеряется общее время выполнения запросов с потоковой передачей.

7. **Функция `create_no_stream` для запросов без потоковой передачи**:
   - Для каждого провайдера выполняется запрос без использования потоковой передачи.
   - Ответы выводятся в консоль после завершения запроса.
   - Измеряется общее время выполнения запросов без потоковой передачи.

Пример использования
-------------------------

```python
import sys
from pathlib import Path
import asyncio

sys.path.append(str(Path(__file__).parent.parent))

import g4f
from testing.log_time import log_time, log_time_async, log_time_yield

_providers = [
    g4f.Provider.H2o,
    g4f.Provider.You,
    g4f.Provider.HuggingChat,
    g4f.Provider.OpenAssistant,
    g4f.Provider.Bing,
    g4f.Provider.Bard
]

_instruct = "Hello, are you GPT 4?."

print("Bing: ", end="")
for response in log_time_yield(
    g4f.ChatCompletion.create,
    model=g4f.models.default,
    messages=[{"role": "user", "content": _instruct}],
    provider=g4f.Provider.Bing,
    stream=True,
    auth=True
):
    print(response, end="", flush=True)
print()
print()

async def run_async():
    responses = [
        log_time_async(
            provider.create_async,
            model=None,
            messages=[{"role": "user", "content": _instruct}],
        )
        for provider in _providers
    ]
    responses = await asyncio.gather(*responses)
    for idx, provider in enumerate(_providers):
        print(f"{provider.__name__}:", responses[idx])
print("Async Total:", asyncio.run(log_time_async(run_async)))
print()

def run_stream():
    for provider in _providers:
        print(f"{provider.__name__}: ", end="")
        for response in log_time_yield(
            provider.create_completion,
            model=None,
            messages=[{"role": "user", "content": _instruct}],
        ):
            print(response, end="", flush=True)
        print()
print("Stream Total:", log_time(run_stream))
print()

def create_no_stream():
    for provider in _providers:
        print(f"{provider.__name__}:", end=" ")
        for response in log_time_yield(
            provider.create_completion,
            model=None,
            messages=[{"role": "user", "content": _instruct}],
            stream=False
        ):
            print(response, end="")
        print()
print("No Stream Total:", log_time(create_no_stream))
print()