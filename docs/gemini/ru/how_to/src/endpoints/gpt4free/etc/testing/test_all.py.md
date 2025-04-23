### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для тестирования различных моделей GPT-4, предоставляемых библиотекой `g4f`. Он отправляет запросы к каждой модели и проверяет, успешно ли модель генерирует текст в ответ на запрос.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**:
   - Импортируются библиотеки `asyncio` для асинхронного выполнения, `sys` для работы с системными параметрами, `Path` из `pathlib` для работы с путями к файлам, и `g4f` для взаимодействия с моделями GPT.

2. **Добавление пути к проекту**:
   - `sys.path.append(str(Path(__file__).parent.parent.parent))` добавляет путь к родительскому каталогу проекта, чтобы можно было импортировать модуль `g4f`.

3. **Определение асинхронной функции `test`**:
   - Функция `test` принимает модель `g4f.Model` в качестве аргумента.
   - Внутри функции происходит попытка отправки запроса к модели с использованием `g4f.ChatCompletion.create` в синхронном режиме.
   - Если происходит ошибка, запрос отправляется асинхронно с использованием `g4f.ChatCompletion.create_async`.
   - В обоих случаях отправляется запрос с просьбой написать стихотворение о дереве (`"write a poem about a tree"`).
   - Ответ от модели выводится в консоль по частям (`stream=True`).
   - Если модель успешно отвечает, функция возвращает `True`, иначе - `False`.
   - Все ошибки, возникающие в процессе, логируются.

4. **Определение асинхронной функции `start_test`**:
   - Функция `start_test` определяет список моделей для тестирования (`models_to_test`).
   - Для каждой модели из списка вызывается функция `test`.
   - Если `test` возвращает `True`, имя модели добавляется в список `models_working`.
   - В конце выводится список работающих моделей.

5. **Запуск тестирования**:
   - `asyncio.run(start_test())` запускает асинхронную функцию `start_test`, что приводит к началу тестирования моделей.

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