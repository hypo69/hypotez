# Magenta Music Generator

## Overview

This module implements a class for generating music using Magenta, a Google research project. It utilizes a melody RNN model for generating melodies and allows customization of parameters like temperature, number of steps, primer MIDI file, and tempo. 

The `MagentaMusic` class provides methods for loading primer sequences, generating melodies, adding chords and drums, setting tempo, and saving the final composition as a MIDI file. 

## Details

This module leverages Magenta's melody RNN model to generate music. The generated music can be customized using various parameters, including:

- **Temperature:** Controls the randomness of the generated melody. Higher values result in more surprising outcomes.
- **Number of Steps:** Defines the length of the generated melody.
- **Primer MIDI File:** Enables using an existing MIDI file as a starting point for the generation process.
- **Tempo:** Sets the tempo of the generated music.

## Classes

### `MagentaMusic`

**Description**: This class encapsulates the logic for generating music using Magenta's melody RNN model.

**Attributes**:

- `output_dir` (str): The directory where generated MIDI files will be saved.
- `model_name` (str): The name of the Magenta melody RNN model to use.
- `temperature` (float): The temperature parameter controlling randomness during melody generation.
- `num_steps` (int): The number of steps in the generated melody.
- `primer_midi_file` (str): The path to the MIDI file used as a primer for the melody.
- `tempo` (int): The tempo of the generated music.

**Methods**:

- `_load_primer_sequence()`: Loads a MIDI primer file or creates an empty NoteSequence if no primer file is found.

- `generate_melody()`: Generates a melody sequence using the specified model and parameters.

- `add_chords()`: Adds chords to the generated melody sequence based on a predefined chord progression.

- `add_drums()`: Adds drum patterns to the melody sequence.

- `set_tempo()`: Sets the tempo of the music sequence.

- `save_midi()`: Saves the finalized music sequence as a MIDI file in the output directory.

- `generate_full_music()`: Combines all steps (melody generation, adding chords, drums, setting tempo, and saving) into a single method call.

## Class Methods

### `_load_primer_sequence()`

```python
    def _load_primer_sequence(self):
        """ 
        Загружает MIDI-файл затравки или создаёт пустую NoteSequence, если файл не найден.

        Returns:
            mm.NoteSequence: Загруженная NoteSequence или пустая NoteSequence.
        """
        if os.path.exists(self.primer_midi_file):
            primer_sequence = mm.midi_file_to_sequence_proto(self.primer_midi_file)
            print(f"Используем primer из {self.primer_midi_file}")
            return primer_sequence
        else:
            print("Не найдена primer, начинаем с пустой мелодии")
            return mm.NoteSequence(notes=[])
```

**Purpose**: Loads a MIDI file as a primer for the music generation process. If no primer file exists, it creates an empty NoteSequence.

**Parameters**:

- None

**Returns**:

- `mm.NoteSequence`: The loaded NoteSequence or an empty NoteSequence if no primer file is found.

**How the Function Works**:

1.  Checks if the primer MIDI file exists at the specified path.
2.  If the file exists, loads it into a NoteSequence using the `magenta.music.midi_file_to_sequence_proto` function.
3.  If the file doesn't exist, creates an empty NoteSequence with no notes.

**Examples**:

```python
    >>> music_generator = MagentaMusic(primer_midi_file='my_primer.mid')
    >>> primer_sequence = music_generator._load_primer_sequence()
    >>> print(primer_sequence)
    NoteSequence(...) # Output will depend on the primer MIDI file
```

### `generate_melody()`

```python
    def generate_melody(self):
        """ 
        Генерирует мелодию с заданными параметрами.

        Returns:
            mm.NoteSequence: Сгенерированная мелодическая последовательность.
        """
        melody_sequence = self.melody_rnn.generate(
            temperature=self.temperature,
            steps=self.num_steps,
            primer_sequence=self.primer_sequence
        )
        return melody_sequence
```

**Purpose**: Generates a melody sequence using the selected melody RNN model and the specified parameters.

**Parameters**:

- None

**Returns**:

- `mm.NoteSequence`: The generated melody sequence.

**How the Function Works**:

1.  Calls the `generate()` method of the `melody_rnn` object, which is an instance of `MelodyRnnSequenceGenerator`.
2.  Passes the `temperature`, `steps`, and `primer_sequence` parameters to the `generate()` method.
3.  The `generate()` method of the `melody_rnn` object generates a melody sequence based on the provided parameters and returns the generated NoteSequence.

**Examples**:

```python
    >>> music_generator = MagentaMusic(temperature=1.2, num_steps=256)
    >>> melody_sequence = music_generator.generate_melody()
    >>> print(melody_sequence)
    NoteSequence(...) # Output will depend on the model and parameters
```

### `add_chords()`

```python
    def add_chords(self, melody_sequence):
        """ 
        Добавляет аккорды к мелодии.

        Args:
            melody_sequence (mm.NoteSequence): Мелодия, к которой нужно добавить аккорды.

        Returns:
            mm.NoteSequence: Мелодия с добавленными аккордами.
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

**Purpose**: Adds chords to the generated melody sequence based on a predefined chord progression.

**Parameters**:

- `melody_sequence` (`mm.NoteSequence`): The melody sequence to which chords should be added.

**Returns**:

- `mm.NoteSequence`: The melody sequence with added chords.

**How the Function Works**:

1.  Creates a list of chords (`chords`) based on a repeating pattern.
2.  Creates a `ChordSequence` object (`chord_sequence`) from the list of chords.
3.  Uses the `concatenate_sequences` function from `magenta.sequences_lib` to combine the `melody_sequence` and the `chord_sequence` into a new NoteSequence.
4.  Returns the resulting NoteSequence with added chords.

**Examples**:

```python
    >>> music_generator = MagentaMusic()
    >>> melody_sequence = music_generator.generate_melody()
    >>> melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
    >>> print(melody_with_chords_sequence)
    NoteSequence(...) # Output will depend on the generated melody
