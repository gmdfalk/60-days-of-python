import datetime

last_id = 0

class Note(object):

    def __init__(self, memo="", tags=""):
        """Initialize a note with memo and optional
        space-separated tags. Automatically set the note's
        creation date and a unique id."""
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global last_id
        last_id += 1
        self.id = last_id

    def match(self, pattern):
        """Determine if this note matches the pattern text.
        Return True if it matches, False otherwise.
        Search is case sensitive and matches both text and
        tags."""
        return pattern in self.memo or pattern in self.tags


class Notebook(object):
    """Represent a collection of notes that can be tagged, modified
    and searched."""

    def __init__(self):
        "Initializes a notebook with an empty list."
        self.notes = []

    def _find_note(self, note_id):
        "Locate the note with the given id."
        for note in self.notes:
            if note.id == note_id:
                return note

    def new_note(self, memo, tags=""):
        "Create a new note and add it to the list."
        self.notes.append(Note(memo, tags))

    def modify_memo(self, note_id, memo):
        "Find the note with the given id and change its memo to the given value"
        self._find_note(note_id).memo = memo

    def modify_tags(self, note_id, tags):
        "Find the note with the given id and change its tags to the given value"
        for note in self.notes:
            if note.id == note_id:
                note.tags = tags
                break

    def search(self, pattern):
        "Find all notes that match the given pattern string."
        return [note for note in self.notes if note.match(pattern)]
