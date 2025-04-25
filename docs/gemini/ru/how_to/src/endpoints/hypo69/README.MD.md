###  Как использовать  `hypo69` 
=========================================================================================

Описание
-------------------------
`hypo69` - это модуль, который включает в себя три основных компонента:
*  **small_talk_bot** - бот с чатом модели ии 
*  **code_assistant** - модуль обучения модели коду проекта
*  **psychologist_bot** - ранняя разработка модуля парсинга диалогов


Шаги выполнения
-------------------------
1.  **Инициализация**: Импортируй необходимый компонент из модуля `hypo69`
2.  **Настройка**: Настройте параметры компонента, например, модель, которую вы хотите использовать
3.  **Запуск**: Запустите компонент и используйте его по назначению.


Пример использования
-------------------------

```python
from src.endpoints.hypo69 import small_talk_bot, code_assistant, psychologist_bot

# Инициализация small_talk_bot
bot = small_talk_bot.SmallTalkBot(model="gpt-3.5-turbo")

# Ввод текста и получение ответа
response = bot.chat("Привет, как дела?")
print(response)

# Инициализация code_assistant
code_assistant = code_assistant.CodeAssistant(model="gpt-3.5-turbo")

# Обучение модели коду
code_assistant.train(code="def hello_world():\n  print('Hello, world!')")

# Генерация кода
generated_code = code_assistant.generate_code(prompt="Напиши функцию, которая выводит 'Hello, world!'")
print(generated_code)

# Инициализация psychologist_bot
psychologist_bot = psychologist_bot.PsychologistBot(model="gpt-3.5-turbo")

# Парсинг диалога
dialogue = psychologist_bot.parse_dialogue(text="Привет, как дела?")
print(dialogue)
```

### Как использовать  `hypo69` 
=========================================================================================

Описание
-------------------------
`hypo69` - это модуль, который включает в себя три основных компонента:
*  **small_talk_bot** - бот с чатом модели ии 
*  **code_assistant** - модуль обучения модели коду проекта
*  **psychologist_bot** - ранняя разработка модуля парсинга диалогов


Шаги выполнения
-------------------------
1.  **Инициализация**: Импортируй необходимый компонент из модуля `hypo69`
2.  **Настройка**: Настройте параметры компонента, например, модель, которую вы хотите использовать
3.  **Запуск**: Запустите компонент и используйте его по назначению.


Пример использования
-------------------------

```python
from src.endpoints.hypo69 import small_talk_bot, code_assistant, psychologist_bot

# Инициализация small_talk_bot
bot = small_talk_bot.SmallTalkBot(model="gpt-3.5-turbo")

# Ввод текста и получение ответа
response = bot.chat("Привет, как дела?")
print(response)

# Инициализация code_assistant
code_assistant = code_assistant.CodeAssistant(model="gpt-3.5-turbo")

# Обучение модели коду
code_assistant.train(code="def hello_world():\n  print('Hello, world!')")

# Генерация кода
generated_code = code_assistant.generate_code(prompt="Напиши функцию, которая выводит 'Hello, world!'")
print(generated_code)

# Инициализация psychologist_bot
psychologist_bot = psychologist_bot.PsychologistBot(model="gpt-3.5-turbo")

# Парсинг диалога
dialogue = psychologist_bot.parse_dialogue(text="Привет, как дела?")
print(dialogue)