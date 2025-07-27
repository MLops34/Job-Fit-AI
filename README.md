# 📄 Job-Fit-AI

An AI-powered Resume Analyzer and Job Matching Engine that provides users with a **JobFit Score** based on how well their resume aligns with a job description. Built for recruiters, job seekers, and HR tech platforms.

![JobFitAI Banner](https://via.placeholder.com/1000x300?text=JobFitAI+Banner) <!-- Replace with your actual banner -->

---

## 🚀 Features

- 🧠 **AI-based Resume Parsing** (Name, Email, Phone, Skills, Education, Experience)
- 📊 **JobFit Score Calculation** using NLP + XGBoost/Cosine Similarity
- ✍️ **Job Description Analyzer**
- 🖼️ **Streamlit Dashboard** with visual insights
- ⚡ Built with FastAPI + Streamlit for blazing fast UX

---

## 🏗️ Tech Stack

| Tech             | Description                       |
|------------------|-----------------------------------|
| `FastAPI`        | Backend API for parsing & matching|
| `Streamlit`      | Frontend interface                |
| `spaCy`          | NLP for resume/job text parsing   |
| `XGBoost`        | Machine learning for scoring      |
| `PDFPlumber / docx` | Resume text extraction         |
| `cosine similarity`| Skill vector-based matching     |

---

## 📂 Project Structure

Job-Fit-AI/
├── Backend/
│ ├── main.py
│ ├── routers/
│ ├── services/
│ ├── models/
│ └── utils/
├── Frontend/
│ └── app.py (Streamlit)
├── README.md
└── requirements.txt


<img src="https://via.placeholder.com/600x400?text=Resume+Upload+Page" width="500"/> <img src="https://via.placeholder.com/600x400?text=Match+Score+Dashboard" width="500"/>