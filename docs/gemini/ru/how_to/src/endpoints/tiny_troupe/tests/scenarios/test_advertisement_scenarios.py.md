### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода содержит несколько тестов, демонстрирующих взаимодействие агентов (виртуальных личностей) в различных сценариях с использованием библиотеки `tinytroupe`. Сценарии включают оценку рекламных объявлений, создание рекламных текстов и профилирование потребителей.

Шаги выполнения
-------------------------
1. **`test_ad_evaluation_scenario(setup)`**:
    - Определяет четыре рекламных объявления (`travel_ad_1`, `travel_ad_2`, `travel_ad_3`, `travel_ad_4`), связанные с туристическими услугами.
    - Формирует запрос (`eval_request_msg`) для оценки этих объявлений.
    - Создает двух агентов: Оскара-архитектора и Лизу-специалиста по данным (`create_oscar_the_architect()`, `create_lisa_the_data_scientist()`).
    - Изменяет контекст агентов (`person.change_context(situation)`), задавая ситуацию, в которой они выбирают тур в Европу.
    - Агенты "слушают" запрос и "действуют" (`person.listen_and_act(eval_request_msg)`), то есть выбирают наиболее привлекательное объявление и объясняют свой выбор.
    - Извлекаются результаты выбора каждого агента (`ResultsExtractor().extract_results_from_agent(...)`).
    - Проверяется, что результаты содержат идентификатор объявления (`ad_id`), заголовок (`ad_title`) и обоснование выбора (`justification`).
    - Утверждается, что каждый агент сделал выбор, и эти выборы сохранены.

2. **`test_ad_creation_scenario(setup, focus_group_world)`**:
    - Определяет ситуацию для фокус-группы, задачей которой является создание рекламного текста для сдачи квартиры в аренду.
    - Описывает характеристики квартиры (`apartment_description`).
    - Указывает задачу для фокус-группы (`task`).
    - Запускает симуляцию фокус-группы на два шага (`focus_group.run(2)`).
    - Извлекает результаты обсуждения фокус-группы (`ResultsExtractor().extract_results_from_world(...)`).
    - Проверяет, что результаты содержат идеи для рекламного объявления квартиры.

3. **`test_consumer_profiling_scenario(setup)`**:
    - Имитирует исследование рынка гаспачо в бутылках.
    - Создает фабрику потребителей (`TinyPersonFactory`) с общим контекстом, описывающим американское население.
    - Определяет функцию `interview_consumer_batch(n)`, которая создает `n` случайных потребителей, "опрашивает" их и сохраняет результаты.
    - Каждый потребитель генерируется с детальными предпочтениями и отвечает на вопросы о своих интересах и готовности купить гаспачо.
    - Используется механизм контрольных точек (`control.checkpoint()`) для сохранения состояния симуляции после каждого опроса.
    - После завершения опроса проверяется наличие файла с контрольными точками.

Пример использования
-------------------------

```python
    import pytest
    from tinytroupe.agent import TinyPerson
    from tinytroupe.environment import TinyWorld, TinySocialNetwork
    from tinytroupe.factory import TinyPersonFactory
    from tinytroupe.extraction import ResultsExtractor

    def test_example_scenario(setup):
        # Создание фабрики личностей
        factory = TinyPersonFactory("Общий контекст для всех агентов.")

        # Создание агентов
        alice = factory.generate_person("Индивидуальное описание Алисы.")
        bob = factory.generate_person("Индивидуальное описание Боба.")

        # Определение ситуации
        situation = "Вы находитесь на конференции по машинному обучению."

        # Задание вопроса
        question = "Какие доклады вы считаете наиболее интересными?"

        # Агенты слушают и действуют
        alice.listen_and_act(question)
        bob.listen_and_act(question)

        # Извлечение результатов
        extractor = ResultsExtractor()
        alice_results = extractor.extract_results_from_agent(alice, extraction_objective="Выделить основные темы докладов.", situation=situation)
        bob_results = extractor.extract_results_from_agent(bob, extraction_objective="Выделить основные темы докладов.", situation=situation)

        print(f"Результаты Алисы: {alice_results}")
        print(f"Результаты Боба: {bob_results}")

        # Проверка результатов
        assert alice_results is not None
        assert bob_results is not None
```