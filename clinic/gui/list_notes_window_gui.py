from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QPlainTextEdit, QVBoxLayout, QHBoxLayout
)

class ListNotesWindow(QWidget):
    """
    GUI window for displaying the full patient record in a QPlainTextEdit widget.
    Provides a simple interface to view all notes associated with a patient.
    """

    def __init__(self, controller, parent, notes):
        """
        Initializes the ListNotesWindow.

        Parameters:
        - controller: The Controller instance for managing business logic.
        - parent: The parent widget, typically the main application window.
        - notes: A list of note objects to be displayed in the window.
        """
        super().__init__(parent)

        # Store references for controller, parent widget, and notes
        self.controller = controller
        self.parent_widget = parent
        self.notes = notes

        # Set up the main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title label
        title_label = QLabel("Full Patient Record")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")  
        self.layout.addWidget(title_label)

        # QPlainTextEdit to display the notes
        self.notes_display = QPlainTextEdit()
        self.notes_display.setReadOnly(True) 
        self.notes_display.setPlainText(self.format_notes()) 
        self.layout.addWidget(self.notes_display)

        # Create a horizontal layout for the back button
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  

        # Back to Menu button
        back_button = QPushButton("Back to Menu")
        back_button.setFixedSize(150, 40)  
        back_button.clicked.connect(self.return_to_menu)  
        button_layout.addWidget(back_button)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

    def format_notes(self):
        """
        Formats the notes for display in the QPlainTextEdit widget.
        Includes ML classification predictions if available.

        Returns:
        - str: A formatted string where each note is separated by two newlines.
        """
        formatted_notes = []

        for note in self.notes:
            # Basic note info
            note_text = f"Note #{note.code}, from {note.timestamp}\n{note.text}"

            # Add ML prediction if available
            if hasattr(note, 'ml_category') and note.ml_category:
                confidence_percent = note.ml_confidence * 100

                # Determine confidence level
                if note.ml_confidence >= 0.7:
                    confidence_level = "High"
                elif note.ml_confidence >= 0.5:
                    confidence_level = "Medium"
                else:
                    confidence_level = "Low"

                note_text += f"\n ML Classification: {note.ml_category} ({confidence_percent:.1f}% - {confidence_level})"

            formatted_notes.append(note_text)

        return "\n\n".join(formatted_notes)

    def return_to_menu(self):
        """
        Navigates back to the appointment main menu GUI.

        If the parent widget is set, transitions back to the AppointMainMenuGUI.
        """
        from clinic.gui.appointment_main_menu_gui import AppointMainMenuGUI  # Delayed import to avoid circular dependencies
        if self.parent_widget:
            self.parent_widget.setCentralWidget(AppointMainMenuGUI(self.controller, self.parent_widget))
