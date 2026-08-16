from src.resume_parser import ResumeParser
from src.exporter import (
    save_to_json,
    save_to_csv,
)


resume_path = (
    "data/resumes/Hetvi_Gandhi_Resume.pdf"
)


parser = ResumeParser()

result = parser.parse(resume_path)


json_output = (
    "output/Hetvi_Gandhi_Resume.json"
)

csv_output = (
    "output/parsed_resumes.csv"
)


save_to_json(
    result,
    json_output,
)

save_to_csv(
    result,
    csv_output,
)


print("Export complete.")
print(f"JSON saved to: {json_output}")
print(f"CSV saved to: {csv_output}")