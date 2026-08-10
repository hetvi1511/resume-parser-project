from src.text_extractor import extract_text


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"

text = extract_text(resume_path)

print("Extracted resume text:")
print("----------------------")
print(text)