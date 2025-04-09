# Документация модуля `Supplier`

## Обзор

Этот документ описывает базовый класс `Supplier`, используемый для унификации различных поставщиков данных в проекте `hypotez`. Класс предоставляет стандартизированный набор операций для взаимодействия с различными источниками данных, такими как веб-сайты, документы, базы данных и таблицы.

## Подробней

В контексте данного кода, `Supplier` представляет собой поставщика информации. Поставщиком может быть производитель товаров, данных или информации. Источники поставщика включают целевую страницу веб-сайта, документ, базу данных или таблицу. Этот класс объединяет различных поставщиков под стандартизированным набором операций. У каждого поставщика есть уникальный префикс.

Класс `Supplier` служит основой для управления взаимодействием с поставщиками. Он обрабатывает инициализацию, конфигурацию, аутентификацию и выполнение рабочих процессов для различных источников данных, таких как `amazon.com`, `walmart.com`, `mouser.com` и `digikey.com`. Клиенты также могут определять дополнительных поставщиков.

## Классы

### `Supplier`

**Описание**: Базовый класс для всех поставщиков.

**Наследует**:
- Нет наследования

**Атрибуты**:
- Нет атрибутов

**Методы**:
- Нет методов

**Принцип работы**:
Класс `Supplier` предназначен для унификации работы с различными поставщиками данных. Он служит основой для создания классов-поставщиков, каждый из которых взаимодействует с конкретным источником данных. Класс обеспечивает стандартизированный интерфейс для выполнения общих операций, таких как инициализация, аутентификация и выполнение рабочих процессов.

## Список реализованных поставщиков:

- [aliexpress](aliexpress) - Реализован с двумя рабочими процессами: `webdriver` и `api`
- [amazon](amazon) - `webdriver`
- [bangood](bangood) - `webdriver`
- [cdata](cdata) - `webdriver`
- [chat_gpt](chat_gpt) - Взаимодействует с интерфейсом ChatGPT (НЕ С МОДЕЛЬЮ!)
- [ebay](ebay) - `webdriver`
- [etzmaleh](etzmaleh) - `webdriver`
- [gearbest](gearbest) - `webdriver`
- [grandadvance](grandadvance) - `webdriver`
- [hb](hb) - `webdriver`
- [ivory](ivory) - `webdriver`
- [ksp](ksp) - `webdriver`
- [kualastyle](kualastyle) `webdriver`
- [morlevi](morlevi) `webdriver`
- [visualdg](visualdg) `webdriver`
- [wallashop](wallashop) `webdriver`
- [wallmart](wallmart) `webdriver`

[Подробнее о WebDriver :class: `Driver`](../webdriver)
[Подробнее о рабочих процессах :class: `Scenario`](../scenarios)

## Диаграмма

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