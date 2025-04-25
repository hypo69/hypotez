# Модуль TinyCalendar

## Обзор

Модуль `TinyCalendar` предоставляет базовый инструмент календаря для агентов, позволяющий им отслеживать встречи и назначения. 

## Подробнее

Класс `TinyCalendar` реализует простой календарь, где события хранятся в словаре `calendar`, где ключами являются даты, а значениями - списки событий. Каждое событие представляет собой словарь с ключами:

- `title`: Заголовок события (обязательный)
- `description`: Краткое описание события (необязательный)
- `owner`: Владелец события (необязательный)
- `mandatory_attendees`: Список агентов, которые должны присутствовать (необязательный)
- `optional_attendees`: Список агентов, которые приглашены, но их присутствие не обязательно (необязательный)
- `start_time`: Время начала события (необязательный)
- `end_time`: Время окончания события (необязательный)


## Классы

### `TinyCalendar`

**Описание**: Класс `TinyCalendar` представляет собой базовый инструмент календаря для агентов, позволяющий им отслеживать встречи и назначения.

**Наследует**: `TinyTool`

**Атрибуты**:

- `calendar` (dict): Словарь, который хранит события в календаре. Ключи - даты, значения - списки событий.

**Методы**:

- `add_event(date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None)`: Добавляет новое событие в календарь.
- `find_events(year, month, day, hour=None, minute=None)`: Находит события в календаре по заданным дате и времени.
- `_process_action(agent, action) -> bool`: Обрабатывает действие агента, связанное с календарем.
- `actions_definitions_prompt() -> str`: Возвращает подсказку для агента с описанием доступных действий.
- `actions_constraints_prompt() -> str`: Возвращает подсказку для агента с описанием ограничений для действий.


## Методы класса

### `add_event`

```python
    def add_event(self, date, title, description=None, owner=None, mandatory_attendees=None, optional_attendees=None, start_time=None, end_time=None):
        """
        Добавляет новое событие в календарь.

        Args:
            date: Дата события.
            title: Заголовок события.
            description: Описание события.
            owner: Владелец события.
            mandatory_attendees: Список агентов, которые должны присутствовать.
            optional_attendees: Список агентов, которые приглашены, но их присутствие не обязательно.
            start_time: Время начала события.
            end_time: Время окончания события.

        Returns:
            None
        """
        if date not in self.calendar:
            self.calendar[date] = []
        self.calendar[date].append({"title": title, "description": description, "owner": owner, "mandatory_attendees": mandatory_attendees, "optional_attendees": optional_attendees, "start_time": start_time, "end_time": end_time})
```


### `find_events`

```python
    def find_events(self, year, month, day, hour=None, minute=None):
        """
        Находит события в календаре по заданным дате и времени.

        Args:
            year: Год события.
            month: Месяц события.
            day: День события.
            hour: Час события.
            minute: Минута события.

        Returns:
            Список событий, соответствующих заданным дате и времени.
        """
        # TODO
        pass
```

### `_process_action`

```python
    def _process_action(self, agent, action) -> bool:
        """
        Обрабатывает действие агента, связанное с календарем.

        Args:
            agent: Агент, который выполняет действие.
            action: Действие, которое выполняет агент.

        Returns:
            True, если действие успешно обработано, иначе False.
        """
        if action['type'] == "CREATE_EVENT" and action['content'] is not None:
            # парсит json-контент
            event_content = json.loads(action['content'])
            
            # проверяет, есть ли невалидные ключи в content
            valid_keys = ["title", "description", "mandatory_attendees", "optional_attendees", "start_time", "end_time"]
            utils.check_valid_fields(event_content, valid_keys)

            # использует kwargs для создания нового события
            self.add_event(event_content)

            return True

        else:
            return False
```


### `actions_definitions_prompt`

```python
    def actions_definitions_prompt(self) -> str:
        """
        Возвращает подсказку для агента с описанием доступных действий.

        Returns:
            Строка с подсказкой для агента.
        """
        prompt = \\\
            """
              - CREATE_EVENT: You can create a new event in your calendar. The content of the event has many fields, and you should use a JSON format to specify them. Here are the possible fields:\n                * title: The title of the event. Mandatory.\n                * description: A brief description of the event. Optional.\n                * mandatory_attendees: A list of agent names who must attend the event. Optional.\n                * optional_attendees: A list of agent names who are invited to the event, but are not required to attend. Optional.\n                * start_time: The start time of the event. Optional.\n                * end_time: The end time of the event. Optional.\n            """
        # TODO как будет обрабатываться список участников? Как им будут отправляться уведомления о приглашении? Я предполагаю, что у них тоже должен быть календарь. <-------------------------------------\
        
        return utils.dedent(prompt)
```

### `actions_constraints_prompt`

```python
    def actions_constraints_prompt(self) -> str:
        """
        Возвращает подсказку для агента с описанием ограничений для действий.

        Returns:
            Строка с подсказкой для агента.
        """
        prompt = \\\
            """
              
            """
            # TODO
        
        return textwrap.dedent(prompt)
```

## Параметры класса

- `calendar` (dict): Словарь, который хранит события в календаре. Ключи - даты, значения - списки событий.


## Примеры

```python
# Создание инстанса TinyCalendar
calendar = TinyCalendar()

# Добавление события
calendar.add_event(date='2024-03-10', title='Встреча с клиентом', description='Обсуждение нового проекта', owner='Иван Иванов', mandatory_attendees=['Петр Петров', 'Анна Сидорова'], start_time='10:00', end_time='11:00')

# Нахождение событий
events = calendar.find_events(year=2024, month=3, day=10)

# Вывод событий
print(events)