```

### `add_drums()`

```python
    def add_drums(self, melody_with_chords_sequence):
        """ 
        Добавляет барабаны к мелодии.

        Args:
            melody_with_chords_sequence (mm.NoteSequence): Мелодия с аккордами, к которой нужно добавить барабаны.

        Returns:
            mm.NoteSequence: Мелодия с аккордами и барабанами.
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

**Purpose**: Adds a drum pattern to the melody and chord sequence.

**Parameters**:

- `melody_with_chords_sequence` (`mm.NoteSequence`): The melody and chord sequence to which drums should be added.

**Returns**:

- `mm.NoteSequence`: The melody and chord sequence with added drums.

**How the Function Works**:

1.  Creates a `DrumTrack` object (`drum_pattern`) with a predefined drum pattern.
2.  Uses the `concatenate_sequences` function from `magenta.sequences_lib` to combine the `melody_with_chords_sequence` and the `drum_pattern` into a new NoteSequence.
3.  Returns the resulting NoteSequence with added drums.

**Examples**:

```python
    >>> music_generator = MagentaMusic()
    >>> melody_sequence = music_generator.generate_melody()
    >>> melody_with_chords_sequence = music_generator.add_chords(melody_sequence)
    >>> music_sequence = music_generator.add_drums(melody_with_chords_sequence)
    >>> print(music_sequence)
    NoteSequence(...) # Output will depend on the generated melody and chords
```

### `set_tempo()`

```python
    def set_tempo(self, music_sequence):
        """ 
        Устанавливает темп.

        Args:
            music_sequence (mm.NoteSequence): Музыкальная последовательность, к которой нужно применить темп.

        Returns:
            mm.NoteSequence: Музыкальная последовательность с заданным темпом.
        """
        music_sequence.tempos[0].qpm = self.tempo
        return music_sequence
```

**Purpose**: Sets the tempo of the music sequence.

**Parameters**:

- `music_sequence` (`mm.NoteSequence`): The music sequence to which the tempo should be applied.

**Returns**:

- `mm.NoteSequence`: The music sequence with the specified tempo.

**How the Function Works**:

1.  Modifies the first tempo event (`music_sequence.tempos[0]`) in the music sequence by setting its `qpm` (quarters per minute) value to the `self.tempo` attribute.
2.  Returns the modified music sequence.

**Examples**:

```python
    >>> music_generator = MagentaMusic(tempo=120)
    >>> music_sequence = music_generator.generate_full_music()
    >>> print(music_sequence.tempos[0].qpm)
    120.0 # Output will be the tempo set during initialization
```

### `save_midi()`

```python
    def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
        """ 
        Сохраняет готовую композицию в MIDI-файл.

        Args:
            music_sequence (mm.NoteSequence): Музыкальная последовательность для сохранения.
            filename (str, optional): Имя файла для сохранения. Defaults to 'full_music_advanced.mid'.
        """
        midi_file = os.path.join(self.output_dir, filename)
        mm.sequence_proto_to_midi_file(music_sequence, midi_file)
        print(f"Полная композиция сгенерирована и сохранена в: {midi_file}")
```

**Purpose**: Saves the finalized music sequence as a MIDI file in the specified output directory.

**Parameters**:

- `music_sequence` (`mm.NoteSequence`): The music sequence to save.
- `filename` (str, optional): The name of the MIDI file to save. Defaults to 'full_music_advanced.mid'.

**Returns**:

- None

**How the Function Works**:

1.  Creates the full path to the MIDI file (`midi_file`) by combining the output directory (`self.output_dir`) and the filename.
2.  Uses the `sequence_proto_to_midi_file` function from `magenta.music` to save the `music_sequence` to the specified MIDI file.
3.  Prints a confirmation message indicating that the music has been generated and saved.

**Examples**:

```python
    >>> music_generator = MagentaMusic(output_dir='my_music')
    >>> music_sequence = music_generator.generate_full_music()
    >>> music_generator.save_midi(music_sequence, filename='my_music.mid')
```

### `generate_full_music()`

```python
    def generate_full_music(self):
        """ 
        Объединяет все шаги в один вызов для удобства.
        """
        melody_sequence = self.generate_melody()
        melody_with_chords_sequence = self.add_chords(melody_sequence)
        music_sequence = self.add_drums(melody_with_chords_sequence)
        music_sequence = self.set_tempo(music_sequence)
        self.save_midi(music_sequence)
```

**Purpose**: This method combines all steps of the music generation process (melody generation, adding chords, drums, setting tempo, and saving) into a single method call for convenience.

**Parameters**:

- None

**Returns**:

- None

**How the Function Works**:

1.  Generates a melody using the `generate_melody()` method.
2.  Adds chords to the melody using the `add_chords()` method.
3.  Adds drums to the melody and chord sequence using the `add_drums()` method.
4.  Sets the tempo of the music sequence using the `set_tempo()` method.
5.  Saves the finalized music sequence to a MIDI file using the `save_midi()` method.

**Examples**:

```python
    >>> music_generator = MagentaMusic(output_dir='my_music')
    >>> music_generator.generate_full_music()
```

## Example Usage

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

This example demonstrates how to create instances of the `MagentaMusic` class with different parameters and generate music using the `generate_full_music()` method. The generated MIDI files will be saved in the specified output directories.