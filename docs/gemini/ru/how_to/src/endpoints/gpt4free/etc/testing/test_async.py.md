### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для асинхронного тестирования различных провайдеров g4f (GPT4Free). Он выполняет запросы к каждому работоспособному провайдеру и логирует время выполнения, а также обрабатывает возможные исключения.

Шаги выполнения
-------------------------
1. **Настройка путей**: Добавляет в `sys.path` пути к родительским директориям, чтобы обеспечить доступ к модулям `g4f` и `testing`.
2. **Импорт модулей**: Импортирует необходимые модули, включая `asyncio`, `g4f`, `get_providers` и `log_time_async`.
3. **Определение асинхронной функции `create_async`**:
   - Принимает провайдера в качестве аргумента.
   - Вызывает метод `create_async` провайдера, передавая параметры `model` и `messages`.
   - Логирует время выполнения запроса с помощью `log_time_async`.
   - Выводит ответ провайдера или информацию об ошибке, если таковая возникает.
4. **Определение асинхронной функции `run_async`**:
   - Создает список асинхронных задач, вызывая `create_async` для каждого работоспособного провайдера, полученного из `get_providers()`.
   - Запускает все задачи параллельно с помощью `asyncio.gather()`.
5. **Запуск асинхронного кода**: Запускает асинхронную функцию `run_async` с помощью `asyncio.run()` и логирует общее время выполнения.

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
  responses: list = [\
      create_async(provider)\
      for provider in get_providers()\
      if provider.working\
  ]
  await asyncio.gather(*responses)

print("Total:", asyncio.run(log_time_async(run_async)))