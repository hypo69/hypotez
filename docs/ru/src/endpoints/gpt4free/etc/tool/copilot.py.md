# Модуль для работы с ассистентом программиста Copilot на основе g4f
## Обзор

Модуль предназначен для автоматического анализа Pull Request'ов в репозитории GitHub с использованием AI-моделей через библиотеку `g4f`. Он позволяет генерировать комментарии к изменениям в коде и создавать ревью для Pull Request'ов.

## Подробнее

Модуль получает информацию о Pull Request'е, анализирует изменения в коде (`diff`) и использует AI-модели для генерации комментариев и ревью. Полученные результаты отправляются в GitHub в виде комментариев к Pull Request'у или ревью.
Для работы модуль использует переменные окружения, такие как `GITHUB_TOKEN`, `GITHUB_REPOSITORY`, `G4F_PROVIDER` и `G4F_MODEL`.

## Классы

В данном модуле классы не определены.

## Функции

### `get_pr_details`

```python
def get_pr_details(github: Github) -> PullRequest:
    """
    Извлекает детали Pull Request из GitHub.

    Args:
        github (Github): Объект Github для взаимодействия с API GitHub.

    Returns:
        PullRequest: Объект, представляющий Pull Request.
    """
```

**Назначение**: Извлечение деталей Pull Request из GitHub.

**Параметры**:
- `github` (Github): Объект Github для взаимодействия с API GitHub.

**Возвращает**:
- `PullRequest`: Объект, представляющий Pull Request.

**Как работает функция**:
Функция читает номер Pull Request'а из файла `./pr_number`, а затем использует объект `github` для получения деталей Pull Request'а из репозитория GitHub. Если номер Pull Request'а не найден или файл отсутствует, функция завершается и возвращает `None`.

**Примеры**:
```python
# Пример использования функции
from github import Github

# Инициализация GitHub API
github = Github("YOUR_GITHUB_TOKEN")  # Замените на ваш токен GitHub

# Получение деталей PR
pull_request = get_pr_details(github)

if pull_request:
    print(f"PR Title: {pull_request.title}")
else:
    print("PR not found")
```

### `get_diff`

```python
def get_diff(diff_url: str) -> str:
    """
    Получает diff Pull Request'а по заданному URL.

    Args:
        diff_url (str): URL diff Pull Request'а.

    Returns:
        str: Diff Pull Request'а.
    """
```

**Назначение**: Получение diff Pull Request'а по заданному URL.

**Параметры**:
- `diff_url` (str): URL diff Pull Request'а.

**Возвращает**:
- `str`: Diff Pull Request'а.

**Как работает функция**:
Функция отправляет GET-запрос по указанному `diff_url` и возвращает текст ответа, который содержит diff Pull Request'а.

**Примеры**:
```python
# Пример использования функции
diff_url = "https://github.com/owner/repo/pull/123/files.diff"
diff_content = get_diff(diff_url)
print(diff_content[:100])  # Вывод первых 100 символов diff
```

### `read_json`

```python
def read_json(text: str) -> dict:
    """
    Разбирает блок JSON кода из строки.

    Args:
        text (str): Строка, содержащая блок JSON кода.

    Returns:
        dict: Словарь, полученный из JSON кода.
    """
```

**Назначение**: Разбор блока JSON кода из строки.

**Параметры**:
- `text` (str): Строка, содержащая блок JSON кода.

**Возвращает**:
- `dict`: Словарь, полученный из JSON кода.

**Вызывает исключения**:
- `RuntimeError`: Если JSON недействителен.

**Как работает функция**:
Функция использует регулярное выражение для поиска блока JSON кода в строке. Затем она пытается разобрать этот блок с помощью `json.loads`. Если разбор не удался, вызывается исключение `RuntimeError`.

