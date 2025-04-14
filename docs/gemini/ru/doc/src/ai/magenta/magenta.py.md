# Модуль magenta.py

## Обзор

Модуль `magenta.py` предоставляет интеграцию с Google generative AI для создания музыки с использованием библиотеки Magenta. Он содержит класс `MagentaMusic`, который позволяет генерировать мелодии, добавлять аккорды и барабаны, устанавливать темп и сохранять готовую композицию в MIDI-файл.

## Подробнее

Этот модуль предназначен для автоматической генерации музыки с использованием моделей машинного обучения, предоставляемых Magenta. Класс `MagentaMusic` упрощает процесс создания музыкальных композиций, объединяя несколько этапов в один вызов. Пользователь может настроить различные параметры, такие как модель, температура, количество шагов, MIDI-файл затравки и темп.

## Классы

### `MagentaMusic`

**Описание**: Класс для генерации музыки с использованием библиотеки Magenta.

**Атрибуты**:
- `output_dir` (str): Директория для сохранения сгенерированной музыки. По умолчанию 'generated_music_advanced'.
- `model_name` (str): Название используемой модели Magenta. По умолчанию 'attention_rnn'.
- `temperature` (float): Параметр температуры для генерации мелодии. По умолчанию 1.2.
- `num_steps` (int): Количество шагов для генерации мелодии. По умолчанию 256.
- `primer_midi_file` (str): Путь к MIDI-файлу затравки. По умолчанию 'primer.mid'.
- `tempo` (int): Темп музыки в ударах в минуту. По умолчанию 100.
- `melody_rnn` (melody_rnn_sequence_generator.MelodyRnnSequenceGenerator): Объект генератора мелодий Magenta.
- `primer_sequence` (mm.NoteSequence): MIDI-последовательность затравки.

**Методы**:
- `__init__`: Инициализирует класс `MagentaMusic` с заданными параметрами.
- `_load_primer_sequence`: Загружает MIDI-файл затравки или создает пустую NoteSequence, если файл не найден.
- `generate_melody`: Генерирует мелодию с заданными параметрами.
- `add_chords`: Добавляет аккорды к мелодии.
- `add_drums`: Добавляет барабаны к мелодии.
- `set_tempo`: Устанавливает темп.
- `save_midi`: Сохраняет готовую композицию в MIDI-файл.
- `generate_full_music`: Объединяет все шаги в один вызов для удобства.

#### `__init__`

```python
def __init__(self, output_dir='generated_music_advanced', model_name='attention_rnn', temperature=1.2,
             num_steps=256, primer_midi_file='primer.mid', tempo=100):
    """
    Инициализирует класс MagentaMusic с заданными параметрами.

    Args:
        output_dir (str): Директория для сохранения сгенерированной музыки. По умолчанию 'generated_music_advanced'.
        model_name (str): Название используемой модели Magenta. По умолчанию 'attention_rnn'.
        temperature (float): Параметр температуры для генерации мелодии. По умолчанию 1.2.
        num_steps (int): Количество шагов для генерации мелодии. По умолчанию 256.
        primer_midi_file (str): Путь к MIDI-файлу затравки. По умолчанию 'primer.mid'.
        tempo (int): Темп музыки в ударах в минуту. По умолчанию 100.
    """
    ...
```

**Назначение**: Инициализация объекта класса `MagentaMusic`. Создает директорию для сохранения сгенерированной музыки, инициализирует генератор мелодий и загружает MIDI-файл затравки.

**Параметры**:
- `output_dir` (str): Директория для сохранения сгенерированной музыки. По умолчанию 'generated_music_advanced'.
- `model_name` (str): Название используемой модели Magenta. По умолчанию 'attention_rnn'.
- `temperature` (float): Параметр температуры для генерации мелодии. По умолчанию 1.2.
- `num_steps` (int): Количество шагов для генерации мелодии. По умолчанию 256.
- `primer_midi_file` (str): Путь к MIDI-файлу затравки. По умолчанию 'primer.mid'.
- `tempo` (int): Темп музыки в ударах в минуту. По умолчанию 100.

**Как работает функция**:
- Создает директорию для сохранения сгенерированной музыки, если она не существует.
- Инициализирует объект генератора мелодий Magenta с заданным именем модели.
- Загружает MIDI-файл затравки с использованием метода `_load_primer_sequence`.
- Сохраняет значения параметров в атрибутах объекта.

**Примеры**:
```python
music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
```

#### `_load_primer_sequence`

```python
def _load_primer_sequence(self):
    """
    Загружает MIDI-файл затравки или создает пустую NoteSequence, если файл не найден.

    Returns:
        mm.NoteSequence: MIDI-последовательность затравки.
    """
    ...
```

**Назначение**: Загружает MIDI-файл затравки или создает пустую `NoteSequence`, если файл не найден.

**Как работает функция**:
- Проверяет, существует ли файл, указанный в `self.primer_midi_file`.
- Если файл существует, он преобразуется в объект `NoteSequence` с использованием `mm.midi_file_to_sequence_proto`.
- Если файл не существует, создается пустая `NoteSequence`.

**Возвращает**:
- `mm.NoteSequence`: MIDI-последовательность затравки.

**Примеры**:
```python
primer_sequence = music_generator._load_primer_sequence()
```

#### `generate_melody`

