# Модуль запуска API gpt4free

## Обзор

Этот модуль является точкой входа для запуска API gpt4free. Он использует argparse для обработки аргументов командной строки и запуска API с заданными параметрами.

## Подробней

Модуль `__main__.py` отвечает за запуск API `gpt4free`. Он импортирует необходимые функции из модуля `cli` для парсинга аргументов командной строки и запуска API с заданными параметрами. Если аргумент `gui` не указан, он устанавливается в `True`.

## Функции

### `get_api_parser`

```python
def get_api_parser() -> argparse.ArgumentParser:
    """
    Возвращает объект ArgumentParser для парсинга аргументов командной строки.

    Args:
        Нет

    Returns:
        argparse.ArgumentParser: Объект ArgumentParser.
    """
    ...
```

**Назначение**: Получение парсера аргументов командной строки.

**Параметры**:
- Нет

**Возвращает**:
- `argparse.ArgumentParser`: Объект парсера аргументов командной строки.

**Как работает функция**:
1. Функция вызывает `get_api_parser()` из модуля `cli`.
2. Возвращает полученный объект `ArgumentParser`.

```text
get_api_parser()
↓
Возвращает ArgumentParser
```

**Примеры**:
```python
parser = get_api_parser()
```

### `run_api_args`

```python
def run_api_args(args: argparse.Namespace) -> None:
    """
    Запускает API с использованием аргументов командной строки.

    Args:
        args (argparse.Namespace): Аргументы командной строки.

    Returns:
        None
    """
    ...
```

**Назначение**: Запуск API с аргументами командной строки.

**Параметры**:
- `args` (`argparse.Namespace`): Аргументы командной строки.

**Возвращает**:
- `None`

**Как работает функция**:
1. Функция вызывает `run_api_args(args)` из модуля `cli`.

```text
run_api_args(args)
↓
Запуск API с заданными аргументами
```

**Примеры**:
```python
run_api_args(args)
```

## Основной код

```python
parser = get_api_parser()
args = parser.parse_args()
if args.gui is None:
    args.gui = True
run_api_args(args)
```

**Назначение**: Основной блок кода для запуска API.

**Как работает**:
1. Получает парсер аргументов командной строки с помощью `get_api_parser()`.
2. Парсит аргументы командной строки с помощью `parser.parse_args()`.
3. Если аргумент `gui` не указан, устанавливает его в `True`.
4. Запускает API с использованием аргументов командной строки с помощью `run_api_args(args)`.