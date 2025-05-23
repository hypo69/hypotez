# Тестовые сценарии для брейнсторминга 

## Обзор

Этот файл содержит тестовый сценарий для проверки работы модели `TinyPerson` в контексте брейнсторминга. 

## Сценарий

Тестовый сценарий имитирует фокус-группу, где участники обсуждают идеи для нового товара. 

## Функции

### `test_brainstorming_scenario`

**Назначение**: Проверка работы модели `TinyPerson` в контексте брейнсторминга.

**Параметры**:
- `setup`: Фикстура pytest для настройки тестовой среды.
- `focus_group_world`: Фикстура pytest, которая создает мир с фокус-группой. 

**Возвращает**:
- `None`: Тест не возвращает значения.

**Как работает функция**:
1. Тест создает мир с фокус-группой.
2.  В мир отправляется сообщение, которое запускает брейнсторминг.
3.  Тест запускает мир на один шаг.
4.  Создается объект `TinyPerson` по имени "Lisa Carter".
5.  "Lisa Carter" задает вопрос о суммировании идей, предложенных группой.
6.  Используется `ResultsExtractor` для извлечения результатов брейнсторминга.
7.  Результаты извлекаются из агента "Lisa Carter", с указанием цели извлечения, что должно быть сделано.
8.  Результаты выводятся на экран.
9.  Проверяется, что полученные результаты содержат идеи для новых функций или товаров.
10.  Тест утверждает, что полученные результаты верны, основываясь на оценке LLM.

**Примеры**:

```python
>>> test_brainstorming_scenario(setup, focus_group_world)
```

**Внутренние функции**:

- Нет.