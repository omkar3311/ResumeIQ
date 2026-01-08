import streamlit as st
from service import extract_text,section_map,count_projects, section_maker, has_email, has_phone, graduation_year, has_experience

def ats_score(resume_text, sections):
    feedback = []
    score = 0

    if not sections or len(sections.keys()) == 0:
        return 0, [
            "No resume sections detected. Please structure your resume with clear headings like Skills, Projects, Education, and Experience."
        ]

    if has_email(resume_text):
        score += 5
    else:
        feedback.append("Add a professional email address.")

    if has_phone(resume_text):
        score += 5
    else:
        feedback.append("Add a valid mobile number.")

    if sections.get("skills"):
        score += 20
    else:
        feedback.append("Skills section is missing.")

    if sections.get("projects"):
        score += 15
        project_count = count_projects(sections["projects"])

        if project_count >= 3:
            score += 10
        elif project_count == 2:
            score += 7
        elif project_count == 1:
            score += 4
        else:
            score += 5
    else:
        feedback.append("Projects section not found.")

    if graduation_year(resume_text):
        score += 15
    else:
        feedback.append("Mention your graduation year clearly.")

    if sections.get("experience"):
        score += 15
        if has_experience(resume_text):
            score += 8
    else:
        score += 5
        feedback.append("No experience section found.")

    if sections.get("objective"):
        score += 5

    structure_feedback, detected_sections, missing_sections = evaluate_resume_structure(sections)
    feedback.extend(structure_feedback)

    return min(score, 100), feedback


def evaluate_resume_structure(sections):
    feedback = []

    expected_sections = ["skills", "projects", "education", "experience", "objective"]
    detected_sections = list(sections.keys())
    missing_sections = [s for s in expected_sections if s not in detected_sections]

    if len(missing_sections) >= 3:
        feedback.append(
            "Resume structure is very weak. Missing multiple essential sections: "
            + ", ".join(missing_sections)
        )
    elif missing_sections:
        feedback.append(
            "Resume structure can be improved. Missing sections: "
            + ", ".join(missing_sections)
        )

    return feedback, detected_sections, missing_sections


st.title("📄 ATS Resume Checker (Rule-Based)")
st.caption(
    "Note: This ATS analysis is based on automated parsing. In some cases, well-formatted information "
    "may not be detected due to layout, styling, or section naming differences."
)
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
if resume_file :
    resume_text = extract_text(resume_file)

    if st.button("Check ATS Score"):
        sections = section_maker(resume_text, section_map)
        project_lines = sections.get("projects", [])
        project_count = count_projects(project_lines)
    
        
        final_score, feedback = ats_score(resume_text,sections)

        st.subheader("📊 ATS Score")
        st.metric("Final ATS Score", f"{final_score} / 100")

        if final_score >= 80:
            st.success("Excellent ATS-ready resume")
        elif final_score >= 60:
            st.warning("Good resume, but needs improvements")
        else:
            st.error("Resume needs major improvements")
        st.write("Present Sections")
        st.write(sections.keys())
        if feedback:
            st.subheader("🛠 Improvement Suggestions")
            for f in feedback:
                st.write("•", f)
            st.warning(
        "If the above-mentioned sections are present in your resume but still flagged as missing, "
        "this indicates a formatting or structuring issue that may prevent ATS systems from correctly reading your content.")
        else:
            st.success("No major issues detected. Your resume is ATS-friendly.")
