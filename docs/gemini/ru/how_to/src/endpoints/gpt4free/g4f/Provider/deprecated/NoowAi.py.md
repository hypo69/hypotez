## Как использовать блок кода NoowAi
=========================================================================================

Описание
-------------------------
Данный код представляет собой класс `NoowAi`, который реализует асинхронный генератор ответов для модели GPT от NoowAi. Он использует библиотеку `aiohttp` для отправки запросов к API NoowAi. 

Шаги выполнения
-------------------------
1. **Инициализация класса:** Создается экземпляр класса `NoowAi` с заданными параметрами, такими как модель и сообщения.
2. **Отправка запроса к API:** Класс `NoowAi` отправляет POST-запрос к API NoowAi с заданными параметрами.
3. **Обработка ответа:** Класс `NoowAi` обрабатывает ответ от API,  извлекая данные из  потока JSON-объектов.
4. **Генерация ответов:** Класс `NoowAi` генерирует ответы в асинхронном режиме, по одной строке за раз.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.NoowAi import NoowAi
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

messages: Messages = [
    {"role": "user", "content": "Привет, как дела?"},
    {"role": "assistant", "content": "У меня все отлично! А у тебя?"},
]

async def main():
    provider = NoowAi()
    async for response in provider.create_async_generator(model="gpt-3.5-turbo", messages=messages):
        print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Важно:** Обратите внимание, что этот фрагмент кода является устаревшим, так как NoowAi больше не предоставляет бесплатный доступ к API GPT.