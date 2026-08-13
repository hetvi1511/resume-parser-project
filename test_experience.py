from src.text_extractor import extract_text
from src.text_cleaner import clean_text
from src.section_parser import parse_sections
from src.experience_extractor import extract_work_experience


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


raw_text = extract_text(resume_path)

cleaned_text = clean_text(raw_text)

sections = parse_sections(cleaned_text)


experience_section = sections.get(
    "work_experience",
    "",
)


experiences = extract_work_experience(
    experience_section
)


print("WORK EXPERIENCE SECTION")
print("=" * 70)
print(experience_section)


print("\nEXTRACTED WORK EXPERIENCE")
print("=" * 70)


for number, experience in enumerate(
    experiences,
    start=1,
):

    print(f"\nEXPERIENCE {number}")

    print(
        f"Job Title: {experience['job_title']}"
    )

    print(
        f"Company: {experience['company']}"
    )

    print(
        f"Location: {experience['location']}"
    )

    print(
        f"Dates: {experience['dates']}"
    )

    print("Description:")

    for bullet in experience["description"]:
        print(f"  - {bullet}")

sample_experience = """
Machine Learning Intern | ABC Technologies (Dubai, UAE)
June 2025 - August 2025
• Built machine learning models using Python and scikit-learn
• Improved classification accuracy by 15%

Software Engineer Intern | XYZ Solutions (Abu Dhabi, UAE)
January 2024 - May 2024
• Developed REST APIs using FastAPI
• Worked with PostgreSQL and Docker
"""


sample_results = extract_work_experience(
    sample_experience
)


print("\n\nSAMPLE EXPERIENCE TEST")
print("=" * 70)


for number, experience in enumerate(
    sample_results,
    start=1,
):

    print(f"\nEXPERIENCE {number}")

    print(
        f"Job Title: {experience['job_title']}"
    )

    print(
        f"Company: {experience['company']}"
    )

    print(
        f"Location: {experience['location']}"
    )

    print(
        f"Dates: {experience['dates']}"
    )

    print("Description:")

    for bullet in experience["description"]:
        print(f"  - {bullet}")