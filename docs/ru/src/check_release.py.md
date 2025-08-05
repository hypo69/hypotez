# Модуль проверки актуальной версии

## Обзор

Модуль предназначен для проверки актуальной версии репозитория на GitHub. Он использует API GitHub для получения информации о последнем релизе и возвращает номер версии.

## Подробней

Модуль содержит функцию `check_latest_release`, которая принимает имя репозитория и имя владельца в качестве аргументов. Функция выполняет запрос к API GitHub и возвращает номер последней версии релиза. Если запрос не удался, функция логирует ошибку и возвращает `None`.

## Функции

### `check_latest_release`

**Назначение**: Проверка последней версии релиза репозитория GitHub.

**Параметры**:
- `repo` (str): Название репозитория.
- `owner` (str): Владелец репозитория.

**Возвращает**:
- `str`: Номер последней версии релиза, если доступен.
- `None`: В случае ошибки или отсутствия релизов.

**Как работает функция**:
1. Формирует URL для запроса к API GitHub для получения информации о последнем релизе.
2. Отправляет GET-запрос к API GitHub.
3. Проверяет статус код ответа:
   - Если статус код 200 (успешно), извлекает номер версии из JSON-ответа и возвращает его.
   - Если статус код отличается от 200, логирует ошибку с использованием `logger.error` и возвращает `None`.

**Примеры**:

```python
from src.check_release import check_latest_release

latest_version = check_latest_release(repo='transformers', owner='huggingface')
if latest_version:
    print(f"Latest version: {latest_version}")
else:
    print("Could not retrieve the latest version.")

# Вывод:
# Latest version: v4.35.2 
```

```python
from src.check_release import check_latest_release

latest_version = check_latest_release(repo='nonexistent_repo', owner='some_owner')
if latest_version:
    print(f"Latest version: {latest_version}")
else:
    print("Could not retrieve the latest version.")

# Вывод в лог:
# logger.error(f"Error fetching data: {response.status_code}")
# Вывод:
# Could not retrieve the latest version.