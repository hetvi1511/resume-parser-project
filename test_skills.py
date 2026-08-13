from src.text_extractor import extract_text
from src.text_cleaner import clean_text
from src.section_parser import parse_sections
from src.skills_extractor import extract_skills


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


raw_text = extract_text(resume_path)

cleaned_text = clean_text(raw_text)

sections = parse_sections(cleaned_text)


skills_section = sections.get("skills", "")


skills = extract_skills(skills_section)


print("SKILLS SECTION")
print("=" * 60)
print(skills_section)

print("\nEXTRACTED SKILLS")
print("=" * 60)

for skill in skills:
    print(f"- {skill}")

sample_text = """
Technical Skills:
Python, FastAPI, PostgreSQL, Docker, AWS,
PyTorch, Hugging Face, REST APIs
"""


sample_skills = extract_skills(sample_text)


print("\nSAMPLE SKILLS TEST")
print("=" * 60)

for skill in sample_skills:
    print(f"- {skill}")