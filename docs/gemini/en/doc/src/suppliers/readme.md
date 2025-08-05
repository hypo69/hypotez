# Документация для модуля `suppliers`

## Обзор

В данном разделе представлена документация для модуля `suppliers` проекта `hypotez`. Модуль содержит описание класса `Supplier`, который является базовым классом для всех поставщиков информации. В контексте данного кода, "поставщик" представляет собой источник данных или информации, такой как производитель товаров, веб-сайт, документ, база данных или таблица. Класс `Supplier` унифицирует взаимодействие с различными поставщиками, предоставляя стандартизированный набор операций.

## Более подробно

Класс `Supplier` является основой для управления взаимодействием с поставщиками. Он обрабатывает инициализацию, конфигурацию, аутентификацию и выполнение рабочих процессов для различных источников данных, таких как `amazon.com`, `walmart.com`, `mouser.com` и `digikey.com`. Также позволяет определять дополнительные поставщики. Каждый поставщик имеет уникальный префикс (подробнее в файле [prefixes.md](prefixes.md)).

## Список реализованных поставщиков:

*   [aliexpress](aliexpress) - Реализован с двумя рабочими процессами: `webdriver` и `api`
*   [amazon](amazon) - `webdriver`
*   [bangood](bangood) - `webdriver`
*   [cdata](cdata) - `webdriver`
*   [chat\_gpt](chat_gpt) - Взаимодействует с интерфейсом ChatGPT (НЕ МОДЕЛЬ!)
*   [ebay](ebay) - `webdriver`
*   [etzmaleh](etzmaleh) - `webdriver`
*   [gearbest](gearbest) - `webdriver`
*   [grandadvance](grandadvance) - `webdriver`
*   [hb](hb) - `webdriver`
*   [ivory](ivory) - `webdriver`
*   [ksp](ksp) - `webdriver`
*   [kualastyle](kualastyle) - `webdriver`
*   [morlevi](morlevi) - `webdriver`
*   [visualdg](visualdg) - `webdriver`
*   [wallashop](wallashop) - `webdriver`
*   [wallmart](wallmart) - `webdriver`

[Подробнее о WebDriver :class: `Driver`](../webdriver)

[Подробнее о рабочих процессах :class: `Scenario`](../scenarios)

```mermaid
graph TD
    subgraph WebInteraction
        webelement <--> executor
        subgraph InnerInteraction
            executor <--> webdriver
        end
    end
    webdriver -->|result| supplier
    supplier -->|locator| webdriver
    supplier --> product_fields
    product_fields --> endpoints
    scenario -->|Specific scenario for supplier| supplier