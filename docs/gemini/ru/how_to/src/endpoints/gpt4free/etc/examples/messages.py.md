## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода реализует класс `ConversationHandler`, который управляет диалогом с языковой моделью, используя библиотеку `g4f`. 

Шаги выполнения
-------------------------
1. **Инициализация объекта `ConversationHandler`**: 
   - Создает экземпляр класса `ConversationHandler`, передавая в конструктор имя модели (по умолчанию "gpt-4").
   - Инициализирует `client` - объект для работы с API `g4f`.
   - Инициализирует список `conversation_history`, который будет хранить историю диалога.

2. **Добавление сообщения пользователя**:
   - Метод `add_user_message` добавляет новое сообщение пользователя в список `conversation_history`.
   - Сообщение добавляется в виде словаря с ключами `role` (равным "user") и `content` (текст сообщения).

3. **Получение ответа от модели**:
   - Метод `get_response` отправляет историю диалога в API `g4f` для получения ответа.
   - Извлекает текст ответа от модели из объекта `response` и добавляет его в список `conversation_history`.
   - Возвращает текст ответа от модели.

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

# Usage example
conversation = ConversationHandler()
conversation.add_user_message("Hello!")
print("Assistant:", conversation.get_response())

conversation.add_user_message("How are you?")
print("Assistant:", conversation.get_response())

```

**Объяснение**:

В примере создания объекта `conversation` - экземпляра класса `ConversationHandler` с моделью "gpt-4".
Затем, в этот объект отправляется сообщение "Hello!". 
Метод `get_response` отправляет это сообщение модели gpt-4, получает ответ и выводит его.
Затем, отправляется второе сообщение, "How are you?" и выводится ответ. 

**Важно**:

- Этот код требует установленной библиотеки `g4f` (pip install g4f).
- Дополнительно, необходимо получить API-ключ для `g4f` и настроить его в клиенте (подробнее см. документацию g4f).