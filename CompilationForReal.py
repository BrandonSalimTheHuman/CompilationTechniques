# Imports
import math
from mido import MidiFile, MidiTrack, Message

# Grammar
grammar = {
    '0a': [0, 0, 0, 0, 0],
    '0b': [1, 0, 0, 0, 0],
    '1b': [0, 1, 0, 0, 0],
    '2b': [0, 0, 1, 0, 0],
    '3b': [0, 0, 0, 1, 0],
    '4b': [0, 0, 0, 0, 1],
    '0c': [1, 1, 0, 0, 0],
    '1c': [1, 0, 1, 0, 0],
    '2c': [1, 0, 0, 1, 0],
    '3c': [1, 0, 0, 0, 1],
    '4c': [0, 1, 1, 0, 0],
    '5c': [0, 1, 0, 1, 0],
    '6c': [0, 1, 0, 0, 1],
    '7c': [0, 0, 1, 1, 0],
    '8c': [0, 0, 1, 0, 1],
    '9c': [0, 0, 0, 1, 1],
    '0d': [1, 1, 1, 0, 0],
    '1d': [1, 1, 0, 1, 0],
    '2d': [1, 1, 0, 0, 1],
    '3d': [1, 0, 1, 1, 0],
    '4d': [1, 0, 1, 0, 1],
    '5d': [1, 0, 0, 1, 1],
    '6d': [0, 1, 1, 1, 0],
    '7d': [0, 1, 1, 0, 1],
    '8d': [0, 1, 0, 1, 1],
    '9d': [0, 0, 1, 1, 1],
    '0e': [1, 1, 1, 1, 0],
    '1e': [1, 1, 1, 0, 1],
    '2e': [1, 1, 0, 1, 1],
    '3e': [1, 0, 1, 1, 1],
    '4e': [0, 1, 1, 1, 1],
    '0f': [1, 1, 1, 1, 1],
    '0o': 'end',
}


# Main function
def text_to_midi2(text):
    # Index
    i = 0
    # Array to store all rows in the current 5 columns
    current_section = []
    # Counter to store the number of empty columns
    total_skips = 0
    # Array for all tokens
    all_tokens = []

    # If the number of character isn't even, there's no way it's correct
    if len(text) % 2 != 0:
        print("Input must have an even number of characters")
        return

    # Separate the input into tokens
    while i < len(text):
        # Current token
        token = text[i:i+2]
        # If token is valid
        if token in grammar or token == '0o':
            # Append it to the array
            all_tokens.append(token)
            print("Valid:", token)
        else:
            # Else, terminate
            print("invalid token:", token)
            return
        # Increment i by 2
        i += 2

    # Create a new MIDI file and track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Loop through each token
    for token in all_tokens:
        # Get the token
        pattern = grammar.get(token)
        # Part below is for drawing a finished section to the midi
        if pattern == 'end':
            # To center the drawing, start at 60 (C4) and go up half the height of the section
            starting_pitch = math.ceil(60 + len(current_section) / 2)
            # Flip the arrays from x arrays of length y to y arrays of length x (rows to columns)
            flipped_section = [list(row) for row in zip(*current_section)]
            # Debugging
            print(current_section)
            print(flipped_section)
            # For each column in the flipped array
            for column in flipped_section:
                # Start at the top of the drawing
                current_pitch = starting_pitch
                # Switch 1 is for the first note on
                switch1 = True
                # Switch 2 is for the first note off
                switch2 = True
                # Switch to detect a completely empty column
                empty_switch = True
                # For each note in the column
                for note in column:
                    # If note is 1
                    if note == 1:
                        # The column is definitely not empty
                        if empty_switch:
                            empty_switch = False
                        # If first note on
                        if switch1:
                            # Draw the note 100 * total_skips from the last note
                            track.append(Message('note_on', note=current_pitch, velocity=64, time=(total_skips * 100)))
                            # Reset total_skips
                            total_skips = 0
                            # Make switch 1 false
                            switch1 = False
                        # Otherwise, append it with time 0
                        else:
                            track.append(Message('note_on', note=current_pitch, velocity=64, time=0))
                    # Go down one pitch to the next note
                    current_pitch -= 1
                current_pitch = starting_pitch
                # Pretty much the same thing, except for stopping the notes
                # Main difference is that the first note turned off is time = 100
                for note in column:
                    if note == 1:
                        if switch2:
                            track.append(Message('note_off', note=current_pitch, velocity=64, time=100))
                            switch2 = False
                        else:
                            track.append(Message('note_off', note=current_pitch, velocity=64, time=0))

                    current_pitch -= 1
                # If the entire column was empty, increment total_skips
                if empty_switch:
                    total_skips += 1
            # Reset current_section
            current_section = []
        else:
            # append pattern to current section
            current_section.append(pattern)

    # Save the generated MIDI file
    mid.save('result.mid')


