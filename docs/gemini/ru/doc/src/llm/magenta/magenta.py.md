# Модуль MagentaMusic

## Обзор

Модуль `MagentaMusic` предоставляет набор инструментов для генерации музыки с использованием моделей Magenta. 

## Подробней

Модуль использует библиотеку Magenta, предоставляемую Google, для генерации музыки. Magenta - это проект с открытым исходным кодом, который предоставляет инструменты и модели машинного обучения для создания и манипулирования музыкой. 

Модуль `MagentaMusic` позволяет создавать MIDI-файлы с помощью различных моделей Magenta, включая:

- `melody_rnn` - модель для генерации мелодий;
- `attention_rnn` - модель для генерации мелодий с использованием внимания;
- `basic_rnn` - простая модель для генерации мелодий;

## Классы

### `MagentaMusic`

**Описание**: Класс `MagentaMusic` предоставляет API для работы с моделями Magenta и генерации музыки.

**Наследует**: 
  - Не наследует других классов

**Атрибуты**:

- `output_dir` (str): Путь к папке для сохранения сгенерированных MIDI-файлов. 
- `model_name` (str): Название модели Magenta, которая используется для генерации музыки.  
- `temperature` (float): Температура генерации, определяющая вариативность сгенерированной музыки.  
- `num_steps` (int): Количество шагов (нот) в сгенерированной композиции.  
- `primer_midi_file` (str): Путь к MIDI-файлу, который используется в качестве затравки для генерации музыки.  
- `tempo` (int): Темп сгенерированной композиции. 
- `melody_rnn` (MelodyRnnSequenceGenerator): Объект модели `melody_rnn` из Magenta. 
- `primer_sequence` (NoteSequence): MIDI-затравка, загруженная из `primer_midi_file`. 

**Методы**:

- `_load_primer_sequence()`: Загружает MIDI-файл затравки или создает пустую `NoteSequence`, если файл не найден.
- `generate_melody()`: Генерирует мелодию с помощью модели `melody_rnn` с заданными параметрами.
- `add_chords()`: Добавляет аккорды к сгенерированной мелодии.
- `add_drums()`: Добавляет барабанный ритм к мелодии.
- `set_tempo()`: Устанавливает темп для композиции.
- `save_midi()`: Сохраняет готовую композицию в MIDI-файл.
- `generate_full_music()`: Выполняет все шаги генерации музыки: генерацию мелодии, добавление аккордов, добавление барабанов, установку темпа и сохранение в MIDI-файл.

#### **Внутренние функции**:

- **`_load_primer_sequence`**: Функция загружает MIDI-файл затравки. 

**Пример**:

```python
# Создание экземпляра класса MagentaMusic
music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn', temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)

# Генерация полной композиции 
music_generator.generate_full_music()

# Другой пример с другими параметрами
music_generator2 = MagentaMusic(output_dir='my_music2', model_name='basic_rnn', temperature=0.9, num_steps=150, primer_midi_file='primer2.mid', tempo=120)
music_generator2.generate_full_music()
```

## Методы класса

### `generate_melody`

```python
    def generate_melody(self):
        """
        Генерирует мелодию с помощью модели melody_rnn с заданными параметрами.

        Returns:
            NoteSequence: Сгенерированная мелодия в формате NoteSequence.
        """
        melody_sequence = self.melody_rnn.generate(
            temperature=self.temperature,
            steps=self.num_steps,
            primer_sequence=self.primer_sequence
        )
        return melody_sequence
```

### `add_chords`

```python
    def add_chords(self, melody_sequence):
        """
        Добавляет аккорды к сгенерированной мелодии.

        Args:
            melody_sequence (NoteSequence): Мелодия, к которой нужно добавить аккорды.

        Returns:
            NoteSequence: Мелодия с добавленными аккордами.
        """
        chords = [
            "C", "G", "Am", "F",
            "Dm", "G", "C", "G",
            "C", "F", "Dm", "G",
            "Am", "G", "F", "E"
        ] * (self.num_steps // 16)

        chord_sequence = mm.ChordSequence(chords)
        melody_with_chords_sequence = mm.sequences_lib.concatenate_sequences(melody_sequence, chord_sequence)
        return melody_with_chords_sequence
```

### `add_drums`

```python
    def add_drums(self, melody_with_chords_sequence):
        """
        Добавляет барабанный ритм к мелодии.

        Args:
            melody_with_chords_sequence (NoteSequence): Мелодия с аккордами, к которой нужно добавить барабанный ритм.

        Returns:
            NoteSequence: Мелодия с аккордами и барабанами.
        """
        drum_pattern = mm.DrumTrack(
            [36, 0, 42, 0, 38, 0, 46, 0, 36, 0, 42, 0, 38, 0, 45, 0],
            start_step=0,
            steps_per_bar=self.num_steps // 8,
            steps_per_quarter=8,
        )
        music_sequence = mm.sequences_lib.concatenate_sequences(melody_with_chords_sequence, drum_pattern)
        return music_sequence
```

### `set_tempo`

```python
    def set_tempo(self, music_sequence):
        """
        Устанавливает темп для композиции.

        Args:
            music_sequence (NoteSequence): Музыкальная композиция, к которой нужно установить темп.

        Returns:
            NoteSequence: Музыкальная композиция с заданным темпом.
        """
        music_sequence.tempos[0].qpm = self.tempo
        return music_sequence
```

### `save_midi`

```python
    def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
        """
        Сохраняет готовую композицию в MIDI-файл.

        Args:
            music_sequence (NoteSequence): Музыкальная композиция, которую нужно сохранить.
            filename (str): Имя файла для сохранения. По умолчанию 'full_music_advanced.mid'.
        """
        midi_file = os.path.join(self.output_dir, filename)
        mm.sequence_proto_to_midi_file(music_sequence, midi_file)
        print(f"Полная композиция сгенерирована и сохранена в: {midi_file}")
```

### `generate_full_music`

```python
    def generate_full_music(self):
        """
        Выполняет все шаги генерации музыки: генерацию мелодии, добавление аккордов, добавление барабанов, установку темпа и сохранение в MIDI-файл.
        """
        melody_sequence = self.generate_melody()
        melody_with_chords_sequence = self.add_chords(melody_sequence)
        music_sequence = self.add_drums(melody_with_chords_sequence)
        music_sequence = self.set_tempo(music_sequence)
        self.save_midi(music_sequence)
```

## Параметры класса

- `output_dir` (str): Путь к папке для сохранения сгенерированных MIDI-файлов. 
- `model_name` (str): Название модели Magenta, которая используется для генерации музыки.  
- `temperature` (float): Температура генерации, определяющая вариативность сгенерированной музыки.  
- `num_steps` (int): Количество шагов (нот) в сгенерированной композиции.  
- `primer_midi_file` (str): Путь к MIDI-файлу, который используется в качестве затравки для генерации музыки.  
- `tempo` (int): Темп сгенерированной композиции. 

**Примеры**:

```python
# Генерация музыки с заданными параметрами
music_generator = MagentaMusic(
    output_dir='my_music', 
    model_name='attention_rnn', 
    temperature=1.1, 
    num_steps=200, 
    primer_midi_file='primer.mid', 
    tempo=110
)
music_generator.generate_full_music()

# Генерация музыки с другим набором параметров
music_generator2 = MagentaMusic(
    output_dir='my_music2', 
    model_name='basic_rnn', 
    temperature=0.9, 
    num_steps=150, 
    primer_midi_file='primer2.mid', 
    tempo=120
)
music_generator2.generate_full_music()
```