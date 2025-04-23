### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует, как использовать библиотеку `g4f` для генерации текста с использованием модели чат-бота. Он показывает синхронный и асинхронный способы создания ответов модели на основе заданных сообщений. Код добавляет директорию уровнем выше в sys.path, чтобы можно было импортировать `g4f`.

Шаги выполнения
-------------------------
1. **Импорт необходимых библиотек**: Импортируются библиотеки `sys`, `Path`, `g4f` и `asyncio`.
2. **Добавление пути к модулю**: Модифицируется `sys.path` для добавления директории, содержащей модуль `g4f`.
3. **Синхронный запрос**:
   - Вызывается функция `g4f.ChatCompletion.create` для генерации текста на основе предоставленного сообщения.
   - Используется модель `g4f.models.default` и сообщение с ролью "user" и содержанием "write a poem about a tree".
   - Устанавливается `stream=True` для потоковой передачи ответа.
   - Полученный ответ выводится в консоль.
4. **Асинхронный запрос**:
   - Определяется асинхронная функция `run_async`.
   - Внутри `run_async` вызывается `g4f.ChatCompletion.create_async` для асинхронной генерации текста.
   - Используется модель `g4f.models.default` и сообщение с ролью "user" и содержанием "hello!".
   - Полученный ответ выводится в консоль.
5. **Запуск асинхронной функции**: Вызывается `asyncio.run` для запуска асинхронной функции `run_async`.

Пример использования
-------------------------

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