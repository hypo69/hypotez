# Модуль CohereForAI_C4AI_Command
## Обзор
Модуль `CohereForAI_C4AI_Command` предоставляет класс `CohereForAI_C4AI_Command`, который реализует асинхронный генератор для взаимодействия с моделью CohereForAI C4AI Command, размещенной на Hugging Face Spaces.  

##  Класс `CohereForAI_C4AI_Command`
### Описание:
Класс `CohereForAI_C4AI_Command`  является асинхронным генератором  и наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin`.  Он обеспечивает взаимодействие с  моделью `CohereForAI C4AI Command`,  предоставляя доступ к ее функциям и асинхронным вызовам.

**Атрибуты**:
- `label` (str):  Название провайдера модели.
- `url` (str):  URL-адрес  Hugging Face Spaces для модели.
- `conversation_url` (str): URL-адрес для работы с беседами (конверсациями).
- `working` (bool):  Флаг, указывающий на работоспособность провайдера.
- `default_model` (str):  Название модели по умолчанию.
- `model_aliases` (dict): Словарь с псевдонимами моделей и их соответствующими идентификаторами.
- `models` (list): Список доступных моделей.

**Методы**:
- `get_model(model: str, **kwargs) -> str`:  Получает  идентификатор модели по ее  названию. 
- `create_async_generator(model: str, messages: Messages, api_key: str = None, proxy: str = None, conversation: JsonConversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`:  Создает асинхронный генератор для взаимодействия с моделью.

**Принцип работы:** 
Класс `CohereForAI_C4AI_Command`  взаимодействует с моделью CohereForAI C4AI Command через HTTP-запросы к серверу Hugging Face Spaces. Он  управляет состоянием бесед (конверсаций), отправляет запросы,  обрабатывает ответы и выдает  результаты в виде  асинхронного генератора.

**Примеры:**
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space import CohereForAI_C4AI_Command

async def main():
    provider = CohereForAI_C4AI_Command(model="command-r")
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "Хорошо, а у тебя?"},
    ]
    async for result in provider.create_async_generator(messages=messages):
        print(result)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

##  Методы класса
### `get_model(model: str, **kwargs) -> str`:
**Назначение**: 
-  Получает  идентификатор модели по ее  названию.  

**Параметры**:
- `model` (str):  Название модели.

**Возвращает**:
- `str`:  Идентификатор модели. 

**Как работает функция**:
-  Если модель  соответствует одному из  псевдонимов моделей в словаре `model_aliases`, то функция возвращает соответствующий идентификатор.
- В противном случае функция перенаправляет запрос к  базовому классу `AsyncGeneratorProvider`.

**Примеры**:
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space import CohereForAI_C4AI_Command

model_id = CohereForAI_C4AI_Command.get_model(model="command-r")
print(model_id)
```

### `create_async_generator(model: str, messages: Messages, api_key: str = None, proxy: str = None, conversation: JsonConversation = None, return_conversation: bool = False, **kwargs) -> AsyncResult`:
**Назначение**: 
- Создает  асинхронный генератор,  который обеспечивает взаимодействие с моделью CohereForAI C4AI Command.

**Параметры**:
- `model` (str): Идентификатор модели.
- `messages` (Messages): Список сообщений в беседе (конверсации).
- `api_key` (str, optional): API-ключ.  По умолчанию `None`. 
- `proxy` (str, optional):  Прокси-сервер. По умолчанию `None`. 
- `conversation` (JsonConversation, optional):  Объект,  содержащий информацию о беседе (конверсации). По умолчанию `None`.
- `return_conversation` (bool, optional): Флаг, указывающий на необходимость возвращения объекта `JsonConversation`. По умолчанию `False`.

**Возвращает**:
- `AsyncResult`:  Асинхронный генератор, который посылает  ответы от модели. 

**Как работает функция**:
- Функция  получает  идентификатор модели.
-  Инициализирует заголовки HTTP-запроса.
- Если  `api_key` задан,  добавляет его в заголовки запроса.
- Создает  сессию  `ClientSession` с  указанными  заголовками и куки (если  `conversation` задан).
-  Создает  системный  промпт из  сообщений с ролью `system`.
-  Создает  промпт  из  сообщений с ролями  `user` и `assistant`.
- Если  `conversation`  не задан,  инициализирует  беседу  с  моделью, отправляя  запрос  POST на  `conversation_url` с  данными  модели и  системного промпта.
-  Отправляет  запрос  GET  на  `conversation_url`  для  получения  данных  из  беседы (конверсации).
-  Создает  форму  `FormData` с  входными данными,  сообщениями и  идентификатором  последнего сообщения в беседе.
-  Отправляет  запрос  POST  на  `conversation_url`  с  данными  формы.
-  Чтение  ответа  от  модели  и  выдача  результатов  в  виде  асинхронного  генератора.


**Примеры:**
```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space import CohereForAI_C4AI_Command

async def main():
    provider = CohereForAI_C4AI_Command(model="command-r")
    messages = [
        {"role": "user", "content": "Привет, как дела?"},
        {"role": "assistant", "content": "Хорошо, а у тебя?"},
    ]
    async for result in provider.create_async_generator(messages=messages):
        print(result)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())