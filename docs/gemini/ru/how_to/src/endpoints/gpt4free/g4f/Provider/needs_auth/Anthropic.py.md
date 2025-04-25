## Как использовать класс Anthropic
=========================================================================================

Описание
-------------------------
Класс `Anthropic` представляет собой провайдера для API Anthropic, который позволяет использовать модели Anthropic для генерации текста, перевода и других задач обработки естественного языка. 

Шаги выполнения
-------------------------
1. **Импорт класса:** Импортируйте класс `Anthropic` из модуля `hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Anthropic`.
2. **Создание объекта:** Создайте объект класса `Anthropic`.
3. **Инициализация:** Задайте `api_key` для использования API Anthropic.
4. **Вызов методов:** Используйте методы класса для вызова различных функций API.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.Anthropic import Anthropic

# Создаем объект класса Anthropic
anthropic = Anthropic()

# Инициализируем API ключ
anthropic.api_key = "YOUR_API_KEY"

# Вызываем метод `create_async_generator` для генерации текста
async def generate_text():
    messages = [
        {"role": "user", "content": "Напишите мне стихотворение о любви."}
    ]
    async for response in anthropic.create_async_generator(model="claude-3-5-sonnet-latest", messages=messages):
        print(response)

# Запускаем асинхронную функцию
asyncio.run(generate_text())

```