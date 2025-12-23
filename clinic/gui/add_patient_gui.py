from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from clinic.exception import (
    IllegalAccessException, IllegalOperationException
)
import re
from datetime import datetime

class AddPatientGUI(QWidget):
    """
    GUI class for adding a new patient in a medical clinic system.
    Provides input fields for patient details and validates them before calling the controller to create the patient.
    """

    def __init__(self, controller, parent=None):
        """
        Initializes the AddPatientGUI widget.

        Parameters:
        - controller: The Controller instance responsible for handling business logic.
        - parent: The parent widget, typically the main window.
        """
        super().__init__(parent)

        # Store the controller and parent for future use
        self.controller = controller
        self.parent_widget = parent

        # Create the main layout for the GUI
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Adjust margins and spacing for the layout
        main_layout.setContentsMargins(40, 120, 40, 160)  
        main_layout.setSpacing(15) 

        # Add title to the window
        title_label = QLabel("ADD PATIENT")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #000000;")
        main_layout.addWidget(title_label)

        # Create a layout for input fields
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)

        # Add input fields for Personal Health Number (PHN)
        self.phn_label = QLabel("Personal Health Number (PHN):")
        input_layout.addWidget(self.phn_label)
        self.phn_input = QLineEdit()
        self.phn_input.setFixedHeight(30)
        input_layout.addWidget(self.phn_input)

        # Add input fields for Full Name
        self.name_label = QLabel("Full Name:")
        input_layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.name_input.setFixedHeight(30)
        input_layout.addWidget(self.name_input)

        # Add input fields for Birth Date
        self.birth_date_label = QLabel("Birth Date (YYYY-MM-DD):")
        input_layout.addWidget(self.birth_date_label)
        self.birth_date_input = QLineEdit()
        self.birth_date_input.setFixedHeight(30)
        input_layout.addWidget(self.birth_date_input)

        # Add input fields for Phone Number
        self.phone_label = QLabel("Phone Number:")
        input_layout.addWidget(self.phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setFixedHeight(30)
        input_layout.addWidget(self.phone_input)

        # Add input fields for Email
        self.email_label = QLabel("Email:")
        input_layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(30)
        input_layout.addWidget(self.email_input)

        # Add input fields for Address
        self.address_label = QLabel("Address:")
        input_layout.addWidget(self.address_label)
        self.address_input = QLineEdit()
        self.address_input.setFixedHeight(30)
        input_layout.addWidget(self.address_input)

        # Add the input layout to the main layout
        main_layout.addLayout(input_layout)

        # Create a layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # Add "Add Patient" button
        self.add_patient_button = QPushButton("Add Patient")
        self.add_patient_button.setFixedSize(150, 40)  
        self.add_patient_button.clicked.connect(self.add_patient)  
        button_layout.addWidget(self.add_patient_button)

        # Add "Back to Menu" button
        self.back_to_menu = QPushButton("Back to Menu")
        self.back_to_menu.setFixedSize(150, 40)
        self.back_to_menu.clicked.connect(self.back_to_menu_func) 
        button_layout.addWidget(self.back_to_menu)

        # Wrap the button layout in a vertical layout for centering
        button_wrapper_layout = QVBoxLayout()
        button_wrapper_layout.addLayout(button_layout)
        button_wrapper_layout.setContentsMargins(0, 0, 0, 0) 
        button_wrapper_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        main_layout.addLayout(button_wrapper_layout)

    def validate_date(self, date):
        """
        Validates the provided date to ensure it is in the YYYY-MM-DD format.

        Parameters:
        - date (str): The date string to validate.

        Returns:
        - bool: True if the date is valid, False otherwise.
        """
        try:
            if date != datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d"):
                raise ValueError("Invalid date format")
            return True
        except ValueError:
            return False

    def add_patient(self):
        """
        Gathers input from the form, validates it, and attempts to create a new patient.

        Handles errors and provides feedback via message boxes.
        """
        try:
            phn = int(self.phn_input.text())
            name = self.name_input.text()
            birth_date = self.birth_date_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()
            address = self.address_input.text()

            # Validate that all fields are filled
            if not all([name, birth_date, phone, email, address]):
                raise ValueError("All fields must be filled out.")

            # Validate the birth date format
            if not self.validate_date(birth_date):
                raise ValueError("Invalid birth date. Please use the format YYYY-MM-DD and ensure the date is correct.")

            # Validate phone number (10 digits)
            if not re.match(r"^\d{10}$", phone):
                raise ValueError("Phone Number must be exactly 10 digits.")

            # Validate email format
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                raise ValueError("Invalid email format.")

            self.controller.create_patient(phn, name, birth_date, phone, email, address)

            QMessageBox.information(self, "Patient Added", "Patient successfully added!")
            self.phn_input.clear()
            self.name_input.clear()
            self.birth_date_input.clear()
            self.phone_input.clear()
            self.email_input.clear()
            self.address_input.clear()

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except IllegalAccessException:
            QMessageBox.critical(self, "Access Error", "You must be logged in to add a patient.")
        except IllegalOperationException as ioe:
            error_message = str(ioe).strip()
            if "DUPLICATE PHN" in error_message.lower():
                QMessageBox.warning(self, "Duplicate PHN", "Someone with that PHN already exists.")
            else:
                QMessageBox.warning(self, "Operation Error", error_message or "A Patient With that PHN Already Exists")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def back_to_menu_func(self):
        """
        Navigates back to the main menu GUI.

        Dynamically imports MainMenuGUI to avoid circular imports.
        """
        from clinic.gui.main_menu_gui import MainMenuGUI # Delayed import to prevent circular dependencies
        if self.parent_widget:
            self.parent_widget.setCentralWidget(MainMenuGUI(self.controller, self.parent_widget))
