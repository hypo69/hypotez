# Модуль для парсинга истории переписок ChatGPT из HTML-файлов

## Обзор

Модуль `converstions_parser.py` предназначен для извлечения истории переписок из HTML-файлов, экспортированных из ChatGPT. Он использует библиотеку `BeautifulSoup` для парсинга HTML и поиска элементов, содержащих информацию о переписках.

## Подробней

Этот модуль предоставляет функцию `extract_conversations_from_html`, которая принимает путь к HTML-файлу и возвращает генератор, позволяющий итерироваться по каждой переписке, найденной в файле. Это позволяет обрабатывать большие файлы переписок, не загружая их целиком в память.

## Функции

### `extract_conversations_from_html`

**Назначение**: Извлекает переписки из HTML-файла, находя все элементы `<div class="conversation">`.

**Параметры**:
- `file_path` (Path): Путь к HTML-файлу.

**Возвращает**:
- `Generator[bs4.element.Tag, None, None]`: Генератор объектов `BeautifulSoup` (bs4.element.Tag), представляющих каждую переписку.

**Как работает функция**:

1.  Функция принимает путь к HTML-файлу (`file_path`) в качестве аргумента.
2.  Открывает файл в режиме чтения с кодировкой UTF-8, чтобы корректно обрабатывать символы Unicode.
3.  Использует `BeautifulSoup` для парсинга содержимого HTML-файла.
4.  Находит все элементы `<div class="conversation">` в HTML-файле.
5.  Возвращает генератор, который позволяет итерироваться по найденным элементам, представляющим переписки.

**Примеры**:

```python
from pathlib import Path
from src import gs
from src.suppliers.suppliers_list.chat_gpt.converstions_parser import extract_conversations_from_html

file_path = Path(gs.path.data / 'chat_gpt'  / 'chat.html')
for conversation in extract_conversations_from_html(file_path):
    print(conversation.prettify())
```
В данном примере создается объект `Path` к файлу `chat.html`, находящемуся в директории `data/chat_gpt`. Затем вызывается функция `extract_conversations_from_html`, которой передается путь к файлу. В цикле `for` итерируются переписки, извлеченные из HTML-файла, и содержимое каждой переписки выводится в консоль с помощью `print(conversation.prettify())`.