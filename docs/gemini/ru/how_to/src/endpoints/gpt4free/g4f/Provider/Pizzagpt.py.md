## Как использовать блок кода Pizzagpt
=========================================================================================

Описание
-------------------------
Блок кода реализует класс `Pizzagpt`, представляющий собой провайдера для использования модели GPT-4o-mini от Pizzagpt.it. Класс наследует от `AsyncGeneratorProvider` и `ProviderModelMixin`, что обеспечивает асинхронную генерацию текста и поддержку различных моделей. 

Шаги выполнения
-------------------------
1. **Инициализация класса:**  Создается экземпляр класса `Pizzagpt` с помощью метода `create_async_generator`.
2. **Формирование запроса:** В методе `create_async_generator` формируется запрос к API Pizzagpt.it с помощью метода `format_prompt`, который преобразует список сообщений (`messages`) в строку запроса.
3. **Отправка запроса:**  Используется `ClientSession` для отправки POST-запроса на API Pizzagpt.it. 
4. **Обработка ответа:**  Происходит обработка ответа от API:
    - Проверяется код ответа (`response.raise_for_status()`).
    - Извлекается текст ответа из поля "content" в JSON-ответе.
    - Проверяется наличие сообщения об ошибке ("Misuse detected...").
    - Выполняется генерация текста (`yield content`) и отправляется сигнал о завершении (`yield FinishReason("stop")`).

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.Pizzagpt import Pizzagpt

async def main():
    # Создание экземпляра Pizzagpt
    provider = Pizzagpt()

    # Создание списка сообщений для запроса
    messages = [
        {'role': 'user', 'content': 'Привет! Как дела?'},
        {'role': 'assistant', 'content': 'Хорошо, спасибо!'},
    ]

    # Получение ответа
    async for response in provider.create_async_generator(model='gpt-4o-mini', messages=messages):
        print(f'Ответ: {response}')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

**Дополнительные сведения:**

- `Pizzagpt` поддерживает только одну модель "gpt-4o-mini".
- При отправке запроса на API Pizzagpt.it используется заголовок "x-secret" со значением "Marinara".
- Если в ответе обнаружено сообщение об ошибке ("Misuse detected..."), генерируется исключение `ValueError`.

**Важно**: Данный код является примером, который может быть использован для получения текста от модели GPT-4o-mini через API Pizzagpt.it.