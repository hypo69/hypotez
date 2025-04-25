## Как использовать блок кода ThebApi
=========================================================================================

Описание
-------------------------
Этот блок кода определяет класс `ThebApi`, который реализует API для TheB.AI, предоставляющего доступ к различным языковым моделям. 

Шаги выполнения
-------------------------
1. **Определение класса `ThebApi`**: Класс наследует `OpenaiTemplate` и предоставляет информацию о TheB.AI API, такую как базовый URL, URL для входа, модель по умолчанию, доступные модели и информацию о необходимости авторизации.
2. **Создание асинхронного генератора `create_async_generator`**: Метод класса, который создает асинхронный генератор для взаимодействия с TheB.AI API.
    - Метод принимает параметры `model` (имя модели), `messages` (список сообщений для чата), `temperature`, `top_p` и другие.
    - Он извлекает системные сообщения из `messages` и создает словарь `data`, который содержит параметры модели, такие как `system_prompt`, `temperature`, `top_p`.
    - Метод вызовет суперкласс `create_async_generator` с `model`, `messages`, `extra_data` (словарь `data`) и другими параметрами.

Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.ThebApi import ThebApi
from hypotez.src.endpoints.gpt4free.g4f.Provider.needs_auth.models import Models

messages = [
    {"role": "system", "content": "Ты - дружелюбный помощник."},
    {"role": "user", "content": "Привет! Как дела?"}
]

# Инициализация ThebApi с моделью "theb-ai"
theb_api = ThebApi(model="theb-ai")

# Создание асинхронного генератора с использованием метода `create_async_generator`
async_generator = theb_api.create_async_generator(model="theb-ai", messages=messages, temperature=0.7)

# Получение результатов из генератора
async for response in async_generator:
    print(f"Ответ модели: {response['content']}")
```

**Важно**: 
- Для использования API необходимо пройти авторизацию.
-  Используйте `models.Models` для получения списка доступных моделей. 
- `temperature` и `top_p`  - параметры, влияющие на творчество и разнообразие ответа.