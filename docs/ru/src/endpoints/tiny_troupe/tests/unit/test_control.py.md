# Модуль тестирования control.py

## Обзор

Этот модуль содержит юнит-тесты для проверки функциональности модуля `control.py` в проекте `tinytroupe`. Он проверяет основные функции управления симуляциями, такие как запуск, создание контрольных точек и завершение симуляций с использованием различных подходов: с агентами, с виртуальным миром и с фабрикой персонажей.

## Подробней

Модуль содержит тесты, которые проверяют сохранение и восстановление состояния симуляции с использованием механизма кэширования. Эти тесты охватывают различные сценарии использования, включая симуляции с агентами (`TinyPerson`), виртуальными мирами (`TinyWorld`) и фабрикой персонажей (`TinyPersonFactory`). Проверяется корректность сохранения и восстановления состояния, а также повторное использование кэшированных данных для ускорения выполнения симуляций.

## Функции

### `test_begin_checkpoint_end_with_agent_only`

**Назначение**: Проверяет запуск, создание контрольной точки и завершение симуляции только с агентами.

**Параметры**:

- `setup`: Фикстура pytest, предоставляющая окружение для тестирования.

**Возвращает**:

- `None`

**Вызывает исключения**:

- Отсутствуют

**Как работает функция**:

1.  Удаляет существующий файл кэша, если он есть.
2.  Вызывает `control.reset()` для сброса состояния симуляции.
3.  Проверяет, что нет запущенных симуляций.
4.  Вызывает `control.begin()` для запуска симуляции.
5.  Создает экземпляры `ArtifactExporter` и `TinyEnricher`.
6.  Создает агентов `agent_1` (Oscar) и `agent_2` (Lisa) с использованием функций `create_oscar_the_architect()` и `create_lisa_the_data_scientist()`.
7.  Добавляет агентам факультеты для использования инструментов.
8.  Определяет атрибуты агентов (возраст, национальность).
9.  Проверяет, что кэш трассировки и трассировка выполнения не пусты.
10. Вызывает `control.checkpoint()` для создания контрольной точки.
11. Агенты выполняют действия (`listen_and_act`).
12. Проверяет, что файл кэша был создан.
13. Вызывает `control.end()` для завершения симуляции.
14. Проверяет, что статус симуляции изменен на `STATUS_STOPPED`.

**Примеры**:

```python
# Пример вызова:
test_begin_checkpoint_end_with_agent_only(setup)
```

### `test_begin_checkpoint_end_with_world`

**Назначение**: Проверяет запуск, создание контрольной точки и завершение симуляции с использованием виртуального мира.

**Параметры**:

- `setup`: Фикстура pytest, предоставляющая окружение для тестирования.

**Возвращает**:

- `None`

**Вызывает исключения**:

- Отсутствуют

**Как работает функция**:

1.  Удаляет существующий файл кэша, если он есть.
2.  Вызывает `control.reset()` для сброса состояния симуляции.
3.  Проверяет, что нет запущенных симуляций.
4.  Вызывает `control.begin()` для запуска симуляции.
5.  Создает виртуальный мир `TinyWorld` с агентами.
6.  Делает всех агентов доступными друг для друга.
7.  Проверяет, что кэш трассировки и трассировка выполнения не пусты.
8.  Запускает симуляцию мира на 2 шага (`world.run(2)`).
9.  Вызывает `control.checkpoint()` для создания контрольной точки.
10. Проверяет, что файл кэша был создан.
11. Вызывает `control.end()` для завершения симуляции.
12. Проверяет, что статус симуляции изменен на `STATUS_STOPPED`.

**Примеры**:

```python
# Пример вызова:
test_begin_checkpoint_end_with_world(setup)
```

### `test_begin_checkpoint_end_with_factory`

**Назначение**: Проверяет запуск, создание контрольной точки и завершение симуляции с использованием фабрики персонажей.

**Параметры**:

- `setup`: Фикстура pytest, предоставляющая окружение для тестирования.

**Возвращает**:

- `None`

**Вызывает исключения**:

- Отсутствуют

**Внутренние функции**:

#### `aux_simulation_to_repeat`

**Назначение**: Внутренняя функция для повторения шагов симуляции.

**Параметры**:

- `iteration` (int): Номер итерации.
- `verbose` (bool, optional): Флаг для включения подробного логирования. По умолчанию `False`.

**Возвращает**:

- `agent` (TinyPerson): Сгенерированный агент.

**Вызывает исключения**:

- Отсутствуют

**Как работает функция**:

1.  Вызывает `control.reset()` для сброса состояния симуляции.
2.  Проверяет, что нет запущенных симуляций.
3.  Вызывает `control.begin()` для запуска симуляции.
4.  Создает фабрику персонажей `TinyPersonFactory`.
5.  Проверяет, что кэш трассировки и трассировка выполнения не пусты.
6.  Генерирует персонажа с использованием фабрики.
7.  Вызывает `control.checkpoint()` для создания контрольной точки.
8.  Проверяет, что файл кэша был создан.
9.  Вызывает `control.end()` для завершения симуляции.
10. Проверяет, что статус симуляции изменен на `STATUS_STOPPED`.
11. Если `verbose` установлен в `True`, логирует информацию об итерации и конфигурации персонажа.

**Примеры**:

```python
# Пример вызова:
agent = aux_simulation_to_repeat(1, verbose=True)
```

**Как работает функция `test_begin_checkpoint_end_with_factory`**:

1.  Удаляет существующий файл кэша, если он есть.
2.  Вызывает `control.reset()` для сброса состояния симуляции.
3.  Определяет вспомогательную функцию `aux_simulation_to_repeat`.
4.  Проверяет отсутствие промахов и попаданий в кэш.
5.  Выполняет первую симуляцию с помощью `aux_simulation_to_repeat`.
6.  Извлекает атрибуты агента (возраст, национальность, мини-биографию).
7.  Выполняет вторую симуляцию с помощью `aux_simulation_to_repeat`.
8.  Извлекает атрибуты агента.
9.  Проверяет, что промахов в кэш по-прежнему нет, а попадания в кэш есть.
10. Проверяет, что атрибуты агентов одинаковы в обеих симуляциях.
11. Проверяет содержимое файла кэша на наличие определенных вызовов методов.

**Примеры**:

```python
# Пример вызова:
test_begin_checkpoint_end_with_factory(setup)
```