import re

import spacy


nlp = spacy.load("en_core_web_sm")


MONTH_PATTERN = (
    r"(January|February|March|April|May|June|July|August|"
    r"September|October|November|December)"
)


def extract_date_range(text: str) -> str | None:
    """
    Extract a graduation date or date range from an education line.

    Examples:
    - June 2026 (Expected)
    - April 2008 - May 2022
    """

    # Date range
    range_pattern = (
        rf"{MONTH_PATTERN}\s+\d{{4}}\s*-\s*"
        rf"{MONTH_PATTERN}\s+\d{{4}}"
    )

    match = re.search(range_pattern, text, re.IGNORECASE)

    if match:
        return match.group(0)

    # Single date with optional Expected
    single_pattern = (
        rf"{MONTH_PATTERN}\s+\d{{4}}"
        r"(?:\s*\(Expected\))?"
    )

    match = re.search(single_pattern, text, re.IGNORECASE)

    if match:
        return match.group(0)

    return None


def remove_date_from_line(line: str, date_text: str | None) -> str:
    """
    Remove the detected date from an education line.
    """

    if not date_text:
        return line.strip()

    cleaned = line.replace(date_text, "")

    # Remove leftover separators
    cleaned = re.sub(r"\s*-\s*$", "", cleaned)

    return cleaned.strip()


def extract_org_with_spacy(text: str) -> str | None:
    """
    Use spaCy as a fallback to find an organization
    that may represent a university or school.
    """

    doc = nlp(text)

    for entity in doc.ents:
        if entity.label_ == "ORG":
            return entity.text.strip()

    return None


def parse_education_line(line: str) -> dict | None:
    """
    Parse one education entry into structured fields.

    Expected common format:
    Degree, Institution - Date
    """

    line = line.strip().lstrip("•").strip()

    if not line:
        return None

    # Ignore coursework lines
    if line.lower().startswith("relevant coursework"):
        return None

    dates = extract_date_range(line)

    text_without_date = remove_date_from_line(line, dates)

    degree = None
    institution = None

    # Split on commas
    parts = [
        part.strip()
        for part in text_without_date.split(",")
        if part.strip()
    ]

    if len(parts) >= 2:
        degree = parts[0]

        # Everything after the first part is treated as institution
        institution = ", ".join(parts[1:])

    elif len(parts) == 1:
        degree = parts[0]

    # Fallback: try spaCy for organization
    if not institution:
        org = extract_org_with_spacy(text_without_date)

        if org:
            institution = org

            degree = text_without_date.replace(org, "").strip(" ,")

    return {
        "degree": degree,
        "institution": institution,
        "dates": dates,
    }


def extract_education(education_text: str) -> list[dict]:
    """
    Extract structured education entries from the EDUCATION section.

    If the section contains bullet-based education entries,
    only those bullet lines are parsed. This prevents supporting
    text such as coursework from being treated as a degree.
    """

    if not education_text:
        return []

    lines = [
        line.strip()
        for line in education_text.splitlines()
        if line.strip()
    ]

    education_entries = []

    # Check whether this resume uses bullets for education entries
    bullet_lines = [
        line
        for line in lines
        if line.startswith("•")
    ]

    if bullet_lines:
        # If bullets exist, treat them as the education entries
        for line in bullet_lines:
            entry = parse_education_line(line)

            if entry:
                education_entries.append(entry)

        return education_entries

    # Fallback for resumes that do not use bullets
    skip_coursework_continuation = False

    for line in lines:

        if line.lower().startswith("relevant coursework"):
            skip_coursework_continuation = True
            continue

        # Ignore likely coursework continuation lines
        if skip_coursework_continuation:
            if extract_date_range(line):
                skip_coursework_continuation = False
            else:
                continue

        entry = parse_education_line(line)

        if entry:
            education_entries.append(entry)

    return education_entries