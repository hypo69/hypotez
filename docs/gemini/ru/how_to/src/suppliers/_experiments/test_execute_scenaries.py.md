### **Инструкции по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот блок кода содержит набор тестов для проверки функциональности модулей `execute_scenarios.py`, который включает в себя тестирование функций `run_scenarios`, `run_scenario_file`, `run_scenario` и `grab_product_page`. Тесты используют `unittest` и `unittest.mock` для имитации различных сценариев и проверки корректности работы функций.

Шаги выполнения
-------------------------
1. **Импорт необходимых модулей**: Импортируются модули `unittest`, `MagicMock` из `unittest.mock`, а также функции для тестирования: `run_scenarios`, `run_scenario_file`, `run_scenario` и `grab_product_page`.
2. **Создание тестовых классов**: Определяются тестовые классы, такие как `TestRunListOfScenarioFiles`, `TestRunScenarioFile`, `TestGrabProductPage` и `TestRunScenario`, которые наследуются от `unittest.TestCase`.
3. **Настройка тестовых методов**: В каждом тестовом классе определяются методы для тестирования конкретных сценариев. Например, `test_with_scenario_files_...ed`, `test_with_no_scenario_files_...ed` и другие.
4. **Использование `MagicMock`**: В тестовых методах создаются объекты `MagicMock` для имитации объектов `Supplier` и других зависимостей. Это позволяет изолировать тестируемые функции и контролировать их поведение.
5. **Установка ожидаемых значений**: Перед вызовом тестируемой функции устанавливаются ожидаемые значения атрибутов и настроек имитированных объектов.
6. **Вызов тестируемой функции**: Вызывается функция, которую необходимо протестировать, например, `run_scenarios(s, scenario_files)`.
7. **Проверка результатов**: После вызова функции проверяются результаты с помощью методов `self.assertTrue`, `self.assertEqual`, `assert_called_once` и других методов `unittest.TestCase`. Проверяется, что функция вернула ожидаемое значение, вызвала ожидаемые методы имитированных объектов и изменила атрибуты объектов нужным образом.

Пример использования
-------------------------

```python
import unittest
from unittest.mock import MagicMock

from execute_scenarios import run_scenarios

class TestRunListOfScenarioFiles(unittest.TestCase):
    
    def test_with_scenario_files_...ed(self):
        s = MagicMock()
        scenario_files = ["scenario1.json", "scenario2.json"]
        s.settings = {
            'check categories on site': False,
            'scenarios': ["default1.json", "default2.json"]
        }
        
        result = run_scenarios(s, scenario_files)
        
        self.assertTrue(result)
        s.related_modules.build_shop_categories.assert_not_called()
        self.assertEqual(s.current_scenario_filename, "scenario2.json")
        self.assertEqual(s.settings['last_runned_scenario'], "scenario2.json")
```
В этом примере тестируется функция `run_scenarios` с имитированным объектом `Supplier`. Проверяется, что функция возвращает `True`, метод `build_shop_categories` не вызывается, а атрибуты `current_scenario_filename` и `settings['last_runned_scenario']` изменяются на ожидаемые значения.