## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода представляет собой набор юнит-тестов для класса TinyPerson из проекта hypotez. Тесты проверяют различные функции агента, такие как:

* **Listen and Act:** Проверяет, может ли агент правильно реагировать на вводные сообщения.
* **Listen:** Проверяет, может ли агент правильно обрабатывать вводные сообщения и сохранять их в своей памяти.
* **Define:** Проверяет, может ли агент устанавливать новые значения в своей конфигурации.
* **Define Several:** Проверяет, может ли агент правильно устанавливать несколько значений для группы конфигурационных параметров.
* **Socialize:** Проверяет, может ли агент правильно взаимодействовать с другим агентом.
* **See:** Проверяет, может ли агент правильно обрабатывать визуальные стимулы.
* **Think:** Проверяет, может ли агент правильно обрабатывать мысли и действия, связанные с ними.
* **Internalize Goal:** Проверяет, может ли агент правильно обрабатывать  цели и задачи.
* **Move To:** Проверяет, может ли агент правильно изменять свое местоположение и контекст.
* **Change Context:** Проверяет, может ли агент правильно изменять контекст.
* **Save Specification:** Проверяет, может ли агент правильно сохранять свою конфигурацию и загружать ее из файла.


Шаги выполнения
-------------------------
1. **Импорт необходимых модулей.** 
2. **Создание тестовых агентов:** Используются функции `create_oscar_the_architect()`, `create_lisa_the_data_scientist()`, `create_oscar_the_architect_2()`, и `create_lisa_the_data_scientist_2()` для создания тестовых агентов.
3. **Проверка работы функций:**  Каждый тест проверяет отдельную функцию TinyPerson, например, `test_listen`, `test_define`, `test_socialize` и т.д.
4. **Использование вспомогательных функций:**  В тестах используются вспомогательные функции, такие как `contains_action_type`, `contains_action_content`, `terminates_with_action_type`, `agent_first_name`, `agents_personas_are_equal`.


Пример использования
-------------------------
```python
    # Тест функции "Listen and Act"
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        actions = agent.listen_and_act("Tell me a bit about your life.", return_actions=True)

        # Проверка, что агент выполнил хотя бы одно действие
        assert len(actions) >= 1, f"{agent.name} should have at least one action to perform (even if it is just DONE)." 
        # Проверка, что агент выполнил действие "TALK" 
        assert contains_action_type(actions, "TALK"), f"{agent.name} should have at least one TALK action to perform, since we asked him to do so." 
        # Проверка, что агент завершил последовательность действиями "DONE" 
        assert terminates_with_action_type(actions, "DONE"), f"{agent.name} should always terminate with a DONE action." 

    # Тест функции "Listen"
    for agent in [create_oscar_the_architect(), create_lisa_the_data_scientist()]:
        agent.listen("Hello, how are you?")

        # Проверка, что агент сохранил сообщение в своей памяти
        assert len(agent.current_messages) > 0, f"{agent.name} should have at least one message in its current messages." 
        # Проверка, что агент правильно определил роль отправителя сообщения
        assert agent.episodic_memory.retrieve_all()[-1]['role'] == 'user', f"{agent.name} should have the last message as \'user\'."
        # Проверка, что агент правильно определил тип стимула 
        assert agent.episodic_memory.retrieve_all()[-1]['content']['stimuli'][0]['type'] == 'CONVERSATION', f"{agent.name} should have the last message as a \'CONVERSATION\' stimulus."
        # Проверка, что агент правильно определил содержимое стимула
        assert agent.episodic_memory.retrieve_all()[-1]['content']['stimuli'][0]['content'] == 'Hello, how are you?', f"{agent.name} should have the last message with the correct content."
```