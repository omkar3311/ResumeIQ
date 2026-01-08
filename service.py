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
    feedback_text = ""
    feedback_text += f"\n{tone}\n"
    feedback_text += "\n🔍 **Skill Analysis**\n"
    feedback_text += f"\n- Matched skills: {len(matched)}"
    feedback_text += f"\n- Missing skills: {len(missing)}\n"
    

    if missing:
        feedback_text += "\n📌 **Recommended Skills to Improve or Highlight:**\n\n"
        feedback_text += "\n".join([f"• {skill}  " for skill in sorted(missing)])
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

def has_email(text):
    return re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text)

def has_phone(text):
    return re.search(r"\b\d{10}\b", text)

def has_experience(text):
    return "experience" in text or "internship" in text

def graduation_year(text):
    years = re.findall(r"(20\d{2})", text)
    return max(map(int, years)) if years else None


def count_projects(project_lines):
    if not project_lines:
        return 0

    project_count = 0
    current_project_lines = []
    detected_titles = 0
    bullet_blocks = 0

    def looks_like_title(line):
        return (
            2 <= len(line.split()) <= 10
            and not line.endswith(".")
            and not line.lower().startswith(
                ("tech", "tools", "description", "responsibilities")
            )
        )

    for i, line in enumerate(project_lines):
        line = line.strip()

        if not line:
            continue

        if re.match(r"^\d+\.", line):
            detected_titles += 1
            continue

        if "|" in line or ":" in line:
            detected_titles += 1
            continue

        if looks_like_title(line):
            detected_titles += 1
            continue

        if re.match(r"^[•\-*]", line):
            bullet_blocks += 1

    if detected_titles > 0:
        project_count = detected_titles
    elif bullet_blocks >= 2:
        project_count = max(1, bullet_blocks // 2)
    else:
        project_count = 0
    return min(project_count, 5)  
