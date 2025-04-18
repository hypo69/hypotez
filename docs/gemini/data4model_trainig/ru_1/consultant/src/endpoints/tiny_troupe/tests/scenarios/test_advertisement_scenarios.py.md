### **Анализ кода модуля `test_advertisement_scenarios.py`**

#### **Качество кода**:
- **Соответствие стандартам**: 7/10
- **Плюсы**:
    - Код разбит на отдельные тестовые сценарии, что упрощает понимание и поддержку.
    - Используются ассерты для проверки ожидаемых результатов, что важно для автоматизированного тестирования.
    - Присутствуют комментарии, объясняющие назначение отдельных блоков кода.
- **Минусы**:
    - Некоторые комментарии отсутствуют или недостаточно информативны.
    - Не все переменные аннотированы типами.
    - Отсутствует docstring для функций.
    - Использованы множественные `sys.path.append` для добавления путей, что может быть улучшено.
    - Не используется модуль `logger` для логирования.

#### **Рекомендации по улучшению**:
1. **Добавить docstring для каждой функции**, чтобы объяснить её назначение, аргументы, возвращаемые значения и возможные исключения.
2. **Аннотировать типы для всех переменных и параметров функций**, чтобы повысить читаемость и облегчить отладку.
3. **Заменить множественные `sys.path.append`** на более надежный способ управления путями, например, с использованием `os.path.join` и `sys.path.insert`.
4. **Использовать модуль `logger`** для логирования вместо `print`.
5. **Улучшить комментарии**, чтобы они были более информативными и соответствовали стандарту оформления.
6. **Перевести docstring на русский язык**.
7. **Удалить ненужные импорты**, если таковые имеются.
8. **Использовать одинарные кавычки** вместо двойных.

#### **Оптимизированный код**:

