### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код выполняет сценарий мозгового штурма в симулированной среде `focus_group_world`, где агенты (представленные классом `TinyPerson`) обсуждают идеи для новых функций продукта. В данном случае, агенты генерируют идеи для добавления AI-функций в Microsoft Word. После обсуждения, один из агентов (Lisa Carter) запрашивает обобщение предложенных идей, которые затем извлекаются и проверяются на соответствие ожидаемым результатам.

Шаги выполнения
-------------------------
1. **Инициализация мира**: Получает объект мира `focus_group_world` из параметра `setup`.
2. **Трансляция задачи**: Отправляет сообщение всем агентам в мире с заданием сгенерировать идеи для новых AI-функций в Microsoft Word.
3. **Запуск симуляции**: Запускает мир на один шаг, чтобы агенты могли обсудить идеи.
4. **Получение агента**: Получает конкретного агента (Lisa Carter) по имени.
5. **Запрос на обобщение**: Агент Lisa Carter запрашивает обобщение предложенных идей.
6. **Извлечение результатов**: Использует класс `ResultsExtractor` для извлечения и обобщения идей, предложенных группой.
7. **Проверка результатов**: Проверяет, что извлеченные результаты содержат идеи для новых функций продукта или новых продуктов, используя функцию `proposition_holds`.
8. **Логирование результатов**: Выводит извлеченные результаты в консоль.

Пример использования
-------------------------

```python
import pytest
import logging
logger = logging.getLogger("tinytroupe")

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from tinytroupe.agent import TinyPerson
from tinytroupe.extraction import ResultsExtractor
from testing_utils import *

def test_brainstorming_scenario(setup, focus_group_world):
    """
    Тест сценария мозгового штурма для генерации идей AI-функций Microsoft Word.
    
    Args:
        setup: Параметр настройки теста.
        focus_group_world: Симулированная среда, в которой агенты обсуждают идеи.
    """
    world = focus_group_world

    # Рассылка задачи всем агентам
    world.broadcast("""
        Folks, we need to brainstorm ideas for a new product. Your mission is to discuss potential AI feature ideas
        to add to Microsoft Word. In general, we want features that make you or your industry more productive,
        taking advantage of all the latest AI technologies.

        Please start the discussion now.
    """)
    
    world.run(1)

    # Получение агента Lisa Carter
    agent = TinyPerson.get_agent_by_name("Lisa Carter")

    # Агент запрашивает обобщение идей
    agent.listen_and_act("Can you please summarize the ideas that the group came up with?")

    # Извлечение результатов
    extractor = ResultsExtractor()
    results = extractor.extract_results_from_agent(
        agent, 
        extraction_objective="Summarize the the ideas that the group came up with, explaining each idea as an item of a list. Describe in details the benefits and drawbacks of each.", 
        situation="A focus group to brainstorm ideas for a new product."
    )

    print("Brainstorm Results: ", results)

    # Проверка результатов
    assert proposition_holds(f"The following contains some ideas for new product features or entirely new products: '{results}'"), "Proposition is false according to the LLM."