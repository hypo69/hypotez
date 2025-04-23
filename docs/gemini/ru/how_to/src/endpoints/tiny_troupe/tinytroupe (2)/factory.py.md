### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код предоставляет класс `TinyFactory`, который является базовым классом для создания различных типов фабрик. Также он включает в себя подкласс `TinyPersonFactory`, который специализируется на создании экземпляров `TinyPerson` с использованием OpenAI LLM. Фабрики используются для генерации и управления агентами (`TinyPerson`) в симуляциях.

Шаги выполнения
-------------------------
1. **Инициализация `TinyFactory`**:
   - Создается экземпляр `TinyFactory` с уникальным именем и идентификатором симуляции (опционально).
   - Фабрика добавляется в глобальный список всех фабрик (`TinyFactory.all_factories`).
2. **Установка симуляции для свободных фабрик**:
   - Метод `set_simulation_for_free_factories` позволяет установить симуляцию для фабрик, у которых `simulation_id` равен `None`. Это позволяет связать фабрики со специфическими областями симуляции.
3. **Создание `TinyPersonFactory`**:
   - Создается экземпляр `TinyPersonFactory`, который принимает контекст (`context_text`) для генерации агентов и идентификатор симуляции (опционально).
   - Определяется путь к шаблону промпта для генерации персонажей (`person_prompt_template_path`).
4. **Генерация фабрик персонажей**:
   - Метод `generate_person_factories` использует OpenAI LLM для создания списка экземпляров `TinyPersonFactory`.
   - Он генерирует описания персонажей на основе общего контекста (`generic_context_text`) и создает фабрики с этими описаниями.
5. **Генерация персонажа**:
   - Метод `generate_person` создает экземпляр `TinyPerson` на основе контекста фабрики и конкретных особенностей агента (`agent_particularities`).
   - Используется шаблон промпта (`person_prompt_template_path`) для формирования запроса к LLM.
   - Сгенерированные персонажи отслеживаются, чтобы избежать повторной генерации одних и тех же персонажей.
6. **Вспомогательные методы**:
   - `_aux_model_call` — вспомогательный метод для выполнения вызова к модели OpenAI. Это необходимо для корректной работы кэширования.
   - `_setup_agent` — настраивает агента с необходимыми параметрами, определенными в конфигурации.

Пример использования
-------------------------

```python
    import os
    from tinytroupe.factory import TinyPersonFactory
    from tinytroupe.simulator import Simulator

    # Пример использования TinyPersonFactory
    simulator = Simulator()
    generic_context_text = "Действие происходит в средневековом городе."
    number_of_factories = 2

    # Создание фабрик персонажей
    factories = TinyPersonFactory.generate_person_factories(number_of_factories, generic_context_text)

    if factories:
        for factory in factories:
            simulator.add_factory(factory)

        # Генерация персонажа из фабрики
        agent_particularities = "Трусливый крестьянин."
        person = factories[0].generate_person(agent_particularities=agent_particularities)

        if person:
            print(f"Сгенерирован персонаж: {person.get('name')}")
        else:
            print("Не удалось сгенерировать персонажа.")
    else:
        print("Не удалось сгенерировать фабрики персонажей.")

    # Очистка фабрик после использования
    TinyPersonFactory.clear_factories()