import streamlit as st
import requests

# App config
st.set_page_config(page_title="JobFitAI", page_icon="📄", layout="centered")
st.title("📄 JobFitAI")
st.subheader("AI-powered Resume Analyzer & Job Matching")
st.markdown("Upload your resume and get a **JobFit Score** with AI-powered insights.")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (pdf or docx)", type=["pdf", "docx"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    response = requests.post("http://127.0.0.1:8000/api/jobfit/upload-resume", files=files)

    if response.status_code == 200:
        st.success("✅ Resume uploaded successfully!")
        parsed_preview = response.json().get("parsed_text_preview", "")
        st.text_area("Parsed Resume Preview", parsed_preview, height=150)
    else:
        st.error(f"❌ Error uploading resume: {response.status_code} - {response.text}")

# Upload job description
job_description = st.text_area("Paste job description here")

if st.button("Upload Job Description"):
    if job_description:
        response = requests.post(
            "http://127.0.0.1:8000/api/jobfit/upload-job",
            data={"description": job_description}
        )
        if response.status_code == 200:
            st.success("✅ Job description uploaded successfully!")
        else:
            st.error(f"❌ Error uploading job: {response.status_code} - {response.text}")
    else:
        st.warning("Please paste a job description before uploading.")

# Match resume with job
if st.button("Get Match Score"):
    response = requests.get("http://127.0.0.1:8000/api/jobfit/match")

    if response.status_code == 200:
        data = response.json()
        score = data.get("match_score_percent")
        st.metric("🎯 Match Score", f"{score}%")
        st.success(data.get("message"))
    else:
        st.error("❌ Could not get match score. Upload resume and job first.")


import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# Sample resume text (replace with your actual resume text)
resume_text = st.text_area("Paste your resume text here for visualization", height=300)

if resume_text:
    # Simple skill extraction: match words longer than 3 letters (you can customize skill list)
    words = re.findall(r'\b\w{4,}\b', resume_text.lower())
    word_counts = Counter(words)

    # Generate WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_counts)

    st.subheader("Skills Word Cloud")
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Bar chart for top 10 skills/words
    top_skills = word_counts.most_common(10)
    skills, counts = zip(*top_skills)

    st.subheader("Top Skills Frequency")
    fig, ax = plt.subplots()
    ax.barh(skills, counts, color='skyblue')
    ax.invert_yaxis()
    ax.set_xlabel("Frequency")
    st.pyplot(fig)
else:
    st.info("Please paste resume text to see visualization.")
