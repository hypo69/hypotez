### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет класс `Cerebras`, который является наследником класса `OpenaiAPI`. Он предназначен для взаимодействия с API Cerebras Inference для генерации текста с использованием различных моделей, таких как llama3.1-70b, llama3.1-8b и deepseek-r1-distill-llama-70b. Класс автоматически получает ключ API из cookies или использует предоставленный, а затем использует его для создания асинхронного генератора.

Шаги выполнения
-------------------------
1. **Определение класса `Cerebras`**:
   - Класс наследуется от `OpenaiAPI`.
   - Определяются статические параметры, такие как `label`, `url`, `api_base`, `working`, `default_model`, `models` и `model_aliases`, которые задают основные настройки для взаимодействия с API Cerebras.

2. **Получение ключа API**:
   - В методе `create_async_generator` сначала проверяется, передан ли `api_key`.
   - Если `api_key` не передан, код пытается получить его из cookies для домена `.cerebras.ai`.
   - Если cookies отсутствуют, они получаются с использованием функции `get_cookies(".cerebras.ai")`.

3. **Создание HTTP сессии**:
   - Создается асинхронная сессия `ClientSession` с использованием полученных cookies.

4. **Запрос ключа API**:
   - Выполняется GET запрос к `https://inference.cerebras.ai/api/auth/session` для получения данных сессии.
   - Функция `raise_for_status` проверяет статус ответа и вызывает исключение в случае ошибки.
   - Извлекается `api_key` из JSON ответа, используя путь `data.get("user", {}).get("demoApiKey")`.

5. **Создание асинхронного генератора**:
   - Вызывается метод `create_async_generator` родительского класса (`OpenaiAPI`) с полученным `api_key` и другими необходимыми параметрами, такими как `model`, `messages` и заголовки (`headers`).

6. **Генерация чанков текста**:
   - Асинхронно перебираются чанки текста, возвращаемые генератором `super().create_async_generator()`.
   - Каждый чанк передается вызывающей стороне через `yield chunk`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.needs_auth.Cerebras import Cerebras
from src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    model = "llama3.1-70b"
    messages: Messages = [
        {"role": "user", "content": "Напиши короткий рассказ о космосе."}
    ]
    
    async for chunk in Cerebras.create_async_generator(model=model, messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())