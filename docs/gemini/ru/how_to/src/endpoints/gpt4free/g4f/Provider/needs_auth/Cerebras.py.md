## Как использовать Cerebras
=========================================================================================

Описание
-------------------------
Класс `Cerebras` реализует API для взаимодействия с моделью Cerebras Inference. 
Он предоставляет возможности авторизации через cookies и получение API ключа для использования модели.

Шаги выполнения
-------------------------
1. **Инициализация класса:**  Создайте экземпляр класса `Cerebras` для работы с API. 
2. **Авторизация через cookies:** Если  API ключ `api_key` не передан, класс попытается получить его из cookies.
3. **Получение API ключа:**  
    - Если cookies найдены, класс использует их для получения API ключа с сервера Cerebras.
    - API ключ извлекается из ответа сервера и сохраняется в переменной `api_key`.
4. **Использование модели:** Используйте `Cerebras.create_async_generator` для получения ответов модели. 

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth import Cerebras
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Инициализация модели
model = Cerebras.default_model  # 'llama3.1-70b'
messages: Messages = [
    {"role": "user", "content": "Привет! Как дела?"}
]

# Получение ответов от модели
async def get_response():
    cerebras = Cerebras()
    async for chunk in cerebras.create_async_generator(model, messages):
        print(chunk)

# Вызов функции
asyncio.run(get_response())
```