```python
import pytest
import os
import sys
import logging
from typing import List, Optional
from pathlib import Path

# Добавляем путь к корневой директории проекта, чтобы избежать sys.path.append
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.logger import logger  # Подключаем логгер из проекта
from src.tinytroupe.agent import TinyPerson
from src.tinytroupe.environment import TinyWorld, TinySocialNetwork
from src.tinytroupe.factory import TinyPersonFactory
from src.tinytroupe.extraction import ResultsExtractor

from src.tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect, create_marcos_the_physician

import src.tinytroupe.control as control
from src.tinytroupe.control import Simulation

from src.endpoints.tiny_troupe.tests.scenarios.testing_utils import *


def test_ad_evaluation_scenario(setup: dict) -> None:
    """
    Тест сценария оценки рекламных объявлений.

    Args:
        setup (dict): Фикстура pytest для настройки тестовой среды.

    Returns:
        None

    Описание:
        Этот тест проверяет, как агенты TinyPerson оценивают различные рекламные объявления,
        основываясь на их личностных характеристиках и предпочтениях.
        Он создает несколько рекламных объявлений, определяет ситуацию и цель извлечения,
        затем заставляет агентов прослушивать и действовать на основе предоставленной информации.
        Наконец, он извлекает результаты и проверяет, соответствуют ли они ожидаемым значениям.
    """
    # user search query: "europe travel package"
    # запрос пользователя: "турпакет по Европе"

    travel_ad_1: str = """
    Tailor-Made Tours Of Europe - Nat'l Geographic Award Winner
    https://www.kensingtontours.com/private-tours/europe
    AdPrivate Guides; Custom Trip Itineraries; 24/7 In-Country Support. Request A Custom Quote. Europe's Best Customized For You - Historic Cities, Scenic Natural Wonders & More.

    Unbeatable Value · Easy Multi-Country · Expert Safari Planners · Top Lodges

    Bulgari & Romania
    Explore Europe Off The Beaten Track
    Exceptional Journey In The Balkans
    Munich, Salzburg, Vienna
    Discover Extraordinary Landscapes
    Explore Castles & Royal Palaces
    Budapest, Vienna, Prague
    Tread Cobblestone Laneways
    Bask In The Elegant Architecture
    30,000+ Delighted Clients
    Customers Love Kensington Tours
    With A Trust Score Of 9.8 Out Of 10
    Expert Planners
    Our Experts Know The Must-Sees,
    Hidden Gems & Everything In Between
    Free Custom Quotes
    Your Itinerary Is Tailored For You
    By Skilled Destination Experts
    See more at kensingtontours.com
    """

    travel_ad_2: str = """
    Europe all-inclusive Packages - Europe Vacation Packages
    https://www.exoticca.com/europe/tours

    AdDiscover our inspiring Europe tour packages from the US: Capitals, Beaches and much more. Enjoy our most exclusive experiences in Europe with English guides and Premium hotels

    100% Online Security · +50000 Happy Customers · Flights + Hotels + Tours

    Types: Lodge, Resort & Spa, Guest House, Luxury Hotel, Tented Lodge
    """

    travel_ad_3: str = """
    Travel Packages - Great Vacation Deals
    https://www.travelocity.com/travel/packages
    AdHuge Savings When You Book Flight and Hotel Together. Book Now and Save! Save When You Book Your Flight & Hotel Together At Travelocity.

    Get 24-Hour Support · 3 Million Guest Reviews · 240,000+ Hotels Worldwide

    Types: Cheap Hotels, Luxury Hotels, Romantic Hotels, Pet Friendly Hotels
    Cars
    Things to Do
    Discover
    All-Inclusive Resorts
    Book Together & Save
    Find A Hotel
    Nat Geo Expeditions® - Trips to Europe
    https://www.nationalgeographic.com/expeditions/europe
    AdTravel Beyond Your Wildest Dreams. See the World Close-Up with Nat Geo Experts. Join Us for An Unforgettable Expedition! Discover the Nat Geo Difference.

    People & Culture · Wildlife Encounters · Photography Trips · Hiking Trips

    Find The Trip For You
    Request a Free Catalog
    Special Offers
    Discover the Difference
    """

    travel_ad_4: str = """
    Europe Luxury Private Tours
    https://www.kensingtontours.com
    Kensington Tours - Private Guides, Custom Itineraries, Hand Picked Hotels & 24/7 Support
    """


    eval_request_msg: str = f"""
    Can you please evaluate these Bing ads for me? Which one convices you more to buy their particular offering? Select **ONLY** one. Please explain your reasoning, based on your background and personality.

    # AD 1
    ```
    {travel_ad_1}
    ```

    # AD 2
    ```
    {travel_ad_2}
    ```

    # AD 3
    ```
    {travel_ad_3}
    ```

    # AD 4
    ```
    {travel_ad_4}
    ```

    """

    logger.info(eval_request_msg) # Записываем сообщение запроса в лог

    situation: str = "You decided you want to visit Europe and you are planning your next vacations. You start by searching for good deals as well as good ideas."
    #Ситуация: Вы решили посетить Европу и планируете свой следующий отпуск. Вы начинаете с поиска выгодных предложений, а также хороших идей.

    extraction_objective: str = "Find the ad the agent chose. Extract the Ad number (just put a number here, no text, e.g., 2), title and justification for the choice."
    #Задача извлечения: Найти объявление, которое выбрал агент. Извлечь номер объявления (просто цифру, без текста, например, 2), заголовок и обоснование выбора.

    people: List[TinyPerson] = [create_oscar_the_architect(), create_lisa_the_data_scientist()]

    for person in people:
        person.change_context(situation)
        person.listen_and_act(eval_request_msg)
        
    extractor: ResultsExtractor = ResultsExtractor()
    choices: List[dict] = []

    for person in people:
        res: Optional[dict] = extractor.extract_results_from_agent(person,
                                        extraction_objective=extraction_objective,
                                        situation=situation,
                                        fields=["ad_id", "ad_title", "justification"])
        
        logger.info(f"Agent {person.name} choice: {res}")#  Логируем выбор агента

        assert res is not None, "There should be a result."
        assert "ad_id" in res, "There should be an ad_id field."
        assert str(res["ad_id"]) in ["1", "2", "3", "4"], "The ad_id should be one of the four options."
        assert "ad_title" in res, "There should be an ad_title field."
        assert "justification" in res, "There should be a justification field."

        choices.append(res)

    assert len(choices) == 2, "There should be two choices made."

    logger.info(f"Agents choices: {choices}") # Логируем выбор агентов


def test_ad_creation_scenario(setup: dict, focus_group_world: TinyWorld) -> None:
    """
    Тест сценария создания рекламного объявления.

    Args:
        setup (dict): Фикстура pytest для настройки тестовой среды.
        focus_group_world (TinyWorld): Мир, представляющий фокус-группу.

    Returns:
        None

    Описание:
        Этот тест проверяет, как фокус-группа TinyWorld генерирует идеи для рекламы квартиры.
        Он определяет ситуацию, описание квартиры и задачу, затем транслирует эту информацию
        в фокус-группу и запускает симуляцию. Наконец, он извлекает результаты и проверяет,
        содержат ли они идеи для рекламного объявления.
    """

    situation: str = """ 
    This is a focus group dedicated to finding the best way to advertise an appartment for rent.
    Everyone in the group is a friend to the person who is renting the appartment, called Paulo.
    The objective is to find the best way to advertise the appartment, so that Paulo can find a good tenant.
    """
    #Ситуация: Это фокус-группа, посвященная поиску лучшего способа рекламы сдаваемой в аренду квартиры.
    #Все в группе - друзья человека, который сдает квартиру, его зовут Пауло.
    #Цель состоит в том, чтобы найти лучший способ рекламы квартиры, чтобы Пауло мог найти хорошего арендатора.

    apartment_description: str = """
    The appartment has the following characteristics:
    - It is in an old building, but was completely renovated and remodeled by an excellent architect. 
        There are almost no walls, so it is very spacious, mostly composed of integrated spaces. 
    - It was also recently repainted, so it looks brand new.
    - 1 bedroom. Originally, it had two, but one was converted into a home office.
    - 1 integrated kitchen and living room. The kitchen is very elegant, with a central eating wood table,
        with 60s-style chairs. The appliances are in gray and steel, and the cabinets are in white, the wood
        is light colored.
    - Has wood-like floors in all rooms, except the kitchen and bathroom, which are tiled.  
    - 2 bathrooms. Both with good taste porcelain and other decorative elements.
    - 1 laundry room. The washing machine is new and also doubles as a dryer.
    - Is already furnished with a bed, a sofa, a table, a desk, a chair, a washing machine, a refrigerator, 
        a stove, and a microwave.
    - It has a spacious shelf for books and other objects.
    - It is close to: a very convenient supermarket, a bakery, a gym, a bus stop, and a subway station. 
        It is also close to a great argentinian restaurant, and a pizzeria.
    - It is located at a main avenue, but the appartment is in the back of the building, so it is very quiet.
    - It is near of the best Medicine School in the country, so it is a good place for a medical student.  
    """
    #Описание квартиры:
    #- Она находится в старом здании, но была полностью отремонтирована и переделана отличным архитектором.
    #Почти нет стен, поэтому она очень просторная, в основном состоит из интегрированных пространств.
    #- Недавно ее перекрасили, поэтому она выглядит как новая.
    #- 1 спальня. Первоначально их было две, но одна была переоборудована в домашний офис.
    #- 1 интегрированная кухня и гостиная. Кухня очень элегантная, с центральным деревянным столом для еды,
    # со стульями в стиле 60-х. Бытовая техника серого и стального цвета, а шкафы белые, дерево
    # светлого цвета.
    #- Во всех комнатах полы под дерево, кроме кухни и ванной, где положена плитка.
    #- 2 ванные комнаты. Обе с хорошим вкусом фарфор и другие декоративные элементы.
    #- 1 прачечная. Стиральная машина новая, а также выполняет функцию сушки.
    #- Уже меблирована кроватью, диваном, столом, письменным столом, стулом, стиральной машиной, холодильником,
    #плитой и микроволновой печью.
    #- Имеет просторную полку для книг и других предметов.
    #- Находится рядом с: очень удобным супермаркетом, булочной, спортзалом, автобусной остановкой и станцией метро.
    #Он также находится рядом с отличным аргентинским рестораном и пиццерией.
    #- Он расположен на главной улице, но квартира находится в задней части здания, поэтому в ней очень тихо.
    #- Он находится рядом с лучшей медицинской школой в стране, поэтому это хорошее место для студента-медика.

    task: str = """
    Discuss the best way to advertise the appartment, so that Paulo can find a good tenant.
    """
    #Задача: Обсудите лучший способ рекламы квартиры, чтобы Пауло мог найти хорошего арендатора.

    focus_group: TinyWorld = focus_group_world

    focus_group.broadcast(situation)
    focus_group.broadcast(apartment_description)
    focus_group.broadcast(task)

    focus_group.run(2)

    extractor: ResultsExtractor = ResultsExtractor()
    res: Optional[str] = extractor.extract_results_from_world(focus_group, verbose=True)

    assert proposition_holds(f"The following contains ideas for an apartment advertisement: '{res}'"), f"Proposition is false according to the LLM."
    #Утверждение ложно, согласно LLM.


def test_consumer_profiling_scenario(setup: dict) -> None:
    """
    Тест сценария профилирования потребителей.

    Args:
        setup (dict): Фикстура pytest для настройки тестовой среды.

    Returns:
        None

    Описание:
        Этот тест проверяет, как создаются профили потребителей на основе их ответов на вопросы.
        Он создает фабрику потребителей, определяет общий контекст и проводит серию интервью
        с потребителями. Затем он проверяет, был ли создан файл контрольной точки.
    """

    checkpoint_file: str = "test_consumer_profiling_scenario.cache.json"
    remove_file_if_exists(checkpoint_file)
    control.begin(checkpoint_file)

    general_context: str = """
    We are performing market research, and in that examining the whole of the American population. We care for the opinion of everyone, from the simplest professions to those of the highest ranks. 
    We are interested in the opinion of everyone, from the youngest to the oldest; from the most conservative, to the most liberal; from the educated, to the ignorant;
    from the healthy to the sick; from rich to poor. You get the idea. We are surveying the market for bottled gazpacho, so we are interested in the opinion of everyone, 
    from the most enthusiastic to the most skeptical.
    """
    #Мы проводим маркетинговые исследования и в рамках этого изучаем все американское население. Нам важно мнение каждого, от самых простых профессий до самых высоких рангов.
    #Нам интересно мнение каждого, от самых молодых до самых старых; от самых консервативных до самых либеральных; от образованных до невежественных;
    #от здоровых до больных; от богатых до бедных. Вы поняли. Мы исследуем рынок бутилированного гаспачо, поэтому нам интересно мнение каждого,
    #от самых восторженных до самых скептически настроенных.

    consumer_factory: TinyPersonFactory = TinyPersonFactory(general_context)

    from time import sleep

    consumers: List[TinyPerson] = []
    def interview_consumer_batch(n: int) -> None:
        """
        Опрашивает пакет потребителей.

        Args:
            n (int): Количество потребителей для опроса.

        Returns:
            None
        """
        for i in range(n):
            logger.info(f"################################### Interviewing consumer {i+1} of {n} ###################################")#  Логируем начало опроса потребителя
            sleep(2)
            consumer: TinyPerson = consumer_factory.generate_person("A random person with highly detailed preferences.")
            logger.info(consumer.minibio())#  Логируем мини-биографию потребителя
            #consumer.listen_and_act("Can you please present yourself, and tell us a bit about your background and preferences?")
            consumer.listen_and_act("We are performing some market research and need to know you more. Can you please present yourself and also list your top-10 interests?")
            #consumer.listen_and_act("Can you plese explain more about why you care for these things?")
            consumer.listen_and_act(
                """
                Would you buy bottled gazpacho if you went to the supermarket today? Why yes, or why not? Please be honest, we are not here to judge you, but just to learn from you.
                We know these choices depend on many factors, but please make your best guess, consider your current situation in life, location, job and interests,
                and tell us whether you would buy bottled gazpacho or not. To make it easier, start your response with "Yes, " or "No, ".
                """)
            
            consumers.append(consumer)

            control.checkpoint()
    
    interview_consumer_batch(15)

    # check if the file was created
    assert os.path.exists(checkpoint_file), "The checkpoint file should have been created."

    control.end()