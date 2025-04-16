# Модуль Kazarinov. Создатель прайс-листов в формате PDF

## Обзор

Модуль `src.endpoints.kazarinov` предназначен для создания прайс-листов в формате PDF на основе данных, полученных от Сергея Казаринова.

## Подробней

Модуль обеспечивает интеграцию с Telegram-ботом и веб-сайтами поставщиков комплектующих для компьютеров, чтобы автоматизировать процесс создания прайс-листов.

## Описание

KazarinovTelegramBot

*   [https://one-tab.co.il](https://one-tab.co.il)
*   [https://morlevi.co.il](https://morlevi.co.il)
*   [https://grandavance.co.il](https://grandavance.co.il)
*   [https://ivory.co.il](https://ivory.co.il)
*   [https://ksp.co.il](https://ksp.co.il)

BotHandler

Client side (Kazarinov):

```mermaid
flowchart TD
    Start[Выбор комплектующих для сборки компьютера] --> Combine[Объединение в One-Tab]
    Combine --> SendToBot{Отправка ссылки One-Tab в Telegram боту}
    SendToBot -->|hypo69_kazarinov_bot| ProdBot[Telegram бот <code>prod</code>]
    SendToBot -->|hypo69_test_bot| TestBot[Telegram бот <code>test</code>]
```

Code side:

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

Следующий

*   [Kazarinov bot](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/kazarinov_bot.md)
*   [Scenario Execution](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/scenarios/README.MD)

[Root ↑](https://github.com/hypo69/hypotez/blob/master/readme.ru.md)
[Русский](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/readme.ru.md)