import re


def clean_text(text: str) -> str:
    """
    Clean and normalize text extracted from a resume.

    This function:
    - Normalizes common Unicode characters
    - Removes unnecessary extra spaces
    - Preserves section headings and resume structure
    - Joins obvious PDF line-wrap breaks
    - Avoids incorrectly merging separate resume entries
    """

    if not text:
        return ""

    # Normalize common Unicode characters
    text = text.replace("\u00a0", " ")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("’", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')

    # Split extracted text into individual lines
    raw_lines = text.splitlines()

    cleaned_lines = []

    for line in raw_lines:
        # Replace multiple spaces/tabs with a single space
        line = re.sub(r"[ \t]+", " ", line).strip()

        # Ignore empty lines for now
        if line:
            cleaned_lines.append(line)

    merged_lines = []

    for line in cleaned_lines:

        # First line is always added directly
        if not merged_lines:
            merged_lines.append(line)
            continue

        previous = merged_lines[-1]

        # Detect section headings such as:
        # EDUCATION
        # SKILLS
        # WORK EXPERIENCE
        is_section_heading = (
            line.isupper()
            and len(line.split()) <= 6
            and not line.startswith("•")
        )

        previous_is_heading = (
            previous.isupper()
            and len(previous.split()) <= 6
            and not previous.startswith("•")
        )

        # Detect new bullet points
        starts_new_bullet = line.startswith("•")

        # Detect lines that look like dates
        looks_like_date = bool(
            re.search(
                r"\b("
                r"January|February|March|April|May|June|July|August|"
                r"September|October|November|December"
                r")\s+\d{4}",
                line,
                re.IGNORECASE,
            )
        )

        # Detect common contact-detail lines
        looks_like_contact = bool(
            re.match(
                r"^(Mobile|Phone|Email|Email ID|LinkedIn|GitHub|"
                r"Website|Portfolio)\b",
                line,
                re.IGNORECASE,
            )
        )

        # PDF continuation lines usually begin with lowercase text.
        #
        # Example:
        #
        # • ... ensuring accuracy and
        # compliance with HIPAA standards
        #
        # The second line begins with "compliance",
        # so it should be joined to the bullet.
        starts_with_lowercase = (
            len(line) > 0
            and line[0].islower()
        )

        # Only merge when:
        # 1. The previous line is a bullet
        # 2. The current line starts with lowercase
        # 3. The current line is not a new section/date/contact line
        should_merge = (
            previous.startswith("•")
            and starts_with_lowercase
            and not starts_new_bullet
            and not is_section_heading
            and not previous_is_heading
            and not looks_like_date
            and not looks_like_contact
        )

        if should_merge:
            merged_lines[-1] = previous + " " + line
        else:
            merged_lines.append(line)

    return "\n".join(merged_lines)