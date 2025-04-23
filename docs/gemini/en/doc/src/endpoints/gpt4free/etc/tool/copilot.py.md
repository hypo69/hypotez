# Модуль для работы с copilot для pull request.

## Обзор

Модуль предназначен для автоматического анализа pull request и создания комментариев с предложениями по улучшению кода. Он использует API g4f для получения комментариев по коду и публикует их в pull request на GitHub.

## Подробнее

Этот модуль предназначен для автоматизации процесса анализа pull request и предоставления обратной связи разработчикам. Он использует модель g4f для анализа изменений кода и создания комментариев с предложениями по улучшению. Модуль интегрируется с GitHub API для получения информации о pull request и публикации комментариев.

## Классы

### `PullRequest`

**Описание**: Класс представляет pull request на GitHub.

**Наследует**:
- Нет

**Атрибуты**:
- Нет

**Методы**:
- Нет

## Функции

### `get_pr_details`

```python
def get_pr_details(github: Github) -> PullRequest:
    """
    Извлекает детали pull request из GitHub.

    Args:
        github (Github): Объект Github для взаимодействия с GitHub API.

    Returns:
        PullRequest: Объект, представляющий pull request.
    """
```

**Назначение**: Извлечение деталей pull request из GitHub.

**Параметры**:
- `github` (Github): Объект Github для взаимодействия с GitHub API.

**Возвращает**:
- `PullRequest`: Объект, представляющий pull request.

**Как работает**:
- Функция читает номер pull request из файла `./pr_number`.
- Если номер отсутствует, функция возвращает `None`.
- Функция использует объект `github` для получения pull request по номеру из репозитория `GITHUB_REPOSITORY`.
- Функция возвращает объект `pull`, представляющий pull request.

**Пример использования**:

```python
github = Github(GITHUB_TOKEN)
pull = get_pr_details(github)
if pull:
    print(f"Pull request title: {pull.title}")
```

### `get_diff`

```python
def get_diff(diff_url: str) -> str:
    """
    Получает diff pull request по заданному URL.

    Args:
        diff_url (str): URL для diff pull request.

    Returns:
        str: Diff pull request.
    """
```

**Назначение**: Получение diff pull request по заданному URL.

**Параметры**:
- `diff_url` (str): URL для diff pull request.

**Возвращает**:
- `str`: Diff pull request.

**Как работает**:
- Функция отправляет GET-запрос по указанному `diff_url`.
- Функция проверяет статус ответа и вызывает исключение, если произошла ошибка.
- Функция возвращает текст ответа, содержащий diff pull request.

**Пример использования**:

```python
diff_url = pull.diff_url
diff = get_diff(diff_url)
print(f"Diff: {diff[:100]}...")
```

### `read_json`

```python
def read_json(text: str) -> dict:
    """
    Разбирает блок кода JSON из строки.

    Args:
        text (str): Строка, содержащая блок кода JSON.

    Returns:
        dict: Словарь, разобранный из блока кода JSON.
    """
```

**Назначение**: Разбор JSON из текста.

**Параметры**:
- `text` (str): Строка, содержащая JSON.

**Возвращает**:
- `dict`: Словарь, полученный из JSON.

**Как работает**:
- Функция ищет блок кода JSON в строке с использованием регулярного выражения.
- Функция извлекает JSON из блока кода.
- Функция пытается разобрать JSON и возвращает словарь.
- Если JSON недействителен, функция вызывает исключение `RuntimeError`.

**Пример использования**:

```python
json_string = "```json\\n{\\"key\\": \\"value\\"}\\n```"
data = read_json(json_string)
print(f"Data: {data}")
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

**Как работает**:
- Функция ищет блок кода markdown в строке с использованием регулярного выражения.
- Функция извлекает текст из блока кода.
- Если блок кода markdown не найден, функция вызывает исключение `RuntimeError`.

**Пример использования**:

```python
markdown_string = "```markdown\\nSome text\\n```"
text = read_text(markdown_string)
print(f"Text: {text}")
```

### `get_ai_response`

```python
def get_ai_response(prompt: str, as_json: bool = True) -> Union[dict, str]:
    """
    Получает ответ от g4f API на основе запроса.

    Args:
        prompt (str): Запрос для отправки в g4f.
        as_json (bool): Определяет, следует ли разбирать ответ как JSON.

    Returns:
        Union[dict, str]: Разобранный ответ от g4f, либо в виде словаря, либо в виде строки.
    """
