from pprint import pprint

from src.resume_parser import ResumeParser


resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"


parser = ResumeParser()

result = parser.parse(resume_path)


print("PARSED RESUME")
print("=" * 70)

pprint(result, sort_dicts=False)