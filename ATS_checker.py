import streamlit as st
from service import extract_text,section_map,count_projects, section_maker, ats_score

def ATS():
    st.title("📄 ATS Resume Checker")
    st.caption(
        "**Note: This ATS analysis is based on automated parsing. In some cases, well-formatted information "
        "may not be detected due to layout, styling, or section naming differences.**"
    )
    resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    button = st.button("Check ATS Score")
    if resume_file and button:
        resume_text = extract_text(resume_file)

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
                
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏠 Home"):
            st.session_state["page"] = "home"
            st.rerun()

    with col2:
        if st.button("📄 JD checker"):
            st.session_state["page"] = "jd"
            st.rerun()