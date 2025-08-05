# Модуль для загрузки тестовых конфигураций агентов и фрагментов

## Обзор

Данный модуль содержит функции для загрузки тестовых конфигураций агентов и фрагментов из файлов JSON. 

## Подробней

Модуль расположен в `hypotez/src/endpoints/tiny_troupe/tinytroupe (2)/examples/loaders.py`. 
Файлы с тестовыми конфигурациями расположены в папках `agents` и `fragments`. 
Имена файлов - `name.agent.json` для агентов и `name.fragment.json` для фрагментов. 

## Функции

### `load_example_agent_specification`

**Назначение**: Загружает тестовую конфигурацию агента из файла JSON.

**Параметры**:

- `name` (str): Имя агента.

**Возвращает**:

- `dict`: Тестовая конфигурация агента.

**Как работает**:

- Функция `load_example_agent_specification` считывает содержимое файла `name.agent.json` из папки `agents`. 
- Использует `os.path.dirname(__file__)` для определения пути к текущему каталогу.
- Использует `json.load` для преобразования JSON-данных в словарь Python.

**Примеры**:

```python
>>> load_example_agent_specification('example_agent')
{'name': 'Example Agent', 'description': 'This is an example agent.', 'role': 'agent', 'type': 'text', 'language': 'ru'}
```

### `load_example_fragment_specification`

**Назначение**: Загружает тестовую конфигурацию фрагмента из файла JSON.

**Параметры**:

- `name` (str): Имя фрагмента.

**Возвращает**:

- `dict`: Тестовая конфигурация фрагмента.

**Как работает**:

- Функция `load_example_fragment_specification` считывает содержимое файла `name.fragment.json` из папки `fragments`. 
- Использует `os.path.dirname(__file__)` для определения пути к текущему каталогу.
- Использует `json.load` для преобразования JSON-данных в словарь Python.

**Примеры**:

```python
>>> load_example_fragment_specification('example_fragment')
{'name': 'Example Fragment', 'description': 'This is an example fragment.', 'type': 'text', 'content': 'Example text'}
```

### `list_example_agents`

**Назначение**: Возвращает список доступных тестовых агентов.

**Параметры**:

- Нет.

**Возвращает**:

- `list`: Список доступных тестовых агентов.

**Как работает**:

- Функция `list_example_agents` сканирует папку `agents` и извлекает имена файлов с расширением `.agent.json`.
-  Затем удаляет `.agent.json` из имени файла, оставляя только имя агента.

**Примеры**:

```python
>>> list_example_agents()
['example_agent', 'another_agent']
```

### `list_example_fragments`

**Назначение**: Возвращает список доступных тестовых фрагментов.

**Параметры**:

- Нет.

**Возвращает**:

- `list`: Список доступных тестовых фрагментов.

**Как работает**:

- Функция `list_example_fragments` сканирует папку `fragments` и извлекает имена файлов с расширением `.fragment.json`.
-  Затем удаляет `.fragment.json` из имени файла, оставляя только имя фрагмента.

**Примеры**:

```python
>>> list_example_fragments()
['example_fragment', 'another_fragment']
```