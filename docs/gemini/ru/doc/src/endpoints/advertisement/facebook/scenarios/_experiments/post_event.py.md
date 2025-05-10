# Модуль для отправки мероприятий на Facebook

## Обзор

Модуль `post_event.py` предназначен для автоматизации отправки мероприятий на Facebook из Google Drive. Он обрабатывает данные о мероприятиях, хранящиеся в JSON-файлах, и публикует их в соответствующие группы Facebook.

## Подробнее

Модуль взаимодействует с Google Drive, чтобы получить информацию о мероприятиях из папки `events` в директории `aliexpress`.  Он загружает данные из JSON-файлов, анализирует их и использует веб-драйвер (Chrome) для авторизации и публикации сообщений в Facebook.

## Классы

### `FacebookPromoter`

**Описание**: Класс `FacebookPromoter` обеспечивает функциональность для отправки мероприятий в Facebook.

**Наследует**: 
    - Класс не наследует другие классы.

**Атрибуты**:
    - `d` (Driver): Экземпляр класса `Driver`, который управляет веб-драйвером. 
    - `group_file_paths` (list): Список путей к JSON-файлам, содержащих информацию о группах Facebook.

**Методы**:
    - `process_groups(events: list, is_event: bool, group_file_paths: list)`: Процесс отправки мероприятий в группы.

## Функции

### `post_events()`

**Назначение**: Функция `post_events()` обрабатывает и отправляет мероприятия на Facebook.

**Как работает функция**:
    - Считывает список папок с событиями из директории `events` в `aliexpress` на Google Drive.
    - Создаёт экземпляр класса `FacebookPromoter` для управления процессом отправки.
    - Для каждого файла с данными о событии (`event_file`):
        - Загружает данные из JSON-файла.
        - Вызывает метод `process_groups` в экземпляре `FacebookPromoter` для отправки информации о событии в группы.

**Параметры**:
    - Нет параметров.

**Возвращает**:
    - `None`.

**Вызывает исключения**:
    - `FileNotFoundError`: Если JSON-файл с информацией о мероприятии отсутствует.

**Примеры**:
    ```python
    from src.endpoints.advertisement.facebook.scenarios._experiments.post_event import post_events

    post_events()  # Запуск обработки и отправки событий
    ```

### `post_to_my_group(event)`

**Назначение**: Функция `post_to_my_group(event)` отправляет информацию о мероприятии в определённую группу.

**Как работает функция**:
    - Загружает информацию о группах из файла `my_managed_groups.json` в директории `groups` на Google Drive.
    - Создает экземпляр `Driver` с веб-драйвером Chrome.
    - Для каждой группы из файла `my_managed_groups.json`:
        - Открывает в браузере URL группы.
        - Отправляет информацию о мероприятии в группу.

**Параметры**:
    - `event`: Словарь с данными о мероприятии.

**Возвращает**:
    - `None`.

**Вызывает исключения**:
    - Нет.

**Примеры**:
    ```python
    from src.endpoints.advertisement.facebook.scenarios._experiments.post_event import post_to_my_group
    from src.utils.jjson import j_loads_ns
    from src import gs

    event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events' / 'sep_11_2024_over60_pricedown' / 'sep_11_2024_over60_pricedown.json')
    post_to_my_group(event)
    ```


## Параметры класса `FacebookPromoter`

- `d` (Driver): Экземпляр класса `Driver`, который управляет веб-драйвером. 
- `group_file_paths` (list): Список путей к JSON-файлам, содержащих информацию о группах Facebook.


## Примеры

```python
from src.endpoints.advertisement.facebook.scenarios._experiments.post_event import post_events, post_to_my_group
from src.utils.jjson import j_loads_ns
from src import gs

# Отправка всех мероприятий
post_events()

# Отправка одного мероприятия в группу
event = j_loads_ns(gs.path.google_drive / 'aliexpress' / 'events' / 'sep_11_2024_over60_pricedown' / 'sep_11_2024_over60_pricedown.json')
post_to_my_group(event)
```

## Твое поведение при анализе кода:

- внутри кода ты можешь встретить выражение между `<` `>`. Например: `<инструкция для модели gemini:Загрузка описаний товаров в PrestaShop.>, <далее, если есть>. Это заготовки, куда ты вставляешь релевантное значение
- всегда смотри системную инструкцию для обработки кода проекта `hypotez`;
- анализируй расположение файла в проекте. Это поможет понять его назначение и взаимосвязь с другими файлами. Расположение файла ты найдешь в самой превой строке кода, начинающейся с `## \\file /...`;
- запоминай предоставленный код и анализируй его связь с другими частями проекта;
- В этой инструкции не надо предлагать улучшение кода. Четко следуй пункту 5. **Пример файла** при составлении ответа