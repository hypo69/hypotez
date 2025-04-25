## Как использовать класс `Opchatgpts`
=========================================================================================

Описание
-------------------------
Класс `Opchatgpts` - это асинхронный генераторный провайдер для работы с API Opchatgpts.net. Он реализует интерфейс `AsyncGeneratorProvider` и предоставляет функциональность для асинхронного получения ответов от модели GPT-3.5 Turbo с использованием истории сообщений.

Шаги выполнения
-------------------------
1. **Инициализация**: Создайте экземпляр класса `Opchatgpts`, указав модель и сообщения.
2. **Вызов метода `create_async_generator`**: Вызовите метод `create_async_generator`, передав ему модель, сообщения и необязательные аргументы, такие как прокси-сервер.
3. **Итерация по генератору**: Получите асинхронный генератор с помощью метода `create_async_generator`. Итерируйте по генератору, чтобы получить ответы от модели GPT-3.5 Turbo.
4. **Обработка ответов**: Каждый элемент генератора содержит ответ от модели. Ответы могут быть обработанны в соответствии с вашими требованиями.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Opchatgpts import Opchatgpts
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра класса Opchatgpts
provider = Opchatgpts(model="gpt-3.5-turbo", messages=[
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Хорошо, а у тебя?"},
])

# Получение асинхронного генератора
async_generator = await provider.create_async_generator(
    model="gpt-3.5-turbo",
    messages=provider.messages
)

# Итерация по генератору и обработка ответов
async for response in async_generator:
    print(f"Ответ от модели: {response}")

```

**Важно:** Класс `Opchatgpts` помечен как **устаревший** и **не рекомендуется к использованию**. Используйте другие провайдеры из `hypotez.src.endpoints.gpt4free.g4f.Provider` для работы с API GPT-4Free.