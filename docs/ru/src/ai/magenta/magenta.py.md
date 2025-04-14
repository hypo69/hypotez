# Модуль для интеграции с Google generative AI (Magenta)

## Обзор

Модуль `magenta.py` предоставляет класс `MagentaMusic` для создания музыкальных композиций с использованием моделей Magenta. Он позволяет генерировать мелодии, добавлять аккорды и барабаны, устанавливать темп и сохранять результат в MIDI-файл.

## Подробнее

Этот модуль интегрируется с Magenta, библиотекой машинного обучения для создания музыки и искусства. Он предоставляет удобный интерфейс для генерации музыкальных последовательностей с использованием различных моделей, таких как `attention_rnn` и `basic_rnn`.

## Классы

### `MagentaMusic`

**Описание**: Класс для генерации музыкальных композиций с использованием моделей Magenta.

**Принцип работы**:
Класс `MagentaMusic` инкапсулирует все необходимые шаги для генерации музыки, начиная с загрузки затравки (primer), генерации мелодии, добавления аккордов и барабанов, установки темпа и заканчивая сохранением результата в MIDI-файл. Все настройки вынесены в конструктор `__init__`, что позволяет легко создавать экземпляры класса с различными параметрами.

**Атрибуты**:
- `output_dir` (str): Директория для сохранения сгенерированных MIDI-файлов. По умолчанию `generated_music_advanced`.
- `model_name` (str): Название используемой модели Magenta. По умолчанию `attention_rnn`.
- `temperature` (float): Параметр temperature для генерации мелодии. Влияет на случайность и креативность. По умолчанию `1.2`.
- `num_steps` (int): Количество шагов для генерации мелодии. По умолчанию `256`.
- `primer_midi_file` (str): Путь к MIDI-файлу затравки. По умолчанию `primer.mid`.
- `tempo` (int): Темп композиции в ударах в минуту (BPM). По умолчанию `100`.
- `melody_rnn` (melody_rnn_sequence_generator.MelodyRnnSequenceGenerator): Объект генератора мелодий.
- `primer_sequence` (mm.NoteSequence): Загруженная или пустая последовательность нот затравки.

**Методы**:
- `__init__(self, output_dir='generated_music_advanced', model_name='attention_rnn', temperature=1.2, num_steps=256, primer_midi_file='primer.mid', tempo=100)`: Инициализирует класс `MagentaMusic` с заданными параметрами.
- `_load_primer_sequence(self)`: Загружает MIDI-файл затравки или создаёт пустую `NoteSequence`, если файл не найден.
- `generate_melody(self)`: Генерирует мелодию с заданными параметрами.
- `add_chords(self, melody_sequence)`: Добавляет аккорды к мелодии.
- `add_drums(self, melody_with_chords_sequence)`: Добавляет барабаны к мелодии.
- `set_tempo(self, music_sequence)`: Устанавливает темп.
- `save_midi(self, music_sequence, filename='full_music_advanced.mid')`: Сохраняет готовую композицию в MIDI-файл.
- `generate_full_music(self)`: Объединяет все шаги в один вызов для удобства.

## Функции

### `MagentaMusic.__init__`

```python
def __init__(self, output_dir='generated_music_advanced', model_name='attention_rnn', temperature=1.2,
                 num_steps=256, primer_midi_file='primer.mid', tempo=100):
```

**Назначение**: Инициализирует объект класса `MagentaMusic` с заданными параметрами.

**Параметры**:
- `output_dir` (str): Директория для сохранения сгенерированных MIDI-файлов. По умолчанию `'generated_music_advanced'`.
- `model_name` (str): Название используемой модели Magenta. По умолчанию `'attention_rnn'`.
- `temperature` (float): Параметр temperature для генерации мелодии. По умолчанию `1.2`.
- `num_steps` (int): Количество шагов для генерации мелодии. По умолчанию `256`.
- `primer_midi_file` (str): Путь к MIDI-файлу затравки. По умолчанию `'primer.mid'`.
- `tempo` (int): Темп композиции в ударах в минуту (BPM). По умолчанию `100`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `OSError`: Если не удается создать директорию для сохранения файлов.

**Как работает функция**:
1. Инициализирует параметры класса, такие как `output_dir`, `model_name`, `temperature`, `num_steps`, `primer_midi_file` и `tempo`.
2. Создает директорию для сохранения сгенерированных MIDI-файлов, если она не существует.
3. Инициализирует объект `melody_rnn_sequence_generator.MelodyRnnSequenceGenerator` с указанным `model_name`.
4. Загружает затравку (primer) с помощью метода `_load_primer_sequence`.

