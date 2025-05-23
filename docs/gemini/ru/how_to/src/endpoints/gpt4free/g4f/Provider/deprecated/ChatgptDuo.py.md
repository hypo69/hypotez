## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Данный блок кода реализует асинхронный провайдер `ChatgptDuo` для взаимодействия с сервисом chatgptduo.com. Он предоставляет функционал для отправки запросов с использованием модели GPT-3.5 Turbo, обработки ответа и извлечения дополнительных источников информации.

### Шаги выполнения
-------------------------
1. **Инициализация класса:** Создается экземпляр класса `ChatgptDuo` с использованием статического метода `create_async`.
2. **Формирование запроса:**  
    -  В качестве входных данных передаются `model` (имя модели, например, `gpt-3.5-turbo`),  `messages` (список сообщений для контекста), `proxy` (прокси-сервер, если требуется), `timeout` (максимальное время ожидания ответа) и другие необязательные параметры.
    -  Формируется текст запроса с использованием метода `format_prompt` и создается словарь данных для отправки.
3. **Отправка запроса:** Используется асинхронный сеанс с заданными параметрами, который отправляет POST-запрос на сервер chatgptduo.com.
4. **Обработка ответа:**  
    -  Проверяется код ответа сервера.
    -  Парсится JSON-ответ сервера.
    -  Извлекаются и обрабатываются источники информации (`_sources`).
5. **Возврат ответа:**  
    -  Возвращается текст ответа сервера (`data["answer"]`).

### Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.ChatgptDuo import ChatgptDuo

async def main():
    # Создание экземпляра класса ChatgptDuo
    provider = await ChatgptDuo.create_async(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Привет!"},
        ],
        timeout=60,
    )

    # Получение ответа от сервиса
    response = await provider.get_response()

    # Вывод ответа
    print(f"Ответ: {response}")

    # Вывод источников информации
    sources = provider.get_sources()
    print(f"Источники информации: {sources}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Дополнительная информация
-------------------------

- Класс `ChatgptDuo` помечен как `deprecated`, т.е. устарел и может быть заменен в будущем.
- Класс наследуется от `AsyncProvider`, что позволяет ему использовать общие методы для работы с асинхронными провайдерами.
- Метод `get_sources` возвращает список источников информации, полученных в процессе обработки ответа от сервиса.