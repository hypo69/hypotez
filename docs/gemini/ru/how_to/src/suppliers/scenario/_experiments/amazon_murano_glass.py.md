## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода запускает сценарий  `Murano Glass` для поставщика `Amazon`. 

Шаги выполнения
-------------------------
1. Импортирует модуль `header`. 
2. Создает экземпляр класса `Supplier` с именем `s` для поставщика `Amazon`. 
3. Вызывает метод `run_scenario()` для запуска сценария `Murano Glass`, который находится в словаре `scenario` из модуля `dict_scenarios`.
4. Извлекает ключ первого элемента из словаря `default_category`, который находится в словаре `presta_categories` в текущем сценарии.

Пример использования
-------------------------

```python
from header import start_supplier
from dict_scenarios import scenario

# Создаем экземпляр класса Supplier для поставщика Amazon
s = start_supplier('amazon')

# Запускаем сценарий 'Murano Glass'
s.run_scenario(scenario['Murano Glass'])

# Извлекаем ключ первого элемента из словаря default_category
k = list(s.current_scenario['presta_categories']['default_category'].keys())[0]

# Дальнейшая обработка данных
print(k)
```