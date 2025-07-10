# Kotel Prayer Service

## Overview

This module provides a Python script for generating a message describing a prayer service at the Western Wall (Kotel) in Jerusalem. The script is designed to be used as an endpoint for a website or application, allowing users to request the service and receive a personalized message.

## Details

The script generates a message that includes the following:

- Introduction: A welcome message and brief self-introduction.
- Description of the service:  Explains how the user's prayers will be delivered to the Western Wall, including the frequency of visits and the option for urgent requests.
- Benefits of choosing the Western Wall:  Highlights the historical significance and spiritual power of the Western Wall.
- Target audience:  Outlines who might benefit from the service.
- Call to action: Encourages users to order the service and receive a photo report.

## Functions

### `generate_kotel_message()`

**Purpose:** Generates a personalized message describing the Kotel prayer service.

**Parameters:**

- `name`:  (str) The user's name.
- `prayer_request`: (str) The user's prayer or message.

**Returns:**

- `str`: A formatted message ready for display.

**Raises Exceptions:**

- `None`

**How the Function Works:**

The function takes the user's name and prayer request as input and assembles a message based on the template outlined in the script. The message is formatted for readability and includes the following:

1. **Introduction:**  A welcome message and the name of the person offering the service.
2. **Service Description:** Explains how the user's prayers will be delivered to the Western Wall, including the frequency of visits and the option for urgent requests.
3. **Benefits of the Western Wall:** Highlights the historical significance and spiritual power of the Western Wall.
4. **Target Audience:** Outlines who might benefit from the service.
5. **Call to Action:** Encourages users to order the service and receive a photo report.

**Examples:**

```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='John Doe', prayer_request='Please pray for my grandmother's health.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Jane Smith', prayer_request='I would like to thank God for my recent promotion.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Bob Johnson', prayer_request='Please pray for peace in the world.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Alice Brown', prayer_request='I would like to request blessings for my upcoming wedding.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Tom Wilson', prayer_request='Please pray for my son's success in his exams.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Mary Jones', prayer_request='Please pray for my husband's recovery.')
print(message)
```

## Parameter Details

- `name`: (str) The user's name, used to personalize the message.
- `prayer_request`: (str) The user's prayer or message, which will be included in the message and delivered to the Western Wall.

## Examples

```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

# Example 1: Simple prayer request
name = 'John Doe'
prayer_request = 'Please pray for my grandmother's health.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Example 2: Prayer for peace
name = 'Jane Smith'
prayer_request = 'I would like to pray for peace in the world.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Example 3: Prayer of gratitude
name = 'Bob Johnson'
prayer_request = 'I would like to thank God for my recent promotion.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Example 4: Prayer for a special occasion
name = 'Alice Brown'
prayer_request = 'Please pray for blessings for my upcoming wedding.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Example 5: Prayer for success
name = 'Tom Wilson'
prayer_request = 'Please pray for my son's success in his exams.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Example 6: Prayer for recovery
name = 'Mary Jones'
prayer_request = 'Please pray for my husband's recovery.'
message = generate_kotel_message(name, prayer_request)
print(message)
```
```python
# -*- coding: utf-8 -*-
#! .pyenv/bin/python3

"""
Модуль для генерации сообщения о молитве у Западной Стены (Котель)
=================================================================

Этот модуль предоставляет сценарий Python для создания сообщения, описывающего
молитвенную службу у Западной Стены (Котель) в Иерусалиме. Сценарий разработан
для использования в качестве конечной точки для веб-сайта или приложения,
позволяя пользователям заказывать эту услугу и получать персонализированное сообщение.

## Функции

### `generate_kotel_message()`

**Цель**: Создает персонализированное сообщение, описывающее молитвенную службу
у Котель.

**Параметры**:

- `name`: (str) Имя пользователя.
- `prayer_request`: (str) Молитва или сообщение пользователя.

**Возвращает**:

- `str`: Форматированное сообщение, готовое к отображению.

**Исключения**:

- `None`

**Как работает функция**:

Функция принимает имя пользователя и его молитвенную просьбу в качестве входных данных
и создает сообщение на основе шаблона, указанного в сценарии. Сообщение
форматируется для удобочитаемости и включает в себя следующее:

1. **Введение**: Приветственное сообщение и имя человека, предлагающего услугу.
2. **Описание услуги**: Поясняет, как молитвы пользователя будут доставлены к Западной Стене,
включая частоту посещений и возможность срочных запросов.
3. **Преимущества Западной Стены**: Выделяет историческое значение и духовную силу
Западной Стены.
4. **Целевая аудитория**: Описывает, кому может быть полезна эта услуга.
5. **Призыв к действию**: Призывает пользователей заказать услугу и получить фотоотчет.

**Примеры**:

```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Иван Иванов', prayer_request='Пожалуйста, помолитесь за здоровье моей бабушки.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Анна Петрова', prayer_request='Я хочу поблагодарить Бога за мое недавнее повышение.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Сергей Сидоров', prayer_request='Пожалуйста, помолитесь за мир во всем мире.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Ольга Смирнова', prayer_request='Я бы хотела попросить благословения на свою предстоящую свадьбу.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Дмитрий Кузнецов', prayer_request='Пожалуйста, помолитесь за успехи моего сына на экзаменах.')
print(message)
```
```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

