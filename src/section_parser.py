SECTION_ALIASES = {
    "objective": {
        "objective",
        "summary",
        "professional summary",
        "career objective",
        "profile",
        "about me",
    },
    "education": {
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
    },
    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "competencies",
        "technical competencies",
    },
    "work_experience": {
        "work experience",
        "professional experience",
        "employment history",
        "experience",
        "employment experience",
    },
    "projects": {
        "projects",
        "academic projects",
        "personal projects",
        "technical projects",
    },
    "awards": {
        "awards",
        "achievements",
        "awards and achievements",
        "honors",
        "honours",
    },
    "certifications": {
        "certifications",
        "certificates",
        "licenses and certifications",
    },
    "positions_of_responsibility": {
        "positions of responsibility",
        "leadership",
        "leadership experience",
        "activities",
        "extracurricular activities",
    },
}


def normalize_heading(line: str) -> str:
    """
    Normalize possible section headings.

    Handles headings such as:
    WORK EXPERIENCE
    Work Experience
    ProfessionalExperience
    """
    line = line.strip().lower().rstrip(":")

    # Remove spaces, underscores, and hyphens so that
    # "Professional Experience" and "ProfessionalExperience"
    # are treated the same.
    line = line.replace(" ", "")
    line = line.replace("_", "")
    line = line.replace("-", "")

    return line


def detect_section(line: str) -> str | None:
    """
    Detect known resume section headings.
    """

    normalized = normalize_heading(line)

    for section_name, aliases in SECTION_ALIASES.items():

        normalized_aliases = {
            normalize_heading(alias)
            for alias in aliases
        }

        if normalized in normalized_aliases:
            return section_name

    return None


def parse_sections(text: str) -> dict[str, str]:
    """
    Split cleaned resume text into logical sections.

    Text that appears before the first recognized heading
    is stored in the 'header' section.
    """

    sections = {}
    current_section = "header"

    sections[current_section] = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        detected_section = detect_section(line)

        if detected_section:
            current_section = detected_section

            if current_section not in sections:
                sections[current_section] = []

            continue

        sections[current_section].append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
        if content
    }