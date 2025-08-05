## Как использовать Qwen_Qwen_2_5M
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой класс `Qwen_Qwen_2_5M`, который реализует асинхронный генератор ответов с помощью модели Qwen 2.5M от Hugging Face Spaces. Он позволяет генерировать текст, используя заданный prompt и модель Qwen 2.5M.

Шаги выполнения
-------------------------
1. **Инициализация класса**:  Класс `Qwen_Qwen_2_5M` создает соединение с API Hugging Face Spaces и устанавливает необходимые параметры для модели Qwen 2.5M. 
2. **Генерация сессии**: Класс генерирует уникальный идентификатор сессии для каждого запроса.
3. **Форматирование запроса**: Данные запроса (prompt) форматируются в соответствии с требованиями API Hugging Face Spaces.
4. **Отправка запроса**:  Класс отправляет запрос на API Hugging Face Spaces с использованием библиотеки `aiohttp`.
5. **Обработка ответа**: Класс получает ответ от API Hugging Face Spaces, преобразует его в удобочитаемый формат и возвращает его в виде асинхронного генератора.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.Qwen_Qwen_2_5M import Qwen_Qwen_2_5M
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

async def main():
    """Пример использования класса Qwen_Qwen_2_5M для генерации текста."""
    model = "qwen-2.5-1m"  # Имя модели Qwen 2.5M
    messages: Messages = [
        {"role": "user", "content": "Напиши короткую историю про кота."}
    ]  # Запрос (prompt)
    provider = Qwen_Qwen_2_5M()  # Инициализация класса Qwen_Qwen_2_5M
    async for response in provider.create_async_generator(model=model, messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```