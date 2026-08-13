import re

import spacy


nlp = spacy.load("en_core_web_sm")


def looks_like_name(line: str) -> bool:
    """
    Check whether a line looks like a person's name.
    """

    line = line.strip()

    if not line:
        return False

    words = line.split()

    # Most names contain between 2 and 5 words
    if len(words) < 2 or len(words) > 5:
        return False

    # Names should not contain email addresses
    if "@" in line:
        return False

    # Names should not contain numbers
    if any(char.isdigit() for char in line):
        return False

    lower_line = line.lower()

    excluded_words = {
        "resume",
        "curriculum vitae",
        "cv",
        "objective",
        "summary",
        "education",
        "skills",
        "experience",
        "work experience",
        "professional experience",
    }

    if lower_line in excluded_words:
        return False

    # Exclude common location indicators
    location_words = {
        "usa",
        "u.s.a",
        "uae",
        "u.a.e",
        "india",
        "canada",
        "uk",
        "united states",
        "united arab emirates",
    }

    words_lower = {word.lower().strip(",.") for word in words}

    if words_lower.intersection(location_words):
        return False

    # Names should primarily contain letters,
    # spaces, apostrophes, periods, or hyphens
    if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ.' -]+", line):
        return False

    return True


def extract_name_from_first_lines(header_text: str) -> str | None:
    """
    First try to extract the name using the position
    of the text in the resume header.

    Resume names are usually found on the first line.
    """

    lines = [
        line.strip()
        for line in header_text.splitlines()
        if line.strip()
    ]

    # Check the first 3 lines only
    for line in lines[:3]:

        if looks_like_name(line):
            return line

    return None


def extract_name_with_spacy(header_text: str) -> str | None:
    """
    Use spaCy Named Entity Recognition as a fallback
    to identify PERSON entities.
    """

    doc = nlp(header_text)

    for entity in doc.ents:

        if entity.label_ == "PERSON":

            name = entity.text.strip()

            if looks_like_name(name):
                return name

    return None


def extract_name(header_text: str) -> str | None:
    """
    Extract the candidate's name.

    Strategy:
    1. Check the first few lines of the resume header.
    2. If that fails, use spaCy PERSON entity recognition.
    """

    # Resume structure is more reliable for the candidate name
    name = extract_name_from_first_lines(header_text)

    if name:
        return name

    # Fall back to spaCy
    return extract_name_with_spacy(header_text)