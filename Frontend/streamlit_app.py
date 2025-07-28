import streamlit as st
import requests

# Load custom CSS
try:
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found. Using default styling.")

# Inline CSS for buttons
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-size: 18px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(page_title="JobFitAI", page_icon="📄", layout="centered")
st.markdown("""
    <h1 style='text-align: center; font-size: 3rem; font-weight: bold; 
               color: #00ADB5; margin-bottom: 10px;'>📄 JobFitAI</h1>
""", unsafe_allow_html=True)

st.subheader("AI-powered Resume Analyzer & Job Matching")
st.markdown("Upload your resume and get a **JobFit Score** with AI-powered insights.")

# Resume upload
uploaded_file = st.file_uploader("Upload your resume (pdf or docx)", type=["pdf", "docx"])
parsed_preview = ""  # Initialize to avoid undefined variable
if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        response = requests.post("http://127.0.0.1:8000/api/jobfit/upload-resume", files=files)
        if response.status_code == 200:
            st.success("✅ Resume uploaded successfully!")
            parsed_preview = response.json().get("parsed_text_full", "")
            st.text_area("Parsed Resume Preview", parsed_preview, height=150)
        else:
            try:
                error_detail = response.json().get('detail', response.text)
            except ValueError:
                error_detail = response.text
            st.error(f"❌ Error uploading resume: {response.status_code} - {error_detail}")
    except requests.ConnectionError:
        st.error("❌ Unable to connect to the backend API. Please check if the server is running.")
else:
    st.info("📤 Please upload a resume file to continue.")



# Job description input
job_description = st.text_area("Paste job description here")

if st.button("Upload Job Description"):
    if job_description:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/jobfit/upload-job",
                data={"description": job_description}
            )
            if response.status_code == 200:
                st.success("✅ Job description uploaded successfully!")
            else:
                try:
                    error_detail = response.json().get('detail', response.text)
                except ValueError:
                    error_detail = response.text  # fallback if response body is not JSON
                st.error(f"❌ Error uploading job: {response.status_code} - {error_detail}")
        except requests.ConnectionError:
            st.error("❌ Unable to connect to the backend API. Please check if the server is running.")
    else:
        st.warning("⚠️ Please paste a job description before uploading.")

# Match score
if st.button("Get Match Score"):
    try:
        with st.spinner("Calculating match score..."):
            response = requests.post("http://127.0.0.1:8000/api/jobfit/match-score")
        if response.status_code == 200:
            data = response.json()
            score = data.get("match_score_percent")
            if score is not None:
                st.metric("🎯 Match Score", f"{score}%")
                st.success(data.get("message", "Match score calculated successfully!"))
            else:
                st.error("❌ Match score not found in response.")
        else:
            st.error(f"❌ Could not get match score. Status code: {response.status_code} - {response.json().get('detail', response.text)}")
    except requests.ConnectionError:
        st.error("❌ Unable to connect to the backend API. Please check if the server is running.")
    except Exception as e:
        st.error(f"❌ Error while getting match score: {e}")

# ATS compatibility check
# ATS compatibility check
st.markdown("---")
st.subheader("🧠 ATS Compatibility Checker")
if uploaded_file:
    if st.button("Run ATS Check"):
        try:
            with st.spinner("Checking ATS compatibility..."):
                response = requests.post(
                    "http://127.0.0.1:8000/api/jobfit/ats-check",
                    json={"resume_text": parsed_preview, "job_description": job_description}
                )
            if response.status_code == 200:
                
                ats_data = response.json()
                st.success("✅ ATS Check Completed")
                # ATS Score Breakdown Table
                st.markdown("### 📊 How Final ATS Score is Calculated")
                st.markdown("""
Each component of the ATS score contributes to the final result based on the following weights:

| Component           | Weight | Score (%) | Contribution |
|---------------------|--------|-----------|--------------|
| **Keyword Match**   | 40%    | {keyword}   | {kw_contribution} |
| **Section Match**   | 25%    | {section}   | {section_contribution} |
| **Bullet Points**   | 20%    | {bullet}   | {bullet_contribution} |
| **Resume Length**   | 15%    | {length}   | {length_contribution} |

🧮 **Final ATS Score = Sum of Contributions** = **{final_score}%**
""".format(
    keyword=f"{ats_data['keyword_match']}%" if ats_data['keyword_match'] is not None else "0%",
    kw_contribution=f"{round((ats_data['keyword_match'] or 0) * 0.4, 2)}%" if ats_data['keyword_match'] is not None else "0%",
    section=f"{ats_data['section_score']}%",
    section_contribution=f"{round(ats_data['section_score'] * 0.25, 2)}%",
    bullet=f"{ats_data['bullet_point_score']}%",
    bullet_contribution=f"{round(ats_data['bullet_point_score'] * 0.2, 2)}%",
    length=f"{ats_data['length_score']}%",
    length_contribution=f"{round(ats_data['length_score'] * 0.15, 2)}%",
    final_score=ats_data['final_ats_score']
))

            else:
                st.error(f"❌ Failed to run ATS check: {response.status_code} - {response.json().get('detail', response.text)}")
        except requests.ConnectionError:
            st.error("❌ Unable to connect to the backend API. Please check if the server is running.")
        except Exception as e:
            st.error(f"❌ Error while running ATS check: {e}")
else:
    st.info("Upload resume to check ATS compatibility.")