```
A: Инициализация параметров
|
B: Создание директории (если не существует)
|
C: Инициализация MelodyRnnSequenceGenerator
|
D: Загрузка затравки
```

**Примеры**:

```python
# Пример 1: Создание объекта MagentaMusic с параметрами по умолчанию
music_generator = MagentaMusic()

# Пример 2: Создание объекта MagentaMusic с указанием директории вывода и модели
music_generator = MagentaMusic(output_dir='my_music', model_name='basic_rnn')

# Пример 3: Создание объекта MagentaMusic с указанием всех параметров
music_generator = MagentaMusic(output_dir='my_music', model_name='basic_rnn', temperature=0.9, num_steps=150, primer_midi_file='primer2.mid', tempo=120)
```

### `MagentaMusic._load_primer_sequence`

```python
def _load_primer_sequence(self):
```

**Назначение**: Загружает MIDI-файл затравки или создаёт пустую NoteSequence, если файл не найден.

**Параметры**:
- `self` (MagentaMusic): Экземпляр класса MagentaMusic.

**Возвращает**:
- `mm.NoteSequence`: Последовательность нот, загруженная из MIDI-файла затравки или пустая последовательность нот.

**Вызывает исключения**:
- `IOError`: Если возникает ошибка при чтении MIDI-файла.

**Как работает функция**:

1. Проверяет существование файла затравки (primer_midi_file).
2. Если файл существует, загружает его с помощью `mm.midi_file_to_sequence_proto` и выводит сообщение об использовании затравки.
3. Если файл не существует, создает пустую NoteSequence и выводит сообщение об отсутствии затравки.

```
A: Проверка существования файла затравки
|
B: Загрузка MIDI-файла (если существует)
|
C: Создание пустой NoteSequence (если файл не существует)
```

**Примеры**:

```python
# Пример 1: Загрузка существующего файла затравки
music_generator = MagentaMusic(primer_midi_file='existing_primer.mid')
primer_sequence = music_generator._load_primer_sequence()

# Пример 2: Создание пустой NoteSequence, если файл затравки не существует
music_generator = MagentaMusic(primer_midi_file='non_existing_primer.mid')
primer_sequence = music_generator._load_primer_sequence()
```

### `MagentaMusic.generate_melody`

```python
def generate_melody(self):
```

**Назначение**: Генерирует мелодию с заданными параметрами.

**Параметры**:
- `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.

**Возвращает**:
- `mm.NoteSequence`: Сгенерированная мелодия.

**Вызывает исключения**:
- `ValueError`: Если параметры генерации мелодии неверны.

**Как работает функция**:
1. Вызывает метод `generate` объекта `self.melody_rnn` для генерации мелодии с использованием заданных параметров `temperature`, `steps` (количество шагов) и `primer_sequence` (затравка).
2. Возвращает сгенерированную мелодию.

```
A: Генерация мелодии с использованием melody_rnn.generate
|
B: Возврат сгенерированной мелодии
```

**Примеры**:

```python
# Пример: Генерация мелодии с использованием параметров по умолчанию
music_generator = MagentaMusic()
melody_sequence = music_generator.generate_melody()
```

### `MagentaMusic.add_chords`

```python
def add_chords(self, melody_sequence):
```

**Назначение**: Добавляет аккорды к мелодии.

**Параметры**:
- `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
- `melody_sequence` (mm.NoteSequence): Последовательность нот мелодии, к которой нужно добавить аккорды.

**Возвращает**:
- `mm.NoteSequence`: Мелодия с добавленными аккордами.

**Вызывает исключения**:
- `TypeError`: Если `melody_sequence` не является объектом `mm.NoteSequence`.

**Как работает функция**:
1. Создает список аккордов `chords`.
2. Создает объект `mm.ChordSequence` из списка аккордов.
3. Объединяет мелодию и аккорды с помощью `mm.sequences_lib.concatenate_sequences`.
4. Возвращает объединенную последовательность.

```
A: Создание списка аккордов
|
B: Создание ChordSequence из списка аккордов
|
C: Объединение мелодии и аккордов
|
D: Возврат объединенной последовательности
```

**Примеры**:

```python
# Пример: Добавление аккордов к существующей мелодии
music_generator = MagentaMusic()
melody_sequence = music_generator.generate_melody()
melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
```

### `MagentaMusic.add_drums`

```python
def add_drums(self, melody_with_chords_sequence):
```

**Назначение**: Добавляет барабаны к мелодии с аккордами.

