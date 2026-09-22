import re
import spacy

# Load spaCy English model safely with fallback
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

# Words that spaCy mistakenly lemmatizes or treats as non-nouns
PROTECTED_TECHNICAL_WORDS = {
    "aws",
    "kubernetes",
    "pandas",
    "transformers",
    "microservices",
    "redis",
    "postgres",
    "postgresql",
    "statistics",
    "devops",
    "jenkins",
    "keras",
    "spacy",
    "analytics",
    "graphics",
    "physics",
    "dynamics",
    "networks",
    "apis",
}

# Mapping of special symbol skills to safe tokens for TF-IDF
SPECIAL_SYMBOL_MAP = [
    (re.compile(r'(?<!\w)c\+\+(?!\w)', re.IGNORECASE), 'cpp'),
    (re.compile(r'(?<!\w)c\#(?!\w)', re.IGNORECASE), 'csharp'),
    (re.compile(r'(?<!\w)\.net(?!\w)', re.IGNORECASE), 'dotnet'),
    (re.compile(r'(?<!\w)asp\.net(?!\w)', re.IGNORECASE), 'aspdotnet'),
    (re.compile(r'\bnode(?:\.|\s*)js\b', re.IGNORECASE), 'nodejs'),
    (re.compile(r'\bnext(?:\.|\s*)js\b', re.IGNORECASE), 'nextjs'),
    (re.compile(r'\bvue(?:\.|\s*)js\b', re.IGNORECASE), 'vuejs'),
    (re.compile(r'\bexpress(?:\.|\s*)js\b', re.IGNORECASE), 'expressjs'),
    (re.compile(r'\bci[\s\/\-]cd\b', re.IGNORECASE), 'cicd'),
    (re.compile(r'\btcp[\s\/\-]ip\b', re.IGNORECASE), 'tcpip'),
]


def normalize_text_for_nlp(text: str) -> str:
    """
    Light normalization for entity and skill extraction.
    Preserves case, punctuation relevant to coding languages (+, #, ., /, -),
    while normalizing special unicode quotes, bullets, and excessive whitespace.
    """
    if not text:
        return ""

    # Normalize unicode bullets and special dashes
    text = text.replace("\u2022", " ").replace("\u2023", " ").replace("\u25e6", " ")
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')

    # Replace tabs and newlines with spaces while keeping sentence structure
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_text_for_tfidf(text: str) -> str:
    """
    NLP preprocessing specifically designed for TF-IDF / Vectorization.
    Preserves technical vocabulary, encodes compound tokens (c++, .net, etc.),
    removes non-technical stopwords, and lemmatizes safely without breaking tech nouns.
    """
    if not text:
        return ""

    # Normalize formatting
    text = normalize_text_for_nlp(text).lower()

    # Protect symbols that would otherwise be destroyed
    for pattern, replacement in SPECIAL_SYMBOL_MAP:
        text = pattern.sub(replacement, text)

    # Clean residual punctuation while keeping alphanumeric and spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return ""

    doc = nlp(text)
    cleaned_tokens = []

    for token in doc:
        # Keep short programming languages/tokens if they are significant
        word = token.text.lower()

        if token.is_space or token.is_punct:
            continue

        # Check stopwords (ensure key tech words aren't dropped)
        if token.is_stop and word not in {"go", "r", "c", "next", "it", "ai", "ml"}:
            continue

        if len(word) <= 1 and word not in {"c", "r"}:
            continue

        # Lemmatize only non-protected words
        if word in PROTECTED_TECHNICAL_WORDS:
            cleaned_tokens.append(word)
        else:
            lemma = token.lemma_.lower()
            # If spaCy truncated an 's' from a known technical word, restore it
            if lemma + "s" in PROTECTED_TECHNICAL_WORDS:
                cleaned_tokens.append(lemma + "s")
            else:
                cleaned_tokens.append(lemma)

    return " ".join(cleaned_tokens)


def clean_text(text: str) -> str:
    """
    Standard clean_text entrypoint used across the application.
    """
    return clean_text_for_tfidf(text)