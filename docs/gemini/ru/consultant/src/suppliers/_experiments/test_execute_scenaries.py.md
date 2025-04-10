### **Анализ кода модуля `test_execute_scenaries.py`**

**Качество кода:**

- **Соответствие стандартам**: 6/10
- **Плюсы**:
    - Код содержит модульные тесты, что помогает в проверке функциональности.
    - Используются `MagicMock` для мокирования зависимостей, что упрощает тестирование отдельных компонентов.
- **Минусы**:
    - Отсутствует единообразие в оформлении кода (например, лишние пустые строки, отсутствие пробелов вокруг операторов).
    - Не хватает аннотаций типов для переменных и параметров функций.
    - Не все функции и классы имеют docstring.
    - Встречаются устаревшие или избыточные комментарии.
    - Есть проблемы с импортами (например, `from execute_scenarios import run_scenarios,run_scenario_file,run_scenario,grab_product_page` без указания модуля).
    - Не используется модуль `logger` для логирования.
    - Есть вызов `patch("your_module.j_loads")`. Необходимо исправить `your_module` на фактический модуль, где находится `j_loads`.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    - Добавить docstring к каждому классу и каждой функции, описывая их назначение, параметры и возвращаемые значения.
    - Использовать русский язык и формат UTF-8 для всех docstring.
2.  **Добавить аннотации типов**:
    - Добавить аннотации типов для всех переменных и параметров функций.
3.  **Удалить лишние комментарии и пустые строки**:
    - Удалить устаревшие и избыточные комментарии, а также лишние пустые строки для улучшения читаемости кода.
4.  **Использовать `logger` для логирования**:
    - Заменить `print` на `logger.info`, `logger.error` и т.д. для логирования информации и ошибок.
5.  **Исправить импорты**:
    - Указать конкретные модули, из которых импортируются функции (например, `from src.execute_scenarios import run_scenarios`).
6.  **Форматирование кода**:
    - Привести код в соответствие со стандартами PEP8 (например, добавить пробелы вокруг операторов, использовать одинарные кавычки).
7.  **Исправить моки**:
    - Заменить `patch("your_module.j_loads")` на `patch("src.suppliers._experiments.execute_scenarios.j_loads")` или другой фактический путь к модулю.
8.  **Добавить обработку исключений**:
    - Добавить блоки `try...except` для обработки возможных исключений и логировать их с помощью `logger.error`.

**Оптимизированный код:**

