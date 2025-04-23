### Как использовать класс `ResultsExtractor`
=========================================================================================

Описание
-------------------------
Класс `ResultsExtractor` предназначен для извлечения результатов из взаимодействий агентов (`TinyPerson`) и окружений (`TinyWorld`). Он использует шаблоны для формирования запросов к OpenAI и извлекает структурированные данные из ответов.

Шаги выполнения
-------------------------
1. **Инициализация `ResultsExtractor`**:
   - Создание экземпляра класса `ResultsExtractor` с указанием пути к шаблону промпта, целей извлечения, контекста ситуации, полей для извлечения и настроек verbosity.

2. **Извлечение результатов из агента**:
   - Использование метода `extract_results_from_agent` для извлечения данных из объекта `TinyPerson`.
   - Этот метод формирует запрос к OpenAI на основе истории взаимодействий агента и извлекает результаты в формате JSON.

3. **Извлечение результатов из окружения**:
   - Использование метода `extract_results_from_world` для извлечения данных из объекта `TinyWorld`.
   - Этот метод аналогично формирует запрос к OpenAI на основе истории взаимодействий агентов в окружении и извлекает результаты.

4. **Сохранение результатов**:
   - Использование метода `save_as_json` для сохранения извлеченных результатов в файл JSON.

5. **Получение значений по умолчанию**:
   - Использование метода `_get_default_values_if_necessary` для получения значений по умолчанию, если не предоставлены аргументы для целей извлечения, контекста ситуации, полей или настроек verbosity.

Пример использования
-------------------------

```python
    import os
    from tinytroupe.extraction.results_extractor import ResultsExtractor
    from tinytroupe.agent.person import TinyPerson
    from tinytroupe.environment import TinyWorld

    # Путь к файлу с шаблоном промпта
    extraction_prompt_template_path = os.path.join(os.path.dirname(__file__), './prompts/interaction_results_extractor.mustache')

    # Инициализация ResultsExtractor
    results_extractor = ResultsExtractor(
        extraction_prompt_template_path=extraction_prompt_template_path,
        extraction_objective="Extract key information about the agent's goals and actions.",
        situation="The agent is in a negotiation scenario.",
        fields=["goal", "actions", "outcome"],
        verbose=True
    )

    # Пример TinyPerson (необходимо создать экземпляр агента)
    agent = TinyPerson(name="Alice", description="A negotiator")
    agent.add_message(role="user", content="I want to buy your product for $100.")
    agent.add_message(role="assistant", content="I can sell it for $120.")

    # Извлечение результатов из агента
    agent_results = results_extractor.extract_results_from_agent(tinyperson=agent)
    print(f"Agent Results: {agent_results}")

    # Пример TinyWorld (необходимо создать экземпляр окружения)
    world = TinyWorld(name="NegotiationWorld")
    world.add_agent(agent)

    # Извлечение результатов из окружения
    world_results = results_extractor.extract_results_from_world(tinyworld=world)
    print(f"World Results: {world_results}")

    # Сохранение результатов в файл
    results_extractor.save_as_json(filename="extraction_results.json", verbose=True)
```