## Как использовать Wewordle для генерации текста с помощью GPT-3.5 Turbo
=========================================================================================

Описание
-------------------------
Этот фрагмент кода представляет класс `Wewordle`, который является асинхронным провайдером для взаимодействия с API GPT-3.5 Turbo от WeWordle. Класс использует aiohttp для выполнения HTTP-запросов и формирует JSON-данные с необходимыми параметрами для отправки запроса к API.

Шаги выполнения
-------------------------
1. **Инициализация класса:** 
    - Создается экземпляр класса `Wewordle` с использованием метода `create_async`.
    - Метод `create_async` принимает следующие параметры:
        - `model`: Строка, указывающая модель, которая будет использоваться (например, `gpt-3.5-turbo`).
        - `messages`: Список словарей, содержащих сообщения для взаимодействия с API.
        - `proxy`: Необязательный параметр, указывающий прокси-сервер для использования.
        - `kwargs`: Дополнительные параметры, которые можно передать.
2. **Формирование JSON-данных:**
    - Генерируются случайные идентификаторы пользователя (`_user_id`) и приложения (`_app_id`).
    - Формируется объект данных (`data`) в формате JSON, содержащий:
        - `user`: Идентификатор пользователя.
        - `messages`: Список сообщений, переданных в качестве параметра.
        - `subscriber`:  Словарь, содержащий информацию о подписчике, включая:
            - `originalPurchaseDate`, `originalApplicationVersion`, `allPurchaseDatesMillis`, `entitlements`, `allPurchaseDates`, `allExpirationDatesMillis`, `allExpirationDates`, `originalAppUserId`, `latestExpirationDate`, `requestDate`, `latestExpirationDateMillis`, `nonSubscriptionTransactions`, `originalPurchaseDateMillis`, `managementURL`, `allPurchasedProductIdentifiers`, `firstSeen`, `activeSubscriptions`.
3. **Отправка запроса к API:**
    - Создается сессия aiohttp с необходимыми заголовками.
    - Используя сессию, выполняется POST-запрос к API-адресу `https://wewordle.org/gptapi/v1/android/turbo`.
    - В заголовке запроса указываются `Content-Type` и другие необходимые параметры.
    - В качестве тела запроса используется сформированный объект данных (`data`) в формате JSON.
4. **Обработка ответа:**
    - Получается ответ от API.
    - Проверяется статус-код ответа, и если он не является успешным, вызывается исключение.
    - Десериализуется ответ от API в JSON-формат.
    - Извлекается текст сообщения (`content`) из ответа.
    - Если текст сообщения не пустой, он возвращается в качестве результата.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.deprecated.Wewordle import Wewordle

async def main():
    messages = [
        {"role": "user", "content": "Привет! Напиши мне стихотворение про кота."}
    ]
    response = await Wewordle.create_async(model="gpt-3.5-turbo", messages=messages)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

В данном примере кода:
- Создается список сообщений, в котором содержится один текст - "Привет! Напиши мне стихотворение про кота."
- Вызывается функция `Wewordle.create_async` с указанием модели `gpt-3.5-turbo` и списка сообщений.
- Полученный ответ API выводится на консоль.