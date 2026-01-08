import streamlit as st
from service import extract_text,section_map,count_projects, section_maker, has_email, has_phone, graduation_year, has_experience, has_objective

def ats_score(resume_text, sections):
    feedback = []
    score = 0

    if has_email(resume_text):
        score += 5
    else:
        feedback.append("Add a professional email address.")

    if has_phone(resume_text):
        score += 5
    else:
        feedback.append("Add a valid mobile number.")

    if "skills" in sections and len(sections["skills"]) > 0:
        score += 12
        skill_count = len([s for s in sections["skills"] if len(s.strip()) > 1])
        if skill_count >= 10:
            score += 8
        elif skill_count >= 5:
            score += 5
        else:
            feedback.append("Add more technical skills to strengthen your profile.")
    else:
        feedback.append("Skills section is missing.")

    if "projects" in sections and len(sections["projects"]) > 0:
        score += 10
        project_count = count_projects(sections["projects"])
        if project_count >= 3:
            score += 10
        elif project_count == 2:
            score += 7
            feedback.append("Add one more project for a stronger profile.")
        elif project_count == 1:
            score += 4
            feedback.append("Try to include 2–3 well-described projects.")
        else:
            score += 5
    else:
        feedback.append("Projects section not found.")

    grad_year = graduation_year(resume_text)
    if grad_year:
        score += 15
    else:
        feedback.append("Mention your graduation year clearly.")

    if "experience" in sections and len(sections["experience"]) > 0:
        score += 12
        if has_experience(resume_text):
            score += 8
        else:
            feedback.append("Experience section detected but details are weak.")
    else:
        score += 5
        feedback.append("No experience section found.")

    if "objective" in sections and sections["objective"]:
        score += 5
    else:
        feedback.append("Add a short career objective or professional summary.")

    detected_sections = sum(
        1 for s in ["skills", "projects", "education", "experience", "objective"]
        if s in sections
    )

    if detected_sections >= 3:
        score += 10
    else:
        score += 5
        feedback.append("Resume structure is weak. Use clear section headings.")

    return min(score, 100), feedback


st.title("📄 ATS Resume Checker (Rule-Based)")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
if resume_file :
    resume_text = extract_text(resume_file)

    if st.button("Check ATS Score"):
        sections = section_maker(resume_text, section_map)
        project_lines = sections.get("projects", [])
        project_count = count_projects(project_lines)
        st.write(project_count)
        final_score, feedback = ats_score(resume_text,sections)

        st.subheader("📊 ATS Score")
        st.metric("Final ATS Score", f"{final_score} / 100")

        if final_score >= 80:
            st.success("Excellent ATS-ready resume")
        elif final_score >= 60:
            st.warning("Good resume, but needs improvements")
        else:
            st.error("Resume needs major improvements")

        if feedback:
            st.subheader("🛠 Improvement Suggestions")
            for f in feedback:
                st.write("•", f)
        else:
            st.success("No major issues detected. Your resume is ATS-friendly.")
