## Как использовать блок кода `Airforce`
=========================================================================================

Описание
-------------------------
Блок кода `Airforce` - это провайдер для асинхронной генерации текста и изображений с использованием сервиса API `airforce`. Он включает в себя методы для работы с различными моделями, такими как `llama-3.1-70b-chat`, `flux`, `openchat-3.5`, `deepseek-coder`, `hermes-2-dpo`, `hermes-2-pro`, `openhermes-2.5`, `lfm-40b`, `german-7b`, `llama-2-7b`, `llama-3.1-70b`, `llama-3.1-8b`, `neural-7b`, `zephyr-7b`, `evil`, `sdxl`, `flux-pro`, и предоставляет асинхронные генераторы для обработки ответов от API.

Шаги выполнения
-------------------------
1. **Импорт класса `Airforce`**: Импортируйте класс `Airforce` из модуля `hypotez/src/endpoints/gpt4free/g4f/Provider/not_working/Airforce.py`.

2. **Инициализация объекта `Airforce`**: Создайте экземпляр класса `Airforce`.

3. **Использование метода `create_async_generator`**: Вызовите метод `create_async_generator` для асинхронной генерации текста или изображений. Передайте в качестве аргументов:
    - `model`: Название модели (например, `llama-3.1-70b-chat`).
    - `messages`: Список сообщений в чате, представляющий контекст.
    - `prompt`: Текстовый запрос для генерации текста или изображения.
    - `proxy`: Прокси-сервер для использования.
    - `max_tokens`: Максимальное количество токенов для генерации текста.
    - `temperature`: Температура для генерации текста (от 0 до 1).
    - `top_p`: Вероятность выбора слова для генерации текста (от 0 до 1).
    - `stream`: Флаг, указывающий, нужно ли использовать потоковую генерацию.
    - `size`: Размер изображения для генерации (например, `1:1`).
    - `seed`: Случайное число для генерации изображения.

4. **Обработка асинхронного генератора**: Итерация по асинхронному генератору для получения результатов.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.Airforce import Airforce

async def generate_text_example():
    """Пример генерации текста."""
    airforce = Airforce()
    messages = [
        {"role": "user", "content": "Привет!"},
    ]
    async for result in airforce.create_async_generator(
        model="llama-3.1-70b-chat",
        messages=messages,
        max_tokens=512,
        temperature=0.7,
        top_p=1,
        stream=True,
    ):
        print(result)  # Вывод результатов

async def generate_image_example():
    """Пример генерации изображения."""
    airforce = Airforce()
    prompt = "Сюрреалистическая картина кошки, сидящей на луне"
    async for result in airforce.create_async_generator(
        model="flux",
        prompt=prompt,
        size="1:1",
        seed=12345,
    ):
        print(result)  # Вывод результатов

if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_text_example())
    asyncio.run(generate_image_example())

```

**Важно**: данный провайдер находится в `not_working` и может быть недоступен. Используйте другие провайдеры.