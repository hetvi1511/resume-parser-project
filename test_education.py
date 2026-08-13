from src.text_extractor import extract_text
from src.text_cleaner import clean_text
from src.section_parser import parse_sections
from src.education_extractor import extract_education


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


raw_text = extract_text(resume_path)

cleaned_text = clean_text(raw_text)

sections = parse_sections(cleaned_text)


education_section = sections.get("education", "")


education_entries = extract_education(education_section)


print("EDUCATION SECTION")
print("=" * 60)
print(education_section)

print("\nEXTRACTED EDUCATION")
print("=" * 60)

for entry in education_entries:
    print(entry)

sample_education = """
Bachelor of Engineering in Computer Science, University of Dubai - May 2025
Master of Science in Artificial Intelligence, Khalifa University - June 2027 (Expected)
"""


sample_entries = extract_education(sample_education)


print("\nSAMPLE EDUCATION TEST")
print("=" * 60)

for entry in sample_entries:
    print(entry)