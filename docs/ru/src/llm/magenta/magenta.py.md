# Модуль magenta.py: Интеграция с Google Generative AI для создания музыки

## Обзор

Модуль `magenta.py` предоставляет класс `MagentaMusic` для интеграции с Google Generative AI, в частности, с библиотекой Magenta, для создания музыки. Он позволяет генерировать мелодии, добавлять аккорды и барабаны, устанавливать темп и сохранять готовую композицию в MIDI-файл. Модуль предназначен для автоматической генерации музыкальных произведений с использованием различных моделей машинного обучения.

## Подробнее

Модуль `magenta.py` предназначен для работы с библиотекой Magenta от Google для генерации музыки. Он предоставляет класс `MagentaMusic`, который упрощает процесс создания музыкальных композиций с использованием предобученных моделей машинного обучения. Класс позволяет настраивать параметры генерации, такие как модель, температура, количество шагов и темп. Также поддерживается использование MIDI-файлов в качестве затравки для генерации.

## Классы

### `MagentaMusic`

**Описание**: Класс для генерации музыки с использованием библиотеки Magenta.

**Атрибуты**:

-   `output_dir` (str): Директория для сохранения сгенерированных MIDI-файлов. По умолчанию 'generated\_music\_advanced'.
-   `model_name` (str): Название используемой модели для генерации мелодии. По умолчанию 'attention\_rnn'.
-   `temperature` (float): Параметр температуры для управления случайностью генерации. По умолчанию 1.2.
-   `num_steps` (int): Количество шагов для генерации мелодии. По умолчанию 256.
-   `primer_midi_file` (str): Путь к MIDI-файлу, используемому в качестве затравки. По умолчанию 'primer.mid'.
-   `tempo` (int): Темп композиции в ударах в минуту. По умолчанию 100.
-   `melody_rnn` (melody_rnn_sequence_generator.MelodyRnnSequenceGenerator): Объект для генерации мелодии с использованием выбранной модели.
-   `primer_sequence` (mm.NoteSequence): Последовательность нот, используемая в качестве затравки для генерации мелодии.

**Методы**:

-   `__init__`: Инициализирует класс `MagentaMusic` с заданными параметрами.
-   `_load_primer_sequence`: Загружает MIDI-файл затравки или создает пустую NoteSequence, если файл не найден.
-   `generate_melody`: Генерирует мелодию с заданными параметрами.
-   `add_chords`: Добавляет аккорды к мелодии.
-   `add_drums`: Добавляет барабаны к мелодии.
-   `set_tempo`: Устанавливает темп.
-   `save_midi`: Сохраняет готовую композицию в MIDI-файл.
-   `generate_full_music`: Объединяет все шаги в один вызов для удобства.

**Принцип работы**:

Класс `MagentaMusic` предоставляет интерфейс для генерации музыки с использованием библиотеки Magenta. Он инициализируется с заданными параметрами, такими как директория вывода, название модели, температура, количество шагов, MIDI-файл затравки и темп. При инициализации класса происходит создание директории для сохранения сгенерированных MIDI-файлов, загрузка MIDI-файла затравки (если он существует) и инициализация объекта `melody_rnn` для генерации мелодии.

Метод `generate_full_music` объединяет все шаги в один вызов для удобства. Он вызывает методы `generate_melody`, `add_chords`, `add_drums`, `set_tempo` и `save_midi` для генерации полной музыкальной композиции.

## Методы класса

### `__init__`

```python
def __init__(self, output_dir='generated_music_advanced', model_name='attention_rnn', temperature=1.2,
             num_steps=256, primer_midi_file='primer.mid', tempo=100):
    """ Инициализирует класс `MagentaMusic` с заданными параметрами.
    Args:
        output_dir (str): Директория для сохранения сгенерированных MIDI-файлов. По умолчанию 'generated_music_advanced'.
        model_name (str): Название используемой модели для генерации мелодии. По умолчанию 'attention_rnn'.
        temperature (float): Параметр температуры для управления случайностью генерации. По умолчанию 1.2.
        num_steps (int): Количество шагов для генерации мелодии. По умолчанию 256.
        primer_midi_file (str): Путь к MIDI-файлу, используемому в качестве затравки. По умолчанию 'primer.mid'.
        tempo (int): Темп композиции в ударах в минуту. По умолчанию 100.
    """
```

