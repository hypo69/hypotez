## Как использовать блок кода `CohereForAI_C4AI_Command`
=========================================================================================

Описание
-------------------------
Блок кода реализует класс `CohereForAI_C4AI_Command`, представляющий собой асинхронный генератор для взаимодействия с моделью CohereForAI C4AI Command, доступной через Hugging Face Spaces. 

Он наследует классы `AsyncGeneratorProvider` и `ProviderModelMixin` и предоставляет возможность генерировать текст с использованием различных моделей CohereForAI C4AI Command, используя метод `create_async_generator()`.

Шаги выполнения
-------------------------
1. **Инициализация**: Создайте экземпляр класса `CohereForAI_C4AI_Command`.
2. **Выбор модели**: Используйте метод `get_model()` для выбора нужной модели (например, `command-a`, `command-r-plus`, `command-r` или `command-r7b`). 
3. **Запуск генерации**: Запустите метод `create_async_generator()`, передав модель, список сообщений (`messages`), а также необязательные параметры, такие как `api_key` (для аутентификации), `proxy` (для использования прокси-сервера) и `conversation` (для сохранения контекста разговора).
4. **Обработка результата**: Метод `create_async_generator()` возвращает асинхронный генератор, который будет выдавать куски текста, пока не завершится генерация. 
5. **Дополнительные параметры**:  
    - Параметр `return_conversation` позволяет вернуть объект `JsonConversation`, хранящий контекст разговора. 
    - Параметр `conversation` позволяет передать объект `JsonConversation` с сохранением контекста предыдущего разговора. 


Пример использования
-------------------------

```python
from hypotez.src.endpoints.gpt4free.g4f.Provider.hf_space.CohereForAI_C4AI_Command import CohereForAI_C4AI_Command

# Инициализация класса
provider = CohereForAI_C4AI_Command()

# Выбор модели
model = provider.get_model("command-r-plus")

# Список сообщений
messages = [
    {"role": "system", "content": "Ты - умный и дружелюбный помощник."},
    {"role": "user", "content": "Расскажи мне анекдот."},
]

# Запуск генерации
async for chunk in provider.create_async_generator(model, messages):
    print(chunk, end="")

# Вывод:
# [Анекдот]
```