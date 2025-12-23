"""
Script to train the clinical note classifier.
Run this file to create and save your trained ML model.
"""

import sys
import os

# Add project root to Python path
# This fixes the import error!
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now imports will work
from clinic.ml.note_classifier import NoteClassifier
from clinic.ml.training_data import TRAINING_NOTES


def main():
    print("=" * 60)
    print("TRAINING CLINICAL NOTE CLASSIFIER")
    print("=" * 60)

    # Separate notes and labels from training data
    notes = [note for note, label in TRAINING_NOTES]
    labels = [label for note, label in TRAINING_NOTES]

    print(f"\nTraining data:")
    print(f"  Total examples: {len(notes)}")
    print(f"  Categories: {len(set(labels))}")
    print(f"  Breakdown:")
    for category in set(labels):
        count = labels.count(category)
        print(f"    - {category}: {count} examples")

    # Create and train classifier
    print("\nTraining model...")
    classifier = NoteClassifier()
    classifier.train(notes, labels)

    # Save the trained model
    print("\nSaving model...")
    classifier.save_model()

    # Test with some examples
    print("\n" + "=" * 60)
    print("TESTING MODEL")
    print("=" * 60)

    test_cases = [
        "Patient arrives with severe chest pain and difficulty breathing",
        "Routine annual physical examination completed today",
        "Follow-up visit to check blood pressure medication effectiveness",
        "New patient presents with persistent cough for 2 weeks"
    ]

    for test_note in test_cases:
        category, confidence = classifier.predict(test_note)
        print(f"\nNote: \"{test_note[:50]}...\"")
        print(f"  → Predicted: {category}")
        print(f"  → Confidence: {confidence*100:.1f}%")

    print("\n" + "=" * 60)
    print("✓ TRAINING COMPLETE!")
    print("=" * 60)
    print("\nYour model is ready to use in the application.")


if __name__ == "__main__":
    main()