import json
import tempfile
from pathlib import Path

import streamlit as st

from src.resume_parser import ResumeParser


st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="wide",
)


st.title("AI Resume Parser")
st.write(
    "Upload a resume and automatically extract "
    "contact information, skills, education, and work experience."
)


uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"],
)


if uploaded_file is not None:

    file_extension = Path(uploaded_file.name).suffix

    # Create a temporary file because ResumeParser
    # currently expects a file path
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension,
    ) as temp_file:

        temp_file.write(uploaded_file.getbuffer())

        temp_path = temp_file.name

    parser = ResumeParser()

    try:

        result = parser.parse(temp_path)

        st.success("Resume parsed successfully!")

        # -------------------------
        # Candidate Information
        # -------------------------

        st.header("Candidate Information")

        st.subheader(result.get("name", "Name not found"))

        contact = result.get("contact", {})

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Email:** "
                f"{contact.get('email') or 'Not found'}"
            )

            st.write(
                f"**Phone:** "
                f"{contact.get('phone') or 'Not found'}"
            )

            st.write(
                f"**Location:** "
                f"{contact.get('location') or 'Not found'}"
            )

        with col2:
            st.write(
                f"**LinkedIn:** "
                f"{contact.get('linkedin') or 'Not found'}"
            )

            st.write(
                f"**GitHub:** "
                f"{contact.get('github') or 'Not found'}"
            )

            st.write(
                f"**Portfolio:** "
                f"{contact.get('portfolio') or 'Not found'}"
            )

        # -------------------------
        # Skills
        # -------------------------

        st.header("Skills")

        skills = result.get("skills", [])

        if skills:

            st.write(", ".join(skills))

        else:

            st.write("No skills detected.")

        # -------------------------
        # Education
        # -------------------------

        st.header("Education")

        education = result.get("education", [])

        if education:

            for entry in education:

                st.subheader(
                    entry.get("degree")
                    or "Education"
                )

                st.write(
                    f"**Institution:** "
                    f"{entry.get('institution') or 'Not found'}"
                )

                st.write(
                    f"**Dates:** "
                    f"{entry.get('dates') or 'Not found'}"
                )

                st.divider()

        else:

            st.write("No education detected.")

        # -------------------------
        # Work Experience
        # -------------------------

        st.header("Work Experience")

        experiences = result.get(
            "work_experience",
            [],
        )

        if experiences:

            for experience in experiences:

                st.subheader(
                    experience.get("job_title")
                    or "Work Experience"
                )

                st.write(
                    f"**Company:** "
                    f"{experience.get('company') or 'Not found'}"
                )

                st.write(
                    f"**Location:** "
                    f"{experience.get('location') or 'Not found'}"
                )

                st.write(
                    f"**Dates:** "
                    f"{experience.get('dates') or 'Not found'}"
                )

                descriptions = experience.get(
                    "description",
                    [],
                )

                if descriptions:

                    st.write("**Responsibilities:**")

                    for description in descriptions:

                        st.write(
                            f"- {description}"
                        )

                st.divider()

        else:

            st.write("No work experience detected.")

        # -------------------------
        # Full JSON
        # -------------------------

        with st.expander(
            "View Full Parsed JSON"
        ):

            st.json(
                result,
                expanded=False,
            )

        # -------------------------
        # Download JSON
        # -------------------------

        json_data = json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        )

        st.download_button(
            label="Download Parsed Resume as JSON",
            data=json_data,
            file_name="parsed_resume.json",
            mime="application/json",
        )

    except Exception as error:

        st.error(
            f"Could not parse resume: {error}"
        )