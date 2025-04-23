## \file hypotez/src/llm/dialogflow/readme.ru.md
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

```rst
 .. module:: src.ai.dialogflow
```

<TABLE >
<TR>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/readme.ru.md'>[Root ↑]</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/readme.ru.md'>src</A> /
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/ai/readme.ru.md'>ai</A> /
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/about.ru.md'>Что такое dialogflow model</A>
</TD>
<TD>
<A HREF = 'https://github.com/hypo69/hypotez/blob/master/src/ai/dialogflow/readme.ru.md'>Русский</A>
</TD>
</TABLE>

https://dialogflow.com/docs/getting-started/basics

### **dialogflow**

Модуль интеграции с Google Dialogflow.  
Предоставляя возможности для обработки естественного языка (NLU) 
и создания разговорных ИИ-приложений. Он включает в себя следующие основные функции:

- **Определение намерений (Intent Detection):** Определяет намерения пользователя на основе введенного текста.
- **Работа с сущностями (Entity Recognition):** Извлекает ключевые данные из пользовательских фраз.
- **Контексты (Contexts):** Управляет диалогом, сохраняя информацию о текущем состоянии разговора.
- **Интеграции:** Поддерживает интеграцию с различными платформами, такими как Google Assistant, Facebook Messenger, Slack, Telegram, и другими.
- **Webhook:** Поддерживает Webhook-интеграции для вызова внешних сервисов и API.

Пример использования подмодуля **dialogflow**:

```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id"
session_id = "unique-session-id"

dialogflow_client = Dialogflow(project_id, session_id)

# Пример использования методов
intent_response = dialogflow_client.detect_intent("Hello")
print("Detected Intent:", intent_response)

intents = dialogflow_client.list_intents()
print("List of Intents:", intents)

new_intent = dialogflow_client.create_intent(
    display_name="NewIntent",
    training_phrases_parts=["new phrase", "another phrase"],
    message_texts=["This is a new intent"]
)
print("Created Intent:", new_intent)

# Удаление намерения (не забудьте заменить intent_id на реальный ID)
# dialogflow_client.delete_intent("your-intent-id")
```

Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует интеграцию с Google Dialogflow для создания разговорных ИИ-приложений. Он охватывает основные функции, такие как определение намерений пользователя, управление диалогом и создание новых намерений.

Шаги выполнения
-------------------------
1. **Импорт модуля `Dialogflow`**:
   - Код импортирует класс `Dialogflow` из модуля `src.ai.dialogflow`. Этот класс предоставляет интерфейс для взаимодействия с API Dialogflow.
2. **Инициализация клиента `Dialogflow`**:
   - Создается экземпляр класса `Dialogflow` с использованием идентификатора проекта (`project_id`) и идентификатора сессии (`session_id`).
3. **Определение намерения**:
   - Вызывается метод `detect_intent` для определения намерения пользователя на основе введенного текста. В примере используется текст "Hello".
   - Результат определения намерения выводится в консоль.
4. **Получение списка намерений**:
   - Вызывается метод `list_intents` для получения списка всех существующих намерений в проекте Dialogflow.
   - Список намерений выводится в консоль.
5. **Создание нового намерения**:
   - Вызывается метод `create_intent` для создания нового намерения с указанными параметрами, такими как отображаемое имя, тренировочные фразы и текстовые сообщения.
   - Результат создания намерения выводится в консоль.
6. **Удаление намерения (опционально)**:
   - Закомментированный код показывает, как можно удалить существующее намерение с использованием метода `delete_intent`. Для этого необходимо указать идентификатор намерения.

Пример использования
-------------------------

```python
from src.ai.dialogflow import Dialogflow

project_id = "your-project-id" # Укажите идентификатор вашего проекта Dialogflow
session_id = "unique-session-id" # Укажите уникальный идентификатор сессии

dialogflow_client = Dialogflow(project_id, session_id)

# Функция определяет намерение пользователя на основе введенного текста
intent_response = dialogflow_client.detect_intent("Hello")
print("Обнаруженное намерение:", intent_response)

# Функция получает список всех существующих намерений в проекте Dialogflow
intents = dialogflow_client.list_intents()
print("Список намерений:", intents)

# Функция создает новое намерение с указанными параметрами
new_intent = dialogflow_client.create_intent(
    display_name="NewIntent",
    training_phrases_parts=["new phrase", "another phrase"],
    message_texts=["This is a new intent"]
)
print("Созданное намерение:", new_intent)

# Удаление намерения (не забудьте заменить intent_id на реальный ID)
# dialogflow_client.delete_intent("your-intent-id")