## Как использовать класс OpenaiTemplate
=========================================================================================

Описание
-------------------------
Класс `OpenaiTemplate` реализует асинхронный генератор для взаимодействия с API OpenAI. Он предоставляет методы для отправки запросов, получения ответов и управления потоком данных.

Шаги выполнения
-------------------------
1. **Инициализация**: Класс `OpenaiTemplate` должен быть инициализирован с помощью API-ключа OpenAI, базой API и точкой входа API.
2. **Получение списка моделей**: Метод `get_models()` позволяет получить список доступных моделей OpenAI.
3. **Создание асинхронного генератора**: Метод `create_async_generator()` создает асинхронный генератор, который отправляет запросы к API и генерирует ответы.
4. **Обработка ответов**: Генератор  `create_async_generator()`  выдает ответы в виде строк, объектов `Usage` и `FinishReason`.
5. **Обработка ошибок**: Класс `OpenaiTemplate` содержит методы для обработки ошибок, которые могут возникнуть при взаимодействии с API.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.template.OpenaiTemplate import OpenaiTemplate

# Инициализация класса
api_key = "YOUR_API_KEY"
api_base = "https://api.openai.com"
api_endpoint = "/v1/chat/completions"
provider = OpenaiTemplate(api_key=api_key, api_base=api_base, api_endpoint=api_endpoint)

# Получение списка моделей
models = provider.get_models()
print(f"Доступные модели: {models}")

# Создание асинхронного генератора
messages = [
    {"role": "user", "content": "Привет! Как дела?"},
]
async_generator = await provider.create_async_generator(model="gpt-3.5-turbo", messages=messages)

# Обработка ответов
async for response in async_generator:
    if isinstance(response, str):
        print(f"Ответ: {response}")
    elif isinstance(response, Usage):
        print(f"Использование токенов: {response.tokens}")
    elif isinstance(response, FinishReason):
        print(f"Причина завершения: {response.reason}")

```

**Описание**:

Этот пример демонстрирует основное использование класса `OpenaiTemplate`. 
В коде сначала инициализируется экземпляр класса с необходимыми параметрами. 
Затем происходит вызов метода `get_models()` для получения списка доступных моделей OpenAI. 
Далее создается асинхронный генератор с помощью метода `create_async_generator()`. 
В цикле `async for` обрабатываются ответы генератора. 
В зависимости от типа ответа (`str`, `Usage` или `FinishReason`) выводится соответствующая информация.