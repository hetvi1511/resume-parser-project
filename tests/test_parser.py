from src.contact_extractor import (
    extract_email,
    extract_phone,
)

from src.name_extractor import extract_name
from src.skills_extractor import extract_skills
from src.education_extractor import extract_education
from src.experience_extractor import (
    extract_work_experience,
)


def test_email_extraction():

    text = (
        "Jane Doe\n"
        "jane.doe@example.com"
    )

    assert (
        extract_email(text)
        == "jane.doe@example.com"
    )


def test_phone_extraction():

    text = "Phone: +971 50 123 4567"

    assert (
        extract_phone(text)
        == "+971 50 123 4567"
    )


def test_name_extraction():

    header = """
Jane Doe
Dubai, UAE
Phone: +971 50 123 4567
"""

    assert extract_name(header) == "Jane Doe"


def test_skills_extraction():

    text = """
Python, React, PostgreSQL, Docker
"""

    skills = extract_skills(text)

    assert "Python" in skills
    assert "React" in skills
    assert "PostgreSQL" in skills
    assert "Docker" in skills


def test_education_extraction():

    text = """
Bachelor of Science in Computer Science, University of Dubai - May 2025
"""

    result = extract_education(text)

    assert len(result) == 1

    assert (
        result[0]["degree"]
        == "Bachelor of Science in Computer Science"
    )

    assert (
        result[0]["institution"]
        == "University of Dubai"
    )


def test_experience_extraction():

    text = """
Software Engineer Intern | ABC Technologies (Dubai, UAE)
June 2025 - August 2025
• Developed REST APIs using FastAPI
"""

    result = extract_work_experience(text)

    assert len(result) == 1

    assert (
        result[0]["job_title"]
        == "Software Engineer Intern"
    )

    assert (
        result[0]["company"]
        == "ABC Technologies"
    )

    assert (
        result[0]["location"]
        == "Dubai, UAE"
    )