## Как использовать блок кода `test_intervention_1` 
=========================================================================================

Описание
-------------------------
Этот блок кода представляет собой юнит-тест для функции `Intervention`, которая реализует вмешательство в ход событий в `TinyWorld`. Тест проверяет, что вмешательство работает корректно, меняя ход мыслей персонажа, когда выполняется определенное условие.

Шаги выполнения
-------------------------
1. **Создание персонажа:** Создается персонаж `Oscar` с помощью функции `create_oscar_the_architect()`.
2. **Инициализация мыслей персонажа:** Персонаж `Oscar` получает мысли, выражающие печаль. 
3. **Проверка начального состояния:** Проверяется, что персонаж действительно думает о печальных вещах.
4. **Создание вмешательства:** Создается объект `Intervention`, который будет изменять ход мыслей персонажа, если выполняется заданное условие.
    - Устанавливается текстовое условие: `Oscar is not very happy.`.
    - Устанавливается эффект вмешательства: `target.think("Enough sadness. I will now talk about something else that makes me happy.")`. 
5. **Создание мира:** Создается `TinyWorld` с персонажем `Oscar` и вмешательством, которое было определено ранее.
6. **Запуск симуляции:** Миру дается команда `run(2)` - запустить симуляцию на два шага.
7. **Проверка конечного состояния:** Проверяется, что персонаж `Oscar` после вмешательства начал думать о счастливых вещах.

Пример использования
-------------------------

```python
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

**Важно:** 
- В этом примере мы видим, как вмешательство `Intervention` меняет ход мыслей персонажа `Oscar`, делая его более позитивным. 
- В реальном проекте `TinyWorld` можно создавать более сложные сценарии с множеством персонажей и различных вмешательств.
- Данный тест демонстрирует, как проверить, что вмешательство работает корректно, изменяя состояние персонажей в заданном контексте.