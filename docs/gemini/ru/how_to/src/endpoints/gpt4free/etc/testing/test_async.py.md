## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой асинхронный тест для проверки производительности различных API-провайдеров для GPT. Он создает асинхронные задачи для каждого работающего провайдера, используя функцию `create_async`, и запускает их параллельно с помощью `asyncio.gather`.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей:**
    - `sys` - для манипулирования путями поиска модулей.
    - `pathlib` - для работы с файловыми путями.
    - `asyncio` - для асинхронного программирования.
    - `g4f` - собственная библиотека для работы с GPT.
    - `testing._providers` - для получения списка провайдеров GPT.
    - `testing.log_time` - для измерения времени выполнения асинхронных функций.
2. **Определение функции `create_async`:**
    - Функция `create_async` принимает в качестве аргумента `provider` (объект провайдера GPT).
    - Внутри функции выполняется асинхронный вызов `log_time_async` для измерения времени выполнения функции `provider.create_async`.
    - `provider.create_async` - функция, которая выполняет запрос к API провайдера GPT.
    - Запрос к API отправляется с использованием модели по умолчанию (`g4f.models.default.name`) и сообщением "Hello, are you GPT 3.5?".
    - Результат выполнения запроса (ответ) выводится на консоль.
    - В случае возникновения исключения, оно также выводится на консоль.
3. **Определение функции `run_async`:**
    - Функция `run_async` создает список асинхронных задач (`responses`) для каждого работающего провайдера GPT.
    - Задачи создаются с помощью `create_async` для каждого провайдера.
    - Затем запускает все задачи параллельно с помощью `asyncio.gather`.
4. **Запуск тестовой функции `run_async`:**
    - `asyncio.run` запускает асинхронную функцию `run_async` и измеряет ее время выполнения с помощью `log_time_async`.
    - Общее время выполнения тестовой функции выводится на консоль.

Пример использования
-------------------------

```python
import sys
from pathlib import Path
import asyncio

sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f
from testing._providers import get_providers
from testing.log_time import log_time_async

async def create_async(provider):
    try:
        response = await log_time_async(
            provider.create_async,
            model=g4f.models.default.name,
            messages=[{"role": "user", "content": "Hello, are you GPT 3.5?"}]
        )
        print(f"{provider.__name__}:", response)
    except Exception as e:
        print(f"{provider.__name__}: {e.__class__.__name__}: {e}")

async def run_async():
  responses: list = [
      create_async(provider)
      for provider in get_providers()
      if provider.working
  ]
  await asyncio.gather(*responses)

print("Total:", asyncio.run(log_time_async(run_async)))
```