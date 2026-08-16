from src.text_extractor import extract_text
from src.text_cleaner import clean_text
from src.section_parser import parse_sections
from src.contact_extractor import extract_contact_info
from src.name_extractor import extract_name
from src.skills_extractor import extract_skills
from src.education_extractor import extract_education
from src.experience_extractor import extract_work_experience


class ResumeParser:
    """
    Main resume parser that combines all extraction modules.

    The parser:
    1. Extracts raw text from a resume
    2. Cleans the text
    3. Detects resume sections
    4. Extracts structured candidate information
    """

    def parse(self, file_path: str) -> dict:
        """
        Parse a resume file and return structured candidate data.
        """

        # Step 1: Extract raw text
        raw_text = extract_text(file_path)

        # Step 2: Clean the text
        cleaned_text = clean_text(raw_text)

        # Step 3: Split resume into sections
        sections = parse_sections(cleaned_text)

        # Get important sections
        header = sections.get("header", "")
        skills_section = sections.get("skills", "")
        education_section = sections.get("education", "")
        experience_section = sections.get("work_experience", "")

        # Step 4: Extract candidate name
        name = extract_name(header)

        # Step 5: Extract contact information
        contact = extract_contact_info(header)

        # Step 6: Extract skills
        skills = extract_skills(skills_section)

        # Step 7: Extract education
        education = extract_education(education_section)

        # Step 8: Extract work experience
        work_experience = extract_work_experience(
            experience_section
        )

        # Final structured result
        result = {
            "name": name,
            "contact": contact,
            "skills": skills,
            "education": education,
            "work_experience": work_experience,
            "sections": sections,
        }

        return result