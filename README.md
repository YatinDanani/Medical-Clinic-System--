# Medical Clinic System GUI

This project implements a medical clinic system in Python using a Model-View-Controller (MVC) architecture. It supports both a command-line interface (CLI) and a graphical user interface (GUI) built with PyQt6, with integrated machine learning for clinical note classification.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [Usage](#usage)
   * [Command-Line Interface](#command-line-interface)
   * [Graphical User Interface](#graphical-user-interface)
   * [Machine Learning Model Training](#machine-learning-model-training)
7. [Testing](#testing)
8. [Development & Version Control](#development--version-control)
9. [Contributing](#contributing)

---

## Overview

This application manages patient records and clinical notes for a medical clinic. It follows the MVC pattern:

* **Model:** Core classes (`Patient`, `PatientRecord`, `Note`) and business logic with ML integration.
* **View:** Two front-ends:
  * CLI via `clinic/cli`
  * GUI via `clinic/gui` (PyQt6)
* **Controller:** Orchestrates CRUD operations between view and model, integrating ML predictions.
* **Machine Learning:** Automatic classification of clinical notes into categories using scikit-learn.

## Features

* User authentication (login/logout)
* CRUD operations for patients and notes
* JSON persistence for patient metadata
* Pickle persistence for clinical notes
* Interactive tables and editors via PyQt6 widgets
* **Machine Learning Note Classification:**
  * Automatic categorization of clinical notes
  * Four categories: Emergency, Follow-up, Routine, Initial Consultation
  * Confidence scoring for predictions
  * TF-IDF vectorization with Naive Bayes classifier

## Prerequisites

* Python 3.9 or later
* pip package manager
* PyQt6 framework
* scikit-learn library
* joblib for model persistence

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:

   ```bash
   pip install PyQt6 scikit-learn joblib
   ```

3. Train the ML model (first-time setup):

   ```bash
   python train_ml_model.py
   ```

   This creates a trained model at `clinic/ml/models/note_classifier.pkl`

## Project Structure

```plaintext
.
├── clinic
│   ├── cli
│   │   └── __main__.py        # CLI entry point
│   ├── dao                   # Data access objects
│   │   ├── patient_dao_json.py
│   │   ├── patient_encoder.py
│   │   ├── patient_decoder.py
│   │   └── note_dao_pickle.py
│   ├── gui                   # GUI components
│   │   ├── clinic_gui.py     # Main GUI window
│   │   └── ...               # Additional widgets
│   ├── ml                    # Machine Learning components
│   │   ├── note_classifier.py   # ML classifier implementation
│   │   ├── training_data.py     # Training dataset
│   │   └── models/              # Trained models directory
│   ├── controller.py         # Application logic with ML integration
│   ├── patient.py            # Patient model
│   ├── patient_record.py     # PatientRecord model
│   └── note.py               # Note model with ML attributes
├── tests
│   ├── patient_test.py
│   ├── patient_record_test.py
│   ├── note_test.py
│   └── integration_test.py    # Persistence & integration tests
├── train_ml_model.py          # ML model training script
└── README.md
```

## Usage

### Command-Line Interface

Get into the clinic folder:
```bash
cd clinic
```

Run the CLI prototype:

```bash
python3 -m clinic cli
```

Follow prompts to log in, manage patients, and edit notes. When creating notes, you'll see ML classification predictions automatically.

### Graphical User Interface

Launch the PyQt6 GUI:

```bash
python3 -m clinic gui
```

Use menus and forms to:

* Log in / Log out
* Search, list, create, update, delete patients
* View and manage notes per patient
* **See ML predictions when adding notes:**
  * Category prediction (Emergency, Follow-up, Routine, Initial Consultation)
  * Confidence percentage (High ≥70%, Medium 50-69%, Low <50%)

### Machine Learning Model Training

To train or retrain the note classifier:

```bash
python train_ml_model.py
```

**What it does:**
* Loads training data from `clinic/ml/training_data.py`
* Trains a TF-IDF + Naive Bayes model
* Saves the model to `clinic/ml/models/note_classifier.pkl`
* Shows training statistics and test predictions

**ML Classification Categories:**

| Category | Description |
|----------|-------------|
| Emergency | Urgent medical situations requiring immediate attention |
| Follow-up | Return visits for ongoing treatment monitoring |
| Routine | Regular checkups and preventive care |
| Initial Consultation | First-time patient visits |

**Example Output:**
```
Note #1, from 2025-01-15 14:30:22
Patient arrives with severe chest pain and difficulty breathing
ML Classification: Emergency (95.3% - High)
```

## Testing

* **Unit Tests:** Model logic and DAO operations

  ```bash
  python3 -m unittest -v tests/patient_test.py tests/patient_record_test.py tests/note_test.py
  ```

* **Integration Tests:** JSON & pickle persistence

  ```bash
  python3 -m unittest -v tests/integration_test.py
  ```

## Development & Version Control

* Create feature branches off `main`.
* Commit frequently with clear messages.
* Merge only after tests pass.

## Contributing

1. Fork the repo and create a new branch.
2. Implement changes and add tests.
3. Commit, push to your fork, and open a pull request.
