# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. Module :: src.ai.gemini
   : Platform: Windows, Unix
   : Synopsis: Google Generate Ai Integration
   https://aistudio.google.com/prumpts/1wm7hzx5Repkplbkub0vlulu3xuvnsp9
   https://github.com/magenta/magenta/issues/1962
   https://colabe


Magentamusic class:

- All settings are made to the __init__ designer, which allows you to easily create specimens of class with different parameters.

- The _load_primer_sequence method loads the MIDI-file of the seed or creates an empty notesQUENCE if the file is not found.
- The Generate_melody method generates a melody with specified parameters.
- The Add_chords method adds chords to the melody.
- The Add_drums method adds drums to the melody.
- Set_TEMPO sets the pace.
- The Save_Midi method retains the finished composition on the midi file.
- The Generate_Full_Music method combines all steps into one call for convenience.

Example of use (IF __name__ == '__main__' :):

How to use:

Create MIDI files Primer.mid and Primer2.mid, or leave them empty if you do not want to use the seed.
Launch the script: Python Magenta_music_class.py.
The generated compositions will be saved in the My_Music and My_Music2 folders."""

import os
import magenta.music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator
import tensorflow as tf  # Import TensorFlow


class MagentaMusic:
    def __init__(self, output_dir='generated_music_advanced', model_name='attention_rnn', temperature=1.2,
                 num_steps=256, primer_midi_file='primer.mid', tempo=100):
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
        if os.path.exists(self.primer_midi_file):
            primer_sequence = mm.midi_file_to_sequence_proto(self.primer_midi_file)
            print(f"Используется primer из {self.primer_midi_file}")
            return primer_sequence
        else:
            print("Не найдена primer, начинаем с пустой мелодии")
            return mm.NoteSequence(notes=[])


    def generate_melody(self):
        melody_sequence = self.melody_rnn.generate(
            temperature=self.temperature,
            steps=self.num_steps,
            primer_sequence=self.primer_sequence
        )
        return melody_sequence

    def add_chords(self, melody_sequence):
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
        drum_pattern = mm.DrumTrack(
            [36, 0, 42, 0, 38, 0, 46, 0, 36, 0, 42, 0, 38, 0, 45, 0],
            start_step=0,
            steps_per_bar=self.num_steps // 8,
            steps_per_quarter=8,
        )
        music_sequence = mm.sequences_lib.concatenate_sequences(melody_with_chords_sequence, drum_pattern)
        return music_sequence


    def set_tempo(self, music_sequence):
        music_sequence.tempos[0].qpm = self.tempo
        return music_sequence

    def save_midi(self, music_sequence, filename='full_music_advanced.mid'):
         midi_file = os.path.join(self.output_dir, filename)
         mm.sequence_proto_to_midi_file(music_sequence, midi_file)
         print(f"Полная композиция сгенерирована и сохранена в: {midi_file}")

    def generate_full_music(self):
        melody_sequence = self.generate_melody()
        melody_with_chords_sequence = self.add_chords(melody_sequence)
        music_sequence = self.add_drums(melody_with_chords_sequence)
        music_sequence = self.set_tempo(music_sequence)
        self.save_midi(music_sequence)


if __name__ == '__main__':
    # An example of using a class
    music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                    temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)
    music_generator.generate_full_music()

    # Another example with other parameters
    music_generator2 = MagentaMusic(output_dir='my_music2', model_name='basic_rnn',
                                    temperature=0.9, num_steps=150, primer_midi_file='primer2.mid', tempo=120)
    music_generator2.generate_full_music()