# Модуль для извлечения бесед из HTML-файлов ChatGPT

## Обзор

Модуль предназначен для парсинга HTML-файлов, содержащих историю переписки с ChatGPT, и извлечения отдельных блоков диалогов. Он использует библиотеку `BeautifulSoup` для анализа HTML и позволяет итерироваться по каждой беседе.

## Подробней

Этот модуль предоставляет функциональность для автоматического извлечения содержимого бесед из HTML-файлов, которые могут быть экспортированы из интерфейса ChatGPT. Это может быть полезно для анализа данных, создания обучающих выборок или архивирования истории переписки.

## Функции

### `extract_conversations_from_html`

```python
def extract_conversations_from_html(file_path: Path):
    """Генератор, который читает один .html файл и извлекает все <div class="conversation">.

    :param file_path: Путь к .html файлу.
    """
    ...
```

**Назначение**: Извлекает все блоки `<div class="conversation">` из HTML-файла.

**Параметры**:

- `file_path` (Path): Путь к HTML-файлу, который необходимо обработать.

**Возвращает**:

- Генератор, который выдает объекты `BeautifulSoup` для каждой найденной беседы.

**Как работает функция**:

1.  Открывает HTML-файл по указанному пути в кодировке UTF-8.
2.  Использует `BeautifulSoup` для парсинга HTML-содержимого.
3.  Находит все элементы `<div class="conversation">`, соответствующие блокам бесед.
4.  Возвращает генератор, который позволяет последовательно перебирать найденные беседы.

**Примеры**:

```python
from pathlib import Path
from src import gs

file_path = Path(gs.path.data / 'chat_gpt'  / 'chat.html')
for conversation in extract_conversations_from_html(file_path):
    print(conversation.prettify())