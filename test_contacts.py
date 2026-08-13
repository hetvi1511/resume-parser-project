from src.text_extractor import extract_text
from src.text_cleaner import clean_text
from src.section_parser import parse_sections
from src.contact_extractor import extract_contact_info


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


raw_text = extract_text(resume_path)

cleaned_text = clean_text(raw_text)

sections = parse_sections(cleaned_text)


header = sections.get("header", "")


contact_info = extract_contact_info(header)


print("RESUME HEADER")
print("=" * 60)
print(header)

print("\nEXTRACTED CONTACT INFORMATION")
print("=" * 60)

for field, value in contact_info.items():
    print(f"{field}: {value}")

sample_header = """
Jane Doe
Dubai, UAE
Phone: +971 50 123 4567
Email: jane.doe@email.com
LinkedIn: linkedin.com/in/janedoe
GitHub: github.com/janedoe
Portfolio: janedoe.dev
"""


sample_contact_info = extract_contact_info(sample_header)


print("\nSAMPLE CONTACT TEST")
print("=" * 60)

for field, value in sample_contact_info.items():
    print(f"{field}: {value}")