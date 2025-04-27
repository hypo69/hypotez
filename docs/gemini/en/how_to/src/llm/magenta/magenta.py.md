**Instructions for Generating Code Documentation**

1. **Analyze the Code**: Understand the logic and actions performed by the code snippet.

2. **Create a Step-by-Step Guide**:
    - **Description**: Explain what the code block does.
    - **Execution Steps**: Describe the sequence of actions in the code.
    - **Usage Example**: Provide a code example of how to use the snippet in the project.

3. **Example**:

How to Use the `MagentaMusic` Class
=========================================================================================

Description
-------------------------
The `MagentaMusic` class provides a framework for generating MIDI music using the Magenta library. It allows you to create melodies, add chords and drums, and set the tempo for your composition.

Execution Steps
-------------------------
1. **Initialize the `MagentaMusic` class:**
    - Pass the desired output directory, model name, temperature, number of steps, primer MIDI file (optional), and tempo as arguments to the constructor.
    - The constructor loads the chosen Magenta model, initializes the primer sequence (if provided), and sets up the necessary variables.

2. **Generate a melody:**
    - Call the `generate_melody()` method. This method uses the chosen Magenta model to generate a melody based on the specified parameters.

3. **Add chords:**
    - Call the `add_chords()` method, passing the generated melody as an argument. This method adds a simple chord progression to the melody.

4. **Add drums:**
    - Call the `add_drums()` method, passing the melody with chords as an argument. This method adds a drum track to the composition.

5. **Set tempo:**
    - Call the `set_tempo()` method, passing the music sequence as an argument. This method sets the tempo for the composition.

6. **Save the MIDI file:**
    - Call the `save_midi()` method, passing the music sequence and a filename as arguments. This method saves the final composition as a MIDI file.

7. **Use the `generate_full_music()` method:**
    - This method combines all the steps above into a single call, allowing you to generate a complete music composition with a single line of code.

Usage Example
-------------------------

```python
    # Create an instance of the MagentaMusic class with desired settings
    music_generator = MagentaMusic(output_dir='my_music', model_name='attention_rnn',
                                    temperature=1.1, num_steps=200, primer_midi_file='primer.mid', tempo=110)

    # Generate the complete music composition
    music_generator.generate_full_music()
```

4. **Avoid Vague Terms** like "getting" or "doing". Be specific about what the code does, for example: "checks", "validates", or "sends".