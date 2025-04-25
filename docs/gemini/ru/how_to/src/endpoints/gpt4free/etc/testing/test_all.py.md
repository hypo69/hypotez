## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода осуществляет тестирование различных моделей GPT-3.5 и GPT-4. Он посылает запрос на генерацию стихотворения о дереве и проверяет, работают ли модели. 

Шаги выполнения
-------------------------
1. **Инициализация:**
    - Импортируются необходимые модули: `asyncio`, `sys`, `Path`, `g4f`.
    - Добавляется путь к директории проекта в `sys.path`.
2. **Функция `test`:**
    - Эта функция тестирует работу модели GPT.
    - Она отправляет запрос на генерацию стихотворения о дереве.
    - Использует `g4f.ChatCompletion.create` или `g4f.ChatCompletion.create_async` для отправки запроса.
    - Печатает результат в консоль.
    - Возвращает `True`, если модель работает, и `False` в противном случае.
3. **Функция `start_test`:**
    - Создает список моделей для тестирования: `models_to_test`.
    - Создает пустой список `models_working` для хранения работающих моделей.
    - Итерирует по каждой модели в `models_to_test`:
        - Вызывает `test(model)` для проверки модели.
        - Если модель работает, добавляет ее имя в `models_working`.
    - Печатает список работающих моделей.
4. **Вызов `asyncio.run(start_test())`:**
    - Запускает асинхронную функцию `start_test()`.

Пример использования
-------------------------

```python
import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f

async def test(model: g4f.Model):
    try:
        try:
            for response in g4f.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": "write a poem about a tree"}],
                    temperature=0.1,
                    stream=True
            ):
                print(response, end="")

            print()
        except:
            for response in await g4f.ChatCompletion.create_async(
                    model=model,
                    messages=[{"role": "user", "content": "write a poem about a tree"}],
                    temperature=0.1,
                    stream=True
            ):
                print(response, end="")

            print()

        return True
    except Exception as e:
        print(model.name, "not working:", e)
        print(e.__traceback__.tb_next)
        return False


async def start_test():
    models_to_test = [
        # GPT-3.5
        g4f.models.gpt_35_turbo,

        # GPT-4
        g4f.models.gpt_4,
    ]

    models_working = []

    for model in models_to_test:
        if await test(model):
            models_working.append(model.name)

    print("working models:", models_working)


asyncio.run(start_test())
```

**Важно**:
- Этот код использует библиотеку `g4f` для взаимодействия с API OpenAI. 
- Не забудьте установить библиотеку `g4f` и настроить API-ключ OpenAI.
- Убедитесь, что вы имеете доступ к API OpenAI, чтобы использовать этот код.