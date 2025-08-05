## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода представляет класс `HeliconeAI`, который объединяет возможности `helicone` и `OpenAI` в единый инструмент для работы с языковыми моделями. 

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей:**
   - Импортируйте модули `Helicone` из `helicone` и `OpenAI` из `openai`. 
   - Определите класс `HeliconeAI`.

2. **Инициализация класса `HeliconeAI`:**
   - Создайте экземпляр класса `HeliconeAI`.
   - В инициализаторе (`__init__`) создайте экземпляры `helicone` и `client` для `Helicone` и `OpenAI` соответственно.

3. **Методы класса:**
   - **`generate_poem(self, prompt: str) -> str`:**
     - Использует `gpt-3.5-turbo` для генерации стихотворения на основе заданного `prompt`.
     - Записывает информацию о завершении запроса в `helicone` с помощью метода `log_completion`.
     - Возвращает сгенерированное стихотворение.
   - **`analyze_sentiment(self, text: str) -> str`:**
     - Использует `text-davinci-003` для анализа настроения заданного `text`.
     - Записывает информацию о завершении запроса в `helicone` с помощью метода `log_completion`.
     - Возвращает результат анализа настроения.
   - **`summarize_text(self, text: str) -> str`:**
     - Использует `text-davinci-003` для создания краткого изложения заданного `text`.
     - Записывает информацию о завершении запроса в `helicone` с помощью метода `log_completion`.
     - Возвращает краткое изложение текста.
   - **`translate_text(self, text: str, target_language: str) -> str`:**
     - Использует `text-davinci-003` для перевода заданного `text` на указанный `target_language`.
     - Записывает информацию о завершении запроса в `helicone` с помощью метода `log_completion`.
     - Возвращает перевод текста.

4. **Пример использования:**
   - Создайте экземпляр класса `HeliconeAI`.
   - Вызовите методы класса, например, `generate_poem`, передавая необходимый параметр (prompt для генерации стихотворения).
   - Выведите полученные результаты.

Пример использования
-------------------------

```python
from helicone import Helicone
from openai import OpenAI

class HeliconeAI:
    def __init__(self):
        self.helicone = Helicone()
        self.client = OpenAI()

    def generate_poem(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        self.helicone.log_completion(response)
        return response.choices[0].message.content

def main():
    helicone_ai = HeliconeAI()

    poem = helicone_ai.generate_poem("Напиши мне стихотворение про кота.")
    print("Generated Poem:\n", poem)

if __name__ == "__main__":
    main()