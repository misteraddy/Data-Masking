import re
import unicodedata
from datetime import datetime
import spacy

# =====================================================================
# Configuration & Global Schemas
# =====================================================================

# Default core regex patterns
DEFAULT_PATTERNS = {
    'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'PHONE_US': r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
    'SSN': r'\b\d{3}-?\d{2}-?\d{4}\b',
    'PASSPORT_US': r'\b[A-Z]\d{8}\b',
    'CREDIT_CARD': r'\b4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}\b',
    'IP_ADDRESS': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
}

# Default spaCy NER token mapping
DEFAULT_NER_TYPES = {
    'PERSON': '[PERSON]',
    'ORG': '[ORGANIZATION]',
    'GPE': '[LOCATION]',
    'MONEY': '[MONEY]',
    'DATE': '[DATE]'
}


# =====================================================================
# Helper Core Components
# =====================================================================

def normalize_text(text: str) -> str:
    """Normalizes text by handling accents and stripping extra whitespace."""
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return ' '.join(text.split())


def is_likely_pii(text: str) -> bool:
    """Heuristic check to discover if a block of text likely contains PII."""
    indicators = {'ssn', 'social', 'phone', 'email', 'address'}
    text_lower = text.lower()
    words = set(text_lower.split())
    return bool(words.intersection(indicators))


# =====================================================================
# Main Redaction Pipeline Engine
# =====================================================================

def redact_text(text: str, nlp_model, custom_patterns: dict = None, exclude_types: set = None) -> tuple:
    """
    Redacts PII from raw string text using regex patterns and a spaCy NLP pipeline.
    Returns a tuple of (redacted_string, statistics_dict).
    """
    if exclude_types is None:
        exclude_types = set()

    # Track processing statistics
    stats = {
        'start_time': datetime.now(),
        'original_length': len(text),
        'entities_redacted': {},
        'patterns_redacted': {}
    }

    # 1. Normalize Input Text
    text = normalize_text(text)

    # 2. Extract Custom Regex Layouts
    if custom_patterns:
        for p_name, (pattern, placeholder) in custom_patterns.items():
            if p_name in exclude_types:
                continue
            matches = re.findall(pattern, text)
            if matches:
                stats['patterns_redacted'][p_name] = len(matches)
                text = re.sub(pattern, placeholder, text)

    # 3. Extract Default Target Regular Expressions
    for p_name, pattern in DEFAULT_PATTERNS.items():
        if p_name in exclude_types:
            continue
        matches = re.findall(pattern, text)
        if matches:
            stats['patterns_redacted'][p_name] = len(matches)
            text = re.sub(pattern, f"[{p_name}]", text)

    # 4. Extract Language Entity Targets (NER)
    # Token operations slice in reverse to protect positional integrity indices
    doc = nlp_model(text)
    entities = sorted(doc.ents, key=lambda e: e.start_char, reverse=True)
    
    text_list = list(text)
    for ent in entities:
        if ent.label_ in DEFAULT_NER_TYPES and ent.label_ not in exclude_types:
            placeholder = DEFAULT_NER_TYPES[ent.label_]
            
            # Record tracking data metric
            stats['entities_redacted'][ent.label_] = stats['entities_redacted'].get(ent.label_, 0) + 1
            
            # Splicing token substitution block 
            text_list[ent.start_char:ent.end_char] = list(placeholder)
            
    text = "".join(text_list)
    stats['duration_seconds'] = (datetime.now() - stats['start_time']).total_seconds()

    return text, stats


# =====================================================================
# Execution Execution Block
# =====================================================================
if __name__ == "__main__":
    
    # Initialize your model once globally outside of runtime loop
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Error: Missing model. Execute: python -m spacy download en_core_web_sm")
        exit(1)

    # Input OCR Document string variable sample
    ocr_text = """
    POLICY NUMBER: 987654321-A
    INSURED PARTY: John Doe
    EMPLOYER: Apple Inc.
    CONTACT INFO: 
    Email: john.doe@email.com
    Phone: (555) 123-4567
    PRIMARY IDENTIFIER: SSN: 123-45-6789
    DATE OF ISSUE: October 24, 2024
    PREMIUM AMOUNT: $1200.00
    ADDITIONAL DETAILS: Patient ID: 884921, Blood Type: O+
    """

    # Custom variables
    custom_patterns = {
        'PATIENT_ID': (r'\b\d{6}\b', '[PATIENT_ID]'),
        'BLOOD_TYPE': (r'\b(A|B|AB|O)[+-]\b', '[BLOOD_TYPE]')
    }
    exclude_types = set()

    # Functional call orchestration
    print("--- Redacting Document (Functional) ---")
    redacted_text, stats = redact_text(
        ocr_text, 
        nlp_model=nlp,
        custom_patterns=custom_patterns, 
        exclude_types=exclude_types
    )

    # Output Redaction Elements
    print("\n### REDACTED OUTPUT ###")
    print(redacted_text)
    
    print("\n### REDACTION STATISTICS ###")
    print(f"Original Length: {stats['original_length']} characters")
    print(f"Processing Duration: {stats['duration_seconds']:.4f} seconds")
    print(f"Regex Pattern Matches: {stats['patterns_redacted']}")
    print(f"NLP Entities Found: {stats['entities_redacted']}")