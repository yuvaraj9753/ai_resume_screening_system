import re
import spacy
from pdfminer.high_level import extract_text
from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Skill Database
# -----------------------------
SKILL_DB = {
    "data scientist": {
        "core": ["python", "sql", "machine learning", "nlp", "deep learning"],
        "secondary": ["statistics", "pandas", "numpy"]
    },
    "data analyst": {
        "core": ["excel", "sql", "python", "power bi"],
        "secondary": ["tableau", "statistics"]
    },
    "machine learning engineer": {
        "core": ["python", "machine learning", "deep learning", "tensorflow", "pytorch"],
        "secondary": ["mlops", "data preprocessing"]
    },
    "python developer": {
        "core": ["python", "django", "flask", "api"],
        "secondary": ["oop", "sql"]
    },
    "business analyst": {
        "core": ["excel", "sql", "power bi", "tableau"],
        "secondary": ["business analysis", "statistics"]
    }
}

# -----------------------------
# Resume Text Extraction
# -----------------------------
def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text(file_path)
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return " ".join(p.text for p in doc.paragraphs)
    return ""

# -----------------------------
# Candidate Name (NER + Fallback)
# -----------------------------
def extract_candidate_name(text):
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if persons:
        return persons[0]

    email_match = re.search(r'([a-zA-Z]+)[._]?[a-zA-Z]*@', text)
    if email_match:
        return email_match.group(1).title()

    return "Not Detected"

# -----------------------------
# Text Preprocessing
# -----------------------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    doc = nlp(text)
    tokens = [t.lemma_ for t in doc if not t.is_stop]
    return " ".join(tokens)

# -----------------------------
# Experience Extraction (Improved)
# -----------------------------
def extract_experience(text):
    text = text.lower()
    patterns = [
        r'(\d+)\s*\+?\s*years?',
        r'(\d+)\s*yrs?',
        r'(\d+)\s*year experience'
    ]

    years = []
    for p in patterns:
        years.extend([int(x) for x in re.findall(p, text)])

    date_ranges = re.findall(r'(20\d{2})\s*[-–to]+\s*(20\d{2}|present)', text)
    for start, end in date_ranges:
        end_year = 2025 if end == "present" else int(end)
        years.append(end_year - int(start))

    return max(years) if years else 0

# -----------------------------
# Education & Certifications
# -----------------------------
def extract_education_certifications(text):
    degrees, certs = [], []
    degree_keywords = ["b.tech","m.tech","bsc","msc","mba","be"]
    cert_keywords = ["certificate","certified","coursera","udemy","kaggle","google"]

    for d in degree_keywords:
        if d in text.lower():
            degrees.append(d.upper())
    for c in cert_keywords:
        if c in text.lower():
            certs.append(c.capitalize())

    return degrees, certs

# -----------------------------
# Skill Extraction
# -----------------------------
def extract_skills(text, job_title):
    job = SKILL_DB[job_title.lower()]
    matched_core = [s for s in job["core"] if s in text]
    matched_sec = [s for s in job["secondary"] if s in text]
    missing_core = [s for s in job["core"] if s not in text]
    missing_sec = [s for s in job["secondary"] if s not in text]
    return matched_core, matched_sec, missing_core, missing_sec

# -----------------------------
# SBERT Similarity
# -----------------------------
def calculate_similarity(resume_text, jd_text):
    emb = model.encode([resume_text, jd_text])
    score = cosine_similarity([emb[0]], [emb[1]])[0][0]
    return round(score * 100, 2)

# -----------------------------
# Suggestions
# -----------------------------
def generate_suggestions(missing_skills, experience):
    s = []
    if missing_skills:
        s.append(f"Improve skills in: {', '.join(missing_skills)}")
    if experience < 2:
        s.append("Add internships / entry-level projects")
    elif experience < 5:
        s.append("Highlight real-world projects")
    s.append("Optimize resume keywords as per job description")
    return s

# -----------------------------
# Main Resume Analysis
# -----------------------------
def analyze_resume(resume_path, jd_text, job_title):
    raw = extract_resume_text(resume_path)
    clean_resume = preprocess_text(raw)
    clean_jd = preprocess_text(jd_text)

    name = extract_candidate_name(raw)
    experience = extract_experience(raw)
    degrees, certs = extract_education_certifications(raw)

    matched_core, matched_sec, missing_core, missing_sec = extract_skills(clean_resume, job_title)

    skill_score = (
        0.7 * len(matched_core) / max(len(SKILL_DB[job_title]["core"]), 1) +
        0.3 * len(matched_sec) / max(len(SKILL_DB[job_title]["secondary"]), 1)
    ) * 100

    similarity = calculate_similarity(clean_resume, clean_jd)
    experience_score = min(experience / 5, 1) * 100

    shortlist = (
        0.45 * skill_score +
        0.35 * similarity +
        0.20 * experience_score
    )

    return {
        "candidate_name": name,
        "job_role": job_title,
        "matched_skills": matched_core + matched_sec,
        "missing_skills": missing_core + missing_sec,
        "similarity_score": similarity,
        "shortlisting_probability": round(shortlist, 2),
        "experience_years": experience,
        "degrees": degrees,
        "certifications": certs,
        "suggestions": generate_suggestions(missing_core + missing_sec, experience)
    }