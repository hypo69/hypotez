Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код реализует класс `ConversationHandler`, предназначенный для управления историей диалога с использованием модели GPT-4 через клиент `g4f`. Класс позволяет добавлять сообщения пользователя и получать ответы от ассистента, сохраняя всю историю переписки.

Шаги выполнения
-------------------------
1. **Инициализация класса `ConversationHandler`**:
   - Создается экземпляр класса `Client` из библиотеки `g4f` для взаимодействия с моделью.
   - Устанавливается модель, используемая для генерации ответов (по умолчанию "gpt-4").
   - Инициализируется пустой список `conversation_history` для хранения истории сообщений.

2. **Добавление сообщения пользователя**:
   - Метод `add_user_message` добавляет сообщение пользователя в историю диалога в формате словаря с ключами "role" (установлен в "user") и "content" (содержимое сообщения).

3. **Получение ответа от ассистента**:
   - Метод `get_response` отправляет историю диалога в модель GPT-4 через метод `client.chat.completions.create`.
   - Функция извлекает ответ ассистента из полученного результата и сохраняет его в истории диалога.
   - Функция возвращает содержимое ответа ассистента.

Пример использования
-------------------------

```python
from g4f.client import Client

class ConversationHandler:
    def __init__(self, model="gpt-4"):
        self.client = Client()
        self.model = model
        self.conversation_history = []
        
    def add_user_message(self, content):
        self.conversation_history.append({
            "role": "user",
            "content": content
        })
        
    def get_response(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history
        )
        assistant_message = {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content
        }
        self.conversation_history.append(assistant_message)
        return assistant_message["content"]

# Пример использования
conversation = ConversationHandler()
conversation.add_user_message("Hello!")
print("Assistant:", conversation.get_response())

conversation.add_user_message("How are you?")
print("Assistant:", conversation.get_response())