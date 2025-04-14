# Модуль для автоматического анализа Pull Request с использованием AI
## Обзор

Модуль предназначен для автоматического анализа изменений кода в Pull Request на GitHub с использованием AI моделей (g4f API). Он позволяет генерировать комментарии и предложения по улучшению кода, а также создавать общие ревью Pull Request.

## Подробней

Этот модуль используется для автоматизации процесса проверки кода в проекте `hypotez`. Он извлекает информацию о Pull Request, анализирует изменения в коде, генерирует комментарии и создает ревью, используя AI.

## Классы

В данном модуле классы отсутствуют.

## Функции

### `get_pr_details`

```python
def get_pr_details(github: Github) -> PullRequest:
    """
    Retrieves the details of the pull request from GitHub.

    Args:
        github (Github): The Github object to interact with the GitHub API.

    Returns:
        PullRequest: An object representing the pull request.
    """
    ...
```

**Назначение**: Получение деталей Pull Request из GitHub.

**Параметры**:
- `github` (Github): Объект Github для взаимодействия с API GitHub.

**Возвращает**:
- `PullRequest`: Объект, представляющий Pull Request.

**Как работает функция**:
- Функция считывает номер Pull Request из файла `./pr_number`.
- Затем использует API GitHub для получения деталей Pull Request по номеру.

**Примеры**:

```python
from github import Github
#Предположим, что GITHUB_TOKEN - это ваш токен GitHub
github = Github(GITHUB_TOKEN) 
pull_request = get_pr_details(github)
if pull_request:
    print(f"Pull Request title: {pull_request.title}")
```

### `get_diff`

```python
def get_diff(diff_url: str) -> str:
    """
    Fetches the diff of the pull request from a given URL.

    Args:
        diff_url (str): URL to the pull request diff.

    Returns:
        str: The diff of the pull request.
    """
    ...
```

**Назначение**: Получение diff Pull Request по URL.

**Параметры**:
- `diff_url` (str): URL diff Pull Request.

**Возвращает**:
- `str`: Diff Pull Request.

**Как работает функция**:
- Функция отправляет GET-запрос по указанному URL и возвращает текст ответа, который содержит diff Pull Request.

**Примеры**:

```python
diff_url = "https://github.com/owner/repo/pull/123.diff"
diff = get_diff(diff_url)
print(f"Diff: {diff[:100]}...")
```

### `read_json`

```python
def read_json(text: str) -> dict:
    """
    Parses JSON code block from a string.

    Args:
        text (str): A string containing a JSON code block.

    Returns:
        dict: A dictionary parsed from the JSON code block.
    """
    ...
```

**Назначение**: Разбор JSON из строки.

**Параметры**:
- `text` (str): Строка, содержащая блок кода JSON.

**Возвращает**:
- `dict`: Словарь, полученный из блока кода JSON.

**Вызывает исключения**:
- `RuntimeError`: Если JSON недействителен.

**Как работает функция**:
- Функция ищет блок кода JSON в строке, используя регулярное выражение.
- Затем пытается разобрать JSON и возвращает словарь.

**Примеры**:

