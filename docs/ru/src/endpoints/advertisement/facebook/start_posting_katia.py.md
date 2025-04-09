# Модуль для отправки рекламных объявлений в Facebook (Katia)

## Обзор

Модуль `start_posting_katia.py` предназначен для автоматической отправки рекламных объявлений в группы Facebook с использованием веб-драйвера. Он использует классы и функции из других модулей проекта, таких как `FacebookPromoter`, `Driver` и `logger`, для управления процессом публикации.

## Подробней

Этот модуль является отправной точкой для запуска рекламной кампании в Facebook. Он инициализирует веб-драйвер, получает URL Facebook, определяет список файлов конфигурации и список кампаний, которые необходимо запустить. Затем он создает экземпляр класса `FacebookPromoter` и запускает рекламные кампании.

## Классы

В данном модуле классы не определены. Используются классы из других модулей: `FacebookPromoter`, `Driver`, `Chrome`.

## Функции

В данном модуле функции не определены.

## Использование внешних модулей

-   `header`: Импортируется, но не используется напрямую в представленном коде.
-   `src.webdriver.driver.Driver`: Класс для управления веб-драйвером.
-   `src.webdriver.driver.Chrome`: Класс для создания экземпляра веб-драйвера Chrome.
-   `src.endpoints.advertisement.facebook.promoter.FacebookPromoter`: Класс для запуска рекламных кампаний в Facebook.
-   `src.logger.logger.logger`: Модуль для логирования событий.

## Переменные

-   `d`: Экземпляр класса `Driver` с использованием Chrome в качестве веб-драйвера.

    ```python
    d = Driver(Chrome)
    ```

-   `filenames`: Список имен файлов конфигурации, используемых для настройки рекламных кампаний.

    ```python
    filenames: list = ['katia_homepage.json']
    ```

-   `campaigns`: Список кампаний, которые необходимо запустить.

    ```python
    campaigns: list = [
        'sport_and_activity',
        'bags_backpacks_suitcases',
        'pain',
        'brands',
        'mom_and_baby',
        'house',
    ]
    ```

-   `promoter`: Экземпляр класса `FacebookPromoter`, который используется для запуска рекламных кампаний.

    ```python
    promoter = FacebookPromoter(d, group_file_paths=filenames, no_video=False)
    ```

## Логика работы модуля

1.  **Инициализация веб-драйвера**:
    *   Создается экземпляр драйвера Chrome.

        ```python
        d = Driver(Chrome)
        ```

2.  **Переход на сайт Facebook**:
    *   Выполняется переход по URL r"https://facebook.com".

        ```python
        d.get_url(r"https://facebook.com")
        ```

3.  **Определение параметров кампании**:
    *   Определяются имена файлов конфигурации (`filenames`) и список кампаний (`campaigns`).

        ```python
        filenames: list = ['katia_homepage.json']
        campaigns: list = [
            'sport_and_activity',
            'bags_backpacks_suitcases',
            'pain',
            'brands',
            'mom_and_baby',
            'house',
        ]
        ```

4.  **Инициализация промоутера Facebook**:
    *   Создается экземпляр промоутера, который будет запускать кампании.

        ```python
        promoter = FacebookPromoter(d, group_file_paths=filenames, no_video=False)
        ```

5.  **Запуск рекламных кампаний**:
    *   Вызывается метод `run_campaigns` промоутера для запуска кампаний.
    *   Обрабатывается прерывание с клавиатуры, чтобы можно было остановить кампанию.

        ```python
        try:
            promoter.run_campaigns(campaigns)
        except KeyboardInterrupt:
            logger.info("Campaign promotion interrupted.")
        ```

## Обработка исключений

-   Обрабатывается исключение `KeyboardInterrupt`, которое возникает при прерывании скрипта пользователем (например, нажатием Ctrl+C). В этом случае в лог выводится сообщение о прерывании кампании.

    ```python
    try:
        promoter.run_campaigns(campaigns)
    except KeyboardInterrupt:
        logger.info("Campaign promotion interrupted.")
    ```

## Схема работы

```
   Начало
   ↓
   Инициализация веб-драйвера (Chrome)
   ↓
   Переход на сайт Facebook
   ↓
   Определение параметров кампании (filenames, campaigns)
   ↓
   Инициализация промоутера Facebook (FacebookPromoter)
   ↓
   Запуск рекламных кампаний (promoter.run_campaigns)
   ↓
   Обработка исключения KeyboardInterrupt (остановка кампании)
   ↓
   Конец
```

## Примеры

Пример запуска модуля:

```python
# В данном коде нет функций, которые можно было бы вызвать напрямую.
# Модуль запускается как скрипт, который выполняет последовательность действий.