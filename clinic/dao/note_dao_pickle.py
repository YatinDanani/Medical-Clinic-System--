import datetime
import pickle
from clinic.dao.note_dao import NoteDAO
from clinic.note import Note
import os

class NoteDAOPickle(NoteDAO):
    """
    Manages the application's core operations, including user authentication,
    patient data handling, and note management.
    """

    def __init__(self, phn: str, autosave: bool):
        """
        Initializes a NoteDAOPickle instance for a specific patient.

        Parameters:
        - phn (str): The patient's personal health number.
        - autosave (bool): Whether to enable automatic saving of notes.
        """
        self.notes = []
        self.autocounter = 1  # ALWAYS initialize autocounter

        self.autosave = autosave
        self.phn = phn

        # Set file path for storing notes
        self.filepath = f'clinic/records/{self.phn}.dat'

        if self.autosave:
            # Automatically load notes if autosave is enabled
            self.load_notes()

    def load_notes(self):
        """
        Loads notes from the pickle file corresponding to the patient's PHN.
        
        If the file does not exist, initializes an empty notes list and resets the counter.
        Updates the autocounter based on the highest existing note ID.
        """
        try:
            with open(self.filepath, 'rb') as f:
                data = pickle.load(f)
                self.notes = data.get('notes',[])
                # Set the autocounter to the next available ID
                if self.notes:
                    self.autocounter = max(note.code for note in self.notes)+1 if self.notes else 1
        except FileNotFoundError:
            # Initialize an empty notes list if no file exists
            self.notes = []
            self.autocounter = 1

    def save_notes(self):
        """
        Saves all notes to a file using pickle.
        
        This method writes the current list of notes to a file identified by the PHN.
        It is only executed if autosave is enabled.
        """
        if not os.path.exists("clinic/records"):
            # Create the directory
            os.makedirs("clinic/records")

        if self.autosave:
            with open(self.filepath, 'wb') as f:
                data = {'notes': self.notes}
                pickle.dump(data, f)

    def search_note(self, key: int) -> None:
        """
        Searches for a note by its unique code.
        
        Parameters:
        - key (int): The unique ID of the note to search for.
        
        Return Type:
        - Note: Returns the `Note` object if found, otherwise None.
        """
        for note in self.notes:
            if note.code == key:
                return note
        return None
   
    def create_note(self, text: str) -> Note:
        """
        Creates a new note with the given text.
        
        Parameters:
        - text (str): The content of the new note.
        
        Return Type:
        - Note: The newly created `Note` object.
        """
        new_note = Note(self.autocounter, text,datetime.datetime.now()) # Create a new note with the next available ID and current timestamp
        self.notes.append(new_note)
        self.autocounter += 1

        if self.autosave:
            self.save_notes()
        return new_note
    
    def retrieve_notes(self, search_string: str) -> list[Note]:
        """
        Retrieves all notes containing a specific search string.
        
        Parameters:
        - search_string (str): The text to search for within notes.
        
        Return Type:
        - list: A list of `Note` objects that match the search string.
        """
        # Filter notes that contain the search string (case-insensitive)
        retrieve_notes = [note for note in self.notes if search_string.lower() in note.text.lower()]
        return retrieve_notes
    
    def update_note(self, key: int, text: str) -> bool:
        """
        Updates the content of an existing note by its unique code.
        
        Parameters:
        - key (int): The unique ID of the note to update.
        - text (str): The new content for the note.
        
        Return Type:
        - bool: True if the update is successful, False if no note is found.
        """
        for note in self.notes:
            if note.code == key:
                # Update the note's details
                note.update_details(text)
                if self.autosave:
                    self.save_notes()

        if not self.notes:
            return False
        return True
        
    def delete_note(self, key: int) -> bool:
        """
        Deletes a note by its unique code.
        
        Parameters:
        - key (int): The unique ID of the note to delete.
        
        Return Type:
        - bool: True if the note is successfully deleted, False otherwise.
        """
        note_to_delete = self.search_note(key)
        if note_to_delete:
            # Remove the note from the list
            self.notes.remove(note_to_delete)

            if self.autosave:
                self.save_notes()
            return True
        return False

    
    def list_notes(self) -> list[Note]:
        """
        Lists all notes in reverse order (latest first).
        
        Return Type:
        - list: A list of `Note` objects in reverse chronological order.
        """
        return list(reversed(self.notes))