### **Как использовать этот блок кода**
=========================================================================================

Описание
-------------------------
Этот код реализует простой чат с использованием OpenAI API. Он позволяет пользователю ввести свой API-ключ, задавать вопросы и получать ответы от модели OpenAI (gpt-3.5-turbo). Код также обрабатывает ошибки, возникающие при взаимодействии с API.

Шаги выполнения
-------------------------
1. **Загрузка системной инструкции**:
   - Определяется путь к файлу `system_instruction.txt`, содержащему системную инструкцию для модели.
   - Функция `read_text_file` извлекает содержимое файла, которое будет использоваться для инициализации модели.

2. **Инициализация класса `OpenAIChat`**:
   - Класс `OpenAIChat` инициализируется с API-ключом и системной инструкцией.
   - API-ключ устанавливается для использования в OpenAI.
   - Системная инструкция добавляется в список сообщений для задания контекста модели.

3. **Метод `ask`**:
   - Метод `ask` принимает вопрос пользователя в качестве входных данных.
   - Вопрос добавляется в список сообщений с ролью "user".
   - Отправляется запрос в модель OpenAI с использованием `openai.ChatCompletion.create`.
   - Извлекается и возвращается ответ модели.
   - В случае возникновения ошибки, она логируется, и возвращается сообщение об ошибке.

4. **Функция `chat`**:
   - Функция `chat` реализует основной цикл чата.
   - Запрашивает у пользователя API-ключ.
   - Создает экземпляр класса `OpenAIChat` с использованием предоставленного API-ключа и системной инструкции.
   - В цикле запрашивает вопросы у пользователя и отправляет их в модель.
   - Выводит ответ модели пользователю.
   - Завершает чат при вводе команды "exit".

5. **Запуск чата**:
   - При запуске скрипта напрямую (`if __name__ == "__main__":`) вызывается функция `chat`, чтобы начать чат.

Пример использования
-------------------------

```python
import openai
from src.utils.file import read_text_file
from src.logger.logger import logger
from pathlib import Path

# Загрузка системной инструкции
system_instruction_path = Path('../src/ai/openai/model/_experiments/system_instruction.txt')
system_instruction = read_text_file(system_instruction_path)

# Инициализация OpenAI модели
class OpenAIChat:
    def __init__(self, api_key: str, system_instruction: str = None):
        openai.api_key = api_key
        self.system_instruction = system_instruction
        self.messages = []

        if self.system_instruction:
            self.messages.append({"role": "system", "content": self.system_instruction})

    def ask(self, prompt: str) -> str:
        """Отправка вопроса в модель OpenAI и получение ответа"""
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
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            return "Произошла ошибка при обработке запроса."

# Пример использования класса OpenAIChat
api_key = "YOUR_API_KEY"  # Замените на ваш фактический API-ключ
ai = OpenAIChat(api_key=api_key, system_instruction=system_instruction)
response = ai.ask(prompt="Как работает OpenAI?")
print(response)