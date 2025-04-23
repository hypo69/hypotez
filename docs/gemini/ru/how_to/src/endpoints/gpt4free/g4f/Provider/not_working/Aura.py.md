### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный код реализует асинхронный генератор для взаимодействия с моделью чата Aura через API `openchat.team`. Он создает асинхронный генератор, который отправляет сообщения пользователя в API Aura и возвращает ответы чата в виде чанков текста.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `aiohttp` для асинхронных HTTP-запросов, `AsyncResult` и `Messages` для типизации данных, а также `AsyncGeneratorProvider` как базовый класс.
2. **Определение класса `Aura`**: Создается класс `Aura`, наследуемый от `AsyncGeneratorProvider`.
3. **Установка атрибутов класса**:
   - `url`: Устанавливается URL API `openchat.team`.
   - `working`: Устанавливается в `False`, указывая, что провайдер может быть нерабочим.
4. **Определение асинхронного метода `create_async_generator`**:
   - Принимает параметры: `model` (модель чата), `messages` (список сообщений), `proxy` (прокси-сервер), `temperature` (температура генерации), `max_tokens` (максимальное количество токенов), `webdriver`.
   - Извлекает аргументы для сессии из браузера, используя функцию `get_args_from_browser`.
   - Создает асинхронную сессию `aiohttp.ClientSession` с переданными аргументами.
   - Разделяет сообщения на системные и пользовательские.
   - Формирует данные для отправки в API, включая модель, сообщения, ключ, системное сообщение и температуру.
   - Отправляет POST-запрос к API `openchat.team` с данными в формате JSON.
   - Обрабатывает ответ от API, итерируясь по чанкам содержимого и декодируя их.
   - Возвращает чанки декодированного текста через `yield`.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.not_working.Aura import Aura
from src.typing import Message

async def main():
    messages: list[Message] = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    async for chunk in Aura.create_async_generator(model="openchat_3.6", messages=messages):
        print(chunk, end="")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())