import streamlit as st
import os
import matplotlib.pyplot as plt
from resume_analysis_core import analyze_resume
from fpdf import FPDF

st.set_page_config(page_title="AI Resume Screening System")
st.title("📄 AI-Powered Resume Screening System")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", ["pdf","docx"])
job_roles = ["data scientist","data analyst","machine learning engineer","python developer","business analyst"]
selected_roles = st.multiselect("Select Job Role(s)", job_roles)
jd_text = st.text_area("Paste Job Description", height=200)

def generate_pdf(result, chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,15,"AI Resume Screening Report",ln=True,align="C")

    pdf.set_font("Arial","",11)
    pdf.ln(5)
    pdf.cell(0,8,f"Candidate: {result['candidate_name']}",ln=True)
    pdf.cell(0,8,f"Job Role: {result['job_role']}",ln=True)
    pdf.cell(0,8,f"Shortlisting Score: {result['shortlisting_probability']}%",ln=True)
    pdf.cell(0,8,f"Experience: {result['experience_years']} years",ln=True)

    if result["degrees"]:
        pdf.cell(0,8,f"Degrees: {', '.join(result['degrees'])}",ln=True)
    if result["certifications"]:
        pdf.cell(0,8,f"Certifications: {', '.join(result['certifications'])}",ln=True)

    pdf.ln(5)
    pdf.multi_cell(0,8,f"Matched Skills: {', '.join(result['matched_skills'])}")
    pdf.multi_cell(0,8,f"Missing Skills: {', '.join(result['missing_skills'])}")

    for s in result["suggestions"]:
        pdf.multi_cell(0,8,f"- {s}")

    if os.path.exists(chart_path):
        pdf.add_page()
        pdf.image(chart_path, x=10, y=20, w=180)

    pdf.output("resume_report.pdf")
    return "resume_report.pdf"

if st.button("Analyze Resume"):
    if uploaded_file and jd_text and selected_roles:
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        for role in selected_roles:
            result = analyze_resume(file_path, jd_text, role)
            st.subheader(f"📊 {role.title()} Result")

            st.metric("Shortlisting Probability", f"{result['shortlisting_probability']} %")
            st.metric("JD Similarity", f"{result['similarity_score']} %")
            st.metric("Experience", f"{result['experience_years']} years")

            st.write("👤 Candidate:", result["candidate_name"])
            if result["degrees"]:
                st.write("🎓 Degrees:", ", ".join(result["degrees"]))

            st.write("✅ Matched Skills:", result["matched_skills"])
            st.write("❌ Missing Skills:", result["missing_skills"])
            st.write("💡 Suggestions:", result["suggestions"])

            skills = result["matched_skills"] + result["missing_skills"]
            values = [1] * len(skills)
            colors = ["green"] * len(result["matched_skills"]) + ["red"] * len(result["missing_skills"])

            plt.figure(figsize=(8,4))
            plt.bar(skills, values, color=colors)
            plt.xticks(rotation=45, ha="right")
            plt.title("Skill Match Overview")
            plt.tight_layout()
            chart_path = "skills.png"
            plt.savefig(chart_path)
            plt.close()

            st.image(chart_path, width=700)

            pdf = generate_pdf(result, chart_path)
            with open(pdf, "rb") as f:
                st.download_button(
                    "📥 Download PDF Report",
                    f,
                    file_name=f"{result['candidate_name']}_Report.pdf",
                    mime="application/pdf",
                    key=role
                )
    else:
        st.warning("Please upload resume, select job role(s) and paste job description.")