### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой набор тестов для класса `Supplier`, который отвечает за взаимодействие с различными поставщиками товаров. Тесты проверяют инициализацию класса, загрузку настроек поставщика, запуск сценариев и обработку различных ситуаций, таких как успешная и неуспешная загрузка данных, выполнение сценариев с и без авторизации.

Шаги выполнения
-------------------------
1. **Инициализация тестового класса**:
   - Создается класс `TestSupplier`, который наследуется от `unittest.TestCase`.
   - В методе `setUp` инициализируются параметры, необходимые для тестов, такие как префикс поставщика, язык, метод сбора данных, настройки поставщика, локаторы элементов и файлы настроек.

2. **Тестирование инициализации класса `Supplier` с методом `webdriver`**:
   - Используется декоратор `@patch` для имитации функций `j_loads` и `Driver`.
   - Создается экземпляр класса `Supplier` с методом сбора данных `web`.
   - Проверяются атрибуты экземпляра класса на соответствие ожидаемым значениям из настроек поставщика.
   - Проверяется, что функции `j_loads` и `Driver` были вызваны с ожидаемыми аргументами.

3. **Тестирование инициализации класса `Supplier` с методом `api`**:
   - Аналогично предыдущему тесту, но с методом сбора данных `api`.
   - Проверяются атрибуты экземпляра класса на соответствие ожидаемым значениям из настроек поставщика.
   - Проверяется, что функция `j_loads` была вызвана с ожидаемыми аргументами.

4. **Тестирование загрузки настроек поставщика при успешной загрузке**:
   - Создается экземпляр класса `Supplier` с префиксом `'dummy'`.
   - Проверяются атрибуты экземпляра класса на соответствие значениям по умолчанию.

5. **Тестирование загрузки настроек поставщика при неудачной загрузке**:
   - Создается экземпляр класса `Supplier` с префиксом `'nonexistent'`.
   - Проверяются атрибуты экземпляра класса на соответствие значениям `None` или пустой строке.

6. **Тестирование загрузки настроек**:
   - Проверяются атрибуты экземпляра класса на соответствие значениям из настроек.

7. **Тестирование загрузки настроек при неверном пути к файлу**:
   - Вызывается метод `_load_settings` и проверяется, что в логах есть сообщение об ошибке чтения файла настроек.

8. **Тестирование загрузки настроек при неверном пути к файлу локаторов**:
   - Устанавливается метод сбора данных `api`, вызывается метод `_load_settings` и проверяется, что в логах есть сообщение об ошибке чтения файла локаторов.

9. **Тестирование загрузки настроек для `api`**:
   - Устанавливается метод сбора данных `api` и проверяется, что атрибуты `locators` и `driver` равны `None`.

10. **Тестирование загрузки связанных функций**:
    - Проверяется наличие атрибута `related_modules` и наличие в нем функции `example_function`.

11. **Тестирование инициализации**:
    - Проверяется, что атрибут `driver` не равен `None`, а атрибуты `p` и `c` являются списками.

12. **Тестирование успешной загрузки настроек**:
    - Используется `patch` для имитации успешного открытия и чтения файла настроек.
    - Вызывается метод `_load_settings` и проверяется, что он возвращает `True` и атрибут `supplier_id` установлен в ожидаемое значение.

13. **Тестирование неудачной загрузки настроек**:
    - Используется `patch` для имитации исключения при открытии файла настроек.
    - Вызывается метод `_load_settings` и проверяется, что он возвращает `False`.

14. **Тестирование запуска `api`**:
    - Используется `patch` для имитации успешного импорта модуля и выполнения функции `run_api`.
    - Вызывается метод `run` и проверяется, что он возвращает `True`.

15. **Тестирование успешного запуска файлов сценариев**:
    - Используется `patch` для имитации успешной авторизации.
    - Вызывается метод `run_scenario_files` с путем к файлу сценария и проверяется, что он возвращает `True`.

16. **Тестирование неудачного запуска файлов сценариев**:
    - Используется `patch` для имитации успешной авторизации.
    - Вызывается метод `run_scenario_files` с путем к неверному файлу сценария и проверяется, что он возвращает `False`.

17. **Тестирование запуска с авторизацией**:
    - Используется `patch` для имитации успешной авторизации.
    - Вызывается метод `run` и проверяется, что метод `login` был вызван и метод `run` возвращает `True`.

18. **Тестирование запуска без авторизации**:
    - Устанавливается атрибут `if_login` в `False`.
    - Используется `patch` для имитации успешного выполнения файлов сценариев.
    - Вызывается метод `run` и проверяется, что метод `run_scenario_files` не был вызван и метод `run` возвращает `True`.

Пример использования
-------------------------

```python
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from mymodule.supplier import Supplier

class TestSupplier(unittest.TestCase):

    def setUp(self):
        self.supplier_prefix = 'test_supplier'
        self.lang = 'en'
        self.method = 'web'
        self.supplier_settings = {
            'supplier_id': '123',
            'price_rule': '*1.2',
            'if_login': True,
            'login_url': 'http://example.com/login',
            'start_url': 'http://example.com/start',
            'parcing method [webdriver|api]': 'webdriver',
            'scenarios': [
                {'name': 'scenario1', 'file': 'scenario1.json'},
                {'name': 'scenario2', 'file': 'scenario2.json'},
            ]
        }
        self.locators = {
            'search_box': {'xpath': '//*[@id="search-box"]'},
            'search_button': {'xpath': '//*[@id="search-button"]'},
            'product_name': {'xpath': '//*[@id="product-name"]'},
            'product_price': {'xpath': '//*[@id="product-price"]'},
        }
        self.supplier = Supplier('example_supplier')
        self.settings_file = Path(__file__).parent / 'data/example_supplier/example_supplier.json'
        self.locators_file = Path(__file__).parent / 'data/example_supplier/locators.json'

    @patch('mymodule.supplier.gs.j_loads')
    @patch('mymodule.supplier.Driver')
    def test_init_webdriver(self, mock_driver, mock_j_loads):
        mock_j_loads.return_value = self.supplier_settings
        mock_driver.return_value = MagicMock()
        supplier = Supplier(self.supplier_prefix, self.lang, self.method)
        self.assertEqual(supplier.supplier_prefix, self.supplier_prefix)
        self.assertEqual(supplier.lang, self.lang)
        self.assertEqual(supplier.scrapping_method, self.method)
        self.assertEqual(supplier.supplier_id, self.supplier_settings['supplier_id'])
        self.assertEqual(supplier.price_rule, self.supplier_settings['price_rule'])
        self.assertEqual(supplier.login_data['if_login'], self.supplier_settings['if_login'])
        self.assertEqual(supplier.login_data['login_url'], self.supplier_settings['login_url'])
        self.assertEqual(supplier.start_url, self.supplier_settings['start_url'])
        self.assertEqual(supplier.scenarios, self.supplier_settings['scenarios'])
        mock_j_loads.assert_called_once_with(Path('suppliers', self.supplier_prefix, f'{self.supplier_prefix}.json'))
        mock_driver.assert_called_once()