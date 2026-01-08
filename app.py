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


st.title("Resume Screening System (ATS Prototype)")

resume_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)", type=["pdf", "docx"]
)

jd_input = st.text_area(
    "Paste Job Description",
    height=250
)

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

