### **Анализ кода модуля `test_execute_scenarios.py`**

**Качество кода:**

- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Наличие тестов для различных сценариев выполнения.
    - Использование `MagicMock` для изоляции тестируемого кода.
    - Проверка различных условий и результатов выполнения функций.
- **Минусы**:
    - Отсутствие docstring для классов и методов, что затрудняет понимание их предназначения.
    - Не все переменные аннотированы типами.
    - В коде используется `your_module`, что говорит о необходимости замены на актуальный модуль.
    -  Много повторений одного и того же кода (`s = MagicMock()`)
    -  Отсутствует логирование.
    -  Не везде используется `ex` при обработке исключений.
    -  Не используется `logger` для логирования ошибок и информации.

**Рекомендации по улучшению:**

1.  **Добавить docstring**:
    - Добавить docstring для всех классов и методов, чтобы описать их функциональность, параметры и возвращаемые значения.
2.  **Добавить аннотацию типов**:
    - Добавить аннотацию типов для всех переменных, чтобы улучшить читаемость и предотвратить ошибки.
3.  **Заменить `your_module`**:
    - Заменить `your_module` на актуальный модуль в тестах `TestRunScenarioFile`.
4.  **Улучшить обработку исключений**:
    - Использовать `ex` вместо `e` при обработке исключений.
    - Добавить логирование ошибок с использованием `logger` из `src.logger`.
5.  **Улучшить структуру и избежать повторений**:
    - Вынести общие части кода в отдельные методы или функции для уменьшения дублирования. Например, создание `MagicMock` можно вынести в отдельный метод.

**Оптимизированный код:**

