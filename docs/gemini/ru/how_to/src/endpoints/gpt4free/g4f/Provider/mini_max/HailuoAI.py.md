## Как использовать класс `HailuoAI`
=========================================================================================

### Описание
-------------------------
Класс `HailuoAI` представляет собой асинхронный провайдер для Hailuo AI API, который позволяет взаимодействовать с моделью MiniMax для генерации текста. 

Класс реализует интерфейсы `AsyncAuthedProvider` и `ProviderModelMixin`, что позволяет использовать его в качестве стандартного провайдера для API в проекте `hypotez`. 

### Шаги выполнения
-------------------------
1. **Инициализация класса:** 
    -  Создается экземпляр класса `HailuoAI`.
    -  Используется метод `on_auth_async()` для аутентификации с API.
    -  Аутентификация включает в себя получение токена доступа и дополнительных параметров, необходимых для взаимодействия с API. 
2. **Создание авторизованного экземпляра:**
    -  Используется метод `create_authed()` для создания авторизованного экземпляра, который может генерировать текст. 
    -  Метод принимает в качестве параметров: 
        -  `model`: модель, которая будет использоваться для генерации текста (например, "MiniMax").
        -  `messages`: история сообщений чата. 
        -  `auth_result`: результат аутентификации.
        -  `return_conversation`: флаг, указывающий, нужно ли возвращать объект `Conversation` (для последующего продолжения чата).
3. **Отправка запроса на генерацию:**
    -  Метод `create_authed()` отправляет запрос на API Hailuo AI с использованием библиотеки `aiohttp`. 
    -  В запросе передаются:
        -  `chatID`: идентификатор чата.
        -  `characterID`: идентификатор персонажа.
        -  `msgContent`: текст запроса.
4. **Обработка ответа:**
    -  Метод `create_authed()` обрабатывает ответ от API, декодируя JSON-данные и возвращая результаты генерации текста.
    -  Если `return_conversation`  равно `True`, метод возвращает объект `Conversation`, который позволяет продолжить чат с помощью того же токена доступа.


### Пример использования
-------------------------
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import HailuoAI
from hypotez.src.endpoints.gpt4free.g4f.Provider.mini_max.HailuoAI import Conversation
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Инициализация класса HailuoAI
hailuo_ai = HailuoAI()

# Аутентификация
async for auth_result in hailuo_ai.on_auth_async():
    print(f"Auth Result: {auth_result}")

# Создание авторизованного экземпляра
async for result in hailuo_ai.create_authed(
    model="MiniMax",
    messages=[
        {"role": "user", "content": "Привет! Как дела?"},
    ],
    auth_result=auth_result,
    return_conversation=True,
):
    if isinstance(result, Conversation):
        conversation = result
        print(f"Conversation ID: {conversation.chatID}")
    elif isinstance(result, str):
        print(f"Generated text: {result}")


# Продолжение чата
async for result in hailuo_ai.create_authed(
    model="MiniMax",
    messages=[
        {"role": "user", "content": "Что ты любишь делать?"},
    ],
    auth_result=auth_result,
    conversation=conversation,
):
    if isinstance(result, str):
        print(f"Generated text: {result}")
```