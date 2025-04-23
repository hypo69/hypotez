# Документация для разработчика: request.json

## Обзор

Данный файл (`request.json`) описывает структуру JSON-запроса, используемого для взаимодействия с моделью Google Gemini. Он содержит параметры для настройки запроса, такие как контент, системные инструкции, инструменты, настройки безопасности, конфигурацию генерации и метки.

## Подробнее

Файл `request.json` содержит определение структуры запроса, отправляемого к API Google Gemini. Эта структура определяет, какие данные и параметры можно передавать в запросе для получения ответов от модели. 
В этом файле описываются различные поля, такие как `cachedContent`, `contents`, `systemInstruction`, `tools`, `safetySettings`, `generationConfig` и `labels`, которые позволяют настраивать поведение модели и получать желаемые результаты.

## Структура JSON

### `cachedContent`

- **Описание**: Закешированный контент.
- **Тип**: `string`

### `contents`

- **Описание**: Массив объектов, представляющих содержимое запроса. Каждый объект содержит роль и части контента.
- **Тип**: `array`
- **Элементы массива**:
  - `role`: Роль контента (`string`).
  - `parts`: Массив частей контента.
    - **Типы данных (Union field data)**: Может быть одним из следующих:
      - `text`: Текст (`string`).
      - `inlineData`: Встроенные данные.
        - `mimeType`: MIME-тип данных (`string`).
        - `data`: Данные (`string`).
      - `fileData`: Данные файла.
        - `mimeType`: MIME-тип файла (`string`).
        - `fileUri`: URI файла (`string`).
      - `videoMetadata`: Метаданные видео.
        - `startOffset`: Начальное смещение.
          - `seconds`: Секунды (`integer`).
          - `nanos`: Наносекунды (`integer`).
        - `endOffset`: Конечное смещение.
          - `seconds`: Секунды (`integer`).
          - `nanos`: Наносекунды (`integer`).

### `systemInstruction`

- **Описание**: Системные инструкции для модели.
- **Тип**: `object`
  - `role`: Роль инструкции (`string`).
  - `parts`: Массив частей инструкции.
    - `text`: Текст инструкции (`string`).

### `tools`

- **Описание**: Массив инструментов, доступных для модели.
- **Тип**: `array`
- **Элементы массива**:
  - `functionDeclarations`: Массив объявлений функций.
    - `name`: Имя функции (`string`).
    - `description`: Описание функции (`string`).
    - `parameters`: Параметры функции (`object`).

### `safetySettings`

- **Описание**: Настройки безопасности.
- **Тип**: `array`
- **Элементы массива**:
  - `category`: Категория (`enum (HarmCategory)`).
  - `threshold`: Порог (`enum (HarmBlockThreshold)`).

### `generationConfig`

- **Описание**: Конфигурация генерации.
- **Тип**: `object`
  - `temperature`: Температура (`number`).
  - `topP`: Top P (`number`).
  - `topK`: Top K (`number`).
  - `candidateCount`: Количество кандидатов (`integer`).
  - `maxOutputTokens`: Максимальное количество выходных токенов (`integer`).
  - `presencePenalty`: Штраф за присутствие (`float`).
  - `frequencyPenalty`: Штраф за частоту (`float`).
  - `stopSequences`: Массив последовательностей остановки (`array` of `string`).
  - `responseMimeType`: MIME-тип ответа (`string`).
  - `responseSchema`: Схема ответа (`schema`).
  - `seed`: Зерно (`integer`).
  - `responseLogprobs`: Возвращать ли вероятности логов ответа (`boolean`).
  - `logprobs`: Количество вероятностей логов (`integer`).
  - `audioTimestamp`: Временная метка аудио (`boolean`).

### `labels`

- **Описание**: Метки.
- **Тип**: `object`
- **Ключ-значение**: `string: string`