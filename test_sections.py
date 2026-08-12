from src.text_extractor import extract_text
from src.text_cleaner import clean_text
from src.section_parser import parse_sections


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


raw_text = extract_text(resume_path)

cleaned_text = clean_text(raw_text)

sections = parse_sections(cleaned_text)


print("DETECTED RESUME SECTIONS")
print("=" * 60)

for section_name, content in sections.items():
    print(f"\n[{section_name.upper()}]")
    print("-" * 60)
    print(content)

sample_text = """
Jane Doe
jane@email.com

PROFESSIONAL SUMMARY
Software engineering student interested in AI.

ACADEMIC BACKGROUND
Bachelor of Science in Computer Science

TECHNICAL SKILLS
Python
SQL

PROFESSIONAL EXPERIENCE
Software Engineering Intern
"""

sample_sections = parse_sections(sample_text)

print("\n\nALIAS TEST")
print("=" * 60)

for section_name, content in sample_sections.items():
    print(f"\n[{section_name.upper()}]")
    print(content)