```python
## \file /src/suppliers/_experiments/test_execute_scenarios.py
# -*- coding: utf-8 -*-

#! .pyenv/bin/python3

"""
Модуль содержит тесты для проверки выполнения различных сценариев.
====================================================================

Модуль включает в себя тесты для функций run_scenarios, run_scenario_file, run_scenario и grab_product_page.
Используются MagicMock для изоляции тестируемого кода и проверки различных условий выполнения функций.

Пример использования:
----------------------
>>> python -m unittest test_execute_scenarios.py
"""

import unittest
from unittest.mock import MagicMock, patch
from execute_scenarios import run_scenarios, run_scenario_file, run_scenario, grab_product_page
from src.logger import logger  # Добавлен импорт logger
from typing import List, Dict, Any


class TestRunListOfScenarioFiles(unittest.TestCase):
    """
    Тесты для функции run_scenarios, которая выполняет список файлов сценариев.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
        self.s = MagicMock()
        self.scenario_files: List[str] = ["scenario1.json", "scenario2.json"]
        self.s.settings: Dict[str, Any] = {
            'check categories on site': False,
            'scenarios': ["default1.json", "default2.json"]
        }

    def test_with_scenario_files_passed(self):
        """
        Тест с переданными файлами сценариев.
        """
        result: bool = run_scenarios(self.s, self.scenario_files)

        self.assertTrue(result)
        self.s.related_modules.build_shop_categories.assert_not_called()
        self.assertEqual(self.s.current_scenario_filename, "scenario2.json")
        self.assertEqual(self.s.settings['last_runned_scenario'], "scenario2.json")

    def test_with_no_scenario_files_passed(self):
        """
        Тест без переданных файлов сценариев.
        """
        self.s.settings['check categories on site'] = True

        result: bool = run_scenarios(self.s)

        self.assertTrue(result)
        self.s.related_modules.build_shop_categories.assert_called_once()
        self.assertEqual(self.s.current_scenario_filename, "default2.json")
        self.assertEqual(self.s.settings['last_runned_scenario'], "default2.json")


class TestRunScenarioFile(unittest.TestCase):
    """
    Тесты для функции run_scenario_file, которая выполняет сценарий из файла.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
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
                    # steps for scenario1
                ]
            },
            "scenario2": {
                "url": None,
                "steps": [
                    # steps for scenario2
                ]
            }
        }

    @patch("execute_scenarios.j_loads")
    @patch("execute_scenarios.run_scenario")
    def test_run_scenario_file_webdriver(self, mock_run_scenario: MagicMock, mock_j_loads: MagicMock):
        """
        Тест выполнения сценария из файла с использованием webdriver.
        """
        mock_j_loads.return_value = {"scenarios": self.s.scenarios}

        run_scenario_file(self.s, "test_scenario.json")

        mock_j_loads.assert_called_once_with("/path/to/scenarios/test_scenario.json")
        mock_run_scenario.assert_any_call(self.s, self.s.scenarios["scenario1"])
        mock_run_scenario.assert_not_called_with(self.s, self.s.scenarios["scenario2"])

    @patch("execute_scenarios.related_modules.run_scenario_file_via_api")
    def test_run_scenario_file_api(self, mock_run_scenario_file_via_api: MagicMock):
        """
        Тест выполнения сценария из файла с использованием API.
        """
        self.s.settings["parcing method [webdriver|api]"] = "api"

        run_scenario_file(self.s, "test_scenario.json")

        mock_run_scenario_file_via_api.assert_called_once_with(self.s, "test_scenario.json")

    @patch("execute_scenarios.j_loads")
    @patch("execute_scenarios.logger.error")
    def test_run_scenario_file_no_scenarios(self, mocklogger_console_error: MagicMock, mock_j_loads: MagicMock):
        """
        Тест выполнения сценария из файла, когда сценарии отсутствуют.
        """
        mock_j_loads.return_value = {"scenarios": None}

        self.assertFalse(run_scenario_file(self.s, "test_scenario.json"))

        mocklogger_console_error.assert_called_once_with("Возможно файл test_scenario.json не содержит сценариев")


class TestGrabProductPage(unittest.TestCase):
    """
    Тесты для функции grab_product_page, которая извлекает информацию о товаре.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
        self.s = MagicMock()  # Use MagicMock instead of Supplier
        self.s.p: List[Dict[str, Any]] = []  # Initialize p as an empty list

    def test_grab_product_page_successful(self):
        """
        Тест успешного извлечения информации о товаре.
        """
        self.s.grab_product_page = MagicMock(return_value={'id': '123', 'price': 19.99, 'name': 'Product Name'})

        result: bool = grab_product_page(self.s)

        self.assertTrue(result)
        self.assertEqual(len(self.s.p), 1)
        self.assertEqual(self.s.p[0]['id'], '123')
        self.assertEqual(self.s.p[0]['price'], 19.99)
        self.assertEqual(self.s.p[0]['name'], 'Product Name')

    def test_grab_product_page_failure(self):
        """
        Тест неудачного извлечения информации о товаре (отсутствуют необходимые данные).
        """
        self.s.grab_product_page = MagicMock(return_value={'name': 'Product Name'})

        result: bool = grab_product_page(self.s)

        self.assertFalse(result)
        self.assertEqual(len(self.s.p), 0)


class TestRunScenario(unittest.TestCase):
    """
    Тесты для функции run_scenario, которая выполняет сценарий.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
        self.supplier = MagicMock()  # Use MagicMock instead of Supplier
        self.supplier.settings: Dict[str, Any] = {'parcing method [webdriver|api]': 'webdriver'}
        self.supplier.current_scenario_filename: str = 'test_scenario.json'
        self.supplier.export_file_name: str = 'test_export'
        self.supplier.dir_export_imagesECTORY_FOR_STORE: str = '/test/path'
        self.supplier.p: List[Dict[str, Any]] = []
        self.supplier.export_files = MagicMock()  # Mock export_files

    def tearDown(self):
        """
        Завершение после каждого теста.
        """
        ...

    def test_run_scenario_no_url(self):
        """
        Тест выполнения сценария без URL.
        """
        scenario: Dict[str, Any] = {'name': 'scenario1', 'url': None}
        self.supplier.scenarios: Dict[str, Any] = {'scenario1': scenario}
        self.supplier.get_list_products_in_category = MagicMock(return_value=[])

        self.assertFalse(run_scenario(self.supplier, scenario))  # Call run_scenario instead of self.supplier.run_scenario

    def test_run_scenario_valid_url(self):
        """
        Тест выполнения сценария с валидным URL.
        """
        scenario: Dict[str, Any] = {'name': 'scenario2', 'url': 'https://example.com/products'}
        self.supplier.scenarios: Dict[str, Any] = {'scenario2': scenario}
        self.supplier.get_list_products_in_category = MagicMock(return_value=['https://example.com/products/1', 'https://example.com/products/2'])
        self.supplier.grab_product_page = MagicMock(return_value=True)

        self.assertTrue(run_scenario(self.supplier, scenario))  # Call run_scenario instead of self.supplier.run_scenario
        self.assertEqual(len(self.supplier.p), 2)
        self.supplier.export_files.assert_called_once_with(self.supplier, self.supplier.p, 'test_export-1', ['csv'])

    def test_run_scenario_export_empty_list(self):
        """
        Тест выполнения сценария с пустым списком для экспорта.
        """
        scenario: Dict[str, Any] = {'name': 'scenario3', 'url': 'https://example.com/products'}
        self.supplier.scenarios: Dict[str, Any] = {'scenario3': scenario}
        self.supplier.get_list_products_in_category = MagicMock(return_value=['https://example.com/products/1'])
        self.supplier.grab_product_page = MagicMock(return_value=False)

        self.assertFalse(run_scenario(self.supplier, scenario))  # Call run_scenario instead of self.supplier.run_scenario
        self.assertEqual(len(self.supplier.p), 0)
        self.supplier.export_files.assert_not_called()


if __name__ == '__main__':
    unittest.main()