# Модуль для работы с ассистентом программиста Copilot
===============================================================

Модуль содержит функции для анализа кода, написания комментариев и создания обзоров Pull Request с помощью AI-модели Copilot.  Модуль взаимодействует с GitHub API и использует модели g4f для получения ответов.  

## TOC

- [Обзор](#обзор)
- [Функции](#функции)
    - [`get_pr_details`](#get_pr_details)
    - [`get_diff`](#get_diff)
    - [`read_json`](#read_json)
    - [`read_text`](#read_text)
    - [`get_ai_response`](#get_ai_response)
    - [`analyze_code`](#analyze_code)
    - [`create_analyze_prompt`](#create_analyze_prompt)
    - [`create_review_prompt`](#create_review_prompt)
    - [`main`](#main)

## Обзор

Модуль `copilot.py`  представляет собой  скрипт Python, который использует API GitHub и g4f для автоматизации процесса анализа кода и написания обзоров Pull Request с помощью модели Copilot.  

## Функции

### `get_pr_details`

**Назначение**: Извлекает информацию о Pull Request с GitHub по номеру.

**Параметры**:

- `github` (Github): Объект Github, который используется для взаимодействия с GitHub API.

**Возвращает**:

- `PullRequest`: Объект, представляющий Pull Request.

**Пример**:

```python
# Получение информации о Pull Request с GitHub
github = Github(GITHUB_TOKEN)
pull = get_pr_details(github)
```

**Как работает функция**:

-  Считывает номер Pull Request из файла `./pr_number`.
-  Получает репозиторий GitHub по имени `GITHUB_REPOSITORY`.
-  Получает Pull Request из репозитория по номеру.
-  Возвращает объект Pull Request.

### `get_diff`

**Назначение**: Извлекает diff Pull Request с GitHub.

**Параметры**:

- `diff_url` (str): URL diff Pull Request.

**Возвращает**:

- `str`: diff Pull Request.

**Пример**:

```python
# Получение diff Pull Request
diff_url = pull.diff_url
diff = get_diff(diff_url)
```

**Как работает функция**:

-  Выполняет запрос к URL diff Pull Request.
-  Проверяет код ответа, чтобы убедиться, что запрос был успешным.
-  Возвращает текст diff.

### `read_json`

**Назначение**: Парсит JSON код из строки.

**Параметры**:

- `text` (str): Строка, содержащая JSON код.

**Возвращает**:

- `dict`: Словарь, полученный после парсинга JSON кода.

**Пример**:

```python
# Парсинг JSON кода из строки
response = get_ai_response(prompt)
data = read_json(response)
```

**Как работает функция**:

-  Использует регулярное выражение для поиска JSON кода в строке.
-  Парсит JSON код с помощью `json.loads`.
-  Возвращает словарь.

### `read_text`

**Назначение**: Извлекает текст из markdown блока кода в строке.

**Параметры**:

- `text` (str): Строка, содержащая markdown блок кода.

**Возвращает**:

- `str`: Извлеченный текст.

**Пример**:

```python
# Извлечение текста из markdown блока кода
response = get_ai_response(prompt, as_json=False)
text = read_text(response)
```

**Как работает функция**:

-  Использует регулярное выражение для поиска markdown блока кода в строке.
-  Извлекает текст из блока кода.
-  Возвращает текст.

### `get_ai_response`

**Назначение**: Получает ответ от API g4f  на основе запроса.

**Параметры**:

- `prompt` (str): Запрос, отправляемый в g4f.
- `as_json` (bool): Флаг, указывающий, нужно ли парсить ответ как JSON.

**Возвращает**:

- `Union[dict, str]`: Парсированный ответ от g4f, либо как словарь, либо как строка.

**Пример**:

```python
# Получение ответа от API g4f
prompt = "Напиши краткий рассказ о роботе"
response = get_ai_response(prompt)
```

**Как работает функция**:

-  Создает запрос к API g4f с использованием модели `G4F_MODEL` и запроса `prompt`.
-  Парсит ответ как JSON, если `as_json` установлен в `True`, иначе извлекает текст.
-  Возвращает ответ.

### `analyze_code`

**Назначение**: Анализирует изменения кода в Pull Request.

**Параметры**:

- `pull` (PullRequest): Объект Pull Request.
- `diff` (str): diff Pull Request.

**Возвращает**:

- `list[dict]`: Список комментариев, сгенерированных анализом.

**Пример**:

```python
# Анализ кода
comments = analyze_code(pull, diff)
```

**Как работает функция**:

-  Итерация по строкам diff.
-  Идентификация измененных строк кода.
-  Создание запроса к g4f для анализа кода.
-  Парсинг ответа от g4f.
-  Добавление комментариев в список `comments`.

### `create_analyze_prompt`

**Назначение**: Создает запрос для g4f.

**Параметры**:

- `changed_lines` (list[str]): Измененные строки кода.
- `pull` (PullRequest): Объект Pull Request.
- `file_path` (str): Путь к файлу.

**Возвращает**:

- `str`: Сгенерированный запрос.

**Пример**:

```python
# Создание запроса
prompt = create_analyze_prompt(changed_lines, pull, file_path)
```

**Как работает функция**:

-  Форматирование измененных строк кода в виде блока кода.
-  Создание запроса для g4f, содержащего:
    -  Инструкции для модели.
    -  Описание Pull Request (заголовок и описание).
    -  Измененный код.

### `create_review_prompt`

**Назначение**: Создает запрос для создания комментария к обзору.

**Параметры**:

- `pull` (PullRequest): Объект Pull Request.
- `diff` (str): diff Pull Request.

**Возвращает**:

- `str`: Сгенерированный запрос для обзора.

**Пример**:

```python
# Создание запроса
prompt = create_review_prompt(pull, diff)
```

**Как работает функция**:

-  Форматирование diff Pull Request в виде блока кода.
-  Создание запроса для g4f, содержащего:
    -  Инструкции для модели.
    -  Описание Pull Request (заголовок и описание).
    -  diff Pull Request.

### `main`

**Назначение**: Главный метод, который запускает процесс анализа кода и создание обзора Pull Request.

**Пример**:

```python
# Запуск главного метода
if __name__ == "__main__":
    main()
```

**Как работает функция**:

-  Получение информации о Pull Request.
-  Получение diff Pull Request.
-  Создание обзора с помощью g4f.
-  Анализ кода с помощью g4f.
-  Опубликование комментариев к обзору.
-  Опубликование обзора Pull Request.

## Параметры

### `GITHUB_TOKEN`

-  **Описание**: Токен доступа к API GitHub.

### `GITHUB_REPOSITORY`

-  **Описание**: Название репозитория GitHub.

### `G4F_PROVIDER`

-  **Описание**:  Имя провайдера g4f.

### `G4F_MODEL`

-  **Описание**: Имя модели g4f.

## Примеры

### Пример 1: Анализ кода

```python
# Создание объекта Github
github = Github(GITHUB_TOKEN)

# Получение информации о Pull Request
pull = get_pr_details(github)

# Получение diff Pull Request
diff = get_diff(pull.diff_url)

# Анализ кода
comments = analyze_code(pull, diff)

# Вывод комментариев
print("Comments:", comments)
```

### Пример 2: Создание обзора Pull Request

```python
# Создание объекта Github
github = Github(GITHUB_TOKEN)

# Получение информации о Pull Request
pull = get_pr_details(github)

# Получение diff Pull Request
diff = get_diff(pull.diff_url)

# Создание обзора с помощью g4f
review = get_ai_response(create_review_prompt(pull, diff), False)

# Опубликование обзора
pull.create_issue_comment(body=review)
```

### Пример 3: Анализ кода с комментариями

```python
# Создание объекта Github
github = Github(GITHUB_TOKEN)

# Получение информации о Pull Request
pull = get_pr_details(github)

# Получение diff Pull Request
diff = get_diff(pull.diff_url)

# Анализ кода с комментариями
comments = analyze_code(pull, diff)

# Опубликование комментариев
if comments:
    pull.create_review(body=review, comments=comments)
else:
    pull.create_issue_comment(body=review)
```