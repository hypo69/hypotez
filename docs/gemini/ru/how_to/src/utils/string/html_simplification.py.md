### Как использовать этот блок кода

Описание
-------------------------
Модуль `html_simplification` предназначен для очистки и упрощения HTML-кода. Он позволяет удалять нежелательные теги и атрибуты, нормализовать пробелы, а также сохранять только значимый контент. Модуль состоит из двух основных функций: `strip_tags` и `simplify_html`, а также класса `Config`, который позволяет настроить параметры очистки.

Шаги выполнения
-------------------------
1. **Импорт модуля**: Импортируйте модуль `html_simplification` в свой проект.
2. **Использование `strip_tags`**: Эта функция удаляет все HTML-теги из входной строки, оставляя только текст.
3. **Использование `simplify_html`**: Эта функция упрощает HTML-код, удаляя или разворачивая определенные теги и атрибуты в соответствии с заданной конфигурацией.
4. **Настройка `Config`**: Создайте экземпляр класса `Config` для настройки параметров очистки HTML, таких как разрешенные теги и атрибуты.

Пример использования
-------------------------

```python
    from src.utils.string import html_simplification
    from src.utils.string.html_simplification import Config, strip_tags, simplify_html
    from src.logger import logger

    # Исходный HTML-код
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Пример страницы</title>
    </head>
    <body>
        <div id="main" class="container">
            <h1>Заголовок</h1>
            <p class="text">Текст с <b>важным</b> элементом.</p>
        </div>
    </body>
    </html>
    """

    # 1. Удаление всех тегов с помощью strip_tags
    stripped_text = strip_tags(sample_html)
    logger.info(f"Текст без тегов: {stripped_text}")

    # 2. Упрощение HTML с настройками по умолчанию
    default_config = Config()
    simplified_html = simplify_html(sample_html, config=default_config)
    logger.info(f"Упрощенный HTML (настройки по умолчанию): {simplified_html}")

    # 3. Упрощение HTML с пользовательскими настройками
    custom_config = Config(
        allowed_tags={'div', 'p', 'b'},
        allowed_attributes={'div': {'id', 'class'}, 'p': {'class'}},
        unwrap_tags={'b'}
    )
    custom_simplified_html = simplify_html(sample_html, config=custom_config)
    logger.info(f"Упрощенный HTML (пользовательские настройки): {custom_simplified_html}")