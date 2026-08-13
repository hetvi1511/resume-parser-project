import re

import spacy


nlp = spacy.load("en_core_web_sm")


MONTHS = (
    "January|February|March|April|May|June|July|August|"
    "September|October|November|December"
)


def is_date_line(line: str) -> bool:
    """
    Check whether a line looks like an employment date range.

    Examples:
    October 2023 - Present
    June 2025 - August 2025
    """

    pattern = (
        rf"^(?:{MONTHS})\s+\d{{4}}\s*-\s*"
        rf"(?:Present|Current|(?:{MONTHS})\s+\d{{4}})$"
    )

    return bool(
        re.match(
            pattern,
            line.strip(),
            re.IGNORECASE,
        )
    )


def clean_description_line(line: str) -> str:
    """
    Remove bullet markers and extra spaces
    from a work experience description.
    """

    line = line.strip()

    if line.startswith("•"):
        line = line[1:].strip()

    return line


def extract_location(text: str) -> tuple[str, str | None]:
    """
    Extract a trailing location written inside parentheses.

    Example:
    Petrofac International Ltd. (Sharjah, U.A.E)

    Returns:
    ("Petrofac International Ltd.", "Sharjah, U.A.E")
    """

    pattern = r"\s*\(([^()]*)\)\s*$"

    match = re.search(pattern, text)

    if not match:
        return text.strip(), None

    location = match.group(1).strip()

    remaining_text = text[:match.start()].strip()

    return remaining_text, location


def extract_company_with_spacy(text: str) -> str | None:
    """
    Use spaCy as a fallback to find an organization.
    """

    doc = nlp(text)

    for entity in doc.ents:

        if entity.label_ == "ORG":
            return entity.text.strip()

    return None


def parse_title_company_line(line: str) -> dict:
    """
    Parse a job heading into job title, company, and location.

    Preferred format:
    Job Title | Company Name (Location)
    """

    line = line.strip()

    job_title = None
    company = None
    location = None

    if "|" in line:

        left, right = line.split("|", 1)

        job_title = left.strip()

        company_text, location = extract_location(
            right.strip()
        )

        company = company_text.strip()

    else:
        # Fallback for resumes without the | separator
        company = extract_company_with_spacy(line)

        if company:
            job_title = line.replace(
                company,
                "",
                1,
            ).strip(" ,-")

        else:
            job_title = line

    return {
        "job_title": job_title,
        "company": company,
        "location": location,
    }


def extract_work_experience(
    experience_text: str,
) -> list[dict]:
    """
    Extract structured work experience entries.

    Expected general structure:

    Job Title | Company (Location)
    Date Range
    • Description
    • Description

    Job Title | Company (Location)
    Date Range
    • Description
    """

    if not experience_text:
        return []

    lines = [
        line.strip()
        for line in experience_text.splitlines()
        if line.strip()
    ]

    experiences = []

    current_entry = None

    for line in lines:

        # -------------------------
        # Date line
        # -------------------------

        if is_date_line(line):

            if current_entry is not None:
                current_entry["dates"] = line

            continue

        # -------------------------
        # Bullet description
        # -------------------------

        if line.startswith("•"):

            if current_entry is not None:

                description = clean_description_line(
                    line
                )

                current_entry[
                    "description"
                ].append(description)

            continue

        # -------------------------
        # New job heading
        # -------------------------

        # Save previous entry first
        if current_entry is not None:
            experiences.append(current_entry)

        heading = parse_title_company_line(line)

        current_entry = {
            "job_title": heading["job_title"],
            "company": heading["company"],
            "location": heading["location"],
            "dates": None,
            "description": [],
        }

    # Save final entry
    if current_entry is not None:
        experiences.append(current_entry)

    return experiences