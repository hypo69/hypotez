## Как использовать этот блок кода
=========================================================================================

### Описание
-------------------------
Этот блок кода демонстрирует два основных сценария работы с агентом TinyTroupe. 

1. **`test_basic_scenario_1`** - Базовая проверка взаимодействия агента с контроллером.
2. **`test_tool_usage_1`** - Проверка использования агентом инструмента `TinyWordProcessor`.

### Шаги выполнения
-------------------------
**`test_basic_scenario_1`:**

1. **Сброс контроллера:** `control.reset()` - сброс состояния контроллера к начальному.
2. **Проверка отсутствия симуляции:** `assert control._current_simulations["default"] is None` - проверяется, что в данный момент никакая симуляция не запущена.
3. **Начало симуляции:** `control.begin()` - запускается симуляция.
4. **Проверка начала симуляции:** `assert control._current_simulations["default"].status == Simulation.STATUS_STARTED` - проверяется, что симуляция успешно запущена.
5. **Создание агента:** `agent = create_oscar_the_architect()` - создается агент с предопределенными свойствами.
6. **Определение свойств агента:** `agent.define("age", 19)` и `agent.define("nationality", "Brazilian")` - устанавливаются свойства агента.
7. **Проверка наличия следов выполнения:**  `assert control._current_simulations["default"].cached_trace is not None` и `assert control._current_simulations["default"].execution_trace is not None` - проверяется, что в контроллере зарегистрированы действия агента.
8. **Создание точки сохранения:** `control.checkpoint()` - создается точка сохранения состояния симуляции.
9. **Взаимодействие агента с окружающей средой:** `agent.listen_and_act("How are you doing??")` - агент реагирует на вводную фразу.
10. **Определение нового свойства:** `agent.define("occupation", "Engineer")` - устанавливается новое свойство агента.
11. **Создание точки сохранения:** `control.checkpoint()` - создается вторая точка сохранения состояния симуляции.
12. **Окончание симуляции:** `control.end()` - завершает симуляцию.


**`test_tool_usage_1`:**

1. **Создание экспортера:** `exporter = ArtifactExporter(base_output_folder=data_export_folder)` - создается экспортер для записи результатов работы агента.
2. **Создание обогатителя:** `enricher = TinyEnricher()` - создается обогатитель, который дополняет информацию об агенте.
3. **Создание объекта использования инструмента:** `tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])` - создается объект, представляющий способность агента использовать инструмент `TinyWordProcessor`. 
4. **Создание агента:** `lisa = create_lisa_the_data_scientist()` - создается агент с предопределенными свойствами.
5. **Добавление способности использовать инструмент:** `lisa.add_mental_faculties([tooluse_faculty])` - агент получает возможность использовать `TinyWordProcessor`.
6. **Взаимодействие агента с окружающей средой:** `actions = lisa.listen_and_act(...)` - агент получает задание и выполняет его, используя инструмент.
7. **Проверка наличия действий:** `assert contains_action_type(actions, "WRITE_DOCUMENT")` - проверяется, что агент выполнил нужное действие.
8. **Проверка создания файла:** `assert os.path.exists(...)` - проверяется, что файл с результатами работы агента был создан. 


### Пример использования
-------------------------

```python
from tinytroupe.control import Simulation, control
from tinytroupe.examples import create_oscar_the_architect

def run_simulation():
    control.reset()
    control.begin()
    agent = create_oscar_the_architect()
    agent.define("age", 19)
    agent.define("nationality", "Brazilian")
    control.checkpoint()
    agent.listen_and_act("How are you doing??")
    control.end()

run_simulation()
```