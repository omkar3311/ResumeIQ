import streamlit as st
from service import extract_text

st.title("📄 ATS Resume Checker (Rule-Based)")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
button = st.button("Upload")
if resume_file and button:
    resume_text = extract_text(resume_file,resume_file.type)

    if st.button("Check ATS Score"):
        final_score, feedback = ats_score(resume_text)

        st.subheader("📊 ATS Score")
        st.metric("Final ATS Score", f"{final_score} / 100")

        if final_score >= 80:
            st.success("Excellent ATS-ready resume")
        elif final_score >= 60:
            st.warning("Good resume, but needs improvements")
        else:
            st.error("Resume needs major improvements")

        st.subheader("🛠 Improvement Suggestions")
        for f in feedback:
            st.write("•", f)