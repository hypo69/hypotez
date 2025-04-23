### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот модуль предоставляет набор утилит для тестирования, включая функции для работы с файлами, проверки действий и стимулов, а также для взаимодействия с LLM (Large Language Model). Он также содержит фикстуры pytest для настройки тестовой среды.

Шаги выполнения
-------------------------
1. **Настройка путей**:
   - В начале модуля настраиваются пути к директориям `tinytroupe`, `../../` и `..`, чтобы обеспечить доступ к необходимым модулям.
   - Определяются глобальные константы, такие как `CACHE_FILE_NAME`, `EXPORT_BASE_FOLDER` и `TEMP_SIMULATION_CACHE_FILE_NAME`, которые используются для управления файлами кэша и экспорта.

2. **Кэширование API**:
   - В зависимости от значений `conftest.refresh_cache` и `conftest.use_cache` выполняется удаление или принудительное включение/выключение кэширования API с использованием функций из модуля `tinytroupe.openai_utils`.

3. **Управление файлами**:
   - Функция `remove_file_if_exists` удаляет файл по указанному пути, если он существует.
   - В начале модуля вызывается `remove_file_if_exists` для удаления временного файла `TEMP_SIMULATION_CACHE_FILE_NAME`.

4. **Проверка действий**:
   - `contains_action_type` проверяет, содержит ли список действий действие заданного типа.
   - `contains_action_content` проверяет, содержит ли список действий действие с заданным содержимым.
   - `terminates_with_action_type` проверяет, завершается ли список действий действием заданного типа.

5. **Проверка стимулов**:
   - `contains_stimulus_type` проверяет, содержит ли список стимулов стимул заданного типа.
   - `contains_stimulus_content` проверяет, содержит ли список стимулов стимул с заданным содержимым.

6. **Взаимодействие с LLM**:
   - `proposition_holds` проверяет, является ли заданное утверждение истинным, используя вызов LLM.
   - `only_alphanumeric` возвращает строку, содержащую только буквенно-цифровые символы из входной строки.
   - `create_test_system_user_message` создает список сообщений для взаимодействия с LLM, содержащий системное и пользовательское сообщения.

7. **Сравнение агентов**:
   - `agents_personas_are_equal` сравнивает конфигурации двух агентов, игнорируя (опционально) имя агента.
    - Функция проходит по ключам в `_persona` атрибуте `agent1`.
    - Если ключ находится в списке игнорируемых ключей, он пропускается.
    - Если значение для текущего ключа в `agent1._persona` не равно значению для того же ключа в `agent2._persona`, функция возвращает `False`.
    - Если все значения совпадают, функция возвращает `True`.
8. **Работа с именами агентов**:
   - `agent_first_name` возвращает имя агента.

9. **Работа с путями**:
   - `get_relative_to_test_path` возвращает путь к тестовому файлу с заданным суффиксом.

10. **Фикстуры pytest**:
    - `focus_group_world` создает тестовый мир (`TinyWorld`) с несколькими агентами (`TinyPerson`).
    - `setup` является фикстурой для очистки агентов и окружений перед каждым тестом.

Пример использования
-------------------------

```python
import pytest
from src.endpoints.tiny_troupe.tests.testing_utils import contains_action_type, proposition_holds, create_test_system_user_message

def test_contains_action_type():
    actions = [{"action": {"type": "message", "content": "Hello"}}]
    assert contains_action_type(actions, "message") == True
    assert contains_action_type(actions, "other_type") == False

def test_proposition_holds():
    # Mock openai_utils.client().send_message to avoid actual API calls during testing
    from unittest.mock import patch
    with patch('src.endpoints.tiny_troupe.tests.testing_utils.openai_utils.client') as mock_client:
        mock_client.return_value.send_message.return_value = {"content": "true"}
        assert proposition_holds("Test proposition") == True

def test_create_test_system_user_message():
    messages = create_test_system_user_message("Hello", "System message")
    assert messages == [{"role": "system", "content": "System message"}, {"role": "user", "content": "Hello"}]

@pytest.mark.asyncio  # Ensure pytest knows this is an async test
async def test_agents_personas_are_equal():
    from src.endpoints.tiny_troupe.tests.testing_utils import agents_personas_are_equal
    from tinytroupe.agent import TinyPerson
    agent1 = TinyPerson(persona={"name": "Alice", "age": 30, "occupation": "Engineer"}, world="test")
    agent2 = TinyPerson(persona={"name": "Bob", "age": 30, "occupation": "Engineer"}, world="test")

    # Test when names are different but other attributes are the same
    assert agents_personas_are_equal(agent1, agent2, ignore_name=True) == True

    # Test when an attribute other than name is different
    agent3 = TinyPerson(persona={"name": "Alice", "age": 35, "occupation": "Engineer"}, world="test")
    assert agents_personas_are_equal(agent1, agent3, ignore_name=True) == False