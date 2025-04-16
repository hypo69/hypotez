# Модуль Kazarinov. Мехирон в pdf

## Обзор

Модуль `src.endpoints.kazarinov` предназначен для создания прайс-листов (мехирон) в формате PDF.

## Подробней

Этот модуль автоматизирует процесс сбора данных о товарах с различных веб-сайтов и формирования прайс-листов для Сергея Казаринова.

## Описание

KazarinovTelegramBot

*   [https://one-tab.co.il](https://one-tab.co.il)
*   [https://morlevi.co.il](https://morlevi.co.il)
*   [https://grandavance.co.il](https://grandavance.co.il)
*   [https://ivory.co.il](https://ivory.co.il)
*   [https://ksp.co.il](https://ksp.co.il)

BotHandler

На стороне клиента:

```mermaid
flowchart TD
    Start[Выбор комплектующих для сборки компьютера] --> Combine[Объединение в One-Tab]
    Combine --> SendToBot{Отправка ссылки One-Tab в Telegram боту}
    SendToBot -->|hypo69_kazarinov_bot| ProdBot[Telegram бот <code>prod</code>]
    SendToBot -->|hypo69_test_bot| TestBot[Telegram бот <code>test</code>]
```

На стороне кода:

*   `kazarinov_bot.handle_message()` -> `kazarinov.scenarios.run_scenario()`:

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

## Ссылки

Далее

*   [Казарионв бот](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/kazarinov_bot.ru.md)
*   [Испоолнение сценария](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/scenarios/readme.ru.md)

[Root ↑](https://github.com/hypo69/hypotez/blob/master/readme.ru.md)
[English](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/README.MD)