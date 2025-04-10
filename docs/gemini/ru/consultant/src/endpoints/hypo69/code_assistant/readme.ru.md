### **Анализ кода модуля `readme.ru.md`**

#### 2. **Качество кода**:
   - **Соответствие стандартам**: 9/10
   - **Плюсы**:
     - Подробное описание модуля и его функциональности.
     - Четкая структура документации с заголовками и подзаголовками.
     - Примеры использования с командами запуска.
     - Описание параметров командной строки и логики работы.
     - Указаны исключения и зависимости.
   - **Минусы**:
     - Отсутствует описание структуры файлов `onela_bot.py` и `bot_handlers.py`.
     - Нет информации об обработке ошибок и повторных попытках при взаимодействии с моделями.

#### 3. **Рекомендации по улучшению**:
   - Добавить описание структуры файлов `onela_bot.py` и `bot_handlers.py`, чтобы пользователи понимали их взаимодействие и назначение.
   - Описать обработку ошибок и повторные попытки при взаимодействии с моделями, чтобы пользователи знали, как обрабатываются сбои.
   - Добавить информацию о процессе логирования и примеры записей, чтобы пользователи понимали, какие данные логируются и как их можно использовать.
   - Улучшить раздел "Создание новой роли для моделей ИИ", добавив более подробные инструкции и примеры.

#### 4. **Оптимизированный код**:
```markdown
# Модуль `Code Assistant`

## Обзор

Модуль `Code Assistant` представляет собой набор инструментов для взаимодействия с моделями **Gemini** и **OpenAI** с целью обработки исходного кода проекта. Он выполняет задачи, такие как создание документации, проверка кода и генерация тестов на основе указанных файлов. Также включает скрипты для создания файла `SUMMARY.md` для компиляции документации и Telegram-бота для обработки задач, связанных с кодом.

## Основные возможности

### `code_assistant.py`
- **Чтение файлов**: Читает код из файлов с расширениями `.py` и `README.MD` в указанных директориях.
- **Взаимодействие с моделями**: Отправляет код в модели для выполнения задач, таких как создание документации или проверка ошибок.
- **Генерация результатов**: Сохраняет ответы моделей в указанные директории для каждой роли.

### `make_summary.py`
- **Генерация `SUMMARY.md`**: Рекурсивно обходит директорию для создания файла `SUMMARY.md` для компиляции документации.
- **Фильтрация по языку**: Поддерживает фильтрацию файлов по языку (`ru` или `en`).

### `onela_bot.py` и `bot_handlers.py`
- **Telegram-бот**: Бот для обработки задач, связанных с кодом, таких как отправка фрагментов кода на проверку или генерация документации.
- **Обработчики бота**: Содержит обработчики для команд и сообщений бота.

#### Структура `onela_bot.py` и `bot_handlers.py`
- `onela_bot.py`: Основной файл бота, содержащий логику запуска и обработки команд.
- `bot_handlers.py`: Файл, содержащий обработчики для различных команд и сообщений бота.

## Структура проекта

- **Модели**: Используются модели **Gemini** и **OpenAI** для обработки запросов.
- **Промпты**: Читает промпты из файлов в директории `src/ai/prompts/developer/` (например, `doc_writer_en.md`).
- **Файлы**: Обрабатываются файлы с расширениями `.py` и `README.MD` в указанных директориях.

## Примеры использования

### Запуск с настройками из JSON:
```bash
python code_assistant.py --settings settings.json
```

### Запуск с явным указанием параметров:
```bash
python code_assistant.py --role doc_writer --lang ru --models gemini openai --start_dirs /path/to/dir1 /path/to/dir2
```

### Пример для роли `code_checker`:
```bash
python code_assistant.py --role code_checker --lang en --models gemini --start_dirs /path/to/dir
```

### Пример для модели `openai`:
```bash
python code_assistant.py --role doc_writer --lang en --models openai
```

## Параметры командной строки

- `--settings`: Путь к JSON-файлу с настройками. Загружает параметры из файла.
- `--role`: Роль модели для выполнения задачи (например, `doc_writer`, `code_checker`).
- `--lang`: Язык выполнения задачи (например, `ru` или `en`).
- `--models`: Список моделей для инициализации (например, `gemini`, `openai`).
- `--start_dirs`: Список директорий для обработки (например, `/path/to/dir1`).

## Логика работы

1. **Чтение файлов**: Ищет файлы с расширениями `.py` и `README.MD` в указанных директориях.
2. **Загрузка промптов**: Загружает промпты для каждой роли из директории `src/ai/prompts/developer/`.
3. **Обработка запросов**: Формирует запросы на основе загруженных файлов и отправляет их в модели.
4. **Сохранение ответов**: Сохраняет ответы моделей в директории, соответствующие роли и модели (например, `docs/raw_rst_from_<model>/<lang>/`).

## Обработка ошибок и повторные попытки

При взаимодействии с моделями могут возникать ошибки, связанные с сетевыми проблемами или неправильными запросами. Для обработки таких ситуаций используются следующие механизмы:
- **Повторные попытки**: В случае ошибки делается несколько повторных попыток отправки запроса.
- **Логирование ошибок**: Все ошибки логируются с использованием библиотеки `logger` для последующего анализа.

## Исключения

Настройка исключений для файлов и директорий с помощью параметров:
- `exclude_file_patterns`: Список регулярных выражений для исключения файлов.
- `exclude_dirs`: Список директорий для исключения.
- `exclude_files`: Список файлов для исключения.

## Логирование

Логи сохраняются с помощью библиотеки `logger` и содержат информацию о процессе обработки файлов и полученных ответах.

Примеры записей лога:
- `INFO: Запущен процесс обработки файлов.`
- `ERROR: Ошибка при отправке запроса в модель: ...`
- `DEBUG: Получен ответ от модели: ...`

## Зависимости

- **Gemini API**: Требуется API-ключ для работы с моделью Gemini.
- **OpenAI API**: Требуется API-ключ для работы с моделью OpenAI.

## Создание новой роли для моделей ИИ

1. **Обновление `code_assistant.json`**:
   - Добавьте новую роль в список ролей:
     ```json
     "roles": [
       "code_checker",
       "new_role",
       ...
     ]
     ```
   - Или исключите её в `"exclude-roles"`.

2. **Добавление роли в переводы**:
   - Обновите файл `translations/translations.json` с новой ролью.

3. **Создание системного промпта**:
   - Добавьте новый системный промпт в директорию `ai/prompts/developer/`.

4. **Создание командной инструкции**:
   - Добавьте новую команду в директорию `instructions/`.

   - Пример создания командной инструкции:
     - Создайте файл `new_role_instruction.md` в директории `instructions/`.
     - Опишите в файле задачу, которую должна выполнять новая роль.