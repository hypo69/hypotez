# Модуль AiAsk
## Обзор

Модуль предоставляет класс `AiAsk`, который реализует асинхронный генератор для получения ответов от модели GPT-4 через API `https://e.aiask.me`.

## Подробнее

`AiAsk` наследует класс `AsyncGeneratorProvider`,  предоставляет асинхронный генератор для получения ответов от модели GPT-4.  Он использует библиотеку `aiohttp` для отправки запросов к API и обработки ответов. 

## Классы

### `class AiAsk`

**Описание**: Класс `AiAsk` реализует асинхронный генератор для получения ответов от модели GPT-4 через API `https://e.aiask.me`.

**Наследует**: 
- `AsyncGeneratorProvider`

**Атрибуты**:

- `url (str)`: URL-адрес API `https://e.aiask.me`.
- `supports_message_history (bool)`: Указывает, поддерживает ли модель историю сообщений.
- `supports_gpt_35_turbo (bool)`: Указывает, поддерживает ли модель GPT-3.5 Turbo.
- `working (bool)`: Флаг, указывающий, работает ли API.

**Методы**:

- `create_async_generator(model: str, messages: Messages, proxy: str = None, **kwargs) -> AsyncResult`: Асинхронный генератор для получения ответов от модели GPT-4.

## Методы класса

### `create_async_generator`

```python
    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: Messages,
        proxy: str = None,
        **kwargs
    ) -> AsyncResult:
        headers = {
            "accept": "application/json, text/plain, */*",
            "origin": cls.url,
            "referer": f"{cls.url}/chat",
        }
        async with ClientSession(headers=headers) as session:
            data = {
                "continuous": True,
                "id": "fRMSQtuHl91A4De9cCvKD",
                "list": messages,
                "models": "0",
                "prompt": "",
                "temperature": kwargs.get("temperature", 0.5),
                "title": "",
            }
            buffer = ""
            rate_limit = "您的免费额度不够使用这个模型啦，请点击右上角登录继续使用！"
            async with session.post(f"{cls.url}/v1/chat/gpt/", json=data, proxy=proxy) as response:
                response.raise_for_status()
                async for chunk in response.content.iter_any():
                    buffer += chunk.decode()
                    if not rate_limit.startswith(buffer):
                        yield buffer
                        buffer = ""
                    elif buffer == rate_limit:
                        raise RuntimeError("Rate limit reached")
```

**Назначение**:  Создает асинхронный генератор для получения ответов от модели GPT-4. 

**Параметры**:

- `model (str)`: Имя модели GPT-4.
- `messages (Messages)`: Список сообщений для отправки в модель.
- `proxy (str)`: Прокси-сервер для использования при отправке запросов. 
- `**kwargs`: Дополнительные аргументы для отправки в модель GPT-4.

**Возвращает**:
- `AsyncResult`: Асинхронный результат, который является генератором для получения ответов от модели GPT-4.

**Вызывает исключения**:

- `RuntimeError`: Если достигнут лимит запросов.

**Как работает функция**:

- Устанавливает заголовки запроса.
- Создает объект `ClientSession` с заданными заголовками.
- Формирует данные для запроса к API.
- Отправляет POST-запрос к API.
- Обрабатывает ответ API и выдает его по частям.
- Если достигнут лимит запросов,  вызывает исключение `RuntimeError`.

**Примеры**:

```python
# Пример использования генератора для получения ответов от GPT-4
async def main():
    messages = [
        {"role": "user", "content": "Привет!"},
    ]
    async for chunk in AiAsk.create_async_generator(model='gpt-4', messages=messages):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())