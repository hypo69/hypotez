# Модуль для отправки рекламных объявлений в группы Facebook

## Обзор

Модуль `src.endpoints.advertisement.facebook.start_sergey` предназначен для автоматической отправки рекламных объявлений в группы Facebook. Он использует драйвер веб-браузера для навигации по Facebook и выполнения действий по размещению рекламы. Модуль поддерживает различные языки и валюты для рекламных кампаний.

## Подробнее

Модуль предназначен для автоматизации процесса размещения рекламы в Facebook. Он использует веб-драйвер для имитации действий пользователя, таких как вход в систему, навигация по группам и публикация объявлений.  Поддерживает несколько языков и валют.

## Функции

### `run_campaign`

```python
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
    ...
```

**Назначение**: Запускает рекламную кампанию для заданного рекламодателя в указанных группах Facebook.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера веб-браузера, используемый для автоматизации действий в Facebook.
-   `promoter_name` (str): Имя рекламодателя, используемое для идентификации в Facebook.
-   `campaigns` (list | str): Список кампаний, которые необходимо запустить.
-   `group_file_paths` (list): Список путей к файлам, содержащим информацию о группах Facebook, в которых будет размещаться реклама.
-   `language` (str): Язык рекламной кампании (например, "RU" для русского или "HE" для иврита).
-   `currency` (str): Валюта рекламной кампании (например, "ILS" для израильского шекеля).

**Как работает функция**:

1.  Создает экземпляр класса `FacebookPromoter`, который отвечает за выполнение действий по размещению рекламы в Facebook.
2.  Вызывает метод `run_campaigns` экземпляра `FacebookPromoter`, передавая ему параметры кампании, группы, языка и валюты.

**Примеры**:

```python
from src.webdriver.driver import Driver, Chrome

# Пример запуска кампании на русском языке
driver = Driver(Chrome)
run_campaign(driver, 'kazarinov', ['kazarinov_ru'], ['sergey_pages.json'], 'RU', 'ILS')

# Пример запуска кампании для aliexpress на иврите
driver = Driver(Chrome)
run_campaign(driver, 'aliexpress', ['campaign1', 'campaign2'], ['sergey_pages.json'], 'HE', 'ILS')
```

### `campaign_cycle`

```python
def campaign_cycle(d: Driver):
    """Цикл для управления запуском кампаний.

    Args:
        d (Driver): Экземпляр драйвера.
        aliexpress_adv (bool): Флаг для определения рекламодателя.
    """
    ...
```

**Назначение**: Управляет циклом запуска рекламных кампаний для разных языков и рекламодателей.

**Параметры**:

-   `d` (Driver): Экземпляр драйвера веб-браузера, используемый для автоматизации действий в Facebook.

**Как работает функция**:

1.  Определяет пути к файлам групп и рекламных объявлений для русского и ивритского языков.
2.  Создает список словарей, содержащих пары язык-валюта.
3.  Перебирает пары язык-валюта и запускает рекламные кампании для каждого языка.
4.  Запускает рекламные кампании для рекламодателя aliexpress.

**Примеры**:

```python
from src.webdriver.driver import Driver, Chrome

# Пример запуска цикла кампаний
driver = Driver(Chrome)
campaign_cycle(driver)
```

### `main`

```python
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

    except KeyboardInterrupt as ex:
        logger.info("Campaign promotion interrupted.", ex, exc_info=True)
```

**Назначение**: Основная функция для запуска рекламных кампаний.

**Как работает функция**:

1.  Создает экземпляр драйвера веб-браузера Chrome.
2.  Открывает страницу Facebook в браузере.
3.  Запускает бесконечный цикл, в котором:
    *   Проверяет, не наступило ли время для перерыва.
    *   Запускает цикл рекламных кампаний для разных языков и рекламодателей.
    *   Выполняет задержку перед следующим циклом.
4.  Обрабатывает исключение `KeyboardInterrupt`, которое возникает при прерывании программы пользователем.

**Внутренние функции**:

Функция `main` не содержит внутренних функций.

**Примеры**:

```python
# Пример запуска основной функции
if __name__ == "__main__":
    main()
```

## Параметры модуля

-   `group_file_paths_ru` (list[str]): Список путей к файлам, содержащим информацию о группах Facebook на русском языке.
-   `adv_file_paths_ru` (list[str]): Список путей к файлам, содержащим рекламные объявления на русском языке.
-   `group_file_paths_he` (list[str]): Список путей к файлам, содержащим информацию о группах Facebook на иврите.
-   `adv_file_paths_he` (list[str]): Список путей к файлам, содержащим рекламные объявления на иврите.
-   `group_categories_to_adv` (list[str]): Список категорий групп, в которых будет размещаться реклама.

```python
group_file_paths_ru: list[str] = ["sergey_pages.json"]
adv_file_paths_ru: list[str] = ["ru_ils.json"]
group_file_paths_he: list[str] = ["sergey_pages.json"]
adv_file_paths_he: list[str] = ["he_ils.json"]
group_categories_to_adv = ['sales', 'biz']