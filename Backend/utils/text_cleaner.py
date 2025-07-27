import spacy

class TextCleaner:
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize the TextCleaner with a spaCy model.
        
        Args:
            model_name (str): Name of the spaCy model to load.
        """
        self.nlp = spacy.load(model_name)

    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess the input text using spaCy.
        Steps:
        - Lowercase
        - Remove stopwords and punctuation
        - Lemmatize tokens
        
        Args:
            text (str): Raw input text.
        
        Returns:
            str: Cleaned and preprocessed text.
        """
        doc = self.nlp(text.lower())
        cleaned_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return " ".join(cleaned_tokens)


# Example usage:
if __name__ == "__main__":
    cleaner = TextCleaner()
    sample_text = "This is an example sentence to demonstrate text cleaning using spaCy!"
    print("Original Text:", sample_text)
    print("Cleaned Text:", cleaner.clean_text(sample_text))
