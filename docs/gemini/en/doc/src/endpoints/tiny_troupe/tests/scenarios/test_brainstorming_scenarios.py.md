# Тестовые сценарии для мозгового штурма

## Обзор

Данный модуль содержит тестовые сценарии для проверки работы функции мозгового штурма в агенте `TinyPerson`. Тесты проверяют, как агент собирает идеи от участников фокус-группы и генерирует сводку по ним.

## Детали

В этом сценарии тестируется функция `test_brainstorming_scenario`, которая запускает симуляцию фокус-группы, где участники обсуждают идеи для нового товара. Агент `TinyPerson` с именем "Lisa Carter"  должен  свести идеи в краткое описание, которое в дальнейшем анализируется на предмет наличия предложений по новым товарам или функциям.

## Тестовые функции

### `test_brainstorming_scenario`

**Цель**: Проверяет, как агент `TinyPerson` собирает идеи от участников фокус-группы и генерирует сводку по ним.

**Параметры**:

- `setup`: Фикстура для установки тестовой среды.
- `focus_group_world`: Фикстура для создания тестового мира фокус-группы.

**Возвращает**:

-  None

**Описание**:

1. Тестовая функция создает тестовый мир `focus_group_world`.
2. В мир отправляется сообщение, чтобы начать мозговой штурм с целью генерирования идей для новой функции в Microsoft Word.
3. Функция запускает мир на 1 шаг, чтобы агенты могли взаимодействовать.
4. Получает агента `TinyPerson` с именем "Lisa Carter".
5. Агент "Lisa Carter" получает задание  свести полученные идеи.
6. Создается экземпляр класса `ResultsExtractor` для извлечения результатов.
7.  `ResultsExtractor` извлекает результаты из агента "Lisa Carter".
8.  Проверяет,  что результаты содержат идеи для новых товаров или функций.
9.  Выводит результаты мозгового штурма.
10. Использует  функцию `proposition_holds`,  чтобы проверить,  верна ли  предложенная  гипотеза.

**Пример**:

```python
>>> test_brainstorming_scenario(setup, focus_group_world)
Brainstorm Results:  The group came up with the following ideas:
- An AI feature that automatically summarizes long documents, highlighting key points and providing a concise overview. This would save time and make it easier to understand complex information.
- A feature that suggests relevant images or videos to accompany text, based on the content of the document. This would make documents more engaging and visually appealing.
- A feature that allows users to translate text between different languages with high accuracy. This would be useful for international collaboration and communication.
- An AI-powered grammar and spelling checker that goes beyond basic errors and suggests more sophisticated improvements. This would help users write clearer and more concise text.
- A feature that suggests alternative wording for phrases or sentences, based on the context of the document. This would help users improve the clarity and effectiveness of their writing.
Proposition is true according to the LLM.
```

**Внутренние функции**:

- `proposition_holds(proposition: str)` -  Функция, которая  проверяет  верность  предложенной  гипотезы.

**Как работает**:

Тестовая функция моделирует реальный  сценарий мозгового штурма.  Она  проверяет,  как агент `TinyPerson`  может  свести  в  краткое  описание  идеи,  полученные  от  участников.

**Примеры**:

-  В  тестовой  функции  используются  фикстуры  `setup`  и  `focus_group_world`  для  создания  тестовой  среды.
-  `proposition_holds`  используется  для  проверки  верности  предложенной  гипотезы.
-  Результаты  мозгового  штурма  выводятся  на  консоль.