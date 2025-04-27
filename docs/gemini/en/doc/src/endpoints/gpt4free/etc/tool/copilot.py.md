# Модуль для работы с помощником программиста
=================================================

Модуль содержит функции для взаимодействия с моделями искусственного интеллекта (например, Google Gemini и OpenAI) и выполнения задач по обработке кода.

## Содержание
- [Введение](#Введение)
- [Функции](#Функции)
    - [`get_pr_details(github: Github) -> PullRequest`](#get_pr_detailsgithub-github--pullrequest)
    - [`get_diff(diff_url: str) -> str`](#get_diffdiff_url-str--str)
    - [`read_json(text: str) -> dict`](#read_jsontext-str--dict)
    - [`read_text(text: str) -> str`](#read_texttext-str--str)
    - [`get_ai_response(prompt: str, as_json: bool = True) -> Union[dict, str]`](#get_ai_responseprompt-str-as_json-bool--true--uniondict-str)
    - [`analyze_code(pull: PullRequest, diff: str) -> list[dict]`](#analyze_codepull-pullrequest-diff-str--listdict)
    - [`create_analyze_prompt(changed_lines: list[str], pull: PullRequest, file_path: str)`](#create_analyze_promptchanged_lines-liststr-pull-pullrequest-file_path-str)
    - [`create_review_prompt(pull: PullRequest, diff: str)`](#create_review_promptpull-pullrequest-diff-str)
    - [`main()`](#main)
- [Пример использования](#Пример-использования)

## Введение

Модуль предназначен для автоматизированной проверки и анализа кода pull-запросов на GitHub. 
Он взаимодействует с моделями искусственного интеллекта (AI) для генерации комментариев к коду и создания обзоров pull-запросов.

## Функции

### `get_pr_details(github: Github) -> PullRequest`

Функция извлекает информацию о pull-запросе из GitHub.

#### Параметры:

- `github (Github)`: Объект Github, используемый для взаимодействия с API GitHub.

#### Возвращает:

- `PullRequest`: Объект, представляющий pull-запрос.

#### Пример использования:

```python
from github import Github

github = Github("YOUR_GITHUB_TOKEN")
pull = get_pr_details(github)
```

### `get_diff(diff_url: str) -> str`

Функция извлекает diff-код pull-запроса по заданному URL.

#### Параметры:

- `diff_url (str)`: URL diff-файла pull-запроса.

#### Возвращает:

- `str`: Diff-код pull-запроса.

#### Пример использования:

```python
diff_url = "https://github.com/example/repo/pull/123/files"
diff = get_diff(diff_url)
```

### `read_json(text: str) -> dict`

Функция парсит JSON-код из строки.

#### Параметры:

- `text (str)`: Строка, содержащая JSON-код.

#### Возвращает:

- `dict`: Словарь, полученный из JSON-кода.

#### Пример использования:

```python
text = '{"name": "Alice", "age": 30}'
data = read_json(text)
```

### `read_text(text: str) -> str`

Функция извлекает текст из markdown-блока кода.

#### Параметры:

- `text (str)`: Строка, содержащая markdown-блок кода.

#### Возвращает:

- `str`: Извлеченный текст.

#### Пример использования:

```python
text = "```markdown\nThis is a markdown code block.\n```"
markdown_text = read_text(text)
```

### `get_ai_response(prompt: str, as_json: bool = True) -> Union[dict, str]`

Функция получает ответ от AI-модели (g4f) на основе заданного запроса.

#### Параметры:

- `prompt (str)`: Запрос для отправки AI-модели.
- `as_json (bool)`: Флаг, указывающий, следует ли парсить ответ как JSON. По умолчанию `True`.

#### Возвращает:

- `Union[dict, str]`: Парсированный ответ AI-модели в виде словаря или строки.

#### Пример использования:

```python
prompt = "Write a short story about a cat."
response = get_ai_response(prompt)
```

### `analyze_code(pull: PullRequest, diff: str) -> list[dict]`

Функция анализирует изменения кода в pull-запросе и генерирует комментарии.

#### Параметры:

- `pull (PullRequest)`: Объект pull-запроса.
- `diff (str)`: Diff-код pull-запроса.

#### Возвращает:

- `list[dict]`: Список сгенерированных комментариев.

#### Пример использования:

```python
comments = analyze_code(pull, diff)
```

### `create_analyze_prompt(changed_lines: list[str], pull: PullRequest, file_path: str)`

Функция формирует запрос для AI-модели для анализа кода.

#### Параметры:

- `changed_lines (list[str])`: Список строк кода, которые были изменены.
- `pull (PullRequest)`: Объект pull-запроса.
- `file_path (str)`: Путь к файлу, который анализируется.

#### Возвращает:

- `str`: Сгенерированный запрос для AI-модели.

#### Пример использования:

```python
prompt = create_analyze_prompt(changed_lines, pull, file_path)
```

### `create_review_prompt(pull: PullRequest, diff: str)`

Функция формирует запрос для AI-модели для создания обзора pull-запроса.

#### Параметры:

- `pull (PullRequest)`: Объект pull-запроса.
- `diff (str)`: Diff-код pull-запроса.

#### Возвращает:

- `str`: Сгенерированный запрос для AI-модели.

#### Пример использования:

```python
prompt = create_review_prompt(pull, diff)
```

### `main()`

Функция, которая запускает основной процесс анализа pull-запроса и публикации отзыва.

#### Пример использования:

```python
main()
```

## Пример использования

```python
# Загрузка необходимых библиотек
from github import Github
from hypotez.src.endpoints.gpt4free.etc.tool.copilot import get_pr_details, get_diff, analyze_code, create_review_prompt

# Получение токена GitHub из переменной окружения
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Инициализация объекта GitHub
github = Github(GITHUB_TOKEN)

# Получение информации о pull-запросе
pull = get_pr_details(github)

# Получение diff-кода pull-запроса
diff = get_diff(pull.diff_url)

# Анализ изменений кода и генерация комментариев
comments = analyze_code(pull, diff)

# Создание запроса для AI-модели для обзора pull-запроса
review_prompt = create_review_prompt(pull, diff)

# Вывод сгенерированных комментариев
print("Comments:", comments)

# Вывод запроса для AI-модели
print("Review prompt:", review_prompt)

# Отправка запроса AI-модели и получение ответа (не показано в этом примере)
# ...

# Публикация обзора pull-запроса на GitHub (не показано в этом примере)
# ...
```

## Замечания
- Модуль использует g4f для взаимодействия с AI-моделями. 
- В нем используется библиотека `github` для взаимодействия с GitHub API.
- Для проверки pull-запросов используется `driver` из `src.webdirver`.
-  `Driver`, `Chrome`, `Firefox`, `Playwright` modules уже содержат все настройки Selenium.
-  Основная команда, используемая в коде: `driver.execute_locator(l:dict)`. Она возвращает значение веб-элемента по локатору.