# Модуль Kazarinov PDF Mexiron Creator 

## Обзор

Данный модуль отвечает за создание PDF-файлов для онлайн-магазина Kazarinov с помощью сценария Mexiron. Сценарий используется для автоматизации процесса создания PDF-файлов, которые затем отправляются клиентам.

## Детали

Модуль взаимодействует с ботом в Telegram, который получает ссылки на страницы товаров из One-Tab. Ссылка отправляется в Telegram-бот, который, в свою очередь, извлекает данные о товаре из One-Tab и запускает сценарий Mexiron для генерации PDF-файла.

## Схема работы

**Клиентская сторона (Kazarinov):**

```mermaid
flowchart TD
    Start[Выбор комплектующих для сборки компьютера] --> Combine[Объединение в One-Tab]
    Combine --> SendToBot{Отправка ссылки One-Tab в Telegram боту}
    SendToBot -->|hypo69_kazarinov_bot| ProdBot[Telegram бот <code>prod</code>]
    SendToBot -->|hypo69_test_bot| TestBot[Telegram бот <code>test</code>]
```

**Серверная сторона (код):**

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

## Kazarinov Telegram Bot

**Ссылки:**

- [One-Tab](https://one-tab.co.il)
- [Morlevi](https://morlevi.co.il)
- [Grand Avance](https://grandavance.co.il)
- [Ivory](https://ivory.co.il)
- [KSP](https://ksp.co.il)

## Дополнительная информация

### Бот обработчик

**Клиентская сторона (Kazarinov):**

- Выбор комплектующих для сборки компьютера
- Объединение комплектующих в One-Tab
- Отправка ссылки One-Tab в Telegram бот

**Серверная сторона (код):**

- Проверка URL на соответствие One-Tab
- Извлечение данных из One-Tab
- Проверка корректности полученных данных
- Запуск сценария Mexiron
- Отправка сообщения о успешном завершении или ошибке

## Следующие шаги

- [Kazarinov Bot](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/kazarinov_bot.md)
- [Исполнение сценария](https://github.com/hypo69/hypotez/blob/master/src/endpoints/kazarinov/scenarios/README.MD)