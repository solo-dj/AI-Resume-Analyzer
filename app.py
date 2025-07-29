import streamlit as st
import pdfplumber
import docx
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load job roles and skill keywords
with open('job_roles.json', 'r') as f:
    job_roles = json.load(f)

stop_words = set(stopwords.words('english'))

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text.lower()

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = " ".join([para.text for para in doc.paragraphs])
    return text.lower()

def preprocess_text(text):
    # Remove symbols and numbers
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = word_tokenize(text)
    return [w.lower() for w in words if w.lower() not in stop_words]

def match_skills(resume_words, required_skills):
    matched = [skill for skill in required_skills if skill in resume_words]
    missing = [skill for skill in required_skills if skill not in resume_words]
    return matched, missing

# ---------------- Streamlit App ---------------- #
st.set_page_config(page_title="Resume Screening Bot", layout="centered")

st.title("📄 Resume Screening Chatbot")
st.markdown("Upload a resume and select a job role to check if the resume is a good match.")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

job_role = st.selectbox("Select Job Role", list(job_roles.keys()))

if st.button("🔍 Analyze Resume"):
    if uploaded_file is not None and job_role:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        resume_words = preprocess_text(resume_text)
        required_skills = job_roles[job_role]

        matched, missing = match_skills(resume_words, required_skills)

        st.success(f"✅ Skills matched: {len(matched)} / {len(required_skills)}")
        st.markdown("**✔️ Matched Skills:** " + ", ".join(matched))
        st.markdown("**❌ Missing Skills:** " + ", ".join(missing))

        if len(matched) == len(required_skills):
            st.balloons()
            st.success("🎉 This resume is a strong match for the selected role!")
        else:
            st.info("👀 Consider improving the resume with the missing skills.")
    else:
        st.warning("Please upload a valid resume file and choose a job role.")
