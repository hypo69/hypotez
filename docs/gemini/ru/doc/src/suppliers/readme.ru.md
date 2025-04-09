# Документация для разработчика: `Supplier`

## Обзор

Этот документ описывает класс `Supplier`, который является базовым классом для всех поставщиков в проекте `hypotez`. В контексте кода, поставщик — это источник информации, такой как производитель товара, данных или информации. Источниками поставщика могут быть целевые страницы сайтов, документы, базы данных или таблицы. Класс `Supplier` предназначен для унификации работы с различными поставщиками посредством единого алгоритма действий. Каждый поставщик имеет свой уникальный префикс (подробнее в [prefixes.md](prefixes.md)).

## Подробней

Класс `Supplier` служит основой для управления взаимодействиями с поставщиками данных. Он выполняет инициализацию, настройку, аутентификацию и запуск сценариев для различных источников данных, таких как `amazon.com`, `walmart.com`, `mouser.com` и `digikey.com`. Клиент может определять дополнительных поставщиков, расширяя функциональность системы.

## Список реализованных поставщиков:

- [aliexpress](aliexpress/README.RU.MD) - Реализован в двух вариантах сценариев: `webdriver` и `api`
- [amazon](amazon/README.RU.MD) - `webdriver`
- [bangood](bangood/README.RU.MD) - `webdriver`
- [cdata](cdata/README.RU.MD) - `webdriver`
- [chat_gpt](chat_gpt/README.RU.MD) - Работа с чатом chatgpt (НЕ С МОДЕЛЬЮ!)
- [ebay](ebay/README.RU.MD) - `webdriver`
- [etzmaleh](etzmaleh/README.RU.MD) - `webdriver`
- [gearbest](gearbest/README.RU.MD) - `webdriver`
- [grandadvance](grandadvance/README.RU.MD) - `webdriver`
- [hb](hb/README.RU.MD) - `webdriver`
- [ivory](ivory/README.RU.MD) - `webdriver`
- [ksp](ksp/README.RU.MD) - `webdriver`
- [kualastyle](kualastyle/README.RU.MD) - `webdriver`
- [morlevi](morlevi/README.RU.MD) - `webdriver`
- [visualdg](visualdg/README.RU.MD) - `webdriver`
- [wallashop](wallashop/README.RU.MD) - `webdriver`
- [wallmart](wallmart/README.RU.MD) - `webdriver`

[подробно о вебдрайвере class `Driver`](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/webdriver/driver.py.md)

[подробно о сценариях class `Scenario`](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/scenario/executor.py.md)

[подробно о локаторах](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/locator.ru.md)

## Схема взаимодействия

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