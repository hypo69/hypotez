## Как использовать TinyPerson
=========================================================================================

Описание
-------------------------
Этот блок кода демонстрирует создание и взаимодействие с агентом TinyPerson. TinyPerson - это объект, который представляет собой персонаж с определенными характеристиками и возможностью взаимодействия.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: 
    - `os`: для работы с окружением.
    - `dotenv`: для загрузки переменных окружения из файла `.env`.
    - `tinytroupe.agent`: для импорта класса `TinyPerson`.
2. **Загрузка ключа API**:
    - Проверяем, есть ли ключ API в файле `.env`. Если да, то загружаем его в переменную окружения `OPENAI_API_KEY`.
3. **Создание экземпляра TinyPerson**:
    - Создаем объект `john` класса `TinyPerson` с именем "John".
4. **Определение характеристик**:
    - Используем метод `define` для задания характеристик агента: возраст, профессия, национальность и навыки.
5. **Взаимодействие с агентом**:
    - Используем метод `listen` для передачи сообщения агенту.
    - Вызываем метод `act`, чтобы агент обработал полученное сообщение.
    - Используем метод `pp_current_interactions` для вывода истории взаимодействия агента.

Пример использования
-------------------------

```python
import os
from dotenv import load_dotenv
# Если ключ хранится в файле .env
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from tinytroupe.agent import TinyPerson

# Create a TinyPerson instance
john = TinyPerson(name="John")

# Define some characteristics
john.define("age", 35)
john.define("occupation", "Software Engineer")
john.define("nationality", "American")
john.define("skills", [{"skill": "Coding in python"}])

# Interact with the agent
john.listen("Hello, John! How are you today?")
john.act()
john.pp_current_interactions()
```

**Результат**:

В консоли выводится история взаимодействия агента, включая сообщение, которое он получил, и сгенерированный ответ.