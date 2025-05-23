# Модуль для работы с моделью OpenAI

## Обзор

Модуль предназначен для взаимодействия с моделью OpenAI для обработки исходного кода и документации. Он отправляет код в модель для анализа и получает от нее ответ.

## Детали

Модуль использует установленную роль выполнения для взаимодействия с моделью. Для роли `doc_writer` используется модель **OpenAI GPT-4** для генерации документации или других текстов.

Входные данные для модели включают комментарии и код/документацию, которые передаются в модель для обработки. Ответ модели сохраняется в файл с расширением `.md` в зависимости от роли.

### Используемые модели

- **OpenAI GPT-4**: Используется для создания документации и других текстовых материалов.

### Ссылки на документацию моделей

- OpenAI: https://platform.openai.com/docs

## Функции

### `main()`

**Описание**: Основная функция, которая обрабатывает файлы и взаимодействует с моделью.

**Параметры**: None

**Возвращает**: None

**Как работает**:

1. Считывает файл с комментариями для модели.
2. Итерирует по указанным файлам в исходной директории.
3. Отправляет содержимое файла в модель для анализа.
4. Обрабатывает ответ модели.

**Пример**:

```python
if __name__ == "__main__":
    print("Starting training ...")
    main()
```

### `save_response()`

**Описание**: Сохраняет ответ модели в файл markdown с обновленным путем, основанным на роли.

**Параметры**:

- `file_path` (Path): Исходный путь к обрабатываемому файлу.
- `response` (str): Ответ от модели для сохранения.

**Возвращает**: None

**Как работает**:

1. Создает новый путь к файлу, основанный на роли и директории.
2. Меняет суффикс файла на `.md`.
3. Сохраняет ответ в новый файл.

**Пример**:

```python
save_response(file_path=Path('path/to/file.py'), response='Model response...', from_model='openai')
```

### `yield_files_content()`

**Описание**: Возвращает содержимое файлов по заданным паттернам из исходной директории, исключая определенные паттерны и директории.

**Параметры**:

- `src_path` (Path): Базовая директория для поиска файлов.
- `patterns` (list[str]): Список паттернов файлов для включения (например, `['*.py', '*.txt']`).

**Возвращает**: 
- `Iterator[tuple[Path, str]]`: Итератор кортежей, состоящих из пути к файлу и его содержимого в виде строки.

**Как работает**:

1. Проверяет каждый файл в указанной директории.
2. Исключает файлы, которые находятся в исключаемых директориях.
3. Исключает файлы, соответствующие исключаемым паттернам.
4. Возвращает кортеж, состоящий из пути к файлу и его содержимого.

**Пример**:

```python
for file_path, content in yield_files_content(gs.path.src, ['*.py', 'README.MD']):
    print(f"File: {file_path}")
    print(f"Content: {content}")
```

## Inner Functions

### `main()`

**Описание**:  None

**Параметры**: None

**Возвращает**: None

**Как работает**:

1.  Считывает файл с комментариями для модели.
2.  Итерирует по указанным файлам в исходной директории.
3.  Отправляет содержимое файла в модель для анализа.
4.  Обрабатывает ответ модели.

**Пример**:  None

## Parameter Details

- `src_path` (Path):  Базовая директория для поиска файлов.
- `patterns` (list[str]):  Список паттернов файлов для включения (например, `['*.py', '*.txt']`).
- `file_path` (Path):  Исходный путь к обрабатываемому файлу.
- `response` (str):  Ответ от модели для сохранения.

## Examples

```python
if __name__ == "__main__":
    print("Starting training ...")
    main()
```

```python
save_response(file_path=Path('path/to/file.py'), response='Model response...', from_model='openai')
```

```python
for file_path, content in yield_files_content(gs.path.src, ['*.py', 'README.MD']):
    print(f"File: {file_path}")
    print(f"Content: {content}")
```