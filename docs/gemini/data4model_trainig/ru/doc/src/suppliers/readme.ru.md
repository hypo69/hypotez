# Модуль `suppliers`

## Обзор

Этот модуль предоставляет базовый класс `Supplier`, который служит основой для взаимодействия с различными поставщиками данных. Он обеспечивает унифицированный интерфейс для работы с различными источниками данных, такими как веб-сайты, документы и базы данных.

## Подробней

Модуль `suppliers` играет центральную роль в проекте `hypotez`, обеспечивая абстракцию и унификацию работы с различными поставщиками информации. Поставщики могут предоставлять данные о товарах, услугах или любую другую информацию, необходимую для функционирования проекта. Основная задача модуля — свести работу с различными поставщиками к единому алгоритму действий внутри класса `Supplier`.

## Классы

### `Supplier`

**Описание**: Базовый класс для всех поставщиков. Этот класс является основой для управления взаимодействиями с поставщиками, выполняя инициализацию, настройку, аутентификацию и запуск сценариев для различных источников данных.

**Наследует**:
- Не наследует другие классы.

**Атрибуты**:
- Отсутствуют явно определенные атрибуты в предоставленном коде. Однако, класс предназначен для инициализации и настройки взаимодействия с различными поставщиками данных, подразумевая наличие атрибутов, специфичных для каждого поставщика.

**Методы**:
- В предоставленном коде не указаны методы класса `Supplier`. Предполагается, что методы будут определены в классах-наследниках, специфичных для каждого поставщика.

**Принцип работы**:
1.  Класс `Supplier` служит базой для создания классов, представляющих конкретных поставщиков данных.
2.  При инициализации класса-наследника происходит настройка соединения с источником данных поставщика, аутентификация (при необходимости) и подготовка к выполнению сценариев.
3.  Основной принцип работы заключается в унификации доступа к данным от различных поставщиков через единый интерфейс, предоставляемый классом `Supplier`.

## Список реализованных поставщиков:

-   [aliexpress](aliexpress/README.RU.MD) - Реализован в двух вариантах сценариев: `webriver` и `api`
-   [amazon](amazon/README.RU.MD) - `webdriver`
-   [bangood](bangood/README.RU.MD) - `webdriver`
-   [cdata](cdata/README.RU.MD) - `webdriver`
-   [chat\_gpt](chat_gpt/README.RU.MD) - Работа с чатом chatgpt (НЕ С МОДЕЛЬЮ!)
-   [ebay](ebay/README.RU.MD) - `webdriver`
-   [etzmaleh](etzmaleh/README.RU.MD) - `webdriver`
-   [gearbest](gearbest/README.RU.MD) - `webdriver`
-   [grandadvance](grandadvance/README.RU.MD) - `webdriver`
-   [hb](hb/README.RU.MD) - `webdriver`
-   [ivory](ivory/README.RU.MD) - `webdriver`
-   [ksp](ksp/README.RU.MD) - `webdriver`
-   [kualastyle](kualastyle/README.RU.MD) `webdriver`
-   [morlevi](morlevi/README.RU.MD) `webdriver`
-   [visualdg](visualdg/README.RU.MD) `webdriver`
-   [wallashop](wallashop/README.RU.MD) `webdriver`
-   [wallmart](wallmart/README.RU.MD) `webdriver`

[Подробно о вебдрайвере class `Driver`](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/webdriver/driver.py.md)

[Подробно о сценариях class `Scenario`](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/scenario/executor.py.md)

[Подробно о локаторах](https://github.com/hypo69/hypotez/blob/master/docs/ru/src/suppliers/locator.ru.md)

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