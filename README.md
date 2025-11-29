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

Working Video : https://drive.google.com/file/d/1tuouu_19-VOmf6Mg9pR7Jg5QbXY1UGpp/view?usp=drivesdk
Setup — Local (Windows PowerShell / macOS / Linux)

1. Clone repo
```bash
git clone https://github.com/keerthanahl16/resume-screening-agent.git
cd resume-screening-agent

2. Create venv & activate

PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1    # if ExecutionPolicy blocks, run PowerShell as Admin or use: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser


macOS / Linux:

python3 -m venv venv
source venv/bin/activate


3. Install dependencies

pip install --upgrade pip
pip install -r requirements.txt


Make sure requirements.txt includes these (example):

streamlit
pandas
numpy
faiss-cpu
sentence-transformers
pdfplumber
python-docx
docx2txt
plotly
openpyxl
openai
pyyaml


4. Add env vars
Set your OpenAI API key (or other):
PowerShell:

$env:OPENAI_API_KEY="sk-..."


macOS/Linux:

export OPENAI_API_KEY="sk-..."


5. Run

streamlit run app/streamlit_app.py


Open http://localhost:8501 in your browser.

How to push to GitHub (clean, exclude venv)

Ensure .gitignore contains:

venv/
__pycache__/
*.pyc
faiss_index/
data/resumes/
.env
.DS_Store
.ipynb_checkpoints


Initialize & push:

git init
git add .
git commit -m "Initial Resume Screening Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/resume-screening-agent.git
git push -u origin main


Important: Do NOT include venv/ or any site-packages in the repo. If you accidentally committed large files, remove them from git history (I can guide you).

Deploy to Streamlit Cloud (quick)

Push repo to GitHub.

Go to https://share.streamlit.io
 → New app → connect GitHub repo.

Set Branch: main and Main file: app/streamlit_app.py.

Under Settings → Advanced → Environment variables, add:

OPENAI_API_KEY = sk-...


Deploy. Monitor logs for dependency install errors — add missing packages to requirements.txt.

Resume Screening Agent — Architecture Diagram
┌───────────────────────┐
│      User Inputs       │
│  • Job Description     │
│  • Desired Skills      │
│  • Experience Level    │
│  • Upload Resumes      │
└──────────┬────────────┘
           │
           ▼
┌─────────────────────────────┐
│      Resume Preprocessing    │
│  • PDF/DOCX Extraction       │
│  • Cleaning & Normalizing    │
│  • Skill Extraction          │
│  • Experience Estimation     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│       Embedding Layer        │
│ Sentence Transformers (MiniLM)│
│ → Converts text → 384-dim vector│
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│     Vector Database (FAISS)  │
│ • Stores all resume vectors   │
│ • Performs similarity search  │
│ • Returns top-K candidates    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│     Scoring Engine           │
│ Composite Score =            │
│ 0.55*Embedding               │
│ 0.25*Skill Match             │
│ 0.15*Experience              │
│ 0.05*Skill Richness          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   AI Enhancement Layer       │
│ OpenAI (GPT-4o-mini):        │
│ • AI Summary of Resume       │
│ • JD-Resume Match Analysis   │
│ • Recruiter Chatbot          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│         Streamlit UI         │
│ • Radar Charts               │
│ • Highlighted Skills         │
│ • CSV/Excel Export           │
│ • Live Chatbot               │
└─────────────────────────────┘




Troubleshooting (common)

ModuleNotFoundError: pdfplumber → add pdfplumber to requirements.txt and re-push.

Streamlit Cloud dependency install failed → open logs, add failing packages to requirements.txt, push again.

Large file push rejected → remove venv/ and large files from repo, add to .gitignore, then force-push a clean commit (I can guide).

Potential improvements (future)

Use a hosted vector DB (Pinecone, Milvus, Weaviate) for scale

Add RBAC + authentication

Improve parser using layout-aware PDF extraction (Donut / LayoutLM)

Add resume anonymization and PII protection / compliance

Add active learning loop to refine scoring using recruiter feedback

Contact / Author

Keerthana H L.





