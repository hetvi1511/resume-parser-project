import re


def extract_email(text: str) -> str | None:
    """
    Extract the first email address found in the text.
    """

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text: str) -> str | None:
    """
    Extract the first phone number found in the text.

    Supports common international and US-style formats.
    """

    pattern = (
        r"(?<!\d)"
        r"(?:\+\d{1,3}[\s.-]?)?"
        r"(?:\(\d{2,4}\)|\d{2,4})"
        r"[\s.-]?"
        r"\d{3,4}"
        r"[\s.-]?"
        r"\d{4}"
        r"(?!\d)"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0).strip()

    return None


def extract_linkedin(text: str) -> str | None:
    """
    Extract a LinkedIn URL if present.
    """

    pattern = r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(0)

    return None


def extract_github(text: str) -> str | None:
    """
    Extract a GitHub profile URL if present.
    """

    pattern = r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_-]+/?"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(0)

    return None


def extract_portfolio(text: str) -> str | None:
    """
    Extract a possible personal portfolio URL.

    Excludes LinkedIn and GitHub URLs.
    """

    url_pattern = r"(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[^\s]*)?"

    matches = re.findall(url_pattern, text, re.IGNORECASE)

    for url in matches:
        lower_url = url.lower()

        if "linkedin.com" in lower_url:
            continue

        if "github.com" in lower_url:
            continue

        # Prevent email domains such as gmail.com from being
        # incorrectly treated as portfolio websites
        if "gmail.com" in lower_url:
            continue

        if "outlook.com" in lower_url:
            continue

        if "yahoo.com" in lower_url:
            continue

        return url

    return None


def extract_location(header_text: str) -> str | None:
    """
    Estimate the candidate's location from the resume header.

    We assume the location is usually one of the first few lines
    and appears before phone/email/contact information.
    """

    lines = [
        line.strip()
        for line in header_text.splitlines()
        if line.strip()
    ]

    if len(lines) < 2:
        return None

    # Skip first line because it is usually the candidate's name
    for line in lines[1:]:

        lower_line = line.lower()

        # Ignore lines containing contact details
        if "@" in line:
            continue

        if "mobile" in lower_line:
            continue

        if "phone" in lower_line:
            continue

        if "email" in lower_line:
            continue

        if "linkedin" in lower_line:
            continue

        if "github" in lower_line:
            continue

        if "http://" in lower_line or "https://" in lower_line:
            continue

        return line

    return None


def extract_contact_info(header_text: str) -> dict:
    """
    Extract structured contact information from a resume header.
    """

    return {
        "email": extract_email(header_text),
        "phone": extract_phone(header_text),
        "linkedin": extract_linkedin(header_text),
        "github": extract_github(header_text),
        "portfolio": extract_portfolio(header_text),
        "location": extract_location(header_text),
    }