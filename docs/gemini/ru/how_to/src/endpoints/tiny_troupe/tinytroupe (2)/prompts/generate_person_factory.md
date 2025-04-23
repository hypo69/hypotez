### Как использовать этот блок кода

=========================================================================================

Описание
-------------------------

Этот блок кода представляет собой запрос (prompt) для генерации множества контекстов, которые будут использоваться в качестве основы для создания списка персон. Основная идея состоит в том, чтобы получить широкий контекст с некоторыми деталями о персонах, которых нужно сгенерировать, такими как демографические параметры, физические характеристики, поведение, убеждения и т. д., а затем создать множество других контекстов, более специфичных, но производных от более общего.

Шаги выполнения
-------------------------

1.  **Получение широкого контекста**: Блок кода принимает широкий контекст с общими деталями о персонах, которых необходимо сгенерировать.
2.  **Создание множества контекстов**: На основе широкого контекста создается несколько более конкретных контекстов, каждый из которых будет использоваться для генерации описания отдельной персоны.
3.  **Форматирование ответа**: Результат представляется в виде массива в формате JSON. Каждый элемент массива является контекстом, который будет использован для генерации описания персоны.

Пример использования
-------------------------

```python
    Your task is create many contexts that will be used as base to generate a list of persons.
    The idea is receive a broad context, with some  details of persons we want to generate, like demographics parameters, physical characteristics, behaviors, believes, etc; and then create many other contexts, more specifics, but derivaded of the more generic one.
    Your response must be an array in JSON format. Each element of the array must be a context that will be used to generate a person description.

    Example:
      - INPUT:
        Please, generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not
      - OUTPUT:
        ["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]
```