**Назначение**: Инициализирует объект класса `MagentaMusic` с заданными параметрами.

**Параметры**:

-   `output_dir` (str): Директория для сохранения сгенерированных MIDI-файлов.
-   `model_name` (str): Название используемой модели для генерации мелодии.
-   `temperature` (float): Параметр температуры для управления случайностью генерации.
-   `num_steps` (int): Количество шагов для генерации мелодии.
-   `primer_midi_file` (str): Путь к MIDI-файлу, используемому в качестве затравки.
-   `tempo` (int): Темп композиции в ударах в минуту.

**Как работает функция**:

Функция инициализирует объект класса `MagentaMusic` с заданными параметрами. Она создает директорию для сохранения сгенерированных MIDI-файлов, инициализирует объект `melody_rnn` для генерации мелодии и загружает MIDI-файл затравки (если он существует).

**Примеры**:

```python
music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
```

### `_load_primer_sequence`

```python
def _load_primer_sequence(self):
    """ Загружает MIDI-файл затравки или создает пустую NoteSequence, если файл не найден.
    Args:
        self (MagentaMusic): Экземпляр класса `MagentaMusic`.

    Returns:
        mm.NoteSequence: Последовательность нот, используемая в качестве затравки для генерации мелодии.
    """
```

**Назначение**: Загружает MIDI-файл затравки или создает пустую `NoteSequence`, если файл не найден.

**Параметры**:

-   `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.

**Возвращает**:

-   `mm.NoteSequence`: Последовательность нот, используемая в качестве затравки для генерации мелодии.

**Как работает функция**:

Функция проверяет существование файла, указанного в `self.primer_midi_file`. Если файл существует, функция преобразует MIDI-файл в объект `NoteSequence` и возвращает его. Если файл не существует, функция создает пустую `NoteSequence` и возвращает ее.

**Примеры**:

```python
primer_sequence = music_generator._load_primer_sequence()
```

### `generate_melody`

```python
def generate_melody(self):
    """ Генерирует мелодию с заданными параметрами.
    Args:
        self (MagentaMusic): Экземпляр класса `MagentaMusic`.

    Returns:
        melody_sequence (mm.NoteSequence): Сгенерированная мелодия в формате NoteSequence.
    """
```

**Назначение**: Генерирует мелодию с заданными параметрами.

**Параметры**:

-   `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.

**Возвращает**:

-   `melody_sequence` (mm.NoteSequence): Сгенерированная мелодия в формате `NoteSequence`.

**Как работает функция**:

Функция использует объект `self.melody_rnn` для генерации мелодии с заданными параметрами, такими как температура, количество шагов и затравка. Она вызывает метод `generate` объекта `self.melody_rnn` и возвращает сгенерированную мелодию в формате `NoteSequence`.

**Примеры**:

```python
melody_sequence = music_generator.generate_melody()
```

### `add_chords`

```python
def add_chords(self, melody_sequence):
    """ Добавляет аккорды к мелодии.
    Args:
        self (MagentaMusic): Экземпляр класса `MagentaMusic`.
        melody_sequence (mm.NoteSequence): Мелодия, к которой нужно добавить аккорды.

    Returns:
        melody_with_chords_sequence (mm.NoteSequence): Мелодия с добавленными аккордами.
    """
```

**Назначение**: Добавляет аккорды к мелодии.

**Параметры**:

-   `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
-   `melody_sequence` (mm.NoteSequence): Мелодия, к которой нужно добавить аккорды.

**Возвращает**:

-   `melody_with_chords_sequence` (mm.NoteSequence): Мелодия с добавленными аккордами.

**Как работает функция**:

Функция создает последовательность аккордов на основе списка аккордов и количества шагов. Затем она объединяет мелодию и аккорды с помощью функции `mm.sequences_lib.concatenate_sequences` и возвращает результат.

**Примеры**:

```python
melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
```

### `add_drums`

```python
def add_drums(self, melody_with_chords_sequence):
    """ Добавляет барабаны к мелодии.
    Args:
        self (MagentaMusic): Экземпляр класса `MagentaMusic`.
        melody_with_chords_sequence (mm.NoteSequence): Мелодия с аккордами, к которой нужно добавить барабаны.

    Returns:
        music_sequence (mm.NoteSequence): Мелодия с аккордами и барабанами.
    """
