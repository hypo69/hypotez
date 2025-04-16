# Модуль для создания и взаимодействия с TinyPerson

## Обзор

Модуль `src.endpoints.tiny_troupe.tiny_person` предназначен для создания и взаимодействия с объектами `TinyPerson`.

## Подробней

Модуль демонстрирует, как создать экземпляр `TinyPerson`, определить его характеристики и взаимодействовать с ним.

## Переменные

*   `john` (TinyPerson): Экземпляр класса `TinyPerson` с именем "John".

## Функции

### Пример использования

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

**Как работает функция**:

1.  Загружает переменные окружения из файла `.env`.
2.  Создает экземпляр класса `TinyPerson` с именем "John".
3.  Определяет характеристики агента, такие как возраст, профессия, национальность и навыки.
4.  Вызывает методы `listen` и `act` для взаимодействия с агентом.
5.  Выводит текущие взаимодействия агента.