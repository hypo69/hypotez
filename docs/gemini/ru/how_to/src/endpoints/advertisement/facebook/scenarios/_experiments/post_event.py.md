## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода управляет отправкой информации о событиях на Facebook. 

Он получает данные из JSON-файлов, расположенных в директории `facebook/events`, и отправляет их в соответствующие группы.

Шаги выполнения
-------------------------
1. **Получение данных о событиях:** 
    -  Извлекаются названия всех поддиректорий в `aliexpress/events` на Google Drive.
    -  Каждая поддиректория представляет собой событие.
    -  Извлекается файл `*.json` из каждой поддиректории, который содержит информацию о событии.
2. **Создание объекта `promoter`:**
    -  Создается объект `FacebookPromoter` с использованием `Chrome` браузера.
    -  Объект `promoter` будет отвечать за отправку информации о событиях в группы.
3. **Обработка групп:**
    -  Для каждой группы, указанной в `facebook/groups` на Google Drive, объект `promoter`  отправляет информацию о событии.
    -  Информация о событиях передается в виде массива `[event]`.


Пример использования
-------------------------

```python
# Пример отправки информации о событии в группы Facebook
from src.endpoints.advertisement.facebook.scenarios._experiments import post_events

# Выполняет отправку информации о всех событиях, хранящихся в `aliexpress/events`
post_events()

# Пример отправки информации о конкретном событии в группу 
from src.endpoints.advertisement.facebook.scenarios._experiments import post_to_my_group
from src.utils.jjson import j_loads_ns
from src import gs

event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events' / 'sep_11_2024_over60_pricedown' / 'sep_11_2024_over60_pricedown.json')
post_to_my_group(event)

# Пример получения данных из JSON-файла о событии
from src.utils.jjson import j_loads_ns
from src import gs

event_file = 'sep_11_2024_over60_pricedown.json'
event_data = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events' / event_file / f'{event_file}.json')

# Вывод информации о событии
print(event_data)
```