**Примеры**:
```python
# Пример использования функции
json_text = "```json\n{\"key\": \"value\"}\n```"
data = read_json(json_text)
print(data)  # Вывод: {'key': 'value'}
```

### `read_text`

```python
def read_text(text: str) -> str:
    """
    Извлекает текст из блока кода markdown.

    Args:
        text (str): Строка, содержащая блок кода markdown.

    Returns:
        str: Извлеченный текст.
    """
```

**Назначение**: Извлечение текста из блока кода markdown.

**Параметры**:
- `text` (str): Строка, содержащая блок кода markdown.

**Возвращает**:
- `str`: Извлеченный текст.

**Вызывает исключения**:
- `RuntimeError`: Если markdown недействителен.

**Как работает функция**:
Функция использует регулярное выражение для поиска блока кода markdown в строке и извлекает текст из этого блока. Если блок кода markdown не найден, вызывается исключение `RuntimeError`.

**Примеры**:
```python
# Пример использования функции
markdown_text = "```markdown\nThis is some text.\n```"
text = read_text(markdown_text)
print(text)  # Вывод: This is some text.
```

### `get_ai_response`

```python
def get_ai_response(prompt: str, as_json: bool = True) -> Union[dict, str]:
    """
    Получает ответ от API g4f на основе запроса.

    Args:
        prompt (str): Запрос для отправки в g4f.
        as_json (bool): Определяет, следует ли разбирать ответ как JSON.

    Returns:
        Union[dict, str]: Разобранный ответ от g4f, либо как словарь, либо как строка.
    """
```

**Назначение**: Получение ответа от API g4f на основе запроса.

**Параметры**:
- `prompt` (str): Запрос для отправки в g4f.
- `as_json` (bool): Определяет, следует ли разбирать ответ как JSON.

**Возвращает**:
- `Union[dict, str]`: Разобранный ответ от g4f, либо как словарь, либо как строка.

**Как работает функция**:
Функция отправляет запрос в API `g4f` и получает ответ. Если `as_json` установлен в `True`, функция пытается разобрать ответ как JSON с помощью функции `read_json`. В противном случае функция возвращает ответ как строку.

**Примеры**:
```python
# Пример использования функции
prompt = "What is the capital of France?"
response = get_ai_response(prompt, as_json=False)
print(response)  # Вывод: The capital of France is Paris.
```

### `analyze_code`

```python
def analyze_code(pull: PullRequest, diff: str) -> list[dict]:
    """
    Анализирует изменения кода в Pull Request'е.

    Args:
        pull (PullRequest): Объект Pull Request.
        diff (str): Diff Pull Request'а.

    Returns:
        list[dict]: Список комментариев, сгенерированных анализом.
    """
```

**Назначение**: Анализ изменений кода в Pull Request'е.

**Параметры**:
- `pull` (PullRequest): Объект Pull Request.
- `diff` (str): Diff Pull Request'а.

**Возвращает**:
- `list[dict]`: Список комментариев, сгенерированных анализом.

**Как работает функция**:
Функция анализирует diff Pull Request'а построчно. Она выделяет измененные строки и формирует запросы к AI-модели для получения комментариев к этим изменениям. Полученные комментарии добавляются в список и возвращаются.

**Примеры**:
```python
# Пример использования функции
from github import Github

# Инициализация GitHub API
github = Github("YOUR_GITHUB_TOKEN")  # Замените на ваш токен GitHub

# Получение деталей PR
pull_request = get_pr_details(github)

# Получение diff
diff_content = get_diff(pull_request.diff_url)

# Анализ кода
comments = analyze_code(pull_request, diff_content)

# Вывод комментариев
for comment in comments:
    print(comment)
```

### `create_analyze_prompt`

```python
def create_analyze_prompt(changed_lines: list[str], pull: PullRequest, file_path: str) -> str:
    """
    Создает запрос для модели g4f.

    Args:
        changed_lines (list[str]): Строки кода, которые были изменены.
        pull (PullRequest): Объект Pull Request.
        file_path (str): Путь к файлу, который просматривается.

    Returns:
        str: Сгенерированный запрос.
    """
```

**Назначение**: Создание запроса для модели g4f.

**Параметры**:
- `changed_lines` (list[str]): Строки кода, которые были изменены.
- `pull` (PullRequest): Объект Pull Request.
- `file_path` (str): Путь к файлу, который просматривается.

**Возвращает**:
- `str`: Сгенерированный запрос.

**Как работает функция**:
Функция формирует запрос для AI-модели, который содержит инструкции по анализу изменений кода в Pull Request'е. Запрос включает в себя измененные строки кода, заголовок и описание Pull Request'а, а также путь к файлу.

**Примеры**:
```python
# Пример использования функции
changed_lines = ["1: def foo():", "2:     print('Hello')", "3:     print('World')"]
from github import Github

# Инициализация GitHub API
github = Github("YOUR_GITHUB_TOKEN")  # Замените на ваш токен GitHub

# Получение деталей PR
pull_request = get_pr_details(github)
file_path = "example.py"

prompt = create_analyze_prompt(changed_lines, pull_request, file_path)
print(prompt)
```

### `create_review_prompt`

```python
def create_review_prompt(pull: PullRequest, diff: str) -> str:
    """
    Создает запрос для создания комментария ревью.

    Args:
        pull (PullRequest): Объект Pull Request.
        diff (str): Diff Pull Request'а.

    Returns:
        str: Сгенерированный запрос для ревью.
    """
```

**Назначение**: Создание запроса для создания комментария ревью.

**Параметры**:
- `pull` (PullRequest): Объект Pull Request.
- `diff` (str): Diff Pull Request'а.

**Возвращает**:
- `str`: Сгенерированный запрос для ревью.

**Как работает функция**:
Функция формирует запрос для AI-модели, который содержит инструкции по созданию комментария ревью для Pull Request'а. Запрос включает в себя информацию об авторе Pull Request'а, заголовок и описание Pull Request'а, а также diff Pull Request'а.

**Примеры**:
```python
# Пример использования функции
from github import Github

# Инициализация GitHub API
github = Github("YOUR_GITHUB_TOKEN")  # Замените на ваш токен GitHub

# Получение деталей PR
pull_request = get_pr_details(github)

diff_content = "diff --git a/example.py b/example.py\nindex 1234567..890abcd 100644\n--- a/example.py\n+++ b/example.py\n@@ -1,2 +1,3 @@\n def foo():\n     print('Hello')\n+    print('World')"

prompt = create_review_prompt(pull_request, diff_content)
print(prompt)
```

### `main`

```python
def main():
    """
    Основная функция для анализа Pull Request'а и создания ревью.
    """
```

**Назначение**: Основная функция для анализа Pull Request'а и создания ревью.

**Как работает функция**:
Функция выполняет следующие шаги:
1. Инициализирует GitHub API.
2. Получает детали Pull Request'а.
3. Получает diff Pull Request'а.
4. Генерирует ревью с помощью AI-модели.
5. Анализирует код с помощью AI-модели и генерирует комментарии.
6. Отправляет ревью и комментарии в GitHub.
7. Обрабатывает исключения, которые могут возникнуть в процессе работы.

**Примеры**:
```python
# Пример использования функции
# Для запуска функции необходимо установить переменные окружения:
# GITHUB_TOKEN, GITHUB_REPOSITORY, G4F_PROVIDER, G4F_MODEL
# и создать файл ./pr_number с номером Pull Request'а.
# После этого можно запустить скрипт.
if __name__ == "__main__":
    main()