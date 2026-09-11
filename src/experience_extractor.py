import re

import spacy


nlp = spacy.load("en_core_web_sm")


MONTHS = (
    "January|February|March|April|May|June|July|August|"
    "September|October|November|December|"
    "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
)


JOB_KEYWORDS = {
    "intern",
    "engineer",
    "developer",
    "analyst",
    "manager",
    "assistant",
    "associate",
    "researcher",
    "consultant",
    "scientist",
    "specialist",
    "coordinator",
    "technician",
    "volunteer",
    "research assistant",
    "designer",
    "administrator",
    "supervisor",
    "journeyman",
}


def normalize_spacing(text: str) -> str:
    """
    Repair common PDF extraction spacing problems.
    """

    text = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        text,
    )

    text = text.replace("My SQL", "MySQL")
    text = text.replace("Postgre SQL", "PostgreSQL")
    text = text.replace("Java Script", "JavaScript")
    text = text.replace("Type Script", "TypeScript")

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def extract_date_from_text(
    text: str,
) -> tuple[str, str | None]:
    """
    Extract an employment date/date range even when it
    occurs on the same line as the job title.

    Returns:
    (text_without_date, date)
    """

    text = normalize_spacing(text)

    range_pattern = (
        rf"({MONTHS})\s+\d{{4}}\s+"
        rf"(?:-|to)\s+"
        rf"(?:Present|Current|"
        rf"({MONTHS})\s+\d{{4}})"
    )

    match = re.search(
        range_pattern,
        text,
        re.IGNORECASE,
    )

    if match:

        date_text = match.group(0)

        remaining = (
            text[:match.start()]
            + text[match.end():]
        ).strip()

        return remaining, date_text

    return text, None


def is_date_line(line: str) -> bool:
    """
    Check whether the full line is a date range.
    """

    cleaned, date = extract_date_from_text(line)

    return bool(
        date and not cleaned.strip()
    )


def clean_description_line(line: str) -> str:
    """
    Remove bullet markers and normalize spacing.
    """

    line = line.strip()

    line = re.sub(
        r"^[•●▪◦\-]\s*",
        "",
        line,
    )

    return normalize_spacing(line)


def extract_location(
    text: str,
) -> tuple[str, str | None]:
    """
    Extract a trailing parenthesized location.

    Examples:
    ABC Technologies (Dubai, UAE)
    Petrofac International Ltd. (Sharjah, U.A.E)

    Parenthetical descriptions such as
    "(in partnership with VISAMO Kids)"
    are preserved as part of the company name.
    """

    pattern = r"\s*\(([^()]*)\)\s*$"

    match = re.search(pattern, text)

    if not match:
        return text.strip(), None

    possible_location = match.group(1).strip()

    lower_location = possible_location.lower()

    # These phrases indicate descriptive text,
    # not a geographic location.
    non_location_phrases = {
        "in partnership",
        "partnered with",
        "formerly",
        "a division of",
        "subsidiary",
    }

    if any(
        phrase in lower_location
        for phrase in non_location_phrases
    ):
        return text.strip(), None

    # A location usually contains a comma:
    # Dubai, UAE
    # San Diego, USA
    # Sharjah, U.A.E
    if "," in possible_location:

        company = text[:match.start()].strip()

        return company, possible_location

    return text.strip(), None


def looks_like_job_heading(line: str) -> bool:
    """
    Determine whether a line looks like the start
    of a new work experience entry.
    """

    line = normalize_spacing(line)

    if not line:
        return False

    # Strongest signal from many resumes
    if "|" in line:
        return True

    # Remove attached date before judging title text
    title_part, _ = extract_date_from_text(line)

    lower = title_part.lower()

    # Avoid treating long description sentences as job titles
    if len(title_part.split()) > 14:
        return False

    # Sentences ending with punctuation are less likely headings
    if title_part.endswith((".", ";")):
        return False

    return any(
        keyword in lower
        for keyword in JOB_KEYWORDS
    )


def extract_company_with_spacy(
    text: str,
) -> str | None:
    """
    Find an organization using spaCy as a fallback.
    """

    doc = nlp(text)

    for entity in doc.ents:

        if entity.label_ == "ORG":
            return entity.text.strip()

    return None


def parse_title_company_line(
    line: str,
) -> dict:
    """
    Parse common experience-heading formats.

    Supported examples:

    Software Engineer Intern | ABC Technologies (Dubai, UAE)

    Intern, UMMEED Child Development Center

    Volunteer, Functional Neuroscience Lab at UCSD Health
    """

    line = normalize_spacing(line)

    line_without_date, inline_date = (
        extract_date_from_text(line)
    )

    job_title = None
    company = None
    location = None

    # --------------------------------
    # Format 1: Title | Company
    # --------------------------------

    if "|" in line_without_date:

        left, right = line_without_date.split(
            "|",
            1,
        )

        job_title = left.strip()

        company, location = extract_location(
            right.strip()
        )

    # --------------------------------
    # Format 2: Title, Company
    # --------------------------------

    elif "," in line_without_date:

        first, rest = line_without_date.split(
            ",",
            1,
        )

        # Only use this strategy if first part looks like a job title
        if any(
            keyword in first.lower()
            for keyword in JOB_KEYWORDS
        ):

            job_title = first.strip()

            company, location = extract_location(
                rest.strip()
            )

        else:
            job_title = line_without_date

    # --------------------------------
    # Format 3: Title only
    # --------------------------------

    else:

        job_title = line_without_date.strip()

    return {
        "job_title": job_title,
        "company": company,
        "location": location,
        "dates": inline_date,
    }


