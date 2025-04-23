### **Инструкции по использованию блока кода**

=========================================================================================

Описание
-------------------------
Этот блок кода предназначен для организации и запуска рекламных кампаний в Facebook. Он включает в себя функции для настройки параметров кампаний, определения целевых групп и языковых предпочтений, а также управления процессом публикации объявлений.

Шаги выполнения
-------------------------
1. **Определение путей к файлам групп и рекламных материалов**:
   - Задаются пути к файлам, содержащим информацию о группах Facebook, в которых будет размещаться реклама, а также к файлам с рекламными материалами на разных языках (русский и иврит).

2. **Функция `run_campaign`**:
   - Принимает в качестве аргументов экземпляр драйвера веб-браузера, имя рекламодателя, список кампаний, пути к файлам групп, язык и валюту.
   - Создает экземпляр класса `FacebookPromoter` и запускает рекламные кампании, используя предоставленные параметры.

3. **Функция `campaign_cycle`**:
   - Определяет пары язык-валюта для кампаний, а также определяет, для какого языка какие группы использовать.
   - Для каждой пары язык-валюта запускает функцию `run_campaign` с соответствующими параметрами.

4. **Основная функция `main`**:
   - Инициализирует драйвер Chrome и открывает Facebook.
   - Запускает бесконечный цикл, в котором периодически проверяется условие `interval()`. Если условие выполняется, программа засыпает на некоторое время.
   - Запускает функцию `campaign_cycle` для выполнения рекламных кампаний.
   - После завершения цикла кампаний логирует информацию и засыпает на случайное время перед следующей итерацией.

Пример использования
-------------------------

```python
import header
import random
import time
import copy
from pathlib import Path 

from src import gs
from src.utils.file import get_directory_names, get_filenames
from src.webdriver.driver import Driver, Chrome
from src.endpoints.advertisement.facebook import FacebookPromoter
from src.logger.logger import logger
from src.utils.date_time import interval

# Определение групп и категорий
group_file_paths_ru: list[str] = ["sergey_pages.json"]
adv_file_paths_ru: list[str] = ["ru_ils.json"]
group_file_paths_he: list[str] = ["sergey_pages.json"]
adv_file_paths_he: list[str] = ["he_ils.json"]
group_categories_to_adv = ['sales', 'biz']

def run_campaign(d: Driver, promoter_name: str, campaigns: list | str, group_file_paths: list, language: str, currency: str):
    """Запуск рекламной кампании.

    Args:
        d (Driver): Экземпляр драйвера.
        promoter_name (str): Имя рекламодателя.
        campaigns (list): Список кампаний.
        group_file_paths (list): Пути к файлам с группами.
        language (str): Язык рекламной кампании.
        currency (str): Валюта рекламной кампании.
    """

    promoter = FacebookPromoter(d, promoter=promoter_name)
    promoter.run_campaigns(
        campaigns=campaigns,
        group_file_paths=group_file_paths,
        group_categories_to_adv=group_categories_to_adv,
        language=language,
        currency=currency,
        no_video=False
    )


def campaign_cycle(d: Driver):
    """Цикл для управления запуском кампаний.

    Args:
        d (Driver): Экземпляр драйвера.
        aliexpress_adv (bool): Флаг для определения рекламодателя.
    """
    
    file_paths_ru = copy.copy(group_file_paths_ru)
    file_paths_ru.extend(adv_file_paths_ru)    # <- промо в группы
    file_paths_he = copy.copy(group_file_paths_he)
    file_paths_he.extend(adv_file_paths_he)

    # Список словарей [{language:currency}]
    language_currency_pairs = [{"HE": "ILS"},{"RU": "ILS"},]

    for lc in language_currency_pairs:
        # Извлечение языка и валюты из словаря
        for language, currency in lc.items():
            # Определение group_file_paths на основе language
            group_file_paths = file_paths_ru if language == "RU" else file_paths_he


            #campaigns = ['kazarinov_tips_ru', 'kazarinov_ru'] if language == "RU" else ['kazarinov_tips_he', 'kazarinov_he']
            campaigns = ['kazarinov_ru'] if language == "RU" else ['kazarinov_he']
            for c in campaigns:
                run_campaign(
                    d, 'kazarinov', c, 
                    group_file_paths=group_file_paths, 
                    language=language, 
                    currency=currency
                )

            campaigns = get_directory_names(gs.path.google_drive / 'aliexpress' / 'campaigns')
            run_campaign(
                d, 'aliexpress', campaigns, 
                group_file_paths=group_file_paths,
                language=language, 
                currency=currency 
                )
                    

    return True


def main():
    """Основная функция для запуска рекламных кампаний."""
    try:
        d = Driver(Chrome)
        d.get_url(r"https://facebook.com")
        aliexpress_adv = True

        while True:
            if interval():
                print("Good night!")
                time.sleep(1000)

            # Первый цикл для русскоязычных кампаний
            campaign_cycle(d)
            ...

            # Логирование и задержка
            logger.debug(f"going to sleep at {time.strftime('%H:%M:%S')}", None, False)
            t = random.randint(30, 360)
            print(f"sleeping {t} sec")
            time.sleep(t)

    except KeyboardInterrupt:
        logger.info("Campaign promotion interrupted.")

if __name__ == "__main__":
    main()