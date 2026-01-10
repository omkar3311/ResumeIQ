import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from service import  extract_text, clean_text, section_clean, compute_similarity, section_maker
from service import resume_weight, ai_feedback, normalize_skills, section_map , text_jd
from service import bar_chart, skill_match, scatter_plot,ranked_plot


def single_resume(resume_files):
    resume_text = extract_text(resume_files[0])
    
    resume_section = section_maker(resume_text, section_map)
    jd_section = section_maker(jd_input, section_map)
    
    clean_resume = section_clean(resume_section)
    clean_jd = section_clean(jd_section)
    
    sections_dict = {}
    for key, value in clean_resume.items():
        if isinstance(value, str):
            sections_dict[key] = [value]
        else:
            sections_dict[key] = value

    wt_resume = resume_weight(sections_dict)

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

def multi_resume(resume_files):
    resume_text = {}
    for resume_file in resume_files:
        resume_text[resume_file.name]  = extract_text(resume_file)
        
    resume_section ={}
    for resume , text in resume_text.items():
        resume_section[resume] = section_maker(text, section_map)
    jd_section = section_maker(jd_input, section_map)
    
    resume_clean = {}   
    for name, sections_list in resume_section.items():
        resume_clean[name] = section_clean(sections_list) 
    clean_jd = section_clean(jd_section)
    
    wt_resume = {}
    for name, sections in resume_clean.items():
        sections_dict = {}
        for key, value in sections.items():
            if isinstance(value, str):
                sections_dict[key] = [value]
            else:
                sections_dict[key] = value
        wt_resume[name] = resume_weight(sections_dict)
    jd_text = text_jd(clean_jd)
    
    overall_score = {}
    for name , resume in wt_resume.items():
        overall_score[name] = compute_similarity(resume, jd_text)
    
    resume_skills = {}
    for name , sections in resume_clean.items():
        resume_skills[name] = sections.get("skills", "")
    jd_skills_text = clean_jd.get("skills", "")
    
    skill_score = {}
    for name , skill in resume_skills.items():
        skill_score[name] = compute_similarity(skill, jd_skills_text) if skill and jd_skills_text else 0.0
    
    final_score = {}
    for name ,value in skill_score.items():
        final_score[name] = (0.6 * skill_score[name]) + (0.5 * overall_score[name])
    df = pd.DataFrame({
        "Resume": list(final_score.keys()),
        "ATS Score": [v * 100 for v in final_score.values()]
    })

    ranked_plot(final_score, skill_score)
    bar_chart(final_score)
    skill_match(skill_score)
    scatter_plot(overall_score,skill_score)

resume_files = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files = True )
jd_input = st.text_area("Paste Job Description",height=250)
button = st.button("upload")

if button and resume_files and jd_input.strip():
    if len(resume_files) == 1 :
        single_resume(resume_files)
    else :
        multi_resume(resume_files)