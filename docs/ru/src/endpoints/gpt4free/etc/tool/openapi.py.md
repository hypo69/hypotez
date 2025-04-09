# Модуль для создания OpenAPI спецификации

## Обзор

Этот модуль предназначен для генерации OpenAPI спецификации для g4f API и сохранения её в файл `openapi.json`. OpenAPI спецификация используется для описания структуры API, включая доступные эндпоинты, параметры и форматы запросов и ответов.

## Подробней

Модуль использует библиотеку `g4f` для создания приложения и последующего получения OpenAPI спецификации. Спецификация сохраняется в формате JSON в файл `openapi.json`. Это позволяет документировать API и использовать его для генерации клиентского кода или интеграции с другими системами.

## Функции

### `create_app`

```python
def create_app():
    """Функция создает и возвращает экземпляр приложения g4f API.

    Returns:
        FastAPI: Экземпляр приложения FastAPI.

    """
```

**Назначение**: Создает и возвращает экземпляр приложения g4f API.

**Возвращает**:
- `FastAPI`: Экземпляр приложения FastAPI.

**Как работает функция**:
1. Функция `create_app()` из модуля `g4f.api` вызывается для создания приложения.
2. Возвращается созданный экземпляр приложения FastAPI.

**Примеры**:
```python
from g4f.api import create_app

app = create_app()
print(type(app))  # Вывод: <class 'fastapi.applications.FastAPI'>
```

### `app.openapi()`

```python
def openapi():
    """Функция генерирует OpenAPI спецификацию для приложения.

    Returns:
        dict: Словарь, представляющий OpenAPI спецификацию в формате JSON.
    """
```

**Назначение**: Генерирует OpenAPI спецификацию для приложения.

**Возвращает**:
- `dict`: Словарь, представляющий OpenAPI спецификацию в формате JSON.

**Как работает функция**:
1. Функция `openapi()` вызывается для экземпляра приложения `app`.
2. Возвращается словарь, содержащий OpenAPI спецификацию.

**Примеры**:
```python
from g4f.api import create_app

app = create_app()
openapi_spec = app.openapi()
print(type(openapi_spec))  # Вывод: <class 'dict'>
```

## Использование
```python
import json
from g4f.api import create_app

app = create_app()

with open("openapi.json", "w") as f:
    data = json.dumps(app.openapi())
    f.write(data)

print(f"openapi.json - {round(len(data)/1024, 2)} kbytes")