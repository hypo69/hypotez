## Как использовать FacebookPromoter
=========================================================================================

Описание
-------------------------
Класс `FacebookPromoter` предназначен для продвижения товаров и мероприятий на Facebook. 

Он автоматизирует публикацию рекламных постов в группах, гарантируя, что категории и события рекламируются, избегая дублирования.

Шаги выполнения
-------------------------
1. **Инициализация:** Создается экземпляр класса `FacebookPromoter`. 
    - **Ввод**:
        - `d`: Экземпляр `Driver` (например, `Chrome`, `Firefox`, `Playwright`) для управления браузером.
        - `group_file_paths`: Список путей к файлам с данными групп Facebook (по умолчанию используется каталог `'facebook/groups'`).
        - `no_video`: Флаг, отключающий видео в постах.
2. **Продвижение:** Метод `promote`  продвигает категорию или событие в группе Facebook.
    - **Ввод**:
        - `group`: Данные группы Facebook (объект `SimpleNamespace`).
        - `item`: Данные товара или события (объект `SimpleNamespace`).
        - `is_event`: Флаг, указывающий, является ли `item` событием.
3. **Обработка групп:** Метод `process_groups` обрабатывает все группы в списке `group_file_paths`.
    - **Ввод**:
        - `campaign_name`: Имя кампании.
        - `events`: Список событий для продвижения.
        - `is_event`: Флаг, указывающий, является ли `item` событием.
        - `group_categories_to_adv`: Список категорий товаров для продвижения.
        - `language`: Язык для продвижения.
        - `currency`: Валюта для продвижения.
    - **Действие**:
        - Проходит по каждой группе в списке `group_file_paths`.
        - Проверяет, соответствует ли группа указанным критериям (категория, язык, валюта, активность).
        - Продвигает выбранный товар или событие в группе, используя метод `promote`.
        - Обновляет данные группы после публикации.
    - **Вывод**:  
        - Обновленный список групп с информацией о последних продвижениях.

Пример использования
-------------------------

```python
from src.webdriver.driver import Driver, Firefox
from src.endpoints.advertisement.facebook.promoter import FacebookPromoter
from src.endpoints.advertisement.facebook.scenarios import post_message, post_event
from src.utils.jjson import j_loads_ns

# Создаем экземпляр Driver
driver = Driver(Firefox)

# Создаем экземпляр FacebookPromoter
promoter = FacebookPromoter(d=driver, promoter='aliexpress', group_file_paths='path/to/group_files')

# Проверяем, что мы можем отправлять сообщения
message = j_loads_ns('path/to/message_data.json')
if post_message(d=driver, message=message, no_video=False, without_captions=False):
    print('Сообщение отправлено!')

# Продвигаем событие
event = j_loads_ns('path/to/event_data.json')
if promoter.promote(group=j_loads_ns('path/to/group_data.json'), item=event, is_event=True):
    print('Событие успешно продвинуто!')

# Обрабатываем группы для кампании 'new_year_sale'
promoter.process_groups(campaign_name='new_year_sale', group_categories_to_adv=['sales'], language='ru', currency='USD')
```