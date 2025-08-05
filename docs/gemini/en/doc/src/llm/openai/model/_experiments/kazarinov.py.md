# Модуль для работы с OpenAI  моделями 
=========================================================================
 
Модуль предоставляет функционал для взаимодействия с OpenAI  моделями  и  реализует  чат с  моделью.
 
## Содержание
 
- [OpenAIChat](#openai-chat)
- [chat](#chat)
- [Основные переменные](#основные-переменные)
 
 
## OpenAIChat
 
```python
class OpenAIChat:
    """ 
    Класс для инициализации OpenAI модели и отправки запросов.
 
    Attributes:
        api_key (str): Ключ API от OpenAI.
        system_instruction (str): Системная инструкция для модели. 
        messages (list): Список сообщений для чата.
 
    Methods:
        ask(prompt: str) -> str: Отправляет вопрос в модель OpenAI и получает ответ.
    """
 
    def __init__(self, api_key: str, system_instruction: str = None):
        """
        Инициализация класса OpenAIChat.
 
        Args:
            api_key (str): Ключ API от OpenAI.
            system_instruction (str, optional): Системная инструкция для модели. По умолчанию `None`.
        """
        openai.api_key = gs.credentials
        self.system_instruction = system_instruction
        self.messages = []
 
        if self.system_instruction:
            self.messages.append({"role": "system", "content": self.system_instruction})
 
    def ask(self, prompt: str) -> str:
        """ 
        Отправка вопроса в модель OpenAI и получение ответа.
 
        Args:
            prompt (str): Вопрос, который отправляется в модель OpenAI.
 
        Returns:
            str: Ответ модели OpenAI.
 
        Raises:
            Exception: Если возникает ошибка при обработке запроса.
        """
        self.messages.append({"role": "user", "content": prompt})
 
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                max_tokens=150,
                temperature=0.7
            )
            answer = response['choices'][0]['message']['content']
            self.messages.append({"role": "assistant", "content": answer})
            return answer
        except Exception as ex:
            logger.error(f"Ошибка: {ex}")
            return "Произошла ошибка при обработке запроса."
```
 
## chat
 
```python
def chat():
    """ 
    Функция запускает  чат с OpenAI моделью.
    """
    print("Добро пожаловать в чат с OpenAI!")
    print("Чтобы завершить чат, напишите \'exit\'.\\n")
    
    # Ввод ключа API и инициализация модели
    api_key = input("Введите ваш OpenAI API ключ: ")
    ai = OpenAIChat(api_key=api_key, system_instruction=system_instruction)
 
    while True:
        # Получаем вопрос от пользователя
        user_input = input("> вопрос\\n> ")
        
        if user_input.lower() == 'exit':
            print("Чат завершен.")
            break
        
        # Отправляем запрос модели и получаем ответ
        response = ai.ask(prompt=user_input)
        
        # Выводим ответ
        print(f">> ответ\\n>> {response}\\n")
```
 
## Основные переменные
 
- `system_instruction_path`: Путь к файлу с системной инструкцией для модели.
- `system_instruction`: Текст системной инструкции для модели.
 
 
##  Как работает модуль 
 
Модуль  предоставляет  функционал  для  взаимодействия  с  OpenAI  моделями.
 
1. **Загрузка  системной  инструкции:** 
    - Функция `read_text_file` считывает текст из файла с системной инструкцией.
 
2. **Инициализация  модели:**
    - Создается  экземпляр  класса `OpenAIChat`,  который  используется  для  взаимодействия  с  моделью.
 
3. **Обработка  запросов:**
    -  Функция  `ask`  отправляет  запрос  в  модель  OpenAI  и  получает  ответ.
    - В  качестве  модели  используется  `gpt-3.5-turbo`.
    -  В  качестве  параметров  запроса  используются:
        -  `messages`: Список  сообщений  для  чата.
        -  `max_tokens`: Максимальное  количество  токенов  в  ответе.
        -  `temperature`:  Уровень  креативности  модели.
 
4. **Выполнение  чата:**
    - Функция `chat`  запускает  чат  с  OpenAI  моделью.
    -  Пользователь  может  вводить  свои  вопросы.
    -  Программа  отправляет  вопросы  в  модель  OpenAI  и  выводит  отве-ты  на  экран.
    -  Чат  завершается,  когда  пользователь  вводит  команду  `exit`.
 
 
## Примеры
 
**Пример  использования  модуля:**
 
```python
# Загрузка  системной  инструкции
system_instruction_path = Path('src/ai/openai/model/_experiments/system_instruction.txt')
system_instruction = read_text_file(system_instruction_path)
 
# Ввод  ключа  API  и  инициализация  модели
api_key = input("Введите ваш OpenAI API ключ: ")
ai = OpenAIChat(api_key=api_key, system_instruction=system_instruction)
 
#  Пример  отправки  запроса  в  модель
question = "Какая  погода  в  Москве?"
answer = ai.ask(question)
print(f"Ответ  модели: {answer}")
 
# Запуск  чата
chat()
```
 
## Дополнительные  сведения
 
-  Для  использования  модуля  необходимо  иметь  ключ  API  от  OpenAI.
-  Можно  настроить  сис-темную  инструкцию  для  модели,  чтобы  изменить  ее  поведение.
-  В  модуле  используется  библиотека  `openai`,  которую  необходимо  уста-новить  до  использования  модуля.
 
 
##  Ссылки
 
-  [OpenAI API](https://platform.openai.com/docs/api-reference/introduction)
-  [OpenAI ChatCompletion](https://platform.openai.com/docs/api-reference/completions/create)