**Параметры**:
- `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
- `melody_with_chords_sequence` (mm.NoteSequence): Последовательность нот мелодии с аккордами, к которой нужно добавить барабаны.

**Возвращает**:
- `mm.NoteSequence`: Мелодия с аккордами и барабанами.

**Вызывает исключения**:
- `TypeError`: Если `melody_with_chords_sequence` не является объектом `mm.NoteSequence`.

**Как работает функция**:
1. Создает объект `mm.DrumTrack` с определенным паттерном барабанов.
2. Объединяет мелодию с аккордами и барабанами с помощью `mm.sequences_lib.concatenate_sequences`.
3. Возвращает объединенную последовательность.

```
A: Создание объекта DrumTrack с паттерном барабанов
|
B: Объединение мелодии с аккордами и барабанами
|
C: Возврат объединенной последовательности
```

**Примеры**:

```python
# Пример: Добавление барабанов к мелодии с аккордами
music_generator = MagentaMusic()
melody_sequence = music_generator.generate_melody()
melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
music_sequence = music_generator.add_drums(melody_with_chords_sequence)
```

### `MagentaMusic.set_tempo`

```python
def set_tempo(self, music_sequence):
```

**Назначение**: Устанавливает темп для музыкальной последовательности.

**Параметры**:
- `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
- `music_sequence` (mm.NoteSequence): Музыкальная последовательность, для которой нужно установить темп.

**Возвращает**:
- `mm.NoteSequence`: Музыкальная последовательность с установленным темпом.

**Вызывает исключения**:
- `AttributeError`: Если `music_sequence` не содержит атрибут `tempos`.

**Как работает функция**:
1. Устанавливает значение `qpm` (ударов в минуту) первого элемента в списке `music_sequence.tempos` равным значению `self.tempo`.
2. Возвращает музыкальную последовательность с установленным темпом.

```
A: Установка темпа для музыкальной последовательности
|
B: Возврат музыкальной последовательности с установленным темпом
```

**Примеры**:

```python
# Пример: Установка темпа для музыкальной последовательности
music_generator = MagentaMusic(tempo=120)
melody_sequence = music_generator.generate_melody()
melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
music_sequence = music_generator.add_drums(melody_with_chords_sequence)
music_sequence = music_generator.set_tempo(music_sequence)
```

### `MagentaMusic.save_midi`

```python
def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
```

**Назначение**: Сохраняет музыкальную последовательность в MIDI-файл.

**Параметры**:
- `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.
- `music_sequence` (mm.NoteSequence): Музыкальная последовательность, которую нужно сохранить.
- `filename` (str): Имя файла для сохранения MIDI-файла. По умолчанию `'full_music_advanced.mid'`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `IOError`: Если не удается создать или записать в файл.

**Как работает функция**:
1. Формирует полный путь к файлу, объединяя `self.output_dir` и `filename`.
2. Сохраняет музыкальную последовательность в MIDI-файл с помощью `mm.sequence_proto_to_midi_file`.
3. Выводит сообщение об успешном сохранении файла.

```
A: Формирование полного пути к файлу
|
B: Сохранение музыкальной последовательности в MIDI-файл
|
C: Вывод сообщения об успешном сохранении
```

**Примеры**:

```python
# Пример: Сохранение музыкальной последовательности в MIDI-файл
music_generator = MagentaMusic(output_dir='my_music')
melody_sequence = music_generator.generate_melody()
melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
music_sequence = music_generator.add_drums(melody_with_chords_sequence)
music_generator.save_midi(music_sequence, filename='my_music.mid')
```

### `MagentaMusic.generate_full_music`

```python
def generate_full_music(self):
```

**Назначение**: Генерирует полную музыкальную композицию, объединяя все шаги в один вызов.

**Параметры**:
- `self` (MagentaMusic): Экземпляр класса `MagentaMusic`.

**Возвращает**:
- `None`

**Вызывает исключения**:
- `Exception`: Если какой-либо из шагов генерации музыки завершается с ошибкой.

**Как работает функция**:
1. Генерирует мелодию с помощью `self.generate_melody()`.
2. Добавляет аккорды к мелодии с помощью `self.add_chords()`.
3. Добавляет барабаны к мелодии с аккордами с помощью `self.add_drums()`.
4. Устанавливает темп с помощью `self.set_tempo()`.
5. Сохраняет полную композицию в MIDI-файл с помощью `self.save_midi()`.

```
A: Генерация мелодии
|
B: Добавление аккордов
|
C: Добавление барабанов
|
D: Установка темпа
|
E: Сохранение MIDI-файла
```

**Примеры**:

```python
# Пример: Генерация полной музыкальной композиции с использованием всех шагов
music_generator = MagentaMusic(output_dir='my_music')
music_generator.generate_full_music()
```

## Примеры

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
```