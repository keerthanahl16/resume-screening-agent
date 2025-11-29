Resume Screening Agent

Short description
AI-powered Resume Screening Agent built with Streamlit.  
It indexes candidate resumes (PDF/DOCX/TXT), creates embeddings, searches via FAISS, and provides AI summaries and JD-resume explainers using OpenAI/Gemini.

---

Demo
Working demo (Streamlit): [YOUR_DEPLOYED_URL_HERE](https://resume-screening-agent-7h4uydtvcj9ut48bvdemb5.streamlit.app/)  

Repository contents (what must be present)
- `app/` — Streamlit app and modules (streamlit_app.py, utils.py, embedder.py, resume_parser.py, search.py, ai_helpers.py, visuals.py, exporter.py, __init__.py)
- `data/resumes/` — sample resumes (not required in repo; add sample anonymized resumes if you want)
- `faiss_index/` — (ignored in repo, will be created at runtime)
- `requirements.txt` — dependencies
- `README.md` — (this file)
- `.gitignore` — ignore venv, large files, data, index, etc.

Tech stack & libraries
- Python 3.10+
- Streamlit (UI)
- FAISS (approximate nearest neighbors)
- sentence-transformers or OpenAI embeddings (configurable)
- pdfplumber / python-docx / docx2txt (resume parsing)
- OpenAI (or Gemini) for chat/summarization
- pandas, plotly (visuals), openpyxl (Excel export)

Features
- Index resumes into FAISS (vector search)
- Skill extraction & approximate experience estimation
- Composite scoring: embed + skill overlap + experience + richness
- Streamlit UI to upload resumes, paste JD, run screening, view results
- AI-powered candidate summary & JD-resume explanation (OpenAI/Gemini)
- Recruiter chatbot using combined short resume contexts
- Plotly radar charts per candidate and Excel export
- Configurable Top-K results and filtering by skills/years

Limitations
- Resume parsing is heuristic and may miss complex formats
- Embedding choice (OpenAI vs local model) affects cost & accuracy
- Chatbot uses truncated resume text to avoid huge prompts (may miss details)
- FAISS index is local — for large scale, move to cloud vector DB
- Privacy: do not deploy with real PII without compliance checks

Setup — Local (Windows PowerShell / macOS / Linux)

**1. Clone repo**
```bash
git clone https://github.com/keerthanahl16/resume-screening-agent.git
cd resume-screening-agent