def looks_like_company_line(line: str) -> bool:
    """
    Identify a line that may contain company information
    immediately after a job heading.
    """

    lower = line.lower()

    indicators = [
        "company",
        "inc.",
        "inc ",
        "llc",
        "ltd",
        "corporation",
        "corp.",
        "technologies",
        "systems",
        "university",
        "college",
        "hospital",
        "center",
        "centre",
        "lab",
    ]

    return any(
        indicator in lower
        for indicator in indicators
    )

def looks_like_month_year(text: str) -> bool:
    """
    Detect date fragments such as:
    Oct 2016
    March 2024
    """

    pattern = (
        rf"^(?:{MONTHS})\s+\d{{4}}$"
    )

    return bool(
        re.match(
            pattern,
            text.strip(),
            re.IGNORECASE,
        )
    )

def extract_work_experience(
    experience_text: str,
) -> list[dict]:
    """
    Extract structured work experience from multiple
    common resume layouts.

    Handles:
    - Job Title | Company (Location)
    - Intern, Company Name
    - Job titles with dates on separate lines
    - Fragmented PDF date lines such as:
        Oct 2016
        to
        Current
    - Bullet descriptions
    - PDF-wrapped continuation lines
    """

    if not experience_text:
        return []

    lines = [
        normalize_spacing(line.strip())
        for line in experience_text.splitlines()
        if line.strip()
    ]

    experiences = []
    current_entry = None

    i = 0

    while i < len(lines):

        line = lines[i]

        # --------------------------------
        # Bullet description
        # --------------------------------

        if re.match(r"^[•●▪◦\-]", line):

            if current_entry is not None:

                current_entry["description"].append(
                    clean_description_line(line)
                )

            i += 1
            continue

        # --------------------------------
        # Fragmented date:
        #
        # Oct 2016
        # to
        # Current
        # --------------------------------

        if (
            current_entry is not None
            and looks_like_month_year(line)
            and i + 2 < len(lines)
            and lines[i + 1].lower() in {"to", "-"}
        ):

            end_value = lines[i + 2]

            if (
                end_value.lower() in {
                    "present",
                    "current",
                }
                or looks_like_month_year(end_value)
            ):

                current_entry["dates"] = (
                    f"{line} "
                    f"{lines[i + 1]} "
                    f"{end_value}"
                )

                i += 3
                continue

        # --------------------------------
        # Normal standalone date
        # --------------------------------

        if is_date_line(line):

            _, date = extract_date_from_text(line)

            if current_entry is not None:
                current_entry["dates"] = date

            i += 1
            continue

        # --------------------------------
        # New job heading
        # --------------------------------

        if looks_like_job_heading(line):

            if current_entry is not None:
                experiences.append(current_entry)

            heading = parse_title_company_line(line)

            current_entry = {
                "job_title": heading["job_title"],
                "company": heading["company"],
                "location": heading["location"],
                "dates": heading["dates"],
                "description": [],
            }

            i += 1
            continue

        # --------------------------------
        # Possible company placeholder /
        # separate company line
        # --------------------------------

        if (
            current_entry is not None
            and current_entry["company"] is None
            and not current_entry["description"]
        ):

            lower = line.lower()

            if (
                "company name" in lower
                or lower == "companyname"
            ):

                current_entry["company"] = "Company Name"

                # Try to consume fragmented location:
                #
                # City
                # ,
                # State

                if i + 4 < len(lines):

                    city = lines[i + 2]
                    comma = lines[i + 3]
                    state = lines[i + 4]

                    if comma == ",":
                        current_entry["location"] = (
                            f"{city}, {state}"
                        )

                        i += 5
                        continue

                i += 1
                continue

        # --------------------------------
        # Ordinary description /
        # continuation line
        # --------------------------------

        if current_entry is not None:

            if line not in {
                "ï¼",
                "ï¼​",
                ",",
            }:

                cleaned_line = clean_description_line(
                    line
                )

                # If previous description does not end
                # with punctuation, assume this is a PDF
                # line-wrap continuation.
                if (
                    current_entry["description"]
                    and not current_entry[
                        "description"
                    ][-1].endswith(
                        (
                            ".",
                            "!",
                            "?",
                            ";",
                            ":",
                        )
                    )
                ):

                    current_entry[
                        "description"
                    ][-1] += (
                        " " + cleaned_line
                    )

                else:

                    current_entry[
                        "description"
                    ].append(
                        cleaned_line
                    )

        i += 1

    # Save final experience
    if current_entry is not None:
        experiences.append(current_entry)

    return experiences