## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код демонстрирует примеры использования библиотеки `g4f` для работы с моделью ChatCompletion.  Код содержит две функции: `create` и `create_async`.  Обе функции предназначены для получения ответа от модели ChatCompletion.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: В начале кода импортируются необходимые модули: `sys`, `Path`, `g4f`, `asyncio`.
2. **Настройка пути**: Используя `sys.path.append` добавляется путь к родительской директории.
3. **Инициализация ChatCompletion**: В первом примере кода создается объект `ChatCompletion` с помощью функции `create`. В данном случае используется модель по умолчанию, `g4f.models.default`, и задается сообщение "write a poem about a tree".  Параметр `stream=True` используется для потоковой передачи ответа.
4. **Потоковая передача**:  В цикле `for` обрабатывается  потоковая передача ответов от модели ChatCompletion.
5. **Асинхронная функция**: Во втором примере кода определена асинхронная функция `run_async()`.
6. **Создание асинхронного ответа**:  В `run_async()` используется `g4f.ChatCompletion.create_async()` для получения асинхронного ответа от модели ChatCompletion. 
7. **Запуск асинхронной функции**:  Функция `run_async()` запускается с помощью `asyncio.run(run_async())`.

Пример использования
-------------------------

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import g4f, asyncio

# Получаем ответ от модели ChatCompletion в режиме потоковой передачи
print("create:", end=" ", flush=True)
for response in g4f.ChatCompletion.create(
    model=g4f.models.default,
    #provider=g4f.Provider.Bing,  # Можно задать провайдера
    messages=[{"role": "user", "content": "write a poem about a tree"}],
    stream=True,
):
    print(response, end="", flush=True)
print()

# Получаем ответ от модели ChatCompletion асинхронно
async def run_async():
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        #provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": "hello!"}],
    )
    print("create_async:", response)

asyncio.run(run_async())
```