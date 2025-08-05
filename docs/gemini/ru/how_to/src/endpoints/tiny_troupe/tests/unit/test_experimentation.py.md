## Как использовать блок кода `check_proposition`
=========================================================================================

Описание
-------------------------
Блок кода `check_proposition`  используется для проверки утверждения (пропозиции)  о TinyPerson или TinyWorld. 

Он принимает на вход:
* `target`:  TinyPerson или TinyWorld,  к которому относится утверждение.
* `claim`: Строка, содержащая само утверждение.

И возвращает `True` или `False`, в зависимости от того, верно ли утверждение.

Шаги выполнения
-------------------------
1. **Получение утверждения:**  В качестве аргумента передается утверждение (`claim`) в виде строки.
2. **Проверка утверждения:**  Функция проверяет,  соответствует ли утверждение (`claim`) текущему состоянию TinyPerson или TinyWorld, заданного  в  `target`.  
3. **Возврат результата:**  Возвращает `True`, если утверждение  верно,  и  `False`,  если  нет.

Пример использования
-------------------------

```python
from tinytroupe.experimentation import Proposition, check_proposition
from tinytroupe.examples import create_oscar_the_architect

oscar = create_oscar_the_architect()
oscar.listen_and_act("Tell me a bit about your travel preferences.")

# Проверка утверждения
assert check_proposition(target=oscar, claim="Oscar mentions his travel preferences.") == True
# Проверка ложного утверждения
assert check_proposition(target=oscar, claim="Oscar writes a novel about how cats are better than dogs.") == False

# Вызов через класс
assert check_proposition(oscar, "Oscar mentions his travel preferences.") == True
assert check_proposition(oscar, "Oscar writes a novel about how cats are better than dogs.") == False

```