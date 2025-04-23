### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Данный блок кода предназначен для подготовки и обработки рекламных кампаний AliExpress. Он позволяет обрабатывать кампании целиком или по категориям, с учетом языка и валюты, а также поддерживает обработку всех кампаний в указанной директории.

Шаги выполнения
-------------------------
1. **Определение путей и импорт необходимых модулей**:
   - Код начинается с определения путей к директориям кампаний и импорта необходимых модулей, таких как `header`, `argparse`, `pathlib`, `typing`, `src.gs`, `AliCampaignEditor`, `locales`, `pprint`, `get_directory_names`, `j_loads_ns` и `logger`.
2. **Функция `process_campaign_category`**:
   - Функция `process_campaign_category` обрабатывает определенную категорию в рамках кампании для заданного языка и валюты.
   - Функция вызывает `AliCampaignEditor.process_campaign_category` для выполнения обработки.
   - Возвращает список заголовков товаров в данной категории.
3. **Функция `process_campaign`**:
   - Функция `process_campaign` обрабатывает кампанию целиком, учитывая язык и валюту.
   - Функция создает экземпляр класса `AliCampaignEditor` и вызывает метод `process_campaign` для обработки кампании.
   - Если язык и валюта не указаны, обрабатываются все доступные локали.
4. **Функция `process_all_campaigns`**:
   - Функция `process_all_campaigns` обрабатывает все кампании, находящиеся в директории `campaigns_directory`.
   - Функция получает список директорий кампаний с помощью `get_directory_names` и итерируется по ним.
   - Для каждой кампании создается экземпляр `AliCampaignEditor` и вызывается метод `process_campaign`.
5. **Функция `main_process`**:
   - Функция `main_process` является основной функцией для обработки кампании.
   - Функция определяет, нужно ли обрабатывать кампанию по категориям или целиком, и вызывает соответствующие функции (`process_campaign_category` или `process_campaign`).
   - Если указаны язык и валюта, обрабатывается только указанная локаль, в противном случае - все доступные.
6. **Функция `main`**:
   - Функция `main` является точкой входа в скрипт.
   - Функция использует `argparse` для разбора аргументов командной строки, таких как название кампании, список категорий, язык, валюта и флаг для обработки всех кампаний.
   - В зависимости от аргументов, вызывается либо `process_all_campaigns`, либо `main_process`.

Пример использования
-------------------------

```python
    import argparse
    from src.suppliers.suppliers_list.aliexpress.campaign.prepare_campaigns import main_process, process_all_campaigns

    # Пример 1: Обработка конкретной кампании по категориям
    campaign_name = "summer_sale"
    categories = ["electronics", "clothing"]
    language = "EN"
    currency = "USD"
    main_process(campaign_name, categories, language, currency)

    # Пример 2: Обработка конкретной кампании целиком
    campaign_name = "winter_sale"
    language = "DE"
    currency = "EUR"
    main_process(campaign_name, [], language, currency)  # categories=[] означает обработку всей кампании

    # Пример 3: Обработка всех кампаний
    language = "FR"
    currency = "CAD"
    process_all_campaigns(language, currency)

    # Пример использования через командную строку:
    # python your_script_name.py summer_sale -c electronics clothing -l EN -cu USD
    # python your_script_name.py winter_sale -l DE -cu EUR
    # python your_script_name.py --all -l FR -cu CAD