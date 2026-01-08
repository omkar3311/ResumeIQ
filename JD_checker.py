import streamlit as st
from service import extract_text, clean_text, section_clean, compute_similarity, section_maker
from service import resume_weight, ai_feedback, normalize_skills, section_map , text_jd


st.title("Resume Screening System (ATS Prototype)")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_input = st.text_area("Paste Job Description",height=250)
button = st.button("upload")

if button and resume_file and jd_input.strip():

    resume_text = extract_text(resume_file)

    resume_section = section_maker(resume_text, section_map)
    jd_section = section_maker(jd_input, section_map)

    clean_resume = section_clean(resume_section)
    clean_jd = section_clean(jd_section)

    wt_resume = resume_weight(clean_resume)
    jd_text = text_jd(clean_jd)

    overall_score = compute_similarity(wt_resume, jd_text)

    resume_skills_text = clean_resume.get("skills", "")
    jd_skills_text = clean_jd.get("skills", "")

    resume_skills = normalize_skills(resume_skills_text)
    jd_skills = normalize_skills(jd_skills_text)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    skills_score = (
        compute_similarity(resume_skills_text, jd_skills_text)
        if resume_skills_text and jd_skills_text else 0.0
    )

    final_score = (0.6 * skills_score) + (0.4 * overall_score)

    st.subheader("📊 Similarity Scores")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric("Overall Resume Match", f"{overall_score*100:.2f}%")
    with col2:
        st.metric("Skills Match", f"{skills_score*100:.2f}%")
    with col3:
        st.metric("Final ATS Score", f"{final_score*100:.2f}%")

    verdict, color, feedback_text = ai_feedback(
    overall_score, skills_score, matched, missing
    )

    st.subheader("🤖 AI Evaluation")

    if color == "green":
        st.success(verdict)
    elif color == "orange":
        st.warning(verdict)
    else:
        st.error(verdict)

    st.write(feedback_text)