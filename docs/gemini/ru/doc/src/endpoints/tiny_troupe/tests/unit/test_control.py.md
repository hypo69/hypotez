# Модуль тестирования `test_control.py`

## Обзор

Модуль `test_control.py` содержит набор юнит-тестов для проверки функциональности модуля `tinytroupe.control`. Он проверяет правильность работы симуляций с агентами, мирами и фабриками персонажей, а также механизмы сохранения и восстановления состояния симуляций через checkpoint.

## Подробнее

Модуль `test_control.py` использует библиотеку `pytest` для организации и запуска тестов. Он включает тесты для проверки начала, checkpoint и завершения симуляций, а также для проверки работы с агентами, мирами и фабриками персонажей. Тесты проверяют, что состояние симуляции сохраняется и восстанавливается правильно, и что кэширование работает как ожидается.

## Классы

В этом модуле нет классов.

## Функции

### `test_begin_checkpoint_end_with_agent_only`

```python
def test_begin_checkpoint_end_with_agent_only(setup):
    """Тестирует начало, checkpoint и завершение симуляции только с агентами.

    Args:
        setup: Фикстура pytest для настройки тестовой среды.

    Raises:
        AssertionError: Если состояние симуляции не соответствует ожидаемому.
    """
    # Стираем файл, если он существует
    remove_file_if_exists("control_test.cache.json")

    control.reset()
    
    assert control._current_simulations["default"] is None, "В этот момент не должно быть запущенных симуляций."

    # Стираем файл, если он существует
    remove_file_if_exists("control_test.cache.json")

    control.begin("control_test.cache.json")
    assert control._current_simulations["default"].status == Simulation.STATUS_STARTED, "Симуляция должна быть запущена в этот момент."

    exporter = ArtifactExporter(base_output_folder="./synthetic_data_exports_3/")
    enricher = TinyEnricher()
    tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])

    agent_1 = create_oscar_the_architect()
    agent_1.add_mental_faculties([tooluse_faculty])
    agent_1.define("age", 19)
    agent_1.define("nationality", "Brazilian")

    agent_2 = create_lisa_the_data_scientist()
    agent_2.add_mental_faculties([tooluse_faculty])
    agent_2.define("age", 80)
    agent_2.define("nationality", "Argentinian")

    assert control._current_simulations["default"].cached_trace is not None, "В этот момент должен быть кэшированный trace."
    assert control._current_simulations["default"].execution_trace is not None, "В этот момент должен быть execution trace."

    control.checkpoint()

    agent_1.listen_and_act("How are you doing?")
    agent_2.listen_and_act("What\'s up?")

    # Проверяем, был ли создан файл
    assert os.path.exists("control_test.cache.json"), "Файл checkpoint должен быть создан."

    control.end()

    assert control._current_simulations["default"].status == Simulation.STATUS_STOPPED, "Симуляция должна быть завершена в этот момент."
### Как работает функция:
1. **Подготовка тестовой среды**:
   - Удаляет файл кэша, если он существует, чтобы начать с чистого состояния.
   - Вызывает `control.reset()`, чтобы убедиться, что нет активных симуляций.
2. **Начало симуляции**:
   - Вызывает `control.begin()`, чтобы начать новую симуляцию с указанным файлом кэша.
   - Проверяет, что статус симуляции установлен в `Simulation.STATUS_STARTED`.
3. **Создание и настройка агентов**:
   - Создает два агента (`agent_1` и `agent_2`) с использованием функций `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
   - Добавляет каждому агенту ментальные способности (`tooluse_faculty`) и определяет их возраст и национальность.
4. **Checkpoint и взаимодействие агентов**:
   - Вызывает `control.checkpoint()`, чтобы сохранить состояние симуляции.
   - Агенты взаимодействуют, вызывая метод `listen_and_act()` с разными сообщениями.
5. **Завершение симуляции**:
   - Проверяет, был ли создан файл кэша (`control_test.cache.json`).
   - Вызывает `control.end()`, чтобы завершить симуляцию.
   - Проверяет, что статус симуляции установлен в `Simulation.STATUS_STOPPED`.
### Примеры:
```python
# Пример вызова функции:
test_begin_checkpoint_end_with_agent_only(setup)
```
### `test_begin_checkpoint_end_with_world`