```python
def generate_melody(self):
    """
    Генерирует мелодию с заданными параметрами.

    Returns:
        mm.NoteSequence: Сгенерированная мелодия.
    """
    ...
```

**Назначение**: Генерирует мелодию с использованием объекта `melody_rnn`.

**Как работает функция**:
- Вызывает метод `generate` объекта `melody_rnn` с параметрами `temperature`, `steps` и `primer_sequence`.
- Возвращает сгенерированную мелодию в виде объекта `NoteSequence`.

**Возвращает**:
- `mm.NoteSequence`: Сгенерированная мелодия.

**Примеры**:
```python
melody_sequence = music_generator.generate_melody()
```

#### `add_chords`

```python
def add_chords(self, melody_sequence):
    """
    Добавляет аккорды к мелодии.

    Args:
        melody_sequence (mm.NoteSequence): Мелодия, к которой нужно добавить аккорды.

    Returns:
        mm.NoteSequence: Мелодия с добавленными аккордами.
    """
    ...
```

**Назначение**: Добавляет аккорды к заданной мелодии.

**Параметры**:
- `melody_sequence` (mm.NoteSequence): Мелодия, к которой нужно добавить аккорды.

**Как работает функция**:
- Определяет последовательность аккордов.
- Создает объект `ChordSequence` из последовательности аккордов.
- Объединяет мелодию и аккорды с использованием `mm.sequences_lib.concatenate_sequences`.

**Возвращает**:
- `mm.NoteSequence`: Мелодия с добавленными аккордами.

**Примеры**:
```python
melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
```

#### `add_drums`

```python
def add_drums(self, melody_with_chords_sequence):
    """
    Добавляет барабаны к мелодии.

    Args:
        melody_with_chords_sequence (mm.NoteSequence): Мелодия с аккордами, к которой нужно добавить барабаны.

    Returns:
        mm.NoteSequence: Мелодия с аккордами и барабанами.
    """
    ...
```

**Назначение**: Добавляет партию барабанов к заданной мелодии с аккордами.

**Параметры**:
- `melody_with_chords_sequence` (mm.NoteSequence): Мелодия с аккордами, к которой нужно добавить барабаны.

**Как работает функция**:
- Определяет паттерн барабанов.
- Создает объект `DrumTrack` из паттерна барабанов.
- Объединяет мелодию с аккордами и барабанами с использованием `mm.sequences_lib.concatenate_sequences`.

**Возвращает**:
- `mm.NoteSequence`: Мелодия с аккордами и барабанами.

**Примеры**:
```python
music_sequence = music_generator.add_drums(melody_with_chords_sequence)
```

#### `set_tempo`

```python
def set_tempo(self, music_sequence):
    """
    Устанавливает темп.

    Args:
        music_sequence (mm.NoteSequence): Музыкальная последовательность, для которой нужно установить темп.

    Returns:
        mm.NoteSequence: Музыкальная последовательность с установленным темпом.
    """
    ...
```

**Назначение**: Устанавливает темп для заданной музыкальной последовательности.

**Параметры**:
- `music_sequence` (mm.NoteSequence): Музыкальная последовательность, для которой нужно установить темп.

**Как работает функция**:
- Устанавливает темп музыкальной последовательности, изменяя атрибут `qpm` первого элемента в списке `tempos`.

**Возвращает**:
- `mm.NoteSequence`: Музыкальная последовательность с установленным темпом.

**Примеры**:
```python
music_sequence = music_generator.set_tempo(music_sequence)
```

#### `save_midi`

```python
def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
    """
    Сохраняет готовую композицию в MIDI-файл.

    Args:
        music_sequence (mm.NoteSequence): Музыкальная последовательность для сохранения.
        filename (str): Имя файла для сохранения. По умолчанию 'full_music_advanced.mid'.
    """
    ...
```

**Назначение**: Сохраняет музыкальную последовательность в MIDI-файл.

**Параметры**:
- `music_sequence` (mm.NoteSequence): Музыкальная последовательность для сохранения.
- `filename` (str): Имя файла для сохранения. По умолчанию 'full_music_advanced.mid'.

**Как работает функция**:
- Формирует полный путь к файлу, объединяя `self.output_dir` и `filename`.
- Преобразует музыкальную последовательность в MIDI-файл с использованием `mm.sequence_proto_to_midi_file`.

**Примеры**:
```python
music_generator.save_midi(music_sequence)
```

#### `generate_full_music`

```python
def generate_full_music(self):
    """
    Объединяет все шаги в один вызов для удобства.
    """
    ...
```

**Назначение**: Генерирует полную музыкальную композицию, объединяя все этапы: генерацию мелодии, добавление аккордов и барабанов, установку темпа и сохранение в MIDI-файл.

**Как работает функция**:
- Вызывает методы `generate_melody`, `add_chords`, `add_drums` и `set_tempo` для создания музыкальной последовательности.
- Сохраняет полученную музыкальную последовательность в MIDI-файл с использованием метода `save_midi`.

**Примеры**:
```python
music_generator.generate_full_music()
```

## Примеры использования

```python
if __name__ == '__main__':
    # Пример использования класса
    music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                    temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
    music_generator.generate_full_music()

    # Другой пример с другими параметрами
    music_generator2 = MagentaMusic(output_dir='my_music2', model_name='basic_rnn',
                                    temperature=0.9, num_steps=150, primer_midi_file='primer2.mid', tempo=120)
    music_generator2.generate_full_music()