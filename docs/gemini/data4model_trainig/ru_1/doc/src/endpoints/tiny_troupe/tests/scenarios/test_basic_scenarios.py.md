# Модуль тестирования базовых сценариев `test_basic_scenarios.py`

## Обзор

Модуль содержит набор тестов для проверки основных сценариев использования библиотеки `tinytroupe`. 
Включает тесты для инициализации и управления симуляциями, создания и настройки агентов, а также проверки использования инструментов агентами.

## Подробнее

Этот модуль предназначен для проверки корректности работы основных функций библиотеки `tinytroupe`.
Он проверяет, что симуляции правильно запускаются и останавливаются, агенты могут быть созданы и настроены,
и что агенты могут использовать инструменты для выполнения задач.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `test_basic_scenario_1`

```python
def test_basic_scenario_1():
    """
    Тестирует основной сценарий инициализации и управления симуляцией с агентом.

    Returns:
        None

    Raises:
        AssertionError: Если состояние симуляции или агента не соответствует ожидаемому.

    Как работает функция:
    - Сбрасывает состояние управления симуляцией.
    - Проверяет, что нет активных симуляций.
    - Запускает симуляцию и проверяет её статус.
    - Создает агента (архитектора Оскара).
    - Определяет атрибуты агента (возраст и национальность).
    - Проверяет наличие кэшированного и исполняемого трейса симуляции.
    - Создает чекпоинт симуляции.
    - Запрашивает у агента действие на основе входного сообщения.
    - Определяет атрибут агента (род занятий).
    - Создает чекпоинт симуляции.
    - Завершает симуляцию.
    """
```

### `test_tool_usage_1`

```python
def test_tool_usage_1():
    """
    Тестирует сценарий использования инструментов агентом для выполнения задачи.

    Returns:
        None

    Raises:
        AssertionError: Если действие агента не соответствует ожидаемому или файл не был создан.

    Как работает функция:
    - Определяет папку для экспорта данных.
    - Создает экземпляры `ArtifactExporter` и `TinyEnricher`.
    - Создает экземпляр `TinyToolUse` с инструментом `TinyWordProcessor`.
    - Создает агента (Лизу, специалиста по данным).
    - Добавляет агенту способность использовать инструменты.
    - Запрашивает у агента действие на основе задачи (написание резюме).
    - Проверяет, что в списке действий присутствует действие `WRITE_DOCUMENT`.
    - Проверяет, что документ был записан в файл.
    """
```
```python
    data_export_folder = f"{EXPORT_BASE_FOLDER}/test_tool_usage_1"
    # `data_export_folder`: Определяет путь к папке, куда будут экспортированы артефакты (документы), созданные в ходе выполнения теста.  Путь формируется на основе константы `EXPORT_BASE_FOLDER` и названия текущего теста.
    
    exporter = ArtifactExporter(base_output_folder=data_export_folder)
    # `exporter`: Создает экземпляр класса `ArtifactExporter`, который отвечает за экспорт артефактов (в данном случае, документов) в указанную папку.
    enricher = TinyEnricher()
    # `enricher`: Создает экземпляр класса `TinyEnricher`, который используется для обогащения данных (например, добавления метаданных к документам).

    tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])
    # `tooluse_faculty`: Создает экземпляр класса `TinyToolUse`, который предоставляет агенту возможность использовать инструменты. В данном случае, агенту предоставляется инструмент `TinyWordProcessor`, который используется для обработки текстовых документов. `TinyWordProcessor` принимает `exporter` и `enricher` для сохранения и обработки созданных документов.

    lisa = create_lisa_the_data_scientist()
    # `lisa`: Создает агента Лизу, специалиста по данным, с использованием функции `create_lisa_the_data_scientist`.
    
    lisa.add_mental_faculties([tooluse_faculty])
    # `lisa.add_mental_faculties`: Добавляет агенту Лизе способность использовать инструменты, предоставляемые `tooluse_faculty`. Это позволяет агенту выполнять действия, связанные с обработкой документов.

    actions = lisa.listen_and_act("""
                            You have just been fired and need to find a new job. You decide to think about what you 
                            want in life and then write a resume. The file must be titled **exactly** 'Resume'.
                            Don't stop until you actually write the resume.
                            """, return_actions=True)
    # `actions`:  Агент Лиза получает задачу (написание резюме после увольнения) через метод `lisa.listen_and_act`. Задача передается в виде текстового запроса. Параметр `return_actions=True` указывает, что метод должен вернуть список действий, которые агент выполнил для решения задачи.

    assert contains_action_type(actions, "WRITE_DOCUMENT"), "There should be a WRITE_DOCUMENT action in the actions list."
    # `assert contains_action_type(actions, "WRITE_DOCUMENT")`: Проверяет, что в списке действий, выполненных агентом, присутствует действие `WRITE_DOCUMENT`. Это гарантирует, что агент попытался написать документ в рамках решения задачи.

    # check that the document was written to a file
    assert os.path.exists(f"{data_export_folder}/Document/Resume.Lisa Carter.docx"), "The document should have been written to a file."
    # `assert os.path.exists(...)`: Проверяет, что файл с расширением `.docx` (Microsoft Word) был создан в указанной папке. Это подтверждает, что документ был успешно экспортирован.
    assert os.path.exists(f"{data_export_folder}/Document/Resume.Lisa Carter.json"), "The document should have been written to a file."
    # `assert os.path.exists(...)`: Проверяет, что файл с расширением `.json` был создан в указанной папке. Это подтверждает, что документ был успешно экспортирован в формате JSON.
    assert os.path.exists(f"{data_export_folder}/Document/Resume.Lisa Carter.md"), "The document should have been written to a file."
    # `assert os.path.exists(...)`: Проверяет, что файл с расширением `.md` (Markdown) был создан в указанной папке. Это подтверждает, что документ был успешно экспортирован в формате Markdown.
```

## Параметры класса

В данном модуле классы отсутствуют.