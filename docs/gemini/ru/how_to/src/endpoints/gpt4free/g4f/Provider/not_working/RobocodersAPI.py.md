## Как использовать блок кода RobocodersAPI
=========================================================================================

Описание
-------------------------
Блок кода реализует асинхронный генератор `RobocodersAPI` для работы с API Robocoders AI. Генератор обеспечивает доступ к модели Robocoders AI, поддерживает историю сообщений и предоставляет асинхронную генерацию ответов. 

Шаги выполнения
-------------------------
1. **Инициализация**: Создается объект `RobocodersAPI`, который представляет собой асинхронный генератор.
2. **Получение токена доступа**: Метод `_fetch_and_cache_access_token` получает токен доступа от API Robocoders AI, используя веб-страничку авторизации и Beautiful Soup для парсинга. Токен сохраняется в кеш для повторного использования.
3. **Создание сессии**: Метод `_create_and_cache_session` создает сессию с API Robocoders AI, используя полученный токен доступа. ID сессии сохраняется в кеш.
4. **Отправка запроса**: Метод `create_async_generator` формирует запрос к API Robocoders AI с заданным текстом запроса (промптом), моделью и ID сессии.
5. **Обработка ответа**: Ответ от API обрабатывается в виде потока данных, где каждый байт декодируется в строку и парсится как JSON.
6. **Генерация ответов**: Из обработанного JSON-ответа извлекается текст сообщения и возвращается как результат генератора.
7. **Обработка ресурсных ограничений**: Если API Robocoders AI сигнализирует о достижении ресурсных ограничений, генератор автоматически отправляет запрос на продолжение диалога и возвращает дополнительные ответы.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.not_working.RobocodersAPI import RobocodersAPI

async def main():
    # Инициализация объекта RobocodersAPI
    provider = RobocodersAPI(model='GeneralCodingAgent')

    # Формирование списка сообщений для отправки
    messages = [
        {'role': 'user', 'content': 'Привет, как дела?'},
        {'role': 'assistant', 'content': 'Хорошо, а у тебя?'}
    ]

    # Запуск асинхронной генерации ответов
    async for message in provider.create_async_generator(messages=messages):
        print(f'Ответ от модели: {message}')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

**Важно**:

- Этот блок кода требует установки библиотеки `beautifulsoup4`: `pip install -U beautifulsoup4`
- Блок кода работает асинхронно, поэтому для его использования необходим асинхронный контекст. 
- `RobocodersAPI` работает через API Robocoders AI. Для использования требуется учетная запись на платформе Robocoders AI.