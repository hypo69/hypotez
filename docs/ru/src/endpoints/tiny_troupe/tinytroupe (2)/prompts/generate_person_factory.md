# Документация для разработчика: Генерация контекстов для персонажей

## Обзор

Этот документ описывает процесс генерации множества контекстов, которые будут использоваться в качестве основы для создания списка персонажей. Идея заключается в получении широкого контекста с некоторыми деталями о персонажах, которых мы хотим сгенерировать, таких как демографические параметры, физические характеристики, поведение, убеждения и т.д., а затем создание множества других, более специфических контекстов, производных от более общего.

## Подробнее

Этот модуль предназначен для генерации контекстов персонажей на основе заданного широкого контекста. Он принимает входные данные в виде текстового описания общих характеристик персонажей и преобразует их в массив JSON, где каждый элемент представляет собой конкретный контекст для создания описания персонажа.

## Инструкция по использованию

### Входные данные

Входные данные представляют собой текстовое описание общих характеристик персонажей, которых необходимо сгенерировать.

### Выходные данные

Выходные данные представляют собой массив JSON, где каждый элемент является контекстом, используемым для генерации описания персонажа.

## Примеры

### Пример 1

#### Входные данные

```
Please, generate 3 person(s) description(s) based on the following broad context: Latin American, age between 20 and 40 years old, economic status can vary between poor and rich, it can be religious or not, it can be married or not, it can have children or not, it can be a professional or not, it can be a worker or not
```

#### Выходные данные

```json
["Mexican person that has formed as lawyer but now works in other are, is single, like sports and movies", "Create a Brazilian person that is a doctor, like pets and the nature and love heavy metal.", "Create a Colombian person that is a lawyer, like to read and drink coffee and is married with 2 children."]