Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код представляет собой класс `Chatgpt4Online`, который является асинхронным провайдером для взаимодействия с API chatgpt4online.org. Он использует `aiohttp` для выполнения асинхронных HTTP-запросов. Код получает `nonce` для авторизации, формирует запрос к API и извлекает данные из потока ответов, отправляемых сервером.

Шаги выполнения
-------------------------
1. **Определение класса `Chatgpt4Online`**: Определяется класс `Chatgpt4Online`, наследующийся от `AsyncGeneratorProvider`. Указываются URL, API endpoint, флаг `working`, модель по умолчанию и список поддерживаемых моделей.
2. **Получение `nonce`**:
   - Функция `get_nonce` выполняет POST-запрос к `https://chatgpt4online.org/wp-json/mwai/v1/start_session` для получения `nonce`, необходимого для авторизации.
   - Создается `ClientSession` для выполнения запроса.
   - Извлекается значение `restNonce` из JSON-ответа.
3. **Создание асинхронного генератора**:
   - Метод `create_async_generator` создает асинхронный генератор для взаимодействия с API.
   - Формируются заголовки (`headers`) для HTTP-запроса, включая `x-wp-nonce`, полученный из `get_nonce`.
   - Создается `ClientSession` с заданными заголовками.
   - Формируется тело запроса (`data`) с использованием переданных сообщений (`messages`) и форматируется с помощью `format_prompt`.
4. **Отправка запроса и обработка ответа**:
   - Выполняется POST-запрос к API endpoint `f"{cls.url}{cls.api_endpoint}"` с использованием `session.post`.
   - Обрабатывается ответ от сервера по частям (`chunk`) в асинхронном режиме.
   - Каждый `chunk` декодируется, разделяется на строки, и извлекаются JSON-данные из строк, начинающихся с `"data: "`.
   - Если `"type"` имеет значение `"live"`, данные добавляются к `full_response`.
   - Если `"type"` имеет значение `"end"`, извлекается финальный ответ из `"data"` и присваивается `full_response`.
   - Генератор возвращает `full_response`.
5. **Обработка ошибок**:
   - В процессе обработки JSON-данных отлавливается исключение `json.JSONDecodeError`, и в случае ошибки итерация продолжается.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.not_working import Chatgpt4Online
from src.endpoints.gpt4free.g4f.typing import Messages
import asyncio

async def main():
    messages: Messages = [{"role": "user", "content": "Привет, как дела?"}]
    model = "gpt-4"
    
    async for response in Chatgpt4Online.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    asyncio.run(main())