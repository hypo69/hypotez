## Описание структуры JSON запроса для Gemini

Этот документ описывает структуру JSON, используемую для запросов к моделям Google Gemini. Он предоставляет детальную информацию о каждом поле и его назначении, помогая разработчикам правильно формировать запросы к API.

### Основные поля

*   **`cachedContent`** (string): Кэшированное содержимое.
*   **`contents`** (array): Массив объектов, описывающих содержимое запроса.
    *   **`role`** (string): Роль участника диалога (например, "user").
    *   **`parts`** (array): Массив объектов, описывающих части содержимого.
        *   **`text`** (string): Текстовая часть содержимого.
        *   **`inlineData`** (object): Встроенные данные. Содержит поля:
            *   `mimeType` (string): MIME-тип данных.
            *   `data` (string): Данные, закодированные в base64.
        *   **`fileData`** (object): Данные, связанные с файлом. Содержит поля:
            *   `mimeType` (string): MIME-тип файла.
            *   `fileUri` (string): URI файла.
        *   **`videoMetadata`** (object): Метаданные видео. Содержит поля:
            *   `startOffset` (object): Начальное смещение. Содержит поля:
                *   `seconds` (integer): Секунды.
                *   `nanos` (integer): Наносекунды.
            *   `endOffset` (object): Конечное смещение. Содержит поля:
                *   `seconds` (integer): Секунды.
                *   `nanos` (integer): Наносекунды.
*   **`systemInstruction`** (object): Системная инструкция.
    *   **`role`** (string): Роль.
    *   **`parts`** (array): Массив частей.
        *   **`text`** (string): Текст инструкции.
*   **`tools`** (array): Массив инструментов.
    *   **`functionDeclarations`** (array): Массив объявлений функций.
        *   **`name`** (string): Имя функции.
        *   **`description`** (string): Описание функции.
        *   **`parameters`** (object): Параметры функции.
            *   `object`: Объект параметров (требуется указать схему).
*   **`safetySettings`** (array): Массив настроек безопасности.
    *   **`category`** (enum): Категория вредоносного контента.
    *   `(HarmCategory)`: Ссылка на перечисление `HarmCategory`.
    *   **`threshold`** (enum): Порог блокировки вредоносного контента.
    *   `(HarmBlockThreshold)`: Ссылка на перечисление `HarmBlockThreshold`.
*   **`generationConfig`** (object): Конфигурация генерации.
    *   **`temperature`** (number): Температура (случайность) генерации.
    *   **`topP`** (number): Параметр Top-P для генерации.
    *   **`topK`** (number): Параметр Top-K для генерации.
    *   `candidateCount` (integer): Количество кандидатов для генерации.
    *   `maxOutputTokens` (integer): Максимальное количество выходных токенов.
    *   `presencePenalty` (float): Штраф за присутствие.
    *   `frequencyPenalty` (float): Штраф за частоту.
    *   `stopSequences` (array): Массив строк, определяющих последовательности остановки.
    *   `responseMimeType` (string): MIME-тип ответа.
    *   `responseSchema` (string): Схема ответа.
    *   `seed` (integer): Зерно для генерации случайных чисел.
    *   `responseLogprobs` (boolean): Если `True`, возвращает логарифмические вероятности для ответа.
    *   `logprobs` (integer): Количество токенов, для которых возвращаются логарифмические вероятности.
    *   `audioTimestamp` (boolean): Включает ли метки времени аудио.
*   **`labels`** (object): Объект, содержащий произвольные метки.
    *   `string`: Значение метки (string).

### Пояснения по полям

*   **Union field data**: Некоторые поля, такие как `data` внутри `parts`, являются объединениями (Union). Это означает, что можно использовать только одно из указанных полей.

### Типы данных

*   **string**: Текстовая строка.
*   **integer**: Целое число.
*   **number**: Число с плавающей точкой.
*   **boolean**: Логическое значение (true/false).
*   **array**: Массив значений.
*   **object**: Объект, содержащий пары ключ-значение.
*   **enum**: Перечисление, представляющее собой набор предопределенных значений.

### Пример структуры JSON

```json
{
  "cachedContent": "string",
  "contents": [
    {
      "role": "string",
      "parts": [
        {
          "text": "string"
        }
      ]
    }
  ],
  "systemInstruction": {
    "role": "string",
    "parts": [
      {
        "text": "string"
      }
    ]
  },
  "tools": [
    {
      "functionDeclarations": [
        {
          "name": "string",
          "description": "string",
          "parameters": {
            "object" 
          }
        }
      ]
    }
  ],
  "safetySettings": [
    {
      "category": "enum",
      "(HarmCategory)",
      "threshold": "enum",
      "(HarmBlockThreshold)"
    }
  ],
  "generationConfig": {
    "temperature": "number",
    "topP": "number",
    "topK": "number",
    "candidateCount": "integer",
    "maxOutputTokens": "integer",
    "presencePenalty": "float",
    "frequencyPenalty": "float",
    "stopSequences": [
      "string"
    ],
    "responseMimeType": "string",
    "responseSchema": "schema",
    "seed": "integer",
    "responseLogprobs": "boolean",
    "logprobs": "integer",
    "audioTimestamp": "boolean"
  },
  "labels": {
    "string": "string"
  }
}
```

В коде видны enum, стоит поискать их определения в библиотеках
Выражения `// Union field data can be only one of the following:` и подобные - это закомментированный код, который стоит убрать, если он не несет полезной информации
`// (HarmCategory)` и `// (HarmBlockThreshold)` - стоит проверить что это за константы
смысл `cachedContent` не понятен, стоит понять подробней и добавить описание

### Сокращения
`AI` - искусственный интеллект
`API` - интерфейс программирования приложений
`JSON` - нотация объектов JavaScript
`XML` - расширяемый язык разметки
`NLU` - понимание естественного языка
`URL` - унифицированный локатор ресурсов