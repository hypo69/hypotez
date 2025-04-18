# Документация для разработчика: Предотвращение нарушений авторских прав

## Обзор

Этот файл содержит инструкцию, предназначенную для предотвращения нарушений авторских прав при обработке пользовательских запросов, касающихся контента, защищенного авторским правом. Инструкция предписывает вежливо отказывать в предоставлении такого контента и объяснять причины отказа.

## Подробнее

Этот модуль содержит строку, которая служит в качестве инструкции для языковой модели. Она указывает, что в случае запроса контента, защищенного авторским правом (книги, тексты песен, рецепты, новостные статьи и контент с WebMD), следует вежливо отказать и объяснить, что нарушение авторских прав недопустимо. Также требуется краткое описание или резюме запрошенного произведения.

## Инструкция

### Содержание инструкции

- Инструкция содержит указание на то, какие типы контента могут нарушать авторские права.
- Подчеркивается необходимость вежливого отказа в предоставлении такого контента.
- Требуется объяснение причины отказа, а именно недопустимость нарушения авторских прав.
- Предписывается предоставлять краткое описание или резюме запрошенного произведения.
- Строго запрещается нарушать авторские права при любых обстоятельствах.

### Как работает инструкция

Инструкция предназначена для использования в системах, обрабатывающих пользовательские запросы на контент. Она служит фильтром, который предотвращает предоставление контента, защищенного авторским правом, без надлежащего разрешения.

### Примеры

```python
instruction = "Если пользователь запрашивает контент, защищенный авторским правом, такой как книги, тексты песен, рецепты, новостные статьи и контент с WebMD, который может нарушать авторские права или считаться нарушением авторских прав, вежливо откажите и объясните, что вы не можете нарушать авторские права. Включите краткое описание или резюме работы, которую запрашивает пользователь. Ни при каких обстоятельствах не нарушайте авторские права."