text_to_midi2('4e1b8d5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c6c5c8c5c6c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c8d1b4e0o0f0a0f0a0f0b3e1c4d4d4d4d4d4d4d4d4d0a0f0b3e1c4d4d4d4d4d4d1c3e0b0e4b2c4d5c4d5c4d5c4d5c4d5c4d2c4b0e0b3e1c4d4d4d4d4d4d1c3e0b0f0a4d4d4d4d4d4d4d4d4d1c3e0b0f0a0f0a0f0o0f0a0f0a0f0a0f0a0f0a4e1b8d5c5c5c5c0a0f0a0f0a0e3b5c5c3b1e3b1e3b1e8c3e8d4d5c4d5c4d5c4d5c4d8d3e8c1e3b1e3b1e3b5c5c3b0e0a0f0a0f0a5c5c5c5c8d1b4e0a0f0a0f0a0f0a0f0a0f0o0f0a0f0a1e4b1e4b1e4b1e4b1e4b1e3c4d0a1e8c4d4d4d4d1c3e0f6c4d7d1e1e1e1e1e1e1e7d4d6c4d7d1e1e1e1e1e1e1e7d4d6c0f3e1c4d4d4d4d8c1e0a4d3c1e4b1e4b1e4b1e4b1e4b1e0a0f0a0f0o0f0a0f0a0f0a4e1b8d5c5c5c8d1b4e0a0f0a0f0f0e2d3e4e0e0f0f0d0c0c0b1c1b2b1b2b1b2b1b2b1b2b1b2b1b2b1b1c0b0c0c0d0f0f0e4e3e2d0e0f0f0a0f0a4e1b8d5c5c5c8d1b4e0a0f0a0f0a0f0o0f0a0f0a0f0a0f0a0f4b1e4b0e9c0e9d0e7c3e4e0f0e3d7c7c0f0f7c2b1d3d3d3d3d3d3d3d3d3d3e3d3d3d3d3d3d3d3d3d3d1d2b0e0f7c7c3d0e0f4e3e7c0e9d0e9c0e4b1e4b0f0a0f0a0f0a0f0a0f0o0f0a0f0a0e3b1d5c6c5c5c5c4d8d3e4e0f0a0f0c3b0a0a4e1b3e4e0a0a0a9d4c1b1b1b1b1b1b0b0a0b1b1b1b1b1b1b4c9d0a0a0a0f4e0b0f0a0a3b0c0f0a0f4e3e8d4d5c5c5c6c5c1d3b0e0a0f0a0f0o0f0a0e4b1d8c5c4d5c4d5c4d1d1e0e0f0f0a0f0a4d0a0a0f0a0f0f0a0a4b0e0a0a0f4d0f1c0d2d5d2d0d1c0f4d0f0a0a0e4b0a0a0f0f0a0f0a0a4d0a0f0a0f0f0e1e1d4d5c4d5c4d5c8c1d4b0e0a0f0o3e1b4d5c4d5c4d5c4d5c4d5c4d5c4d8d3e0a0f0a5c0a0a0f0a0f0f1b1c3b4b0a0a0f3d9c1b0d0e0f0e0d1b9c3d0f0a0a4b3b1c1b0f0f0a0f0a0a5c0a0f0a3e8d4d5c4d5c4d5c4d5c4d5c4d5c4d1b3e0o0f0a0f0a7d3c6c4d5c4d6c4d6d0f0f0f0f0a0f0a4d0a0a0f0a0f0f0a0a0a0f0a0a0d1c0d1c0d4c2b4c0d1c0d1c0d0a0a0f0a0a0a0f0f0a0f0a0a4d0a0f0a0f0f0f0f6d4d6c4d5c4d6c3c7d0a0f0a0f0o0f0a0f0a0f0a4e1b8d5c5c5c4d8d4d2e1e4b0f4e9c4b4b1e8c2e1e0a4b4b3c2d6c6c6c6c6c6c8c9c8c6c6c6c6c6c6c2d3c4b4b0a1e2e8c1e4b4b9c4e0f4b1e2e4d8d4d5c5c5c8d1b4e0a0f0a0f0a0f0o0f0a0f0a0f0a0f0a0f4b1e4b0f0a0f0b0f0b3e2e1e0e3e5d3c0f0f0b4c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c1c4c0b0f0f3c5d3e0e1e2e3e0b0f0b0f0a0f4b1e4b0f0a0f0a0f0a0f0a0f0o0f0a0f0a0e3b1d5c5c5c5c5c5c5c1d3b0e0a0e0e0e6d3d1d0d0f0f0e6d6d7c3d5c2c5c2c5c2c5c2c5c2c5c2c5c2c5c3d7c6d6d0e0f0f0d1d3d6d0e0e0e0a0e3b1d5c5c5c5c5c5c5c1d3b0e0a0f0a0f0o0f0a0f0a0f0a0f0a0f0a0f0a0f4b1e8c4d0a0f0b3e1c4d4d4d4d1e5c4d1d1e0e0f0f0f0e1e1d4d5c4d1d1e0e0f0f0f0e1e1d4d5c1e4d4d4d4d1c3e0b0f0a4d8c1e4b0f0a0f0a0f0a0f0a0f0a0f0a0f0o0f0a0f0a0f0a0f0a0e3b1d5c5c5c5c5c5c0a0f0a0f0a0e3b5c5c3b0e0a0f0a1e3b4d5c4d5c4d5c4d5c4d5c4d5c4d3b1e0a0f0a0e3b5c5c3b0e0a0f0a0f0a5c5c5c5c5c5c1d3b0e0a0f0a0f0a0f0a0f0o0f0a0f4b1e8c4d4d4d4d4d4d4d4d4d4d4d4b1e8c4d4d4d4d4d4d4d4d4d4d8c1e4b8c4d6c4d5c4d5c4d5c4d6c4d8c4b1e8c4d4d4d4d4d4d4d4d4d4d8c1e4b4d4d4d4d4d4d4d4d4d4d4d8c1e4b0f0a0f0o0c1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b0b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b0c')
