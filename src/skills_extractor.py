import csv
from pathlib import Path

import spacy
from spacy.matcher import PhraseMatcher


nlp = spacy.load("en_core_web_sm")


def load_skills(skill_file: str = "data/skills.csv") -> list[str]:
    """
    Load skills from a CSV file.

    The CSV must contain a column named 'skill'.
    """

    path = Path(skill_file)

    if not path.exists():
        raise FileNotFoundError(f"Skills file not found: {skill_file}")

    skills = []

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            skill = row.get("skill", "").strip()

            if skill:
                skills.append(skill)

    return skills


def build_skill_matcher(skills: list[str]) -> PhraseMatcher:
    """
    Build a spaCy PhraseMatcher from a list of skills.

    Matching is case-insensitive using LOWER.
    """

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    patterns = [nlp.make_doc(skill) for skill in skills]

    matcher.add("SKILLS", patterns)

    return matcher


def normalize_skill(skill: str) -> str:
    """
    Normalize common aliases to a consistent skill name.
    """

    aliases = {
        "c programming": "C",
        "node js": "Node.js",
        "node.js": "Node.js",
        "postgres": "PostgreSQL",
        "rest api": "REST APIs",
        "rest apis": "REST APIs",
    }

    normalized = skill.strip()

    alias = aliases.get(normalized.lower())

    if alias:
        return alias

    return normalized


def extract_skills(
    text: str,
    skill_file: str = "data/skills.csv",
) -> list[str]:
    """
    Extract known technical skills from resume text
    using spaCy PhraseMatcher.
    """

    if not text:
        return []

    skills = load_skills(skill_file)

    matcher = build_skill_matcher(skills)

    doc = nlp(text)

    matches = matcher(doc)

    extracted_skills = []

    for _, start, end in matches:
        matched_text = doc[start:end].text

        skill = normalize_skill(matched_text)

        if skill not in extracted_skills:
            extracted_skills.append(skill)

    return extracted_skills