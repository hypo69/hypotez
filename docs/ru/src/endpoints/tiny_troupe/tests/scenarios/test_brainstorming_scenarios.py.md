# Модуль тестирования сценария мозгового штурма

## Обзор

Этот модуль содержит функцию `test_brainstorming_scenario`, которая тестирует сценарий мозгового штурма с использованием TinyPerson агентов в виртуальном мире. Цель теста - стимулировать обсуждение идей для новых функций товара, в данном случае, для Microsoft Word, с использованием AI технологий.

## Подробней

Модуль использует виртуальный мир `focus_group_world`, в котором агенты TinyPerson генерируют и обсуждают идеи. Затем, извлекаются результаты обсуждения и проверяются на соответствие заданным критериям.

## Функции

### `test_brainstorming_scenario`

```python
def test_brainstorming_scenario(setup, focus_group_world):
    """ Тестирует сценарий мозгового штурма с использованием TinyPerson агентов.

    Args:
        setup: Параметр настройки (не используется в коде функции).
        focus_group_world: Виртуальный мир, содержащий агентов TinyPerson.

    Returns:
        None

    Raises:
        AssertionError: Если предложение о наличии идей для новых функций товара не подтверждается LLM.

    
    - Инициализирует виртуальный мир `focus_group_world`.
    - Отправляет сообщение агентам в мире с запросом на мозговой штурм идей для нового товара (AI-функции для Microsoft Word).
    - Запускает мир на один шаг.
    - Находит агента по имени "Lisa Carter".
    - Запрашивает у агента обобщение предложенных идей.
    - Извлекает результаты, используя ResultsExtractor.
    - Проверяет, содержит ли извлеченный текст идеи для новых функций товара.

    Примеры:
        Предполагается использование в рамках pytest с настроенным виртуальным миром и агентами.
    """
    world = focus_group_world

    world.broadcast("""
             Folks, we need to brainstorm ideas for a new product. Your mission is to discuss potential AI feature ideas
             to add to Microsoft Word. In general, we want features that make you or your industry more productive,
             taking advantage of all the latest AI technologies.

             Please start the discussion now.
             """)
    
    world.run(1)

    agent = TinyPerson.get_agent_by_name("Lisa Carter")

    agent.listen_and_act("Can you please summarize the ideas that the group came up with?")

    from tinytroupe.extraction import ResultsExtractor

    extractor = ResultsExtractor()

    results = extractor.extract_results_from_agent(agent, 
                            extraction_objective="Summarize the the ideas that the group came up with, explaining each idea as an item of a list. Describe in details the benefits and drawbacks of each.", 
                            situation="A focus group to brainstorm ideas for a new product.")

    print("Brainstorm Results: ", results)

    assert proposition_holds(f"The following contains some ideas for new product features or entirely new products: \'{results}\'"), f"Proposition is false according to the LLM."