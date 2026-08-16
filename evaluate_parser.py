from src.resume_parser import ResumeParser


parser = ResumeParser()

resume_path = "data/resumes/Hetvi_Gandhi_Resume.pdf"

result = parser.parse(resume_path)


expected = {
    "name": "HETVI GANDHI",
    "email": "hetvigandhi1511@gmail.com",
    "phone": "+1 (858) 214-7692",
    "location": "San Diego CA, USA",
    "skills": {
        "Python",
        "Java",
        "C",
        "SQL",
        "R",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "Git",
        "MySQL",
        "Windows",
        "Linux",
        "macOS",
    },
    "education_count": 2,
    "experience_count": 3,
}


checks = []


def check(field: str, actual, expected_value):
    passed = actual == expected_value

    checks.append(passed)

    status = "PASS" if passed else "FAIL"

    print(f"{status}: {field}")

    if not passed:
        print(f"  Expected: {expected_value}")
        print(f"  Actual:   {actual}")


check(
    "Name",
    result.get("name"),
    expected["name"],
)

check(
    "Email",
    result.get("contact", {}).get("email"),
    expected["email"],
)

check(
    "Phone",
    result.get("contact", {}).get("phone"),
    expected["phone"],
)

check(
    "Location",
    result.get("contact", {}).get("location"),
    expected["location"],
)

check(
    "Education count",
    len(result.get("education", [])),
    expected["education_count"],
)

check(
    "Experience count",
    len(result.get("work_experience", [])),
    expected["experience_count"],
)


actual_skills = set(result.get("skills", []))

missing_skills = expected["skills"] - actual_skills

extra_skills = actual_skills - expected["skills"]


skills_passed = len(missing_skills) == 0

checks.append(skills_passed)

print(
    f"{'PASS' if skills_passed else 'FAIL'}: Skills"
)

if missing_skills:
    print(
        "  Missing:",
        ", ".join(sorted(missing_skills)),
    )

if extra_skills:
    print(
        "  Extra:",
        ", ".join(sorted(extra_skills)),
    )


passed = sum(checks)

total = len(checks)

accuracy = (
    passed / total * 100
    if total
    else 0
)


print("\n" + "=" * 60)

print(
    f"Passed {passed}/{total} checks"
)

print(
    f"Field-level accuracy: {accuracy:.1f}%"
)