```

**Назначение**: Добавляет барабаны к мелодии.

**Параметры**:

-   `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
-   `melody_with_chords_sequence` (mm.NoteSequence): Мелодия с аккордами, к которой нужно добавить барабаны.

**Возвращает**:

-   `music_sequence` (mm.NoteSequence): Мелодия с аккордами и барабанами.

**Как работает функция**:

Функция создает барабанный паттерн на основе списка MIDI-номеров барабанов и параметров такта. Затем она объединяет мелодию с аккордами и барабанами с помощью функции `mm.sequences_lib.concatenate_sequences` и возвращает результат.

**Примеры**:

```python
music_sequence = music_generator.add_drums(melody_with_chords_sequence)
```

### `set_tempo`

```python
def set_tempo(self, music_sequence):
    """ Устанавливает темп.
    Args:
        self (MagentaMusic): Экземпляр класса `MagentaMusic`.
        music_sequence (mm.NoteSequence): Музыкальная последовательность, для которой нужно установить темп.

    Returns:
        music_sequence (mm.NoteSequence): Музыкальная последовательность с установленным темпом.
    """
```

**Назначение**: Устанавливает темп.

**Параметры**:

-   `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
-   `music_sequence` (mm.NoteSequence): Музыкальная последовательность, для которой нужно установить темп.

**Возвращает**:

-   `music_sequence` (mm.NoteSequence): Музыкальная последовательность с установленным темпом.

**Как работает функция**:

Функция устанавливает темп музыкальной последовательности, изменяя значение `qpm` в первом элементе списка `tempos` объекта `music_sequence`.

**Примеры**:

```python
music_sequence = music_generator.set_tempo(music_sequence)
```

### `save_midi`

```python
def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
    """ Сохраняет готовую композицию в MIDI-файл.
    Args:
        self (MagentaMusic): Экземпляр класса `MagentaMusic`.
        music_sequence (mm.NoteSequence): Музыкальная последовательность, которую нужно сохранить.
        filename (str): Имя файла для сохранения MIDI-файла. По умолчанию 'full_music_advanced.mid'.
    """
```

**Назначение**: Сохраняет готовую композицию в MIDI-файл.

**Параметры**:

-   `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
-   `music_sequence` (mm.NoteSequence): Музыкальная последовательность, которую нужно сохранить.
-   `filename` (str): Имя файла для сохранения MIDI-файла.

**Как работает функция**:

Функция преобразует музыкальную последовательность в MIDI-файл и сохраняет его в указанной директории с указанным именем файла.

**Примеры**:

```python
music_generator.save_midi(music_sequence)
```

### `generate_full_music`

```python
def generate_full_music(self):
    """ Объединяет все шаги в один вызов для удобства.
    Args:
        self (MagentaMusic): Экземпляр класса `MagentaMusic`.
    """
```

**Назначение**: Объединяет все шаги в один вызов для удобства.

**Параметры**:

-   `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.

**Как работает функция**:

Функция вызывает методы `generate_melody`, `add_chords`, `add_drums`, `set_tempo` и `save_midi` для генерации полной музыкальной композиции.

**Примеры**:

```python
music_generator.generate_full_music()
```

## Параметры класса

-   `output_dir` (str): Директория для сохранения сгенерированных MIDI-файлов. По умолчанию 'generated\_music\_advanced'.
-   `model_name` (str): Название используемой модели для генерации мелодии. По умолчанию 'attention\_rnn'.
-   `temperature` (float): Параметр температуры для управления случайностью генерации. По умолчанию 1.2.
-   `num_steps` (int): Количество шагов для генерации мелодии. По умолчанию 256.
-   `primer_midi_file` (str): Путь к MIDI-файлу, используемому в качестве затравки. По умолчанию 'primer.mid'.
-   `tempo` (int): Темп композиции в ударах в минуту. По умолчанию 100.

## Примеры

```python
# Пример использования класса
music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
music_generator.generate_full_music()

# Другой пример с другими параметрами
music_generator2 = MagentaMusic(output_dir='my_music2', model_name='basic_rnn',
                                temperature=0.9, num_steps=150, primer_midi_file='primer2.mid', tempo=120)
music_generator2.generate_full_music()