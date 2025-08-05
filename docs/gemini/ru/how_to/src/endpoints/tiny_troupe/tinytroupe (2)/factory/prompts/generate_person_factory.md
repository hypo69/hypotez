### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот код представляет собой шаблон запроса для генерации множества контекстов, которые будут использоваться в качестве основы для создания списка персон. Он принимает широкий контекст с общими деталями о персонах, такими как демографические параметры, физические характеристики, поведение, убеждения и т.д., и создает множество более специфических контекстов, производных от общего.

Шаги выполнения
-------------------------
1.  Получаем широкий контекст с общими деталями о персонах.
2.  Формируем запрос к модели для генерации множества контекстов, производных от общего.
3.  Получаем массив контекстов в формате JSON.
4.  Каждый элемент массива представляет собой контекст, который будет использован для генерации описания персоны.

Пример использования
-------------------------

```python
    # Пример входного контекста
    input_context = "Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not"

    # Пример запроса к модели
    query = f"""
    Your task is create many contexts that will be used as base to generate a list of persons.
    The idea is receive a broad context, with some  details of persons we want to generate, like demographics parameters, physical characteristics, behaviors, believes, etc; and then create many other contexts, more specifics, but derivaded of the more generic one.
    Your response must be an array in JSON format. Each element of the array must be a context that will be used to generate a person description.

    Example:
      - INPUT:
        Please, generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not
      - OUTPUT:
        ["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]
    """
    # response = generate_contexts(query)
    # print(response)

    # Ожидаемый результат (пример)
    # ["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]
```