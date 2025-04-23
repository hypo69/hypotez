### Как использовать класс `MagentaMusic`
=========================================================================================

Описание
-------------------------
Класс `MagentaMusic` предназначен для генерации музыкальных композиций с использованием моделей Magenta. Он предоставляет методы для загрузки затравки из MIDI-файла, генерации мелодии, добавления аккордов и барабанов, установки темпа и сохранения результата в MIDI-файл.

Шаги выполнения
-------------------------
1. **Инициализация класса**: Создается экземпляр класса `MagentaMusic` с указанием параметров, таких как директория для сохранения результатов, имя модели, температура, количество шагов, файл затравки и темп.
2. **Загрузка затравки**: Метод `_load_primer_sequence` загружает MIDI-файл затравки или создает пустую `NoteSequence`, если файл не найден.
3. **Генерация мелодии**: Метод `generate_melody` генерирует мелодию на основе затравки и параметров модели.
4. **Добавление аккордов**: Метод `add_chords` добавляет аккорды к мелодии.
5. **Добавление барабанов**: Метод `add_drums` добавляет партию ударных к мелодии с аккордами.
6. **Установка темпа**: Метод `set_tempo` устанавливает темп для музыкальной последовательности.
7. **Сохранение в MIDI-файл**: Метод `save_midi` сохраняет готовую композицию в MIDI-файл.
8. **Генерация полной композиции**: Метод `generate_full_music` объединяет все шаги в один вызов для удобства.

Пример использования
-------------------------

```python
import os
import magenta.music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator
import tensorflow as tf  # Import TensorFlow


class MagentaMusic:
    def __init__(self, output_dir='generated_music_advanced', model_name='attention_rnn', temperature=1.2,
                 num_steps=256, primer_midi_file='primer.mid', tempo=100):
        """
        Инициализирует экземпляр класса MagentaMusic с заданными параметрами.

        Args:
            output_dir (str): Директория для сохранения сгенерированной музыки.
            model_name (str): Имя используемой модели melody_rnn.
            temperature (float): Параметр temperature для генерации.
            num_steps (int): Количество шагов для генерации мелодии.
            primer_midi_file (str): Путь к MIDI-файлу затравки.
            tempo (int): Темп композиции в ударах в минуту.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.model_name = model_name
        self.temperature = temperature
        self.num_steps = num_steps
        self.primer_midi_file = primer_midi_file
        self.tempo = tempo
        self.melody_rnn = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
            model_name=self.model_name
        )
        self.primer_sequence = self._load_primer_sequence()

    def _load_primer_sequence(self):
        """
        Загружает MIDI-файл затравки или создает пустую NoteSequence, если файл не найден.

        Returns:
            mm.NoteSequence: Загруженная или пустая NoteSequence.
        """
        if os.path.exists(self.primer_midi_file):
            primer_sequence = mm.midi_file_to_sequence_proto(self.primer_midi_file)
            print(f"Используем primer из {self.primer_midi_file}")
            return primer_sequence
        else:
            print("Не найдена primer, начинаем с пустой мелодии")
            return mm.NoteSequence(notes=[])


    def generate_melody(self):
        """
        Генерирует мелодию на основе затравки и параметров модели.

        Returns:
            mm.NoteSequence: Сгенерированная мелодия.
        """
        melody_sequence = self.melody_rnn.generate(
            temperature=self.temperature,
            steps=self.num_steps,
            primer_sequence=self.primer_sequence
        )
        return melody_sequence

    def add_chords(self, melody_sequence):
        """
        Добавляет аккорды к мелодии.

        Args:
            melody_sequence (mm.NoteSequence): Мелодия для добавления аккордов.

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

    def add_drums(self, melody_with_chords_sequence):
        """
        Добавляет партию ударных к мелодии с аккордами.

        Args:
            melody_with_chords_sequence (mm.NoteSequence): Мелодия с аккордами для добавления ударных.

        Returns:
            mm.NoteSequence: Мелодия с аккордами и ударными.
        """
        drum_pattern = mm.DrumTrack(
            [36, 0, 42, 0, 38, 0, 46, 0, 36, 0, 42, 0, 38, 0, 45, 0],
            start_step=0,
            steps_per_bar=self.num_steps // 8,
            steps_per_quarter=8,
        )
        music_sequence = mm.sequences_lib.concatenate_sequences(melody_with_chords_sequence, drum_pattern)
        return music_sequence


    def set_tempo(self, music_sequence):
        """
        Устанавливает темп для музыкальной последовательности.

        Args:
            music_sequence (mm.NoteSequence): Музыкальная последовательность для установки темпа.

        Returns:
            mm.NoteSequence: Музыкальная последовательность с установленным темпом.
        """
        music_sequence.tempos[0].qpm = self.tempo
        return music_sequence

    def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
        """
        Сохраняет готовую композицию в MIDI-файл.

        Args:
            music_sequence (mm.NoteSequence): Музыкальная последовательность для сохранения.
            filename (str): Имя файла для сохранения.
        """
        midi_file = os.path.join(self.output_dir, filename)
        mm.sequence_proto_to_midi_file(music_sequence, midi_file)
        print(f"Полная композиция сгенерирована и сохранена в: {midi_file}")

    def generate_full_music(self):
        """
        Генерирует полную музыкальную композицию, объединяя все шаги.
        """
        melody_sequence = self.generate_melody()
        melody_with_chords_sequence = self.add_chords(melody_sequence)
        music_sequence = self.add_drums(melody_with_chords_sequence)
        music_sequence = self.set_tempo(music_sequence)
        self.save_midi(music_sequence)


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
В этом примере создаются два экземпляра класса `MagentaMusic` с разными параметрами и генерируются две музыкальные композиции, которые сохраняются в разные директории.