```python
def test_begin_checkpoint_end_with_world(setup):
    """Тестирует начало, checkpoint и завершение симуляции с использованием TinyWorld.

    Args:
        setup: Фикстура pytest для настройки тестовой среды.

    Raises:
        AssertionError: Если состояние мира или симуляции не соответствует ожидаемому.
    """
    # Стираем файл, если он существует
    remove_file_if_exists("control_test_world.cache.json")

    control.reset()
    
    assert control._current_simulations["default"] is None, "В этот момент не должно быть запущенных симуляций."

    control.begin("control_test_world.cache.json")
    assert control._current_simulations["default"].status == Simulation.STATUS_STARTED, "Симуляция должна быть запущена в этот момент."

    world = TinyWorld("Test World", [create_oscar_the_architect(), create_lisa_the_data_scientist()])

    world.make_everyone_accessible()

    assert control._current_simulations["default"].cached_trace is not None, "В этот момент должен быть кэшированный trace."
    assert control._current_simulations["default"].execution_trace is not None, "В этот момент должен быть execution trace."

    world.run(2)

    control.checkpoint()

    # Проверяем, был ли создан файл
    assert os.path.exists("control_test_world.cache.json"), "Файл checkpoint должен быть создан."

    control.end()

    assert control._current_simulations["default"].status == Simulation.STATUS_STOPPED, "Симуляция должна быть завершена в этот момент."
```
### Как работает функция:
1. **Подготовка тестовой среды**:
   - Удаляет файл кэша, если он существует, чтобы начать с чистого состояния.
   - Вызывает `control.reset()`, чтобы убедиться, что нет активных симуляций.
2. **Начало симуляции**:
   - Вызывает `control.begin()`, чтобы начать новую симуляцию с указанным файлом кэша.
   - Проверяет, что статус симуляции установлен в `Simulation.STATUS_STARTED`.
3. **Создание и настройка мира**:
   - Создает экземпляр `TinyWorld` с двумя агентами (`create_oscar_the_architect()` и `create_lisa_the_data_scientist()`).
   - Делает всех агентов доступными друг для друга.
4. **Запуск мира и checkpoint**:
   - Запускает мир на 2 шага с помощью `world.run(2)`.
   - Вызывает `control.checkpoint()`, чтобы сохранить состояние симуляции.
5. **Завершение симуляции**:
   - Проверяет, был ли создан файл кэша (`control_test_world.cache.json`).
   - Вызывает `control.end()`, чтобы завершить симуляцию.
   - Проверяет, что статус симуляции установлен в `Simulation.STATUS_STOPPED`.
### Примеры:
```python
# Пример вызова функции:
test_begin_checkpoint_end_with_world(setup)
```
### `test_begin_checkpoint_end_with_factory`

```python
def test_begin_checkpoint_end_with_factory(setup):
    """Тестирует начало, checkpoint и завершение симуляции с использованием TinyPersonFactory.

    Args:
        setup: Фикстура pytest для настройки тестовой среды.

    Raises:
        AssertionError: Если состояние симуляции не соответствует ожидаемому или кэширование работает некорректно.
    """
    # Стираем файл, если он существует
    remove_file_if_exists("control_test_personfactory.cache.json")

    control.reset()

    def aux_simulation_to_repeat(iteration, verbose=False):
        """Внутренняя функция для повторения симуляции.

        Args:
            iteration (int): Номер итерации.
            verbose (bool, optional): Флаг для включения подробного логирования. По умолчанию False.

        Returns:
            TinyPerson: Сгенерированный агент.

        Raises:
            AssertionError: Если состояние симуляции не соответствует ожидаемому.
        """
        control.reset()
    
        assert control._current_simulations["default"] is None, "В этот момент не должно быть запущенных симуляций."

        control.begin("control_test_personfactory.cache.json")
        assert control._current_simulations["default"].status == Simulation.STATUS_STARTED, "Симуляция должна быть запущена в этот момент."    
        
        factory = TinyPersonFactory("We are interested in experts in the production of the traditional Gazpacho soup.")

        assert control._current_simulations["default"].cached_trace is not None, "В этот момент должен быть кэшированный trace."
        assert control._current_simulations["default"].execution_trace is not None, "В этот момент должен быть execution trace."

        agent = factory.generate_person("A Brazilian tourist who learned about Gazpaccho in a trip to Spain.")

        assert control._current_simulations["default"].cached_trace is not None, "В этот момент должен быть кэшированный trace."
        assert control._current_simulations["default"].execution_trace is not None, "В этот момент должен быть execution trace."

        control.checkpoint()

        # Проверяем, был ли создан файл
        assert os.path.exists("control_test_personfactory.cache.json"), "Файл checkpoint должен быть создан."

        control.end()
        assert control._current_simulations["default"].status == Simulation.STATUS_STOPPED, "Симуляция должна быть завершена в этот момент."

        if verbose:
            logger.debug(f"###################################################################################### Sim Iteration:{iteration}")
            logger.debug(f"###################################################################################### Agent persona configs:{agent._persona}")

        return agent

    assert control.cache_misses() == 0, "В этом тесте не должно быть промахов кэша."
    assert control.cache_hits() == 0, "Здесь не должно быть попаданий в кэш"

    # FIRST simulation ########################################################
    agent_1 = aux_simulation_to_repeat(1, verbose=True)
    age_1 = agent_1.get("age")
    nationality_1 = agent_1.get("nationality")
    minibio_1 = agent_1.minibio()
    print("minibio_1 =", minibio_1)


    # SECOND simulation ########################################################
    logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>> Second simulation...")
    agent_2 = aux_simulation_to_repeat(2, verbose=True)
    age_2 = agent_2.get("age")
    nationality_2 = agent_2.get("nationality")
    minibio_2 = agent_2.minibio()
    print("minibio_2 =", minibio_2)

    assert control.cache_misses() == 0, "В этом тесте не должно быть промахов кэша."
    assert control.cache_hits() > 0, "Здесь должны быть попадания в кэш."

    assert age_1 == age_2, "Возраст должен быть одинаковым в обеих симуляциях."
    assert nationality_1 == nationality_2, "Национальность должна быть одинаковой в обеих симуляциях."
    assert minibio_1 == minibio_2, "Мини-биография должна быть одинаковой в обеих симуляциях."

    #
    # let\'s also check the contents of the cache file, as raw text, not dict
    #
    with open("control_test_personfactory.cache.json", "r") as f:
        cache_contents = f.read()

    assert "\'_aux_model_call\'" in cache_contents, "Файл кэша должен содержать вызов \'_aux_model_call\'."
    assert "\'_setup_agent\'" in cache_contents, "Файл кэша должен содержать вызов \'_setup_agent\'."
    assert "\'define\'" not in cache_contents, "Файл кэша не должен содержать методы \'define\', так как они reentrant."
    assert "\'define_several\'" not in cache_contents, "Файл кэша не должен содержать методы \'define_several\', так как они reentrant."
```

