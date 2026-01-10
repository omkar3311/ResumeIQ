# ResumeIQ

**AI-Powered Resume Evaluator & Job Match Tool**  
Live App: https://resumeiq-ai.streamlit.app/ (deployed on Streamlit) :contentReference[oaicite:0]{index=0}

ResumeIQ helps job seekers understand how an uploaded resume performs against ATS criteria and how well it matches a given job description.

---

## 🚀 What It Is

ResumeIQ is a **Python + Streamlit** application that:

- **Evaluates resumes** for ATS friendliness and structure  
- **Compares resumes** with job descriptions for keyword and skill match  
- **Scores and visualizes compatibility**  
- Provides actionable feedback to improve resume quality

This is perfect if you want to tailor your resume for specific jobs and improve interview chances.

---

## 🧠 Key Features

✔ **ATS Compatibility Check** – Analyzes your resume for ATS-friendly formatting, keywords, and structure.

✔ **Job Description Match** – Compares resume content to job postings and scores how well they align.

✔ **Live Web App UI** – Users can upload files directly through a Streamlit interface. :contentReference[oaicite:1]{index=1}

✔ **Deployable** – Works locally or on Streamlit Community Cloud.

---

## 📂 Repository Structure

```bash
ResumeIQ/
├── ATS_checker.py # ATS scoring logic
├── JD_checker.py # JD vs Resume comparative logic
├── app.py # Main Streamlit app
├── service.py # Helper functions & parsing utilities
├── requirements.txt # Python dependencies
└── README.md 
```


---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend UI | Streamlit |
| Backend Logic | Python |
| Parsing | PDF / DOCX extraction |
| Deployment | Streamlit Cloud |

---

## 🧩 How It Works

1. **Upload your Resume** (PDF/DOCX/TXT)  
2. Internally the app parses text and extracts structured content  
3. **ATS_checker** reviews compatibility with common ATS rules  
4. **JD_checker** compares your resume against a target JD file  
5. Results are shown in the UI with scores and suggestions

---
## 👨‍💻 **Author**

   **Omkar Waghmare**  
🎓 Aspiring Data Scientist.