from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QMessageBox, QInputDialog, QVBoxLayout, QHBoxLayout
)
from clinic.exception import NoCurrentPatientException, IllegalOperationException


class AppointMainMenuGUI(QWidget):
    """
    GUI for managing a patient's appointment and medical records.
    Provides options to add, retrieve, modify, remove notes, and finish the appointment.
    """

    def __init__(self, controller, parent=None):
        """
        Initializes the appointment menu GUI.

        Parameters:
        - controller: The Controller instance for managing business logic.
        - parent: The parent widget, typically the main window.
        """
        super().__init__(parent)

        # Store the controller and parent for later use
        self.controller = controller
        self.parent_widget = parent

        # Get the current patient from the controller
        self.current_patient = self.controller.get_current_patient()

        # Set up the appointment menu layout
        self.appointment_menu()

    def appointment_menu(self):
        """
        Creates the layout and components for the appointment menu.
        """
        # Main layout setup
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # Title
        title_label = QLabel("MEDICAL CLINIC SYSTEM - APPOINTMENT MENU")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(30)

        # Patient information section
        patient_info_label = QLabel(
            f"PATIENT:\n"
            f"PHN: {self.current_patient.phn}\n"
            f"Name: {self.wrap_text(self.current_patient.name)}\n"
            f"Birth Date: {self.wrap_text(self.current_patient.birth_date)}\n"
            f"Phone: {self.wrap_text(self.current_patient.phone)}\n"
            f"Email: {self.wrap_text(self.current_patient.email)}\n"
            f"Address: {self.wrap_text(self.current_patient.address)}"
        )
        patient_info_label.setStyleSheet("font-size: 14px; color: gray;")
        patient_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(patient_info_label)
        main_layout.addSpacing(40)

        # Button layout for actions
        button_layout = QHBoxLayout()

        # Left-side buttons
        left_button_layout = QVBoxLayout()
        left_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_button_layout.setSpacing(15)  # Spacing between buttons

        # Add buttons to the left side layout
        add_note_button = QPushButton("Add Note to Patient Record")
        add_note_button.setFixedSize(450, 35)
        add_note_button.clicked.connect(self.open_add_note)
        left_button_layout.addWidget(add_note_button)

        retrieve_notes_button = QPushButton("Retrieve Notes by Text")
        retrieve_notes_button.setFixedSize(450, 35)
        retrieve_notes_button.clicked.connect(self.open_retrieve_notes)
        left_button_layout.addWidget(retrieve_notes_button)

        change_note_button = QPushButton("Change Note in Patient Record")
        change_note_button.setFixedSize(450, 35)
        change_note_button.clicked.connect(self.open_change_note)
        left_button_layout.addWidget(change_note_button)

        button_layout.addLayout(left_button_layout)

        # Right-side buttons
        right_button_layout = QVBoxLayout()
        right_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_button_layout.setSpacing(15)

        # Add buttons to the right side layout
        remove_note_button = QPushButton("Remove Note from Patient Record")
        remove_note_button.setFixedSize(450, 35)
        remove_note_button.clicked.connect(self.open_remove_note)
        right_button_layout.addWidget(remove_note_button)

        list_full_record_button = QPushButton("List Full Patient Record")
        list_full_record_button.setFixedSize(450, 35)
        list_full_record_button.clicked.connect(self.open_list_full_record)
        right_button_layout.addWidget(list_full_record_button)

        finish_appointment_button = QPushButton("Finish Appointment")
        finish_appointment_button.setFixedSize(450, 35)
        finish_appointment_button.clicked.connect(self.finish_appointment)
        right_button_layout.addWidget(finish_appointment_button)

        button_layout.addLayout(right_button_layout)

        # Add button layout to the main layout
        main_layout.addLayout(button_layout)
        main_layout.addSpacing(20)

    def wrap_text(self, text, max_width=50):
        """
        Wraps the given text to the specified width.

        Parameters:
        - text (str): The text to wrap.
        - max_width (int): The maximum number of characters per line.

        Returns:
        - str: Wrapped text with line breaks.
        """
        if len(text) <= max_width:
            return text
        wrapped_lines = []
        while len(text) > max_width:
            split_index = text.rfind(" ", 0, max_width)
            if split_index == -1:  # If no space is found, split at max_width
                split_index = max_width
            wrapped_lines.append(text[:split_index])
            text = text[split_index:].strip()
        wrapped_lines.append(text)
        return "\n".join(wrapped_lines)

    def open_add_note(self):
        """
        Opens a dialog to add a new note to the patient's record.
        Displays ML classification prediction after adding the note.
        """
        try:
            note_text, ok = QInputDialog.getText(self, "Add Note", "Enter note text:")
            if ok and note_text.strip():
                # Create the note and get the returned note object
                new_note = self.controller.create_note(note_text.strip())

                # Build success message with ML prediction
                message = "Note successfully added to the patient's record!"

                # Add ML prediction if available
                if new_note and hasattr(new_note, 'ml_category') and new_note.ml_category:
                    confidence_percent = new_note.ml_confidence * 100

                    # Determine confidence level
                    if new_note.ml_confidence >= 0.7:
                        confidence_level = "High"
                    elif new_note.ml_confidence >= 0.5:
                        confidence_level = "Medium"
                    else:
                        confidence_level = "Low"

                    message += f"\n\n ML Classification:\n"
                    message += f"Category: {new_note.ml_category}\n"
                    message += f"Confidence: {confidence_percent:.1f}% ({confidence_level})"

                QMessageBox.information(self, "Success", message)

        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_retrieve_notes(self):
        """
        Opens a dialog to retrieve notes by searching for specific text.
        """
        try:
            search_text, ok = QInputDialog.getText(self, "Retrieve Notes", "Enter text to search:")
            if not ok:
                return
            if not search_text.strip():
                QMessageBox.warning(self, "Input Error", "Search text cannot be empty.")
                return
            notes = self.controller.retrieve_notes(search_text.strip())
            if notes:
                from clinic.gui.retrieve_notes_window_gui import RetrieveNotesWindow  # Delayed import
                self.parent_widget.setCentralWidget(
                    RetrieveNotesWindow(self.controller, self.parent_widget, notes, search_text.strip()))
            else:
                QMessageBox.information(self, "No Results", "No notes found matching the search criteria.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_change_note(self):
        """
        Opens a dialog to change a specific note in the patient's record.
        """
        try:
            note_code, ok = QInputDialog.getInt(self, "Change Note", "Enter Note Number (Code):")
            if not ok:
                return
            try:
                note = self.controller.search_note(note_code)
                if not note:
                    raise IllegalOperationException(f"Note #{note_code} does not exist.")
            except IllegalOperationException as ioe:
                QMessageBox.warning(self, "Invalid Note", str(ioe))
                return
            from clinic.gui.change_note_window_gui import ChangeNoteWindow  # Delayed import
            self.parent_widget.setCentralWidget(ChangeNoteWindow(self.controller, note_code, self.parent_widget))
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_remove_note(self):
        """
        Opens a dialog to remove a specific note from the patient's record.
        """
        try:
            note_code, ok = QInputDialog.getInt(self, "Remove Note", "Enter Note Number (Code):")
            if not ok:
                return
            try:
                note = self.controller.search_note(note_code)
                if not note:
                    raise IllegalOperationException(f"Note #{note_code} does not exist.")
            except IllegalOperationException as ioe:
                QMessageBox.warning(self, "Invalid Note", str(ioe))
                return
            from clinic.gui.remove_note_window_gui import RemoveNoteWindow  # Delayed import
            self.parent_widget.setCentralWidget(RemoveNoteWindow(self.controller, note_code, self.parent_widget))
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def open_list_full_record(self):
        """
        Lists the full record of the current patient.
        """
        try:
            notes = self.controller.list_notes()
            if notes:
                from clinic.gui.list_notes_window_gui import ListNotesWindow  # Delayed import
                self.parent_widget.setCentralWidget(ListNotesWindow(self.controller, self.parent_widget, notes))
            else:
                QMessageBox.information(self, "No Notes", "The patient's record is empty.")
        except NoCurrentPatientException:
            QMessageBox.critical(self, "Error", "No current patient is selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def finish_appointment(self):
        """
        Finishes the appointment and unsets the current patient.
        """
        try:
            self.controller.unset_current_patient()
            self.back_to_main_menu()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def back_to_main_menu(self):
        """
        Navigates back to the main menu GUI.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI  # Delayed import to avoid circular dependencies
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))