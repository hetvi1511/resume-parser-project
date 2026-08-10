from src.text_extractor import extract_text
from src.text_cleaner import clean_text


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


raw_text = extract_text(resume_path)

cleaned_text = clean_text(raw_text)


print("CLEANED RESUME TEXT")
print("=" * 60)
print(cleaned_text)