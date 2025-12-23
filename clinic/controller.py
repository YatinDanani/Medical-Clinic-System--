import hashlib
import json
from datetime import datetime
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note
from clinic.exception import (
    DuplicateLoginException, IllegalAccessException, IllegalOperationException,
    InvalidLoginException, InvalidLogoutException, NoCurrentPatientException
)
from clinic.dao import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle

# NEW: Import ML classifier
from clinic.ml.note_classifier import NoteClassifier




class Controller:
    """
    A class for managing patient data and user authentication.
    Handles login, logout, patient management, and note management within a session.
    """

    def __init__(self, autosave=False):
        """
        Initializes the Controller instance with default settings.

        Parameters:
        - autosave (bool): Determines whether changes to patients are automatically saved.
        """
        self.current_patient = None
        self.username = None
        self.logged_in = False
        self.autosave = autosave
        self.patient_dao = PatientDAOJSON(autosave)
        self.users = {}

        # NEW: Initialize ML classifier
        self.note_classifier = NoteClassifier()
        self.note_classifier.load_model()  # Load pre-trained model
      
    def load_patients(self):
        """
        Loads patient credentials from a file into a dictionary.

        Reads the file `clinic/users.txt` and parses lines into a dictionary
        of usernames and hashed passwords.

        Return Type:
        - dict: A dictionary with usernames as keys and hashed passwords as values, 
          or an empty dictionary if the file is not found.
        """
        patients={}
        try:
            with open('clinic/users.txt', 'r') as file:
                for line in file:
                    # Load JSON data and split lines into username and password
                    data = json.load(file)
                    names = line.strip().split(',')
                    patients[names[0]] = names[1]
        except FileNotFoundError:
            # Inform the user if the file is missing
            print("Users file not found.Please create 'users.txt' with user credentials.")
        return patients
        
    def login(self, username: str, password: str) -> bool:
        """
        Logs in a user by validating credentials against the stored data.

        Parameters:
        - username (str): The username provided for login.
        - password (str): The password provided for login.

        Return Type:
        - bool: Returns True if login is successful, False otherwise.
        """
        if self.logged_in:
            # Prevent multiple logins
            raise DuplicateLoginException
        try:
                with open('clinic/users.txt', 'r') as file:
                    for line in file:
                        # Parse credentials into the users dictionary
                        names = line.strip().split(',')
                        self.users[names[0]] = names[1]
        except FileNotFoundError:
            print("Users file not found.Please create 'users.txt' with user credentials.")
        
        # Validate username and password
        if username in self.users:
            password_hash = self.get_password_hash(password)
            if self.users[username] == str(password_hash):
                self.logged_in = True
                return True
            else:
                raise InvalidLoginException
        else:
            raise InvalidLoginException

    def get_password_hash(self, password: str) -> str:
        """
        Hashes a given password using SHA-256.

        Parameters:
        - password (str): The plain text password to hash.

        Return Type:
        - str: The hashed password as a hexadecimal string.
        """
        # Encode the password and generate its hash
        encoded_password = password.encode('utf-8')
        hash_obj = hashlib.sha256(encoded_password)
        hex_dig = hash_obj.hexdigest()
        return hex_dig
             
    def logout(self) -> bool:
        """
        Logs out the current user, resetting session variables.

        Parameters:
        - None

        Return Type:
        - bool: Returns True if logout is successful, False otherwise.
        """
        if self.logged_in:
            # Reset session variables
            self.logged_in = False
            self.username = None
            self.current_patient = None
            return True
        raise InvalidLogoutException

    def search_patient(self, phn: int) -> 'Patient':
        """
        Retrieves a patient by PHN if the user is logged in.

        Parameters:
        - phn (int): The unique Personal Health Number of the patient to search for.

        Return Type:
        - Patient: Returns the Patient instance if found, or None if not found or if not logged in.
        """
        if not self.logged_in:
            # Ensure the user is logged in before searching
            raise IllegalAccessException
        return self.patient_dao.search_patient(phn)
        

    def create_patient(self, phn: int, name: str, birth_date: str, phone: str, email: str, address: str) -> 'Patient':
        """
        Adds a new patient to the system if the user is logged in and the PHN is unique.

        Parameters:
        - phn (int): The unique Personal Health Number of the patient.
        - name (str): The patient's full name.
        - birth_date (str): The patient's birth date.
        - phone (str): The patient's phone number.
        - email (str): The patient's email address.
        - address (str): The patient's home address.

        Return Type:
        - Patient: Returns the newly created Patient instance.
        """
        if not self.logged_in:
            # Ensure the user is logged in before creating a patient
            raise IllegalAccessException
        if phn in self.patient_dao.patients:
            # Prevent creating a patient with a duplicate PHN
            raise IllegalOperationException
        
        # Create and add the new patient
        patient = Patient(phn,name,birth_date,phone,email,address,self.autosave)
        self.patient_dao.create_patient(patient)
        return patient

    def retrieve_patients(self, name: str) -> list:
        """
        Retrieves a list of patients whose names contain the search string (case-insensitive).

        Parameters:
        - name (str): The name to search for within patient records.

        Return Type:
        - list: A list of matching Patient instances, or an empty list if no matches are found.
        """
        if not self.logged_in:
            # Ensure the user is logged in before retrieving patients
            raise IllegalAccessException
        return self.patient_dao.retrieve_patients(name)

    def update_patient(self, old_phn: int, phn=None, name=None, birth_date=None, phone=None, email=None, address=None) -> bool:
        """
        Updates a patient's details. Moves the patient if PHN changes and is unique.

        Parameters:
        - old_phn (int): The PHN of the patient to update.
        - phn (Optional[int]): The new PHN, if changing.
        - name (Optional[str]): The new name, if updating.
        - birth_date (Optional[str]): The new birth date, if updating.
        - phone (Optional[str]): The new phone number, if updating.
        - email (Optional[str]): The new email address, if updating.
        - address (Optional[str]): The new address, if updating.

        Return Type:
        - bool: Returns True if the update is successful, False otherwise.
        """
        if not self.logged_in:
            # Ensure the user is logged in before updating a patient
            raise IllegalAccessException
        
        if old_phn not in self.patient_dao.patients:
            # Ensure the patient exists before updating
            raise IllegalOperationException
        
        patient = self.patient_dao.patients.get(old_phn)

         # Check for conflicts if a new PHN is specified
        if (self.current_patient and phn == self.current_patient.phn) or (phn and phn != old_phn and phn in self.patient_dao.patients):
            raise IllegalOperationException
        
        if phn:
            self.patient_dao.patients.pop(old_phn)
            self.patient_dao.patients[phn] = patient

        # Update patient details
        patient.phn = phn
        patient.name = name
        patient.birth_date = birth_date
        patient.phone = phone
        patient.email = email
        patient.address = address
        self.patient_dao.update_patient(patient.phn,patient)
        return True
        
    def delete_patient(self, phn: int) -> bool:
        """
        Deletes a patient by their PHN if the user is logged in and the patient exists.

        Parameters:
        - phn (int): The PHN of the patient to delete.

        Return Type:
        - bool: Returns True if the patient is successfully deleted, raises an exception otherwise.
        """
        if not self.logged_in:
            raise IllegalAccessException
         
        if phn not in self.patient_dao.patients:
            raise IllegalOperationException
        
        if self.current_patient and self.current_patient.phn == phn:
            raise IllegalOperationException

        # Perform the deletion through the DAO
        self.patient_dao.delete_patient(phn)
        return True
            
    def list_patients(self) -> list:
        """
        Lists all patients in the system if the user is logged in.

        Return Type:
        - list: A list of all Patient instances.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        return self.patient_dao.list_patients()

    def set_current_patient(self, phn: int) -> bool:
        """
        Sets the current patient in the session by their PHN.

        Parameters:
        - phn (int): The PHN of the patient to set as the current patient.

        Return Type:
        - bool: Returns True if the patient is successfully set, raises an exception otherwise.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        patient = self.patient_dao.patients.get(phn)

        if patient:
            self.current_patient = patient
            return True
        
        raise IllegalOperationException

    def get_current_patient(self) -> 'Patient':
        """
        Retrieves the currently selected patient.

        Return Type:
        - Patient: The currently selected Patient instance, raises an exception if none is set or if not logged in.
        """
        if not self.logged_in:
            raise IllegalAccessException
        return self.current_patient

    def unset_current_patient(self) -> bool:
        """
        Unsets the currently selected patient in the session.

        Return Type:
        - bool: Returns True if the current patient is successfully unset, raises an exception otherwise.
        """
        if not self.logged_in or self.current_patient is None:
            raise IllegalAccessException
        
        self.current_patient = None
        return True

    def create_note(self, text: str) -> 'Note':
        """
        Creates a new note for the current patient with ML classification.

        Parameters:
        - text (str): The content of the note to be created.

        Return Type:
        - Note: The newly created Note instance with ML predictions.
        """
        if not self.logged_in:
            raise IllegalAccessException

        if self.current_patient is None:
            raise NoCurrentPatientException

        # Create the note
        note = self.current_patient.create_note(text)

        # Add ML prediction
        try:
            if hasattr(self, 'note_classifier') and self.note_classifier.is_trained:
                category, confidence = self.note_classifier.predict(text)
                note.ml_category = category
                note.ml_confidence = confidence
                print(f"✓ ML Prediction: {category} ({confidence * 100:.1f}%)")
            else:
                print(f"⚠️ ML Classifier not available or not trained")
                note.ml_category = None
                note.ml_confidence = 0.0
        except Exception as e:
            print(f"✗ ML Error: {e}")
            note.ml_category = None
            note.ml_confidence = 0.0

        return note
    def search_note(self, code: int) -> 'Note':
        """
        Searches for a note by its code for the current patient.

        Parameters:
        - code (int): The unique code of the note to search for.

        Return Type:
        - Note: The Note instance if found, raises an exception otherwise.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        if self.current_patient is None:
            raise NoCurrentPatientException
        
        return self.current_patient.search_note(code)

    def retrieve_notes(self, search_text: str) -> list:
        """
        Retrieves notes containing the specified text for the current patient.

        Parameters:
        - search_text (str): The text to search for in notes.

        Return Type:
        - list: A list of matching Note instances.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        if  self.current_patient is None:
            raise NoCurrentPatientException
        
        return self.current_patient.retrieve_notes_by_text(search_text)

    def delete_note(self, code: int) -> bool:
        """
        Deletes a note by its code for the current patient.

        Parameters:
        - code (int): The unique code of the note to delete.

        Return Type:
        - bool: Returns True if the note is successfully deleted, raises an exception otherwise.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        if self.current_patient is None:
            raise NoCurrentPatientException
        
        return self.current_patient.delete_note(code)
        
        
    def update_note(self, code: int, text: str) -> bool:
        """
        Updates a note's content for the current patient.

        Parameters:
        - code (int): The unique code of the note to update.
        - text (str): The new content for the note.

        Return Type:
        - bool: Returns True if the note is successfully updated, raises an exception otherwise.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        if self.current_patient is None:
           raise NoCurrentPatientException
        
        return self.current_patient.update_note(code, text)
       
    def list_notes(self) -> list:
        """
        Lists all notes for the current patient.

        Return Type:
        - list: A list of all Note instances for the current patient.
        """
        if not self.logged_in:
            raise IllegalAccessException
        
        if self.current_patient is None:
            raise NoCurrentPatientException
        
        return self.current_patient.list_notes()