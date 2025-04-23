### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для настройки и управления параметрами тестирования в проекте `hypotez` с использованием `pytest`. Он позволяет управлять использованием кэша API, обновлением кэша и запуском примеров в процессе тестирования. Глобальные параметры тестирования настраиваются через аргументы командной строки pytest.

Шаги выполнения
-------------------------
1. **Определение глобальных переменных**:
   - Объявляются глобальные переменные `refresh_cache`, `use_cache` и `test_examples` для хранения настроек тестирования.

2. **Регистрация аргументов командной строки**:
   - Функция `pytest_addoption(parser)` добавляет аргументы командной строки:
     - `--refresh_cache`: указывает, следует ли обновлять кэш API для тестов.
     - `--use_cache`: указывает, следует ли использовать кэш API для тестов.
     - `--test_examples`: указывает, следует ли перезапускать все примеры для проверки их работоспособности.

3. **Обработка аргументов командной строки**:
   - Функция `pytest_generate_tests(metafunc)` извлекает значения аргументов командной строки, переданных при запуске `pytest`:
     - Обновляет значения глобальных переменных `refresh_cache`, `use_cache` и `test_examples` на основе аргументов командной строки.

4. **Вывод информации о настройках теста**:
   - Внутри `pytest_generate_tests(metafunc)` выводится информация о текущих настройках теста, включая название теста, использование кэша, обновление кэша и запуск примеров.

Пример использования
-------------------------

```python
# conftest.py
refresh_cache = False
use_cache = False
test_examples = False

def pytest_addoption(parser):
    parser.addoption("--refresh_cache", action="store_true", help="Refreshes the API cache for the tests.")
    parser.addoption("--use_cache", action="store_true", help="Uses the API cache for the tests.")
    parser.addoption("--test_examples", action="store_true", help="Reruns all examples to make sure they still work.")

def pytest_generate_tests(metafunc):
    global refresh_cache, use_cache, test_examples
    refresh_cache = metafunc.config.getoption("refresh_cache")
    use_cache = metafunc.config.getoption("use_cache")
    test_examples = metafunc.config.getoption("test_examples")

    test_case_name = metafunc.function.__name__

    print(f"Test case: {test_case_name}")
    print(f"  - refresh_cache: {refresh_cache}")
    print(f"  - use_cache: {use_cache}")
    print(f"  - test_examples: {test_examples}")
    print("")
```

Для запуска тестов с определенными параметрами используйте команду `pytest` с соответствующими аргументами:

```bash
pytest --refresh_cache --use_cache --test_examples
```

Этот пример покажет, как можно управлять параметрами тестирования через командную строку, что позволяет гибко настраивать тесты в зависимости от потребностей.