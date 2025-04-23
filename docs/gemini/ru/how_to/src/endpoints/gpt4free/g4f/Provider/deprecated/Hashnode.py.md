Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код определяет асинхронный провайдер `Hashnode` для взаимодействия с API Hashnode Rix. Он поддерживает модели GPT-3.5 Turbo и позволяет выполнять поисковые запросы различных типов (быстрый, код, веб-поиск). Класс `Hashnode` использует `aiohttp` для асинхронных HTTP-запросов к API Hashnode, чтобы генерировать ответы на основе предоставленных сообщений и поисковых данных.

Шаги выполнения
-------------------------
1. **Инициализация класса `Hashnode`**:
   - Определяется класс `Hashnode`, наследующийся от `AsyncGeneratorProvider`.
   - Указывается URL `https://hashnode.com` как базовый для API Hashnode.
   - Устанавливается флаг `working = False`, который, вероятно, указывает на работоспособность провайдера (требуется актуализация).
   - Включается поддержка истории сообщений (`supports_message_history = True`) и модели GPT-3.5 Turbo (`supports_gpt_35_turbo = True`).
   - Инициализируется пустой список `_sources` для хранения результатов поиска.

2. **Метод `create_async_generator`**:
   - Этот метод является асинхронным генератором, который отправляет запросы к API Hashnode и возвращает чанки данных.
   - Принимает параметры:
     - `model` (str): Не используется в коде, но подразумевается для указания используемой модели.
     - `messages` (Messages): Список сообщений для контекста запроса.
     - `search_type` (str): Тип поиска (`quick`, `code`, `websearch`). По умолчанию используется `websearch`.
     - `proxy` (str): URL прокси-сервера для использования.
     - `**kwargs`: Дополнительные параметры.

3. **Формирование заголовков**:
   - Создаются HTTP-заголовки для запроса, включающие `User-Agent`, `Accept`, `Referer`, `Content-Type` и другие необходимые параметры.

4. **Создание асинхронной сессии**:
   - Используется `aiohttp.ClientSession` для выполнения асинхронных HTTP-запросов.

5. **Подготовка данных для запроса**:
   - Извлекается последний элемент из списка `messages` и берется его содержимое (`content`) в качестве `prompt`.
   - Очищается список `cls._sources`.

6. **Выполнение поискового запроса (если `search_type == "websearch"`):**
   - Отправляется POST-запрос к `f"{cls.url}/api/ai/rix/search"` с параметром `prompt`.
   - Извлекаются результаты поиска из JSON-ответа и сохраняются в `cls._sources`.

7. **Формирование данных для запроса на завершение**:
   - Создается словарь `data`, включающий:
     - `chatId`: Случайный шестнадцатеричный идентификатор, полученный с помощью `get_random_hex()`.
     - `history`: Список сообщений `messages`.
     - `prompt`: Текст запроса.
     - `searchType`: Тип поиска.
     - `urlToScan`: Всегда `None`.
     - `searchResults`: Результаты поиска `cls._sources`.

8. **Отправка запроса на завершение**:
   - Отправляется POST-запрос к `f"{cls.url}/api/ai/rix/completion"` с данными `data`.
   - Полученные чанки данных из ответа декодируются и генерируются через `yield`.

9. **Метод `get_sources`**:
   - Возвращает список источников (источники поиска) в формате словарей, содержащих `title` и `url` для каждого источника.

Пример использования
-------------------------

```python
from src.endpoints.gpt4free.g4f.Provider.deprecated import Hashnode
from src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import SearchTypes

async def main():
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    async for chunk in Hashnode.create_async_generator(
        model="gpt-3.5-turbo", 
        messages=messages,
        search_type=SearchTypes.websearch
    ):
        print(chunk, end="")

    sources = Hashnode.get_sources()
    print(f"\nSources: {sources}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())