```python
## \file /src/suppliers/_experiments/test_execute_scenaries.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль содержит модульные тесты для проверки функциональности выполнения сценариев.
==============================================================================

В модуле определены классы тестов:
- TestRunListOfScenarioFiles: для тестирования запуска списка файлов сценариев.
- TestRunScenarioFile: для тестирования запуска отдельного файла сценария.
- TestGrabProductPage: для тестирования извлечения данных со страницы продукта.
- TestRunScenario: для тестирования запуска отдельного сценария.
"""

import unittest
from unittest.mock import MagicMock, patch
from typing import List, Optional, Dict, Any
from src.suppliers._experiments.execute_scenarios import run_scenarios, run_scenario_file, run_scenario, grab_product_page
from src.logger import logger
from src.suppliers.supplier import Supplier


class TestRunListOfScenarioFiles(unittest.TestCase):
    """
    Класс для тестирования функции run_scenarios, которая запускает сценарии из списка файлов.
    """

    def test_with_scenario_files_passed(self) -> None:
        """
        Тест проверяет, что функция run_scenarios корректно запускает сценарии из указанных файлов.
        """
        s = MagicMock()
        scenario_files: List[str] = ["scenario1.json", "scenario2.json"]
        s.settings: Dict[str, Any] = {
            'check categories on site': False,
            'scenarios': ["default1.json", "default2.json"]
        }

        result: bool = run_scenarios(s, scenario_files)

        self.assertTrue(result)
        s.related_modules.build_shop_categories.assert_not_called()
        self.assertEqual(s.current_scenario_filename, "scenario2.json")
        self.assertEqual(s.settings['last_runned_scenario'], "scenario2.json")

    def test_with_no_scenario_files_passed(self) -> None:
        """
        Тест проверяет, что функция run_scenarios корректно запускается без указанных файлов сценариев,
        используя сценарии, указанные в настройках.
        """
        s = MagicMock()
        s.settings: Dict[str, Any] = {
            'check categories on site': True,
            'scenarios': ["default1.json", "default2.json"]
        }

        result: bool = run_scenarios(s)

        self.assertTrue(result)
        s.related_modules.build_shop_categories.assert_called_once()
        self.assertEqual(s.current_scenario_filename, "default2.json")
        self.assertEqual(s.settings['last_runned_scenario'], "default2.json")


class TestRunScenarioFile(unittest.TestCase):
    """
    Класс для тестирования функции run_scenario_file, которая запускает сценарии из указанного файла.
    """

    def setUp(self) -> None:
        """
        Метод для настройки тестового окружения перед каждым тестом.
        """
        # Создание мок-объекта Supplier с необходимыми атрибутами
        self.s = MagicMock()
        self.s.current_scenario_filename: str = "test_scenario.json"
        self.s.settings: Dict[str, Any] = {
            "parcing method [webdriver|api]": "webdriver"
        }
        self.s.dir_export_imagesECTORY_FOR_STORE: str = "/path/to/images"
        self.s.scenarios: Dict[str, Any] = {
            "scenario1": {
                "url": "https://example.com",
                "steps": [
                    # шаги для scenario1
                ]
            },
            "scenario2": {
                "url": None,
                "steps": [
                    # шаги для scenario2
                ]
            }
        }

    def test_run_scenario_file_webdriver(self) -> None:
        """
        Тест проверяет, что функция run_scenario_file корректно запускает сценарии из файла,
        используя метод webdriver.
        """
        with patch("src.suppliers._experiments.execute_scenarios.j_loads") as mock_j_loads:
            mock_j_loads.return_value = {"scenarios": self.s.scenarios}
            with patch("src.suppliers._experiments.execute_scenarios.run_scenario") as mock_run_scenario:
                run_scenario_file(self.s, "test_scenario.json")
                mock_j_loads.assert_called_once_with("/path/to/scenarios/test_scenario.json")
                mock_run_scenario.assert_any_call(self.s, self.s.scenarios["scenario1"])
                mock_run_scenario.assert_not_called_with(self.s, self.s.scenarios["scenario2"])

    def test_run_scenario_file_api(self) -> None:
        """
        Тест проверяет, что функция run_scenario_file корректно запускает сценарии из файла,
        используя метод api.
        """
        self.s.settings["parcing method [webdriver|api]"] = "api"
        with patch("src.suppliers._experiments.execute_scenarios.related_modules.run_scenario_file_via_api") as mock_run_scenario_file_via_api:
            run_scenario_file(self.s, "test_scenario.json")
            mock_run_scenario_file_via_api.assert_called_once_with(self.s, "test_scenario.json")

    def test_run_scenario_file_no_scenarios(self) -> None:
        """
        Тест проверяет, что функция run_scenario_file корректно обрабатывает ситуацию,
        когда в файле сценариев нет сценариев.
        """
        with patch("src.suppliers._experiments.execute_scenarios.j_loads") as mock_j_loads:
            mock_j_loads.return_value = {"scenarios": None}
            with patch("src.logger.logger.error") as mocklogger_console_error:
                self.assertFalse(run_scenario_file(self.s, "test_scenario.json"))
                mocklogger_console_error.assert_called_once_with("Возможно файл test_scenario.json не содержит сценариев")


class TestGrabProductPage(unittest.TestCase):
    """
    Класс для тестирования функции grab_product_page, которая извлекает данные со страницы продукта.
    """

    def setUp(self) -> None:
        """
        Метод для настройки тестового окружения перед каждым тестом.
        """
        # Настройка необходимых объектов, таких как мок-объекты или экземпляр Supplier
        self.s = Supplier()

    def test_grab_product_page_success(self) -> None:
        """
        Тест проверяет успешное извлечение данных со страницы продукта, когда все необходимые данные присутствуют.
        """
        self.s.grab_product_page = lambda _: {'id': '123', 'price': 19.99, 'name': 'Product Name'}
        result: bool = grab_product_page(self.s)
        self.assertTrue(result)
        self.assertEqual(len(self.s.p), 1)
        self.assertEqual(self.s.p[0]['id'], '123')
        self.assertEqual(self.s.p[0]['price'], 19.99)
        self.assertEqual(self.s.p[0]['name'], 'Product Name')

    def test_grab_product_page_failure(self) -> None:
        """
        Тест проверяет ситуацию, когда не удается извлечь данные со страницы продукта из-за отсутствия необходимых данных.
        """
        self.s.grab_product_page = lambda _: {'name': 'Product Name'}
        result: bool = grab_product_page(self.s)
        self.assertFalse(result)
        self.assertEqual(len(self.s.p), 0)


class TestRunScenario(unittest.TestCase):
    """
    Класс для тестирования функции run_scenario, которая запускает отдельный сценарий.
    """

    def setUp(self) -> None:
        """
        Метод для настройки тестового окружения перед каждым тестом.
        """
        self.supplier = Supplier()
        self.supplier.settings['parcing method [webdriver|api]'] = 'webdriver'
        self.supplier.current_scenario_filename: str = 'test_scenario.json'
        self.supplier.export_file_name: str = 'test_export'
        self.supplier.dir_export_imagesECTORY_FOR_STORE: str = '/test/path'
        self.supplier.p: List[Dict[str, Any]] = []

    def tearDown(self) -> None:
        """
        Метод для очистки тестового окружения после каждого теста.
        """
        ...

    def test_run_scenario_no_url(self) -> None:
        """
        Тест проверяет, что сценарий не запускается, если отсутствует URL.
        """
        scenario: Dict[str, Optional[str]] = {'name': 'scenario1', 'url': None}
        self.supplier.scenarios: Dict[str, Dict[str, Optional[str]]] = {'scenario1': scenario}
        self.supplier.get_list_products_in_category = MagicMock(return_value=[])
        self.assertFalse(self.supplier.run_scenario(scenario))

    def test_run_scenario_valid_url(self) -> None:
        """
        Тест проверяет успешный запуск сценария с валидным URL.
        """
        scenario: Dict[str, Optional[str]] = {'name': 'scenario2', 'url': 'https://example.com/products'}
        self.supplier.scenarios: Dict[str, Dict[str, Optional[str]]] = {'scenario2': scenario}
        self.supplier.get_list_products_in_category = MagicMock(return_value=['https://example.com/products/1', 'https://example.com/products/2'])
        self.supplier.grab_product_page = MagicMock(return_value=True)
        self.supplier.export_files = MagicMock()
        self.assertTrue(self.supplier.run_scenario(scenario))
        self.assertEqual(len(self.supplier.p), 2)
        self.supplier.export_files.assert_called_once_with(self.supplier, self.supplier.p, 'test_export-1', ['csv'])

    def test_run_scenario_export_empty_list(self) -> None:
        """
        Тест проверяет ситуацию, когда список продуктов пуст и экспорт не производится.
        """
        scenario: Dict[str, Optional[str]] = {'name': 'scenario3', 'url': 'https://example.com/products'}
        self.supplier.scenarios: Dict[str, Dict[str, Optional[str]]] = {'scenario3': scenario}
        self.supplier.get_list_products_in_category = MagicMock(return_value=['https://example.com/products/1'])
        self.supplier.grab_product_page = MagicMock(return_value=False)
        self.supplier.export_files = MagicMock()
        self.assertFalse(self.supplier.run_scenario(scenario))
        self.assertEqual(len(self.supplier.p), 0)
        self.supplier.export_files.assert_not_called()


if __name__ == '__main__':
    unittest.main()