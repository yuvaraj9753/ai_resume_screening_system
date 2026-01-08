
# 🤖 AI-Powered Resume Screening System

An industry-ready AI-powered Resume Screening System that automatically analyzes resumes and matches them with job descriptions using Natural Language Processing (NLP) and Semantic Similarity techniques.

This system simulates real-world recruiter logic by evaluating candidate skills, experience, education, and job description relevance to generate a realistic shortlisting score and actionable suggestions.

---

## 🚀 Features

- 📄 Upload resumes in **PDF or DOCX** format
- 🧠 **Candidate Name Extraction** using spaCy Named Entity Recognition (NER)
- ⏳ **Accurate Experience Extraction** (years, date ranges, present)
- 🧩 **Role-based Skill Matching** (Core & Secondary skills)
- 🔍 **Semantic Job Description Matching** using SBERT (Sentence Transformers)
- 📊 **Normalized Shortlisting Score** (Recruiter-style scoring)
- 💡 AI-generated improvement suggestions
- 📈 Skill match visualization
- 📥 Downloadable **PDF Resume Screening Report**
- 🔁 Analyze one resume for **multiple job roles**

---

## 🧠 Tech Stack

- **Programming Language:** Python
- **Frontend / UI:** Streamlit
- **NLP:** spaCy
- **Semantic Similarity:** Sentence Transformers (SBERT)
- **Resume Parsing:** pdfminer.six, python-docx
- **Visualization:** matplotlib
- **Report Generation:** FPDF
- **ML Utilities:** scikit-learn

---


## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
2️⃣ Install Dependencies
Copy code
Bash
pip install -r requirements.txt
3️⃣ Download spaCy Language Model
Copy code
Bash
python -m spacy download en_core_web_sm
▶️ Run the Application
Copy code
Bash
streamlit run app.py
The app will open in your browser.
📊 How Scoring Works
The final shortlisting score is calculated using:
Skills Match: 45%
JD Semantic Similarity: 35%
Experience: 20%
This ensures realistic recruiter-style evaluation instead of harsh or biased scoring.
🏭 Project Level
Industry-Ready (Junior / Intern Level)
This project demonstrates:
Real-world NLP usage
Semantic text matching
Recruiter-aligned decision logic
Clean and modular architecture
📌 Future Enhancements
Batch resume processing
Skill-to-skill semantic similarity
Bias & fairness analysis
Cloud deployment (Docker / AWS / Streamlit Cloud)
ATS-style score explanation

