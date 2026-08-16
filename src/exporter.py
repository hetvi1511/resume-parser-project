import json
from pathlib import Path

import pandas as pd


def save_to_json(
    data: dict,
    output_path: str,
) -> None:
    """
    Save parsed resume data to a JSON file.
    """

    path = Path(output_path)

    # Make sure the output directory exists
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def flatten_resume_for_csv(
    data: dict,
) -> dict:
    """
    Convert nested parsed resume data into a flat dictionary
    suitable for storing in a CSV row.
    """

    contact = data.get("contact", {})

    education = data.get("education", [])

    work_experience = data.get(
        "work_experience",
        [],
    )

    skills = data.get("skills", [])

    # -------------------------
    # Education
    # -------------------------

    education_text = []

    for entry in education:
        parts = [
            entry.get("degree"),
            entry.get("institution"),
            entry.get("dates"),
        ]

        parts = [
            part
            for part in parts
            if part
        ]

        education_text.append(
            " | ".join(parts)
        )

    # -------------------------
    # Work experience
    # -------------------------

    experience_text = []

    for entry in work_experience:
        parts = [
            entry.get("job_title"),
            entry.get("company"),
            entry.get("location"),
            entry.get("dates"),
        ]

        parts = [
            part
            for part in parts
            if part
        ]

        experience_text.append(
            " | ".join(parts)
        )

    # -------------------------
    # Flat result
    # -------------------------

    return {
        "name": data.get("name"),
        "email": contact.get("email"),
        "phone": contact.get("phone"),
        "location": contact.get("location"),
        "linkedin": contact.get("linkedin"),
        "github": contact.get("github"),
        "portfolio": contact.get("portfolio"),
        "skills": ", ".join(skills),
        "education": " || ".join(
            education_text
        ),
        "work_experience": " || ".join(
            experience_text
        ),
    }


def save_to_csv(
    data: dict | list[dict],
    output_path: str,
) -> None:
    """
    Save one or more parsed resumes to a CSV file.
    """

    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Allow either one resume dictionary
    # or a list of resume dictionaries
    if isinstance(data, dict):
        data = [data]

    rows = [
        flatten_resume_for_csv(resume)
        for resume in data
    ]

    dataframe = pd.DataFrame(rows)

    dataframe.to_csv(
        path,
        index=False,
    )