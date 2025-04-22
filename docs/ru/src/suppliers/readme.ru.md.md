# Модуль `suppliers`

## Обзор

Данный модуль предоставляет структуру для работы с различными поставщиками данных. Он содержит базовый класс `Supplier`, который служит основой для создания классов, взаимодействующих с конкретными поставщиками, такими как `amazon.com`, `walmart.com`, `mouser.com` и `digikey.com`. Модуль обеспечивает унифицированный подход к инициализации, настройке, аутентификации и выполнению сценариев для извлечения данных из различных источников.

## Подробней

Модуль `suppliers` предназначен для упрощения работы с различными поставщиками данных, предоставляя единый интерфейс для взаимодействия с ними. Это позволяет клиентам легко добавлять и поддерживать новых поставщиков, не изменяя основной код приложения.

## Классы

### `Supplier`

**Описание**: Базовый класс для всех поставщиков.

**Наследует**:
Отсутствует.

**Атрибуты**:
- Отсутствуют.

**Принцип работы**:
Класс `Supplier` служит основой для управления взаимодействиями с поставщиками данных. Он предоставляет общую структуру для инициализации, настройки, аутентификации и запуска сценариев для различных источников данных.

**Методы**:
Отсутствуют.

## Список реализованных поставщиков:

- [aliexpress](aliexpress/README.RU.MD) - Реализован в двух вариантах сценариев: `webdriver` и `api`.
- [amazon](amazon/README.RU.MD) - `webdriver`.
- [bangood](bangood/README.RU.MD) - `webdriver`.
- [cdata](cdata/README.RU.MD) - `webdriver`.
- [chat_gpt](chat_gpt/README.RU.MD) - Работа с чатом chatgpt (НЕ С МОДЕЛЬЮ!).
- [ebay](ebay/README.RU.MD) - `webdriver`.
- [etzmaleh](etzmaleh/README.RU.MD) - `webdriver`.
- [gearbest](gearbest/README.RU.MD) - `webdriver`.
- [grandadvance](grandadvance/README.RU.MD) - `webdriver`.
- [hb](hb/README.RU.MD) - `webdriver`.
- [ivory](ivory/README.RU.MD) - `webdriver`.
- [ksp](ksp/README.RU.MD) - `webdriver`.
- [kualastyle](kualastyle/README.RU.MD) - `webdriver`.
- [morlevi](morlevi/README.RU.MD) - `webdriver`.
- [visualdg](visualdg/README.RU.MD) - `webdriver`.
- [wallashop](wallashop/README.RU.MD) - `webdriver`.
- [wallmart](wallmart/README.RU.MD) - `webdriver`.

## Дополнительная информация

- [подробно о вебдрайвере class `Driver`](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/webdriver/driver.py.md)
- [подробно о сценариях class `Scenario`](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/scenario/executor.py.md)
- [подробно о локаторах](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/locator.ru.md)

## Диаграмма взаимодействия

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