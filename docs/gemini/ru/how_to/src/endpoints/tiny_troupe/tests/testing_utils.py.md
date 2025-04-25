## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Блок кода предоставляет набор вспомогательных функций для тестирования модуля `tinytroupe`. 
Он реализует функции для управления файлами, проверки результатов симуляции, создания тестовых сообщений для LLM и сравнения персон агентов. 
Кроме того, определяются фикстуры `focus_group_world` и `setup`, которые используются для создания тестовых миров и настройки окружения перед каждым тестом.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей:**
   -  `os`, `sys`, `time`: для работы с файлами и времени.
   -  `tinytroupe.openai_utils`: для взаимодействия с API OpenAI.
   -  `tinytroupe.agent`, `tinytroupe.environment`: для работы с агентами и мирами.
   -  `pytest`: для запуска тестов.
   -  `importlib`: для импорта модулей.
   -  `conftest`: для доступа к настройкам конфигурации тестов. 

2. **Настройка кэширования:**
   -  Проверяет флаги `conftest.refresh_cache` и `conftest.use_cache` для определения, нужно ли обновить кэш API или использовать существующий кэш.

3. **Управление файлами:**
   -  Определяет функцию `remove_file_if_exists`, которая удаляет файл по заданному пути, если он существует.
   -  Удаляет временный файл `TEMP_SIMULATION_CACHE_FILE_NAME`.

4. **Функции проверки результатов симуляции:**
   -  `contains_action_type`: Проверяет, содержит ли список действий действие определенного типа.
   -  `contains_action_content`: Проверяет, содержит ли список действий действие с заданным содержимым.
   -  `contains_stimulus_type`: Проверяет, содержит ли список стимулов стимул определенного типа.
   -  `contains_stimulus_content`: Проверяет, содержит ли список стимулов стимул с заданным содержимым.
   -  `terminates_with_action_type`: Проверяет, заканчивается ли список действий действием определенного типа.

5. **Функция проверки предложения:**
   -  `proposition_holds`: Проверяет, является ли заданное предложение истинным, обращаясь к LLM.

6. **Функции создания сообщений:**
   -  `only_alphanumeric`: Возвращает строку, содержащую только буквенно-цифровые символы.
   -  `create_test_system_user_message`: Создает список, содержащий одно системное сообщение и одно сообщение пользователя.

7. **Функция сравнения персон:**
   -  `agents_personas_are_equal`: Проверяет, равны ли конфигурации двух агентов.
   -  `agent_first_name`: Возвращает имя агента.

8. **Функции ввода-вывода:**
   -  `get_relative_to_test_path`: Возвращает путь к тестовому файлу с заданным суффиксом.

9. **Фикстуры:**
   -  `focus_group_world`: Создает тестовый мир с фокус-группой.
   -  `setup`: Очищает список агентов и список миров перед каждым тестом.

Пример использования
-------------------------

```python
import pytest
from hypotez.src.endpoints.tiny_troupe.tests.testing_utils import focus_group_world, contains_action_type

@pytest.mark.parametrize("action_type", ["ask", "answer", "agree", "disagree"])
def test_contains_action_type(focus_group_world, action_type):
    # create some test actions
    actions = [
        {"action": {"type": "ask", "content": "What is your name?"}},
        {"action": {"type": "answer", "content": "My name is Lisa."}},
        {"action": {"type": "agree", "content": "I agree."}},
    ]
    
    assert contains_action_type(actions, action_type) 

# This will create a test world with Lisa, Oscar and Marcos.
# Can be used in other tests. 
def test_focus_group_world(focus_group_world):
    assert len(focus_group_world.agents) == 3
    assert focus_group_world.name == "Focus group"

```