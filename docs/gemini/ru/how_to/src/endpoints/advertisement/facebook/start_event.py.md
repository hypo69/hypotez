## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода запускает кампанию по продвижению товаров в группах Facebook. Он работает с файлами, содержащими информацию о группах и событиях, и отправляет эти события в указанные группы.

Шаги выполнения
-------------------------
1. **Инициализация**:
    - Загружается веб-драйвер Chrome (Driver(Chrome)).
    - Открыть веб-страницу Facebook (d.get_url(r"https://facebook.com")).
    - Определяются списки файлов с группами: 
        - `filenames` - список файлов с группами, для которых будет запущена кампания.
        - `excluded_filenames` - список файлов с группами, которые будут исключены из кампании. 
    - Загружается список названий событий: `events_names` - список событий, которые будут отправлены в группы.
    - Создается объект FacebookPromoter с веб-драйвером, списком файлов с группами и флагом `no_video = True`, который запрещает отправку видео.

2. **Запуск кампании**:
    - В бесконечном цикле `while True` код выполняет следующие действия:
        - Выводит сообщение в лог о запуске (`logger.debug`).
        - Вызывает функцию `run_events` класса FacebookPromoter для отправки событий в группы.
        - Выводит сообщение в лог о переходе в спящий режим (`logger.debug`).
        - Устанавливает временной интервал в 7200 секунд (2 часа) (`time.sleep(7200)`).

3. **Обработка прерывания**:
    - Если пользователь нажимает `Ctrl+C`, код прерывается, и выводится сообщение в лог о прерывании кампании (`logger.info`).

Пример использования
-------------------------

```python
from src.endpoints.advertisement.facebook import FacebookPromoter
from src.webdriver.driver import Driver, Chrome
from src.logger.logger import logger

# Инициализация драйвера и FacebookPromoter
d = Driver(Chrome)
d.get_url(r"https://facebook.com")
promoter = FacebookPromoter(d, group_file_paths=["my_managed_groups.json", "usa.json"], no_video=True)

# Запуск кампании
try:
    while True:
        logger.debug(f"waikig up {time.strftime('%H:%M:%S')}", None, False)
        promoter.run_events(events_names=["choice_day_01_10"], group_file_paths=["my_managed_groups.json", "usa.json"])
        logger.debug(f"going to sleep at {time.strftime('%H:%M:%S')}", None, False)
        time.sleep(7200)  # Пауза 2 часа

except KeyboardInterrupt:
    logger.info("Campaign promotion interrupted.")
```