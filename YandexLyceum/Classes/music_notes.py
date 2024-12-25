N = 7
PITCHES = ["до", "ре", "ми", "фа", "соль", "ля", "си"]
LONG_PITCHES = ["до-о", "ре-э", "ми-и", "фа-а", "со-оль", "ля-а", "си-и"]
INTERVALS = ["прима", "секунда", "терция", "кварта", "квинта", "секста", "септима"]


class Note:
    def __init__(self, note, is_long=False):
        self.note = note
        self.index = PITCHES.index(note)
        self.is_long = is_long

    def __str__(self):
        if self.is_long:
            return {'до': 'до-о', 'ре': 'ре-э', 'ми': 'ми-и', 'фа': 'фа-а',
                    'соль': 'со-оль', 'ля': 'ля-а', 'си': 'си-и'}[self.note]
        else:
            return self.note

    def get_index(self):
        return PITCHES.index(self.note)

    def __eq__(self, other):
        if self.index == other.finder:
            return True
        return False

    def __ne__(self, other):
        if self.index != other.finder:
            return True
        return False

    def __lt__(self, other):
        if self.index < other.finder:
            return True
        return False

    def __le__(self, other):
        if self.index <= other.finder:
            return True
        return False

    def __gt__(self, other):
        if self.index > other.finder:
            return True
        return False

    def __ge__(self, other):
        if self.index >= other.finder:
            return True
        return False

    def __lshift__(self, other):
        return Note(PITCHES[(self.index - other) % N], self.is_long)

    def __rshift__(self, other):
        return Note(PITCHES[(self.index + other) % N], self.is_long)

    def get_interval(self, other):
        return INTERVALS[abs(self.index - other.finder)]


class Melody:
    def __init__(self, PITCHES=None):
        if PITCHES is None:
            PITCHES = []
        self.PITCHES = PITCHES

    def __str__(self):
        return ', '.join([str(i) for i in self.PITCHES]).capitalize()

    def append(self, note):
        self.PITCHES.append(note)

    def replace_last(self, note):
        if len(self.PITCHES) > 0:
            self.PITCHES = self.PITCHES[:-1] + [note]
            return None
        self.PITCHES = [note]

    def remove_last(self):
        if len(self.PITCHES) > 0:
            self.PITCHES = self.PITCHES[:-1]

    def clear(self):
        self.PITCHES.clear()

    def __len__(self):
        return len(self.PITCHES)

    def __rshift__(self, other):
        output = []
        for note_i in self.PITCHES:
            if note_i.get_index() + other > 6:
                return Melody(self.PITCHES)
        for i in self.PITCHES:
            output.append(i >> other)
        return Melody(output)

    def __lshift__(self, other):
        output = []
        for note_i in self.PITCHES:
            if note_i.get_index() - other < 0:
                return Melody(self.PITCHES)
        for i in self.PITCHES:
            output.append(i << other)
        return Melody(output)


class LoudNote(Note):
    def __init__(self, note, is_long=False):
        super().__init__(note, is_long=is_long)

    def __str__(self):
        return super().__str__().upper()


class DefaultNote(Note):
    def __init__(self, note='до', is_long=False):
        super().__init__(note, is_long=is_long)


class NoteWithOctave(Note):
    def __init__(self, note, octave, is_long=False):
        self.octave = octave
        super().__init__(note, is_long=is_long)

    def __str__(self):
        return f'{super().__str__()} ({self.octave})'