message = generate_kotel_message(name='Екатерина Иванова', prayer_request='Пожалуйста, помолитесь за выздоровление моего мужа.')
print(message)
```

## Подробности параметров

- `name`: (str) Имя пользователя, Используетсяое для персонализации сообщения.
- `prayer_request`: (str) Молитва или сообщение пользователя, которое будет включено
в сообщение и доставлено к Западной Стене.

## Примеры

```python
from src.endpoints.hypo69.ebay.kotel.kotel import generate_kotel_message

# Пример 1: Простой молитвенный запрос
name = 'Иван Иванов'
prayer_request = 'Пожалуйста, помолитесь за здоровье моей бабушки.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Пример 2: Молитва за мир
name = 'Анна Петрова'
prayer_request = 'Я хочу помолиться за мир во всем мире.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Пример 3: Молитва благодарности
name = 'Сергей Сидоров'
prayer_request = 'Я хочу поблагодарить Бога за мое недавнее повышение.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Пример 4: Молитва по особому случаю
name = 'Ольга Смирнова'
prayer_request = 'Пожалуйста, помолитесь за благословения на мою предстоящую свадьбу.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Пример 5: Молитва за успех
name = 'Дмитрий Кузнецов'
prayer_request = 'Пожалуйста, помолитесь за успехи моего сына на экзаменах.'
message = generate_kotel_message(name, prayer_request)
print(message)

# Пример 6: Молитва за выздоровление
name = 'Екатерина Иванова'
prayer_request = 'Пожалуйста, помолитесь за выздоровление моего мужа.'
message = generate_kotel_message(name, prayer_request)
print(message)
```
"""

from typing import Optional

def generate_kotel_message(name: str, prayer_request: str) -> str:
    """
    Создает персонализированное сообщение о молитве у Западной Стены (Котель).

    Args:
        name (str): Имя пользователя.
        prayer_request (str): Молитва или сообщение пользователя.

    Returns:
        str: Форматированное сообщение, готовое к отображению.
    """
    message = f"""
                📜 Делиться своим сердцем с Богом у Западной Стены – личное приношение 🙏

Shalom! Меня зовут Давид бен Авраам, и с смиренным сердцем я предлагаю 
передать ваши самые глубокие молитвы к Западной Стене (Котель) в Иерусалиме,
самое святое место для еврейского народа.

✨ Как ваши молитвы достигают небес:

Поделитесь со мной своей молитвой или посланием. Будь то исцеление любимого
человека, желание мира или личная мечта, доверьтесь мне, чего желает ваше сердце.
Дважды в неделю, каждое воскресенье, я отправляюсь в Иерусалим, к этому 
древнему и могущественному месту, где шепот поколений эхом разносится по камням.
Там, с величайшим почтением, я лично положу вашу записку с молитвой в щели
Западной Стены.

Прежде чем доверить ваши слова Котель, я подниму ваши намерения в молитве
в синагоге Котель, наполняя вашу просьбу моей искренней надеждой и преданностью.
Если возникнет срочная потребность или особое важное событие потребует
внимания, я могу немедленно отправиться к Западной Стене, вне моего обычного
расписания, чтобы гарантировать, что ваша молитва достигнет своего назначения 
без задержки.

Чтобы успокоить ваши мысли, я предоставлю вам фотоотчет, гарантируя, что 
ваша молитва была обработана с необходимой заботой и уважением, и была 
доставлена прямо к Богу.

Для тех, кто желает испытать глубокую энергию этого святого места в режиме
реального времени, я также могу организовать прямую трансляцию с Западной Стены
в то время, которое вы назначите, позволяя вам соединиться с вашей молитвой
в момент ее передачи.

🙌 Почему стоит выбрать Западную Стену?

На протяжении веков Западная Стена привлекала верующих со всех уголков 
планеты, каждый из которых искал благословения, исцеления и руководства. 
Стоя перед этими древними камнями, человек ощущает благоговение, смирение
и уверенность, что его голос будет услышан. Это место, где чудеса кажутся
возможными, и где связь с Божественным ощущается осязаемо.

💖 Эта служба идеально подходит для:

Отправки личных молитв за себя или дорогих вам людей.
Поиска исцеления, утешения и защиты в трудные времена.
Выражения искренней благодарности и принесения благодарности за полученные
благословения.
Просьбы о благословениях для важных жизненных событий, таких как свадьбы,
рождения и значимые достижения.

📍 Записки помещаются с искренней молитвой каждое воскресенье. Срочные запросы
учитываются.
📸 Каждая молитва сопровождается личным фотоотчетом для вашего спокойствия.

💌 Позвольте своим словам резонировать в одном из самых святых мест на Земле.
Закажите сейчас, и я понесу вашу молитву с непоколебимой верой, глубоким
почтением и сердцем, полным надежды.
                """
    return message