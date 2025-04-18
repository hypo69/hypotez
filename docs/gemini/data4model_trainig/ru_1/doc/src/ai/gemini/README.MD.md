# Модуль интеграции Google Generative AI

## Обзор

Класс `GoogleGenerativeAi` разработан для облегчения взаимодействия с моделями Generative AI от Google. Этот класс предоставляет методы для отправки запросов, обработки ответов, управления диалогами и интеграции с различными функциями AI. Он включает надежную обработку ошибок, ведение журнала и параметры конфигурации для обеспечения бесперебойной работы.

## Содержание

- [Ключевые функции](#ключевые-функции)
    - [`__init__`](#__init__)
    - [`config`](#config)
    - [`_start_chat`](#_start_chat)
    - [`_save_dialogue`](#_save_dialogue)
    - [`ask`](#ask)
    - [`chat`](#chat)
    - [`describe_image`](#describe_image)
    - [`upload_file`](#upload_file)
- [Обработка ошибок](#обработка-ошибок)
- [Ведение журнала и история](#ведение-журнала-и-история)
- [Зависимости](#зависимости)
- [Пример использования](#пример-использования)

## Подробней

Этот модуль предоставляет класс `GoogleGenerativeAi`, который упрощает взаимодействие с моделями Google Generative AI. Он обеспечивает методы для отправки запросов, обработки ответов и управления диалогами.

## Ключевые функции

### `__init__(self, api_key: str, model_name: Optional[str] = None, generation_config: Optional[Dict] = None, system_instruction: Optional[str] = None, **kwargs)`

**Назначение**: Инициализирует класс `GoogleGenerativeAi` с необходимыми конфигурациями.

**Параметры**:
- `api_key` (str): Ключ API для доступа к сервисам Google Generative AI.
- `model_name` (Optional[str]): Название используемой модели AI. По умолчанию `None`.
- `generation_config` (Optional[Dict]): Конфигурация генерации для модели AI. По умолчанию `None`.
- `system_instruction` (Optional[str]): Системные инструкции для модели AI. По умолчанию `None`.
- `**kwargs`: Дополнительные аргументы ключевого слова.

**Как работает функция**:
- Устанавливает ключ API, имя модели, конфигурацию генерации и системные инструкции.
- Определяет пути для ведения журнала диалогов и хранения истории.
- Инициализирует модель Google Generative AI.

### `config()`

**Назначение**: Извлекает конфигурацию из файла настроек.

**Как работает функция**:
- Читает и анализирует файл конфигурации, расположенный в `gs.path.src / 'ai' / 'gemini' / 'gemini.json'`.

### `_start_chat(self)`

**Назначение**: Запускает сеанс чата с моделью AI.

**Как работает функция**:
- Инициализирует сеанс чата с пустой историей.

### `_save_dialogue(self, dialogue: list)`

**Назначение**: Сохраняет диалог в текстовый и JSON-файлы.

**Параметры**:
- `dialogue` (list): Список сообщений в диалоге.

**Как работает функция**:
- Добавляет каждое сообщение в диалоге в текстовый файл.
- Добавляет каждое сообщение в формате JSON в JSON-файл.

### `ask(self, q: str, attempts: int = 15) -> Optional[str]`

**Назначение**: Отправляет текстовый запрос в модель AI и получает ответ.

**Параметры**:
- `q` (str): Текстовый запрос.
- `attempts` (int): Количество попыток в случае сетевых ошибок или недоступности сервиса. По умолчанию 15.

**Возвращает**:
- `Optional[str]`: Ответ от модели AI или `None` в случае ошибки.

**Как работает функция**:
- Обрабатывает несколько попыток в случае сетевых ошибок или недоступности сервиса.
- Регистрирует ошибки и повторяет попытки с экспоненциальной задержкой.
- Сохраняет диалог в файлы истории.

### `chat(self, q: str) -> str`

**Назначение**: Отправляет сообщение в чат модели AI и получает ответ.

**Параметры**:
- `q` (str): Сообщение чата.

**Возвращает**:
- `str`: Текст ответа.

**Как работает функция**:
- Использует сеанс чата, инициализированный `_start_chat`.
- Регистрирует ошибки и возвращает текст ответа.

### `describe_image(self, image_path: Path) -> Optional[str]`

**Назначение**: Генерирует текстовое описание изображения.

**Параметры**:
- `image_path` (Path): Путь к файлу изображения.

**Возвращает**:
- `Optional[str]`: Сгенерированное описание или `None`, если операция завершилась неудачно.

**Как работает функция**:
- Кодирует изображение в base64 и отправляет его в модель AI.
- Возвращает сгенерированное описание или регистрирует ошибку, если операция завершается неудачно.

### `upload_file(self, file: str | Path | IOBase, file_name: Optional[str] = None) -> bool`

**Назначение**: Загружает файл в модель AI.

**Параметры**:
- `file` (str | Path | IOBase): Файл для загрузки.
- `file_name` (Optional[str]): Имя файла. По умолчанию `None`.

**Возвращает**:
- `bool`: `True`, если загрузка прошла успешно, `False` в противном случае.

**Как работает функция**:
- Обрабатывает загрузку файла и регистрирует успех или неудачу.
- Предоставляет логику повторных попыток в случае ошибок.

## Обработка ошибок

Класс включает в себя комплексную обработку ошибок для различных сценариев:
- **Сетевые ошибки**: Повторные попытки с экспоненциальной задержкой.
- **Недоступность сервиса**: Регистрация ошибок и повторные попытки.
- **Ограничения квоты**: Регистрация и ожидание перед повторной попыткой.
- **Ошибки аутентификации**: Регистрация и прекращение дальнейших попыток.
- **Недопустимый ввод**: Регистрация и повторные попытки с тайм-аутом.
- **Ошибки API**: Регистрация и прекращение дальнейших попыток.

## Ведение журнала и история

Все взаимодействия с моделями AI регистрируются, а диалоги сохраняются в текстовом и JSON-форматах для будущего анализа. Это гарантирует, что все операции отслеживаются и могут быть просмотрены для отладки или аудита.

## Зависимости

- `google.generativeai`
- `requests`
- `grpc`
- `google.api_core.exceptions`
- `google.auth.exceptions`
- `src.logger`
- `src.utils.printer`
- `src.utils.file`
- `src.utils.date_time`
- `src.utils.convertors.unicode`
- `src.utils.jjson`

## Пример использования

```python
ai = GoogleGenerativeAi(api_key="your_api_key", system_instruction="Instruction")
response = ai.ask("Как дела?")
print(response)
```

Этот пример инициализирует класс `GoogleGenerativeAi` и отправляет запрос в модель AI, выводя ответ.