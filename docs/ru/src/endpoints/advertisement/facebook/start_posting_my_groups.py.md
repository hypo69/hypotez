# Модуль для отправки рекламных объявлений в группы Facebook

## Обзор

Модуль предназначен для автоматической публикации рекламных объявлений в группы Facebook. Он использует веб-драйвер для взаимодействия с Facebook и выполняет цикл публикации объявлений до прерывания пользователем.

## Подробней

Этот модуль является частью системы автоматизации рекламы в Facebook. Он использует класс `FacebookPromoter` для управления процессом публикации и работает в бесконечном цикле, пока не будет прерван пользователем. Модуль предназначен для автоматизации рутинной задачи публикации объявлений, освобождая время для других задач.

## Классы

### `FacebookPromoter`

**Описание**: Класс для управления процессом публикации рекламных объявлений в Facebook.

**Наследует**:
- Нет явного наследования.

**Атрибуты**:
- `driver`: Экземпляр веб-драйвера для взаимодействия с Facebook.
- `group_file_paths` (list): Список путей к файлам, содержащим информацию о группах Facebook.
- `no_video` (bool): Флаг, указывающий, следует ли публиковать видеообъявления.

**Методы**:
- `run_campaigns()`: Запускает кампании по продвижению в Facebook.

## Функции

В данном коде отсутствуют отдельные функции, не относящиеся к классам. Основная логика работы сосредоточена в классе `FacebookPromoter` и его методах.

## Методы класса

### `run_campaigns`

```python
def run_campaigns(campaigns: list, group_file_paths: list):
    """
    Запускает кампании по продвижению в Facebook.

    Args:
        campaigns (list): Список названий кампаний для запуска.
        group_file_paths (list): Список путей к файлам, содержащим информацию о группах Facebook.

    Returns:
        None

    Raises:
        Exception: В случае возникновения ошибки при выполнении кампании.

    
    - Функция перебирает список кампаний и файлов групп, передавая их в соответствующие методы класса `FacebookPromoter` для публикации объявлений.
    - Функция вызывает методы `prepare_groups`, `process_groups` для подготовки и обработки групп.
    - Функция вызывает методы `get_ads` для подготовки рекламных материалов

    """
    ...
```

## Параметры класса

- `filenames` (list): Список имен файлов, содержащих информацию о группах. Используется 'my_managed_groups.json'.
- `campaigns` (list): Список названий кампаний. Включает 'brands', 'mom_and_baby', 'pain', 'sport_and_activity', 'house', 'bags_backpacks_suitcases', 'man'.
- `promoter` (FacebookPromoter): Объект класса `FacebookPromoter`, используемый для запуска рекламных кампаний.

## Примеры

```python
# Пример создания экземпляра FacebookPromoter и запуска кампаний
d = Driver(Chrome)
d.get_url(r"https://facebook.com")

filenames: list = ['my_managed_groups.json']

campaigns: list = ['brands',
                    'mom_and_baby',
                    'pain',
                    'sport_and_activity',
                    'house',
                    'bags_backpacks_suitcases',
                    'man']

promoter = FacebookPromoter(d, group_file_paths=filenames, no_video=True)

try:
    while True:
        promoter.run_campaigns(campaigns=copy.copy(campaigns), group_file_paths=filenames)
        ...
except KeyboardInterrupt as ex:
    logger.info("Campaign promotion interrupted.", ex, exc_info=True)