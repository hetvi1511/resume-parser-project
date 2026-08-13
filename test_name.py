from src.text_extractor import extract_text
from src.text_cleaner import clean_text
from src.section_parser import parse_sections
from src.name_extractor import extract_name


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


raw_text = extract_text(resume_path)

cleaned_text = clean_text(raw_text)

sections = parse_sections(cleaned_text)


header = sections.get("header", "")

name = extract_name(header)


print("RESUME HEADER")
print("=" * 60)
print(header)

print("\nEXTRACTED NAME")
print("=" * 60)
print(name)

sample_header = """
Jane Doe
Dubai, UAE
Phone: +971 50 123 4567
Email: jane.doe@email.com
"""


sample_name = extract_name(sample_header)


print("\nSAMPLE NAME TEST")
print("=" * 60)
print(sample_name)
