## Как использовать блок кода `DeepInfra`
=========================================================================================

Описание
-------------------------
Блок кода `DeepInfra` предоставляет функциональность для взаимодействия с API DeepInfra, платформой для генерации текста и изображений с использованием моделей искусственного интеллекта. 

Шаги выполнения
-------------------------
1. **Инициализация:** Создается экземпляр класса `DeepInfra`, который определяет базовые URL-адреса, модель по умолчанию и другие параметры для взаимодействия с API DeepInfra. 
2. **Получение доступных моделей:** Метод `get_models()`  запрашивает API DeepInfra и получает список доступных моделей для генерации текста и изображений. 
3. **Создание асинхронного генератора:** Метод `create_async_generator()` создает асинхронный генератор для взаимодействия с API DeepInfra. 
4. **Обработка ответа:**  Асинхронный генератор генерирует ответы от API DeepInfra, обрабатывая потоки данных (chunks) с помощью метода `create_async_generator` и возвращая результаты в виде объекта `AsyncResult`.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth import DeepInfra
from hypotez.src.endpoints.gpt4free.g4f.typing import Messages

# Создание экземпляра класса DeepInfra
provider = DeepInfra()

# Получение списка доступных моделей
available_models = provider.get_models()
print(available_models)

# Подготовка данных для запроса
messages = Messages(
    [
        {
            "role": "user",
            "content": "Напиши мне стихотворение про любовь",
        },
    ]
)

# Создание асинхронного генератора
async_generator = provider.create_async_generator(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
    messages=messages,
    stream=True,
    temperature=0.7,
)

# Проход по результатам генерации
async for result in async_generator:
    print(result)

```