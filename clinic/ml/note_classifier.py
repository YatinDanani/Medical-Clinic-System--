"""
Machine Learning classifier for clinical notes.
Uses TF-IDF vectorization and Naive Bayes algorithm.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os


class NoteClassifier:
    """
    Classifies clinical notes into categories using machine learning.

    Categories:
    - Emergency: Urgent medical situations
    - Follow-up: Return visits for ongoing treatment
    - Routine: Regular checkups and preventive care
    - Initial Consultation: First-time patient visits
    """

    def __init__(self):
        """Initialize the classifier with a ML pipeline."""
        # Create a pipeline that:
        # 1. Converts text to numbers (TF-IDF)
        # 2. Classifies using Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=200, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        self.categories = []
        self.is_trained = False

    def train(self, notes, labels):
        """
        Train the model with example notes and their categories.

        Parameters:
        - notes: List of note texts (strings)
        - labels: List of categories (strings)

        Example:
            notes = ["Patient has fever", "Routine checkup"]
            labels = ["Emergency", "Routine"]
            classifier.train(notes, labels)
        """
        self.categories = list(set(labels))
        self.model.fit(notes, labels)
        self.is_trained = True
        print(f"✓ Model trained successfully with {len(self.categories)} categories")
        print(f"  Categories: {', '.join(self.categories)}")

    def predict(self, note_text):
        """
        Predict the category for a new note.

        Parameters:
        - note_text: The clinical note text (string)

        Returns:
        - Tuple of (predicted_category, confidence_score)

        Example:
            category, confidence = classifier.predict("Patient has severe chest pain")
            # Returns: ("Emergency", 0.95)
        """
        if not self.is_trained:
            return "Unknown", 0.0

        prediction = self.model.predict([note_text])[0]
        probabilities = self.model.predict_proba([note_text])[0]
        confidence = max(probabilities)

        return prediction, confidence

    def predict_with_all_probabilities(self, note_text):
        """
        Get probabilities for all categories.

        Returns:
        - Dictionary with {category: probability} for all categories
        """
        if not self.is_trained:
            return {}

        probabilities = self.model.predict_proba([note_text])[0]
        return dict(zip(self.categories, probabilities))

    def save_model(self, filepath='clinic/ml/models/note_classifier.pkl'):
        """
        Save the trained model to disk.

        Parameters:
        - filepath: Where to save the model file
        """
        if not self.is_trained:
            print("✗ Cannot save untrained model")
            return False

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save the model
        joblib.dump({
            'model': self.model,
            'categories': self.categories,
            'is_trained': self.is_trained
        }, filepath)

        print(f"✓ Model saved to {filepath}")
        return True

    def load_model(self, filepath='clinic/ml/models/note_classifier.pkl'):
        """
        Load a pre-trained model from disk.

        Parameters:
        - filepath: Path to the saved model file

        Returns:
        - True if loaded successfully, False otherwise
        """
        if not os.path.exists(filepath):
            print(f"✗ No saved model found at {filepath}")
            return False

        try:
            data = joblib.load(filepath)
            self.model = data['model']
            self.categories = data['categories']
            self.is_trained = data['is_trained']
            print(f"✓ Model loaded successfully")
            print(f"  Categories: {', '.join(self.categories)}")
            return True
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            return False


# For testing the classifier
if __name__ == "__main__":
    # Quick test
    classifier = NoteClassifier()

    # Sample data
    test_notes = [
        "Patient has severe chest pain",
        "Routine checkup completed",
        "Follow-up on blood pressure medication"
    ]
    test_labels = ["Emergency", "Routine", "Follow-up"]

    # Train
    classifier.train(test_notes, test_labels)

    # Test prediction
    category, confidence = classifier.predict("Patient comes with headache")
    print(f"\nTest prediction:")
    print(f"  Category: {category}")
    print(f"  Confidence: {confidence * 100:.1f}%")