# Модуль `tiny_person.py`

## Обзор

Модуль предназначен для демонстрации работы с классом `TinyPerson` из библиотеки `tinytroupe`. Он создает экземпляр агента `TinyPerson`, определяет его характеристики и взаимодействует с ним, выводя результаты взаимодействия.

## Подробнее

Этот код демонстрирует основные шаги работы с агентом `TinyPerson`: создание, определение характеристик и взаимодействие. Он используется для тестирования и демонстрации возможностей библиотеки `tinytroupe`.

## Классы

### `TinyPerson`

**Описание**: Класс представляет собой программного агента с определенными характеристиками и способностями к взаимодействию.

**Наследует**:
- Нет

**Атрибуты**:
- `name` (str): Имя агента.

**Методы**:
- `define(property, value)`: Определяет характеристику агента.
- `listen(message)`: Получает сообщение от пользователя.
- `act()`: Активирует действие агента.
- `pp_current_interactions()`: Выводит текущие взаимодействия агента.

**Принцип работы**:
1.  Создается экземпляр класса `TinyPerson` с заданным именем.
2.  Определяются различные характеристики агента с использованием метода `define`.
3.  Агент получает сообщение через метод `listen`.
4.  Вызывается метод `act` для выполнения действия агентом.
5.  Результаты взаимодействия выводятся на экран с помощью метода `pp_current_interactions`.

## Функции

В данном модуле нет отдельных функций, кроме методов класса `TinyPerson`.

## Примеры

```python
import os
from dotenv import load_dotenv
# Если ключ хранится в файле .env
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from tinytroupe.agent import TinyPerson

# Создание экземпляра TinyPerson
john = TinyPerson(name="John")

# Определение характеристик
john.define("age", 35)
john.define("occupation", "Software Engineer")
john.define("nationality", "American")
john.define("skills", [{"skill": "Coding in python"}])

# Взаимодействие с агентом
john.listen("Hello, John! How are you today?")
john.act()
john.pp_current_interactions()