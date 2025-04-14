# Документация модуля `src.endpoints.kazarinov`

## Обзор

Данный модуль предназначен для работы с Kazarinov. PDF Mexiron Creator. Описывает взаимодействие клиентской и серверной частей, включая использование Telegram ботов `prod` и `test`, а также сценарии обработки данных из OneTab.

## Подробней

Модуль предназначен для автоматизации процесса создания PDF-файлов из ссылок, полученных из OneTab. Клиентская часть предполагает выбор комплектующих для сборки компьютера, объединение их в OneTab и отправку ссылки в Telegram бот. Серверная часть обрабатывает ссылку, проверяет данные и запускает сценарий Mexiron. В случае успеха, отправляет ссылку в WhatsApp.

## Содержание

- [KazarinovTelegramBot](#kazarinovtelegrambot)
- [BotHandler](#bothandler)
- [Клиентская сторона (Kazarinov)](#клиентская-сторона-kazarinov)
- [Код](#код)
- [Далее](#далее)

## KazarinovTelegramBot

- Ссылки на полезные ресурсы:
    - https://one-tab.co.il
    - https://morlevi.co.il
    - https://grandavance.co.il
    - https://ivory.co.il
    - https://ksp.co.il

## BotHandler

Описание обработчика бота.

## Клиентская сторона (Kazarinov)

```mermaid
flowchart TD
    Start[Выбор комплектующих для сборки компьютера] --> Combine[Объединение в One-Tab]
    Combine --> SendToBot{Отправка ссылки One-Tab в Telegram боту}
    SendToBot -->|hypo69_kazarinov_bot| ProdBot[Telegram бот <code>prod</code>]
    SendToBot -->|hypo69_test_bot| TestBot[Telegram бот <code>test</code>]
```

Схема описывает взаимодействие клиента с Telegram ботами `prod` и `test` через OneTab.

## Код

```mermaid
flowchart TD
    A[Start] --> B{URL is from OneTab?}
    B -->|Yes| C[Get data from OneTab]
    B -->|No| D[Reply - Try again]
    C --> E{Data valid?}
    E -->|No| F[Reply Incorrect data]
    E -->|Yes| G[Run Mexiron scenario]
    G --> H{Scenario successful?}
    H -->|Yes| I[Reply Done! I will send the link to WhatsApp]
    H -->|No| J[Reply Error running scenario]
    F --> K[Return]
    I --> K[Return]
    D --> K[Return]
    J --> K[Return]
```

Схема описывает логику обработки URL из OneTab, проверки данных и запуска сценария Mexiron.

## Далее

- [Kazarinov bot](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/kazarinov_bot.md)
- [Scenario Execution](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/scenarios/README.MD)