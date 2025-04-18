# Генерация фабрики персонажей

## Обзор

Этот файл содержит инструкции для создания множества контекстов, которые будут использоваться в качестве основы для генерации списка персонажей. Идея заключается в получении широкого контекста с некоторыми деталями о персонажах, которых мы хотим сгенерировать, такими как демографические параметры, физические характеристики, поведение, убеждения и т. д., а затем создании множества других, более специфичных контекстов, производных от более общего.

## Подробней

Этот код используется для генерации описаний персонажей на основе заданного широкого контекста. Он принимает общие параметры, такие как демография, физические характеристики, поведение и убеждения, и создает множество более конкретных контекстов, которые будут использоваться для генерации отдельных описаний персонажей. Это позволяет создавать разнообразных персонажей, основанных на заданных общих параметрах.

## Инструкции

### Формат ввода

Входные данные должны представлять собой строку, содержащую общий контекст для генерации описаний персонажей. Например:

```
"Пожалуйста, сгенерируйте 3 описания персонажей на основе следующего широкого контекста: Латиноамериканцы, возраст от 20 до 40 лет, экономический статус может варьироваться от бедного до богатого, могут быть религиозными или нет, могут быть женатыми или нет, могут иметь детей или нет, могут быть профессионалами или нет, могут быть работниками или нет."
```

### Формат вывода

Выходные данные должны быть массивом в формате JSON. Каждый элемент массива должен быть контекстом, который будет использоваться для генерации описания персонажа. Например:

```json
[
  "Мексиканец, получивший образование юриста, но сейчас работающий в другой области, не женат, любит спорт и фильмы",
  "Создайте бразильца, который является врачом, любит домашних животных и природу и любит тяжелый металл.",
  "Создайте колумбийца, который является юристом, любит читать и пить кофе и женат, имеет 2 детей."
]
```

## Примеры

### Пример 1

#### Вход

```
"Пожалуйста, сгенерируйте 2 описания персонажей на основе следующего широкого контекста: Европейцы, возраст от 30 до 50 лет, высокий социальный статус, интересуются искусством и наукой."
```

#### Выход

```json
[
  "Французский галерист, женат, двое детей, увлекается современной живописью и классической музыкой.",
  "Немецкий профессор физики, не женат, увлекается квантовой механикой и горным туризмом."
]
```

### Пример 2

#### Вход

```
"Пожалуйста, сгенерируйте 4 описания персонажей на основе следующего широкого контекста: Азиаты, возраст от 18 до 25 лет, студенты, изучают программирование."
```

#### Выход

```json
[
  "Китайский студент, увлекается машинным обучением и онлайн-играми.",
  "Японская студентка, увлекается веб-разработкой и косплеем.",
  "Корейский студент, увлекается мобильной разработкой и K-pop.",
  "Индийский студент, увлекается анализом данных и крикетом."
]