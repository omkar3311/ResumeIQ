import streamlit as st
import pdfplumber
from docx import Document
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text(file):
    if file.type == "application/pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return " ".join(p.text for p in doc.paragraphs)

    return ""

def clean_text(text):
    cleaned_text = re.sub(r'[•▪◦–—*]', '', text)
    cleaned_text = re.sub(r'page \d+ of \d+', '', cleaned_text, flags=re.I)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

def section_clean(sections):
    for key, value in sections.items():
        sections[key] = clean_text(" ".join(value))
    return sections
def compute_similarity(resume, jd):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume, jd])
    return cosine_similarity(vectors[0], vectors[1])[0][0]

def section_maker(text,section_map):
    lines = text.splitlines()
    sections = {}
    current_section = None
    
    for line in lines:
        line_clean = line.strip().lower()
        if line_clean in section_map:
            current_section = section_map[line_clean]
            if current_section not in sections:
                sections[current_section] = []
        elif current_section:
            sections[current_section].append(line.strip())
    return sections

def resume_weight(sections):
    skills = sections.get("skills", []) 
    experience = sections.get("experience", [])
    projects = sections.get("projects", [])
    objective = sections.get("objective", [])
    education = sections.get("education", [])
    resume_text = "".join(
        (skills + " " ) * 3 +
        (experience + " " )  * 2 +
        (projects + " " )  * 2 +
        objective +
        education)
    return resume_text

def text_jd(sections):
    text =""
    for key, value in sections.items():
        text = text + value + " "
    return text

def ai_feedback(overall, skills, matched, missing):
    if skills >= 0.75:
        verdict = "Strong Match"
        color = "green"
        tone = "Your resume strongly aligns with this role."
    elif skills >= 0.5:
        verdict = "Moderate Match"
        color = "orange"
        tone = "You meet many requirements, but some skills are missing."
    else:
        verdict = "Weak Match"
        color = "red"
        tone = "Your resume currently lacks several key requirements."

    feedback_text = f"""
        {tone}

        🔍 **Skill Analysis**
        - Matched skills: {len(matched)}
        - Missing skills: {len(missing)}

        📌 **Recommended Improvements**
        """

    if missing:
        feedback_text += "\n📌 **Recommended Skills to Improve or Highlight:**\n"
        feedback_text += "\n".join([f"• {skill}" for skill in sorted(missing)])
    else:
        feedback_text += "\n📌 **Excellent** — no critical skills missing."

    return verdict, color, feedback_text


def normalize_skills(text):
    text = text.lower()
    text = re.sub(r"[()\[\]{}/]", " ", text)
    text = re.sub(r"[^a-z0-9+.#\- ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    skills = set(skill.strip() for skill in text.split() if len(skill) > 2)
    return skills


section_map = {
    "objective": "objective",
    "summary": "objective",

    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "internships": "experience",

    "projects": "projects",
    "academic projects": "projects",
    
    "required skills": "skills",
    "preferred skills": "skills",
    "skills": "skills",
    "technical skills": "skills",

    "education": "education",
    "awards": "awards",
    "awards": "achievements",
    "certifications": "certifications"
}

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