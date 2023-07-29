import math

import mido

# Load the MIDI file
midi_file = mido.MidiFile('input/ヴァンパイア.mid')  # your midi file path

STANDARD_TIME = midi_file.ticks_per_beat    # quarter=480
STANDARD_NOTE = 64  # C3=60
section_time = 0
pitch_info = ['1', '1#', '2', '2#', '3', '4', '4#', '5', '5#', '6', '6#', '7']  # pitch marker


# mark octave
def print_oct_mark(_oc):
    if _oc > 0:
        return "↑"*abs(_oc)
    elif _oc < 0:
        return "↓"*abs(_oc)
    else:
        return ""


# mark note lenghth
def print_time_mark(_ti):
    _ti = math.floor(_ti*4)/4
    out_str = ""
    have_16 = (_ti / 0.25) % 2 == 1
    if have_16:
        out_str = "'" + out_str
        _ti -= 0.25
    have_8 = (_ti / 0.5) % 2 == 1
    if have_8:
        out_str = "." + out_str
        _ti -= 0.5
    out_str = ":" * int(_ti) + out_str
    if out_str == ".":  # 1/8 omits length mark
        out_str = ""
    return out_str


def print_notes(_file, _no_list):
    section_num = 0
    for note in _no_list:
        if len(note) > 2:
            _file.write(f'{print_time_mark(note[1])}{note[0]}{print_oct_mark(note[2])}')    # note
        elif len(note) == 2:
            _file.write(f'{print_time_mark(note[1])}{note[0]}')     # rest
        else:
            _file.write(note[0])    # section divider
            section_num = section_num + 1
            if section_num % 4 == 0:
                _file.write('\n\r')
                continue
        _file.write(' ')


file = open('output/output1.txt', 'w')
# Iterate over all the tracks in the MIDI file
for track in midi_file.tracks:
    # Iterate over all the messages in the track
    note_list = []
    note_list_org = []
    for msg in track:
        if msg.is_meta:
            pass
        else:
            note_output = pitch_info[(msg.note - STANDARD_NOTE) % 12]
            note_oct = math.floor((msg.note - STANDARD_NOTE) / 12)
            if msg.note < STANDARD_NOTE:
                note_oct = math.floor((msg.note - STANDARD_NOTE) / 12)
            time_output = msg.time / STANDARD_TIME
            # Check if the message is a note-on or note-off event
            if msg.type == 'note_on' and msg.time > 0:
                note_list.append(('0', time_output))   # rest
            if msg.type == 'note_off':
                note_list.append((note_output, time_output, note_oct))    # note
                note_list_org.append(msg.note)
            section_time += time_output
            if section_time >= 4:
                note_list.append('|')     # section divider
                section_time -= 4

print_notes(file, note_list)
file.close()
