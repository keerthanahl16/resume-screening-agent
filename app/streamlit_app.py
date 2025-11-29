# app/streamlit_app.py

import sys, os, re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from pathlib import Path
from app.utils import build_index_from_folder
from app.embedder import embed_texts
from app.search import search
from app.ai_helpers import summarize_candidate, explain_match
from app.visuals import candidate_radar_chart
from app.exporter import export_excel
from openai import OpenAI
import pandas as pd

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =============================
# Skill Highlighter
# =============================
def highlight_skills(text, skills):
    def repl(match):
        word = match.group(0)
        return f"**:green[{word}]**"

    for s in skills:
        if not s:
            continue
        pattern = re.compile(rf"\b{re.escape(s)}\b", flags=re.IGNORECASE)
        text = pattern.sub(repl, text)
    return text


# =============================
# Page Setup
# =============================
st.set_page_config(page_title="Resume Screening Agent", layout="wide")

st.title("💼 Resume Screening Agent (AI-Powered)")


# =============================
# Sidebar
# =============================
st.sidebar.header("⚙ Settings")

if st.sidebar.button("📌 Build / Rebuild Index"):
    count = build_index_from_folder("data/resumes")
    st.sidebar.success(f"Indexed {count} resumes")

k = st.sidebar.slider("Top K Candidates", 1, 20, 5)


# =============================
# Layout
# =============================
col1, col2 = st.columns([2, 1])


# =============================
# LEFT PANEL
# =============================
with col1:

    st.header("1️⃣ Job Description")
    jd = st.text_area("Paste job description here", height=240)

    st.write("Desired skills (comma-separated):")
    skills_raw = st.text_input("Example: python, sql, aws, machine learning")
    query_skills = [s.strip().lower() for s in skills_raw.split(",") if s.strip()]

    query_years = st.number_input("Desired years of experience", 0, 50, 0)

    st.header("2️⃣ Upload Resumes (Optional)")
    uploaded = st.file_uploader("Upload PDF / DOCX / TXT resumes", accept_multiple_files=True)

    if uploaded:
        save_dir = Path("data/resumes")
        save_dir.mkdir(parents=True, exist_ok=True)

        for f in uploaded:
            with open(save_dir / f.name, "wb") as out:
                out.write(f.getbuffer())

        st.success("Uploaded! Now click **Build / Rebuild Index** from the sidebar.")

    # =============================
    # RUN SCREENING
    # =============================
    if st.button("🚀 Run Screening"):

        if not jd.strip():
            st.error("Please paste a job description.")

        else:
            with st.spinner("Embedding JD..."):
                q_emb = embed_texts([jd])[0]

            with st.spinner("Searching resumes..."):
                results = search(q_emb, k=k, query_skills=query_skills, query_years=query_years)

            if not results:
                st.warning("No index found. Add resumes and rebuild index.")

            else:
                st.success(f"Found {len(results)} candidates")

                rows = []

                for i, r in enumerate(results, 1):

                    st.subheader(f"⭐ {i}. {r['file']} — Score: {r['composite_score']:.3f}")

                    st.markdown(f"""
                    **Embedding Score:** {r['embed_score']:.3f}  
                    **Skill Match:** {r['skill_score']:.2f}  
                    **Experience Score:** {r['exp_score']:.2f}
                    """)

                    st.write("**Extracted Skills:**", ", ".join(r.get("skills", [])) or "—")
                    st.write("**Estimated Experience:**", r.get("years_experience", 0), "years")

                    # Radar Chart
                    st.plotly_chart(candidate_radar_chart(r), use_container_width=True)

                    # Highlighted Snippet
                    snippet = r.get("full_text", "")[:1000]
                    highlighted = highlight_skills(snippet, r.get("skills", []))
                    st.markdown(highlighted)

                    # Full Resume Preview
                    with st.expander("📄 Full Resume Text (Preview)"):
                        full_res_text = highlight_skills(r["full_text"], r["skills"])
                        st.markdown(full_res_text)

                    # AI Summary
                    if st.checkbox(f"Show AI Summary for {r['file']}"):
                        with st.spinner("Summarizing candidate..."):
                            summary = summarize_candidate(r["full_text"])
                        st.write(summary)

                    # AI Match Explanation
                    if st.checkbox(f"Explain JD Match for {r['file']}"):
                        with st.spinner("Analyzing match..."):
                            explanation = explain_match(jd, r["full_text"])
                        st.write(explanation)

                    st.markdown("---")

                    rows.append({
                        "rank": i,
                        "file": r["file"],
                        "composite": r["composite_score"],
                        "embed": r["embed_score"],
                        "skill_score": r["skill_score"],
                        "exp_score": r["exp_score"]
                    })

                # Download CSV
                df = pd.DataFrame(rows)
                st.download_button(
                    "⬇ Download Screening Results (CSV)",
                    df.to_csv(index=False),
                    file_name="screening_results.csv",
                    mime="text/csv"
                )

                # Download Excel
                if st.button("⬇ Download Excel (Formatted)"):
                    file_path = export_excel(rows)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            "Download Excel File",
                            f.read(),
                            file_name=file_path,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                # Recruiter Chatbot
                st.header("🤖 Recruiter Chatbot")
                chat_q = st.text_input("Ask anything about the shortlisted candidates...")

                if chat_q:
                    st.write("Thinking...")

                    full_context = ""
                    for r in results:
                        full_context += f"""
Candidate: {r['file']}
Skills: {', '.join(r['skills'])}
Experience: {r['years_experience']} yrs
Text:
{r['full_text'][:1500]}

"""

                    prompt = f"""
You are a recruiter assistant. Use ONLY the information from these resumes:

{full_context}

Question: {chat_q}
"""

                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}]
                    )

                    st.write(resp.choices[0].message["content"])


# =============================
# RIGHT PANEL
# =============================
with col2:
    st.header("💡 Quick Tips")
    st.markdown("""
    - Upload resumes or place them inside **data/resumes/**
    - Click **Build Index** before searching  
    - AI summary helps understand each candidate  
    - JD-match explainer tells why the candidate fits  
    - Recruiter bot can compare multiple candidates  
    """)

    st.markdown("### Sample JD")
    st.code("""
We are hiring a Data Scientist with 3+ years of experience.
Skills: Python, pandas, scikit-learn, SQL, ML.
""")

st.markdown("""
<style>

    /* Force light theme for all widgets */
    :root {
        color-scheme: light !important;
    }

    /* Make sidebar fully white */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Make main area clean white */
    .stApp, .main, html, body {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Fix text areas */
    textarea, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 16px !important;
    }

    /* Fix sample JD code box */
    .stCodeBlock pre {
        background-color: #f3f3f3 !important;
        color: #000000 !important;
    }

    /* Fix drag & drop uploader */
    [data-testid="stFileDropzone"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px dashed #888 !important;
    }

    /* Buttons stay blue */
    .stButton>button {
        background-color:#0066FF !important;
        color:white !important;
        border-radius:10px !important;
        padding:10px 20px !important;
    }

</style>
""", unsafe_allow_html=True)
