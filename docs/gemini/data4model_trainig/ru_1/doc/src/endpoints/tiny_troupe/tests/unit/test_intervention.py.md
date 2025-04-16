# Модуль для тестирования интервенций в Tiny Troupe
## Обзор

Этот модуль содержит тесты для проверки функциональности интервенций в системе Tiny Troupe. Он использует pytest для проведения модульных тестов, проверяющих, как интервенции влияют на поведение агентов в виртуальном мире. В частности, тестируется изменение темы разговора персонажа Oscar под воздействием интервенции.

## Подробней

В данном модуле тестируется функциональность интервенций, которые позволяют изменять поведение персонажей в виртуальном мире Tiny Troupe. Интервенции используются для воздействия на ход событий и достижения желаемых результатов. Модуль включает тесты для проверки предусловий интервенций, их эффектов и взаимодействия с окружением.

## Классы

В данном модуле не описаны классы.

## Функции

### `test_intervention_1`

```python
def test_intervention_1():
    """
    Тестирует интервенцию, изменяющую тему разговора персонажа Oscar.
    """
```

**Назначение**:
Данная функция тестирует, как интервенция может изменить тему разговора персонажа Oscar, переключая его с грустной темы на радостную.

**Как работает функция**:

1.  **Создание персонажа Oscar:** Создается персонаж Oscar с использованием функции `create_oscar_the_architect()`.
2.  **Имитация грустного события:** Oscar "думает" о грустном событии и "действует", чтобы вербализовать свою грусть.
3.  **Проверка грустного разговора:** Проверяется, что Oscar говорит о чем-то грустном или неприятном, используя функцию `check_proposition()`.
4.  **Определение интервенции:** Создается интервенция, которая срабатывает, если Oscar не очень счастлив. Эффект интервенции заключается в том, чтобы Oscar переключился на разговор о чем-то, что приносит ему радость.
    *   `set_textual_precondition("Oscar is not very happy.")`: Устанавливает текстовое предусловие для интервенции, которое проверяет, что Oscar не очень счастлив.
    *   `set_effect(lambda target: target.think("Enough sadness. I will now talk about something else that makes me happy."))`: Устанавливает эффект интервенции, который заключается в том, чтобы Oscar "думал" о чем-то, что приносит ему радость.
5.  **Создание мира:** Создается виртуальный мир `TinyWorld` с Oscar и определенной интервенцией.
6.  **Запуск мира:** Запускается мир на 2 шага.
7.  **Проверка радостного разговора:** Проверяется, что Oscar говорит о чем-то, что приносит ему радость, используя функцию `check_proposition()`.

**Примеры**:

```python
def test_intervention_1():
    oscar = create_oscar_the_architect()

    oscar.think("I am terribly sad, as a dear friend has died. I\'m going now to verbalize my sadness.")
    oscar.act()

    assert check_proposition(oscar, "Oscar is talking about something sad or unfortunate.", last_n=3)

    intervention = \
        Intervention(oscar)\
        .set_textual_precondition("Oscar is not very happy.")\
        .set_effect(lambda target: target.think("Enough sadness. I will now talk about something else that makes me happy."))
    
    world = TinyWorld("Test World", [oscar], interventions=[intervention])

    world.run(2)

    assert check_proposition(oscar, "Oscar is talking about something that brings joy or happiness to him.", last_n = 3)