### Внутренние функции

#### `aux_simulation_to_repeat`

```python
def aux_simulation_to_repeat(iteration, verbose=False):
    """Внутренняя функция для повторения симуляции.

    Args:
        iteration (int): Номер итерации.
        verbose (bool, optional): Флаг для включения подробного логирования. По умолчанию False.

    Returns:
        TinyPerson: Сгенерированный агент.

    Raises:
        AssertionError: Если состояние симуляции не соответствует ожидаемому.
    """
```

**Назначение**: Внутренняя функция `aux_simulation_to_repeat` используется для повторения симуляции с фабрикой персонажей.

**Параметры**:
   - `iteration` (int): Номер итерации симуляции. Используется для логирования и отладки.
   - `verbose` (bool, optional): Флаг, определяющий, нужно ли выводить подробную информацию о симуляции в лог. По умолчанию `False`.

**Возвращает**:
   - `TinyPerson`: Сгенерированный агент.

**Вызывает исключения**:
   - `AssertionError`: Если состояние симуляции не соответствует ожидаемому.

### Как работает функция:

1. **Подготовка симуляции**:
   - Вызывает `control.reset()` для сброса состояния симуляции.
   - Проверяет, что нет активных симуляций.
   - Вызывает `control.begin()` для начала новой симуляции с указанным файлом кэша.
   - Проверяет, что статус симуляции установлен в `Simulation.STATUS_STARTED`.
2. **Создание фабрики и агента**:
   - Создает экземпляр `TinyPersonFactory` для создания экспертов по приготовлению супа гаспачо.
   - Генерирует персонажа (`agent`) с помощью фабрики, указывая, что это бразильский турист, узнавший о гаспачо в Испании.
3. **Checkpoint и завершение симуляции**:
   - Вызывает `control.checkpoint()` для сохранения состояния симуляции.
   - Проверяет, был ли создан файл кэша.
   - Вызывает `control.end()` для завершения симуляции.
   - Проверяет, что статус симуляции установлен в `Simulation.STATUS_STOPPED`.
4. **Логирование (если `verbose=True`)**:
   - Выводит в лог номер итерации и конфигурацию персонажа (`agent._persona`).

### Как работает `test_begin_checkpoint_end_with_factory`:

1. **Подготовка тестовой среды**:
   - Удаляет файл кэша, если он существует.
   - Вызывает `control.reset()` для сброса состояния симуляции.
2. **Проверка начального состояния кэша**:
   - Утверждает, что `control.cache_misses()` и `control.cache_hits()` равны 0, чтобы убедиться, что кэш пуст.
3. **Первая симуляция**:
   - Вызывает `aux_simulation_to_repeat(1, verbose=True)` для запуска первой симуляции.
   - Извлекает возраст, национальность и мини-биографию агента.
4. **Вторая симуляция**:
   - Вызывает `aux_simulation_to_repeat(2, verbose=True)` для запуска второй симуляции.
   - Извлекает возраст, национальность и мини-биографию агента.
5. **Проверка кэша**:
   - Утверждает, что `control.cache_misses()` равен 0 (кэш не должен пропускать вызовы).
   - Утверждает, что `control.cache_hits()` больше 0 (должны быть попадания в кэш).
6. **Сравнение агентов**:
   - Утверждает, что возраст, национальность и мини-биография агентов из обеих симуляций одинаковы.
7. **Проверка содержимого файла кэша**:
   - Читает содержимое файла кэша как текст.
   - Утверждает, что файл кэша содержит вызовы `_aux_model_call` и `_setup_agent`, но не содержит методы `define` и `define_several`.

### Примеры:

```python
# Пример вызова test_begin_checkpoint_end_with_factory:
test_begin_checkpoint_end_with_factory(setup)
```

## Параметры

В этом модуле нет параметров, кроме тех, что передаются в функции.