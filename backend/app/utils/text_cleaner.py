import re
import spacy

# Load spaCy English model once when the application starts
nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """
    Performs NLP preprocessing on text.

    Steps:
    1. Convert to lowercase
    2. Remove punctuation and special characters
    3. Remove extra whitespace
    4. Tokenize
    5. Remove stop words
    6. Lemmatize
    7. Return cleaned text
    """

    # Lowercase
    text = text.lower()

    # Remove punctuation / special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    # NLP processing
    doc = nlp(text)

    cleaned_tokens = []

    for token in doc:

        # Skip stop words and spaces
        if token.is_stop:
            continue

        if token.is_space:
            continue

        # Skip very short meaningless tokens
        if len(token.text) <= 1:
            continue

        # Lemmatization
        cleaned_tokens.append(token.lemma_)

    return " ".join(cleaned_tokens)