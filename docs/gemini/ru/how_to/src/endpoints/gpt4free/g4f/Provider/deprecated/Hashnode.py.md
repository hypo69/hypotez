## Как использовать класс `Hashnode`
=========================================================================================

Описание
-------------------------
Класс `Hashnode` реализует асинхронный генератор, который использует API сайта `hashnode.com` для получения ответов от модели GPT-3.5 Turbo.

Шаги выполнения
-------------------------
1. **Инициализация генератора**: Вызывается метод `Hashnode.create_async_generator`, который создает асинхронный генератор. Метод принимает в качестве аргументов:
    - `model`: Имя модели (например, `gpt-3.5-turbo`).
    - `messages`: Список сообщений в истории диалога.
    - `search_type`: Тип поиска (по умолчанию `SearchTypes.websearch`).
    - `proxy`: Прокси-сервер (необязательно).
2. **Инициализация заголовков запроса**: Создается словарь `headers` с необходимыми заголовками для запроса к API `hashnode.com`.
3. **Инициализация `prompt`**: Извлекается текст последнего сообщения из списка `messages`.
4. **Поиск в интернете (при необходимости)**:
    - Если `search_type` равен `SearchTypes.websearch`, отправляется POST-запрос к `https://hashnode.com/api/ai/rix/search` с текстом `prompt`.
    - Полученный ответ преобразуется в JSON и сохраняется в атрибуте `cls._sources`.
5. **Отправка запроса на генерацию текста**:
    - Формируется словарь `data`, содержащий информацию о чате, истории сообщений, тексте `prompt`, типе поиска и результатах поиска (если они были).
    - Отправляется POST-запрос к `https://hashnode.com/api/ai/rix/completion` с JSON-данными из `data`.
6. **Получение ответа**: 
    - Генератор последовательно выдает полученные от API данные в виде отдельных кусков текста.
7. **Получение источников (при наличии)**:
    -  Метод `Hashnode.get_sources()` возвращает список источников, полученных в процессе поиска (если он был запущен).

Пример использования
-------------------------
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Hashnode, SearchTypes
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import Messages
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Hashnode import AsyncResult

async def main():
    messages: Messages = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "Хорошо, а у тебя?"},
    ]
    async for chunk in Hashnode.create_async_generator(
        model='gpt-3.5-turbo',
        messages=messages,
        search_type=SearchTypes.websearch
    ):
        print(chunk, end='')

    print(Hashnode.get_sources())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Важные замечания**:
- Данный фрагмент кода использует API сайта `hashnode.com` для получения ответов от модели GPT-3.5 Turbo.
- Метод `Hashnode.create_async_generator` создает асинхронный генератор, который последовательно выдает полученные от API данные в виде отдельных кусков текста.
- Метод `Hashnode.get_sources` возвращает список источников, полученных в процессе поиска (если он был запущен).
- Класс `Hashnode` помечен как `deprecated`, что означает, что он может быть устаревшим и не рекомендуется к использованию в новых проектах.