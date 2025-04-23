### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Класс `TinyFactory` представляет собой базовый класс для различных типов фабрик, упрощающий расширение системы, особенно в отношении кэширования транзакций. Он предоставляет механизмы для управления и кэширования фабрик, а также методы для кодирования и декодирования состояния фабрики.

Шаги выполнения
-------------------------
1. **Инициализация фабрики**:
   - При создании экземпляра `TinyFactory` генерируется уникальное имя для фабрики и присваивается идентификатор симуляции (если указан).
   - Функция `TinyFactory.add_factory(self)` добавляет созданную фабрику в глобальный список всех фабрик `TinyFactory.all_factories`.
2. **Управление фабриками**:
   - Метод `set_simulation_for_free_factories(simulation)` позволяет привязать "свободные" фабрики (без указанного `simulation_id`) к определенной симуляции.
   - Метод `clear_factories()` очищает глобальный список фабрик, удаляя все зарегистрированные фабрики.
3. **Кэширование состояния фабрики**:
   - Метод `encode_complete_state()` кодирует полное состояние фабрики в словарь для кэширования или сериализации. Подклассы могут переопределять этот метод, если содержат несериализуемые элементы.
   - Метод `decode_complete_state(state: dict)` декодирует состояние фабрики из словаря, восстанавливая состояние объекта.

Пример использования
-------------------------

```python
import copy

from tinytroupe.factory import logger
import tinytroupe.utils as utils

class TinyFactory:
    """
    A base class for various types of factories. This is important because it makes it easier to extend the system, particularly 
    regarding transaction caching.
    """

    # A dict of all factories created so far.
    all_factories = {} # name -> factories
    
    def __init__(self, simulation_id:str=None) -> None:
        """
        Initialize a TinyFactory instance.

        Args:
            simulation_id (str, optional): The ID of the simulation. Defaults to None.
        """
        self.name = f"Factory {utils.fresh_id()}" # we need a name, but no point in making it customizable
        self.simulation_id = simulation_id

        TinyFactory.add_factory(self)
    
    def __repr__(self):
        return f"TinyFactory(name=\'{self.name}\')"
    
    @staticmethod
    def set_simulation_for_free_factories(simulation):
        """
        Sets the simulation if it is None. This allows free environments to be captured by specific simulation scopes
        if desired.
        """
        for factory in TinyFactory.all_factories.values():
            if factory.simulation_id is None:
                simulation.add_factory(factory)

    @staticmethod
    def add_factory(factory):
        """
        Adds a factory to the list of all factories. Factory names must be unique,\n
        so if an factory with the same name already exists, an error is raised.
        """
        if factory.name in TinyFactory.all_factories:
            raise ValueError(f"Factory names must be unique, but \'{factory.name}\' is already defined.")
        else:
            TinyFactory.all_factories[factory.name] = factory
    
    @staticmethod
    def clear_factories():
        """
        Clears the global list of all factories.
        """
        TinyFactory.all_factories = {}

    ################################################################################################
    # Caching mechanisms
    #
    # Factories can also be cached in a transactional way. This is necessary because the agents they
    # generate can be cached, and we need to ensure that the factory itself is also cached in a 
    # consistent way.
    ################################################################################################

    def encode_complete_state(self) -> dict:
        """
        Encodes the complete state of the factory. If subclasses have elmements that are not serializable, they should override this method.
        """

        state = copy.deepcopy(self.__dict__)
        return state

    def decode_complete_state(self, state:dict):
        """
        Decodes the complete state of the factory. If subclasses have elmements that are not serializable, they should override this method.
        """
        state = copy.deepcopy(state)

        self.__dict__.update(state)
        return self
 
# Пример использования
factory1 = TinyFactory(simulation_id="sim1")
print(factory1)

factory_state = factory1.encode_complete_state()
print(f"Encoded state: {factory_state}")

factory2 = TinyFactory()
factory2.decode_complete_state(factory_state)
print(factory2)