```python
json_string = "```json\n{\"key\": \"value\"}\n```"
data = read_json(json_string)
print(f"Data: {data}")
```

### `read_text`

```python
def read_text(text: str) -> str:
    """
    Extracts text from a markdown code block.

    Args:
        text (str): A string containing a markdown code block.

    Returns:
        str: The extracted text.
    """
    ...
```

**Назначение**: Извлечение текста из блока кода markdown.

**Параметры**:
- `text` (str): Строка, содержащая блок кода markdown.

**Возвращает**:
- `str`: Извлеченный текст.

**Вызывает исключения**:
- `RuntimeError`: Если markdown недействителен.

**Как работает функция**:
- Функция ищет блок кода markdown в строке, используя регулярное выражение.
- Затем извлекает текст из блока кода и возвращает его.

**Примеры**:

```python
markdown_string = "```markdown\nSome text\n```"
text = read_text(markdown_string)
print(f"Text: {text}")
```

### `get_ai_response`

```python
def get_ai_response(prompt: str, as_json: bool = True) -> Union[dict, str]:
    """
    Gets a response from g4f API based on the prompt.

    Args:
        prompt (str): The prompt to send to g4f.
        as_json (bool): Whether to parse the response as JSON.

    Returns:
        Union[dict, str]: The parsed response from g4f, either as a dictionary or a string.
    """
    ...
```

**Назначение**: Получение ответа от g4f API на основе запроса.

**Параметры**:
- `prompt` (str): Запрос для отправки в g4f.
- `as_json` (bool): Флаг, указывающий, следует ли разбирать ответ как JSON. По умолчанию `True`.

**Возвращает**:
- `Union[dict, str]`: Разобранный ответ от g4f, либо как словарь, либо как строка.

**Как работает функция**:
- Функция отправляет запрос в g4f API с указанным запросом.
- Если `as_json` установлен в `True`, функция пытается разобрать ответ как JSON и возвращает словарь. В противном случае функция возвращает текст ответа.

**Примеры**:

```python
prompt = "Translate 'hello' to Russian"
response = get_ai_response(prompt, as_json=False)
print(f"Response: {response}")
```

### `analyze_code`

```python
def analyze_code(pull: PullRequest, diff: str)-> list[dict]:
    """
    Analyzes the code changes in the pull request.

    Args:
        pull (PullRequest): The pull request object.
        diff (str): The diff of the pull request.

    Returns:
        list[dict]: A list of comments generated by the analysis.
    """
    ...
```

**Назначение**: Анализ изменений кода в Pull Request.

**Параметры**:
- `pull` (PullRequest): Объект Pull Request.
- `diff` (str): Diff Pull Request.

**Возвращает**:
- `list[dict]`: Список комментариев, сгенерированных анализом.

**Как работает функция**:
- Функция анализирует diff Pull Request, разбивает его на строки и ищет изменения в коде.
- Для каждого измененного участка кода функция создает запрос к AI модели (через `create_analyze_prompt`) и получает ответ с комментариями.
- Сгенерированные комментарии добавляются в список и возвращаются.

**Примеры**:

```python
from github import Github
#Предположим, что GITHUB_TOKEN - это ваш токен GitHub
github = Github(GITHUB_TOKEN)
pull_request = get_pr_details(github)
if pull_request:
    diff = get_diff(pull_request.diff_url)
    comments = analyze_code(pull_request, diff)
    print(f"Comments: {comments}")
```

### `create_analyze_prompt`

```python
def create_analyze_prompt(changed_lines: list[str], pull: PullRequest, file_path: str):
    """
    Creates a prompt for the g4f model.

    Args:
        changed_lines (list[str]): The lines of code that have changed.
        pull (PullRequest): The pull request object.
        file_path (str): The path to the file being reviewed.

    Returns:
        str: The generated prompt.
    """
    ...
```

**Назначение**: Создание запроса для модели g4f.

**Параметры**:
- `changed_lines` (list[str]): Измененные строки кода.
- `pull` (PullRequest): Объект Pull Request.
- `file_path` (str): Путь к файлу, который проверяется.

**Возвращает**:
- `str`: Сгенерированный запрос.

**Как работает функция**:
- Функция принимает измененные строки кода, объект Pull Request и путь к файлу.
- Формирует запрос к модели g4f, включая инструкции по анализу кода и предоставлению комментариев в определенном формате JSON.
- Важно, чтобы запрос содержал контекст Pull Request (заголовок и описание) и код для анализа.

**Примеры**:

```python
from github import Github
#Предположим, что GITHUB_TOKEN - это ваш токен GitHub
github = Github(GITHUB_TOKEN)
pull_request = get_pr_details(github)
if pull_request:
    diff = get_diff(pull_request.diff_url)
    changed_lines = diff.split('\n') # Имитация измененных строк
    file_path = "example.py"
    prompt = create_analyze_prompt(changed_lines, pull_request, file_path)
    print(f"Prompt: {prompt}")
```

### `create_review_prompt`

```python
def create_review_prompt(pull: PullRequest, diff: str):
    """
    Creates a prompt to create a review comment.

    Args:
        pull (PullRequest): The pull request object.
        diff (str): The diff of the pull request.

    Returns:
        str: The generated prompt for review.
    """
    ...
```

**Назначение**: Создание запроса для создания комментария ревью.

**Параметры**:
- `pull` (PullRequest): Объект Pull Request.
- `diff` (str): Diff Pull Request.

**Возвращает**:
- `str`: Сгенерированный запрос для ревью.

**Как работает функция**:
- Функция принимает объект Pull Request и diff Pull Request.
- Формирует запрос к AI модели, включая инструкции по написанию ревью в стиле g4f copilot, с учетом автора, заголовка и описания Pull Request.
- Запрос также содержит diff Pull Request для анализа.

**Примеры**:

```python
from github import Github
#Предположим, что GITHUB_TOKEN - это ваш токен GitHub
github = Github(GITHUB_TOKEN)
pull_request = get_pr_details(github)
if pull_request:
    diff = get_diff(pull_request.diff_url)
    prompt = create_review_prompt(pull_request, diff)
    print(f"Prompt: {prompt}")
```

### `main`

```python
def main():
    """
    The main function of the script.
    """
    ...
```

**Назначение**: Главная функция скрипта.

**Как работает функция**:
- Функция выполняет следующие шаги:
    - Инициализирует объект `Github` с использованием токена доступа.
    - Получает детали Pull Request с помощью функции `get_pr_details`.
    - Получает diff Pull Request с помощью функции `get_diff`.
    - Создает запрос для ревью с помощью функции `create_review_prompt`.
    - Получает ответ от AI модели с помощью функции `get_ai_response`.
    - Если Pull Request уже имеет ревью или комментарии, функция создает комментарий к задаче с ревью.
    - В противном случае функция анализирует код с помощью функции `analyze_code` и создает ревью с комментариями, если они есть.

**Примеры**:
Запуск функции `main`
```python
if __name__ == "__main__":
    main()