## Как использовать TinyFactory
=========================================================================================

Описание
-------------------------
Класс `TinyFactory`  является базовым классом для создания различных типов фабрик. Он предназначен для упрощения расширения системы, особенно в контексте транзакционного кеширования. Класс хранит все созданные фабрики в статическом атрибуте `all_factories`.

Шаги выполнения
-------------------------
1. **Создание экземпляра TinyFactory**:
   - Вызовите конструктор `TinyFactory`, передавая в него опциональный параметр `simulation_id`. 
   - Экземпляр автоматически добавляется в список `all_factories` с уникальным именем.
2. **Использование фабрики**:
   - Создайте подкласс `TinyFactory` и переопределите методы `encode_complete_state` и `decode_complete_state` для сериализации и десериализации состояния фабрики.
   - Используйте методы класса `TinyFactory` для управления фабриками:
      - `set_simulation_for_free_factories(simulation)` - задает симуляцию для фабрик, у которых `simulation_id` не определен.
      - `add_factory(factory)` - добавляет фабрику в список `all_factories`.
      - `clear_factories()` - очищает глобальный список фабрик.

Пример использования
-------------------------

```python
from tinytroupe.factory import TinyFactory

# Создание фабрики с идентификатором симуляции
factory = TinyFactory(simulation_id="my_simulation")

# Проверка наличия фабрики в списке всех фабрик
print(f"Factory name: {factory.name}")
print(f"Factory in all_factories: {factory.name in TinyFactory.all_factories}")

# Очистка списка всех фабрик
TinyFactory.clear_factories()

# Проверка пустого списка фабрик
print(f"Factory in all_factories after clearing: {factory.name in TinyFactory.all_factories}")
```