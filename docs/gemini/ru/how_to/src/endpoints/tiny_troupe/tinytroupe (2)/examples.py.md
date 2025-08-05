## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода представляет собой коллекцию примеров, иллюстрирующих, как создавать и настраивать объекты `TinyPerson` в библиотеке tinytroupe. 
Каждый пример создает объект `TinyPerson` с уникальными характеристиками, которые могут быть использованы для различных целей. 

Шаги выполнения
-------------------------
1. **Импортируй необходимый модуль**:  `from tinytroupe.agent import TinyPerson`
2. **Создай объект `TinyPerson`**:  `tiny_person = TinyPerson("Имя")`
3. **Определи характеристики**:  Используй методы `.define()`, `.define_several()`, для добавления различных атрибутов, таких как возраст, национальность, профессия, интересы, навыки и отношения.
4. **Используй объект**:  После создания объект `TinyPerson` готов к использованию в других сценариях, где требуется взаимодействие с виртуальным персонажем.

Пример использования
-------------------------

```python
from tinytroupe.agent import TinyPerson

# Создание объекта TinyPerson
oscar = TinyPerson("Oscar")

# Определение возраста
oscar.define("age", 30)

# Определение национальности
oscar.define("nationality", "German")

# Определение профессии
oscar.define("occupation", "Architect")

# Определение описания профессии
oscar.define("occupation_description", 
                """
                You are an architect. You work at a company called "Awesome Inc.". Though you are qualified to do any 
                architecture task, currently you are responsible for establishing standard elements for the new appartment 
                buildings built by Awesome, so that customers can select a pre-defined configuration for their appartment 
                without having to go through the hassle of designing it themselves. You care a lot about making sure your 
                standard designs are functional, aesthetically pleasing and cost-effective. Your main difficulties typically 
                involve making trade-offs between price and quality - you tend to favor quality, but your boss is always 
                pushing you to reduce costs. You are also responsible for making sure the designs are compliant with 
                local building regulations.
                """)

# Определение черт личности
oscar.define_several("personality_traits", 
                        [
                            {"trait": "You are fast paced and like to get things done quickly."}, 
                            {"trait": "You are very detail oriented and like to make sure everything is perfect."},
                            {"trait": "You have a witty sense of humor and like to make jokes."},
                            {"trait": "You don't get angry easily, and always try to stay calm. However, in the few occasions you do get angry, you get very very mad."}
                      ])

# Возвращение объекта TinyPerson
return oscar
```

**Важно**: Примеры из данного блока кода могут быть использованы как отправная точка для создания собственных агентов с уникальными характеристиками.