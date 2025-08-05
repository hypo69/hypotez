#  Тестирование `Intervention`

##  Обзор

Этот модуль содержит юнит-тесты для класса `Intervention` из модуля `tinytroupe.steering`. 

## Детали 

Тестовый модуль `test_intervention.py` проверяет функциональность класса `Intervention`,  который используется для моделирования вмешательств в  TinyWorld. В этом модуле реализован один тестовый сценарий `test_intervention_1`.

##  Функции 

###  `test_intervention_1`

**Цель**: Тестирует сценарий, где вмешательство изменяет мысли и действия Oscar.

**Параметры**:  Отсутствуют

**Возвращает**:  Отсутствует

**Исключения**:  Отсутствуют

**Как работает функция**:

1. Создает объект Oscar с помощью `create_oscar_the_architect()`.
2. Задает Oscar мысли о печали.
3. Проверяет, что Oscar говорит о печали.
4. Создает вмешательство, которое срабатывает, если Oscar не очень счастлив. Вмешательство заставляет Oscar думать о чем-то, что его радует.
5. Создает мир TinyWorld с Oscar и вмешательством.
6. Запускает мир на 2 шага.
7. Проверяет, что Oscar теперь говорит о чем-то радостном. 

**Пример**:
```python
def test_intervention_1():
    oscar = create_oscar_the_architect()

    oscar.think("I am terribly sad, as a dear friend has died. I'm going now to verbalize my sadness.")
    oscar.act()

    assert check_proposition(oscar, "Oscar is talking about something sad or unfortunate.", last_n=3)

    intervention = \
        Intervention(oscar) \
        .set_textual_precondition("Oscar is not very happy.") \
        .set_effect(lambda target: target.think("Enough sadness. I will now talk about something else that makes me happy."))
    
    world = TinyWorld("Test World", [oscar], interventions=[intervention])

    world.run(2)

    assert check_proposition(oscar, "Oscar is talking about something that brings joy or happiness to him.", last_n = 3)
```