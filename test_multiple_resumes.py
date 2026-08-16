from pathlib import Path
from pprint import pprint

from src.resume_parser import ResumeParser


parser = ResumeParser()

resume_folder = Path("data/resumes")


for resume_path in resume_folder.iterdir():

    if resume_path.suffix.lower() not in {
        ".pdf",
        ".docx",
        ".txt",
    }:
        continue

    print("\n" + "=" * 80)
    print(f"TESTING: {resume_path.name}")
    print("=" * 80)

    try:

        result = parser.parse(str(resume_path))

        pprint(
            result,
            sort_dicts=False,
        )

    except Exception as error:

        print(
            f"ERROR: {error}"
        )