```

**Назначение**: Получение ответа от g4f API.

**Параметры**:
- `prompt` (str): Запрос для отправки в g4f.
- `as_json` (bool): Определяет, следует ли разбирать ответ как JSON.

**Возвращает**:
- `Union[dict, str]`: Разобранный ответ от g4f, либо в виде словаря, либо в виде строки.

**Как работает**:
- Функция отправляет запрос в g4f API с использованием предоставленного `prompt`.
- Функция использует `g4f.ChatCompletion.create` для отправки запроса.
- Если `as_json` имеет значение `True`, функция разбирает ответ как JSON с использованием функции `read_json`.
- Если `as_json` имеет значение `False`, функция извлекает текст из ответа с использованием функции `read_text`.
- Функция возвращает разобранный ответ.

**Пример использования**:

```python
prompt = "Review this code."
response = get_ai_response(prompt)
print(f"Response: {response}")
```

### `analyze_code`

```python
def analyze_code(pull: PullRequest, diff: str)-> list[dict]:
    """
    Анализирует изменения кода в pull request.

    Args:
        pull (PullRequest): Объект pull request.
        diff (str): Diff pull request.

    Returns:
        list[dict]: Список комментариев, сгенерированных анализом.
    """
```

**Назначение**: Анализ изменений кода в pull request.

**Параметры**:
- `pull` (PullRequest): Объект pull request.
- `diff` (str): Diff pull request.

**Возвращает**:
- `list[dict]`: Список комментариев, сгенерированных анализом.

**Как работает**:
- Функция анализирует diff pull request построчно.
- Функция определяет измененные строки кода и формирует запрос к g4f для анализа этих строк.
- Функция получает комментарии от g4f и добавляет их в список.
- Функция возвращает список комментариев.

**Пример использования**:

```python
comments = analyze_code(pull, diff)
print(f"Comments: {comments}")
```

### `create_analyze_prompt`

```python
def create_analyze_prompt(changed_lines: list[str], pull: PullRequest, file_path: str):\n
    """
    Создает запрос для модели g4f.

    Args:
        changed_lines (list[str]): Строки кода, которые были изменены.
        pull (PullRequest): Объект pull request.
        file_path (str): Путь к файлу, который проверяется.

    Returns:
        str: Сгенерированный запрос.
    """
```

**Назначение**: Создание запроса для модели g4f.

**Параметры**:
- `changed_lines` (list[str]): Список измененных строк кода.
- `pull` (PullRequest): Объект pull request.
- `file_path` (str): Путь к анализируемому файлу.

**Возвращает**:
- `str`: Сгенерированный запрос.

**Как работает**:
- Функция создает запрос для модели g4f, включающий инструкции по анализу кода.
- Функция форматирует измененные строки кода и добавляет их в запрос.
- Функция добавляет заголовок и описание pull request в запрос.
- Функция возвращает сгенерированный запрос.

**Пример использования**:

```python
changed_lines = ["+line1", "-line2", "+line3"]
file_path = "example.py"
prompt = create_analyze_prompt(changed_lines, pull, file_path)
print(f"Prompt: {prompt}")
```

### `create_review_prompt`

```python
def create_review_prompt(pull: PullRequest, diff: str):\n
    """
    Создает запрос для создания комментария к обзору.

    Args:
        pull (PullRequest): Объект pull request.
        diff (str): Diff pull request.

    Returns:
        str: Сгенерированный запрос для обзора.
    """
```

**Назначение**: Создание запроса для создания комментария к обзору.

**Параметры**:
- `pull` (PullRequest): Объект pull request.
- `diff` (str): Diff pull request.

**Возвращает**:
- `str`: Сгенерированный запрос для обзора.

**Как работает**:
- Функция создает запрос для модели g4f, включающий инструкции по созданию комментария к обзору.
- Функция добавляет информацию об авторе, заголовке и описании pull request в запрос.
- Функция добавляет diff pull request в запрос.
- Функция возвращает сгенерированный запрос.

**Пример использования**:

```python
prompt = create_review_prompt(pull, diff)
print(f"Prompt: {prompt}")
```

### `main`

```python
def main():
    """
    Основная функция для запуска анализа pull request и создания комментариев.
    """
```

**Назначение**: Основная функция для запуска анализа pull request и создания комментариев.

**Параметры**:
- Отсутствуют.

**Возвращает**:
- Отсутствует.

**Как работает**:
- Функция получает детали pull request и diff.
- Функция создает комментарий к обзору с использованием g4f API.
- Функция анализирует код и создает комментарии с предложениями по улучшению.
- Функция публикует комментарии в pull request.

**Пример использования**:

```python
if __name__ == "__main__":
    main()
```