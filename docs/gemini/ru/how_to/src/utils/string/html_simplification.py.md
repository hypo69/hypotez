## Как использовать `simplify_html`

=========================================================================================

### Описание

-------------------------

Функция `simplify_html` предназначена для упрощения HTML-кода, оставляя только 
самое важное содержание. Она фокусируется на содержимом тега `<body>` и позволяет 
управлять процессом упрощения с помощью объекта `Config`.

### Шаги выполнения

-------------------------

1. **Изоляция содержимого `<body>`:** 
    - Функция извлекает HTML-код из входных данных (`html_content`).
    - Находит тег `<body>` в этом коде.
    - Если `<body>` не найден, но в коде есть контент, обрабатывает его как фрагмент.
    - Если `<body>` не найден и нет контента, возвращает пустую строку.
    - Сохраняет содержимое `<body>` (или весь фрагмент) в переменную `body_content_str`.

2. **Обработка изолированного содержимого `<body>` (или фрагмента):**
    - Создает новый объект `BeautifulSoup` только из содержимого `<body>` (или всего фрагмента).
    - **Начальная чистка:**
        - Удаляет HTML-комментарии, если опция `config.remove_comments` установлена в `True`.
        - Удаляет теги `<script>` и `<style>` вместе с содержимым, если опция `config.remove_scripts_styles` установлена в `True`.
    - **Удаление незначимых контейнеров:**
        - Если опция `config.keep_only_significant` установлена в `True`:
            - Проверяет каждый тег в коде.
            - Тег считается "значимым", если:
                - Он относится к разрешенным "пустым" тегам (например, `<br>`) и входит в список разрешенных тегов (`config.allowed_tags`).
                - Он содержит текст, не являющийся пробелом.
                - Он содержит "значимые" дочерние теги (теги, прошедшие предыдущие проверки).
            - Незначимые теги удаляются из дерева HTML.
    - **Финальная обработка тегов и атрибутов:**
        - Проходит по всем оставшимся тегам.
        - **Разворачивание тегов:** 
            - Удаляет теги из списка `config.unwrap_tags`, оставляя их содержимое, если они не являются корневыми элементами.
        - **Фильтрация по разрешенным тегам:**
            - Удаляет теги, которые не включены в список `config.allowed_tags`, если они не являются корневыми элементами.
        - **Фильтрация атрибутов:**
            - Удаляет атрибуты из тегов, если они не входят в список `config.allowed_attributes`.

3. **Получение финального HTML и нормализация пробелов:**
    - Получает HTML-код из обработанного объекта `BeautifulSoup`.
    - Нормализует пробелы (заменяет множественные пробелы на один) если опция `config.normalize_whitespace` установлена в `True`.
    - Возвращает финальный упрощенный HTML-код.


### Пример использования

-------------------------

```python
from src.utils.string.html_simplification import simplify_html, Config

# Пример HTML-кода
sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Тестовая страница</title>
    </head>
    <body>
        <div id="main" class="container">
            <h1>Пример HTML</h1>
            <p class="main-text">
                Это <span class="highlight">ненужный</span> текст.
            </p>
            <div class="empty-container"></div>
        </div>
    </body>
    </html>
    """

# Создаем объект конфигурации, разрешая тег 'div' и атрибут 'style'
config = Config(allowed_tags={'div'}, allowed_attributes={'*': {'style'}})

# Упрощаем HTML-код с использованием созданной конфигурации
simplified_html = simplify_html(sample_html, config=config)

# Выводим упрощенный HTML-код
print(simplified_html)
```

### Ожидаемый результат:

```html
<div style="">
    <h1>Пример HTML</h1>
    <p style="">
        Это текст.
    </p>
    <div style=""></div>
</div>
```