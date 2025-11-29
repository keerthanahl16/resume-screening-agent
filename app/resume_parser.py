# app/resume_parser.py

import pdfplumber
import docx2txt
import re
from pathlib import Path
from datetime import datetime

# -------------------------------
# TEXT EXTRACTION
# -------------------------------
def extract_text_from_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_text_from_docx(path):
    return docx2txt.process(path)

def load_resume_text(path):
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(str(p))
    elif suffix in [".doc", ".docx"]:
        return extract_text_from_docx(str(p))
    else:
        return p.read_text(encoding="utf-8", errors="ignore")

# -------------------------------
# CONTACT INFORMATION EXTRACTION
# -------------------------------
def extract_email(text):
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return m.group(0) if m else None

def extract_phone(text):
    m = re.search(r"(\+?\d[\d\-\s]{8,15})", text)
    return m.group(0) if m else None

def extract_linkedin(text):
    m = re.search(r"(https?://)?(www\.)?linkedin\.com/[A-Za-z0-9_/.-]+", text)
    return m.group(0) if m else None

def extract_name(text):
    lines = text.strip().split("\n")
    if lines:
        first_line = lines[0].strip()
        if 1 <= len(first_line.split()) <= 5:
            return first_line
    return "Unknown"

# -------------------------------
# SKILL EXTRACTION
# -------------------------------
COMMON_SKILLS = [
    "python","java","c++","c#","sql","pandas","numpy","tensorflow",
    "pytorch","scikit-learn","machine learning","deep learning",
    "react","node","aws","azure","docker","kubernetes","excel",
    "nlp","computer vision","javascript","html","css"
]

def extract_skills(text):
    t = text.lower()
    
    found = set()

    # global skill search
    for s in COMMON_SKILLS:
        if s in t:
            found.add(s)

    # section-based skill search
    m = re.search(r"(skills|technical skills)[:\n](.*?)(\n[A-Z][a-z]+:|\Z)",
                  text, re.S | re.I)

    if m:
        skills_block = m.group(2)
        for part in re.split(r"[,\n/;•\-]", skills_block):
            clean = part.strip().lower()
            if clean:
                found.add(clean)

    return list(found)[:50]

# -------------------------------
# EXPERIENCE CALCULATION
# -------------------------------
def estimate_years_experience(text):
    years = []
    text = text.lower()

    # pattern: 2018–2022
    for m in re.finditer(r"(19|20)\d{2}\s*(?:-|–|—|to)\s*(present|19\d{2}|20\d{2})", text):
        start = int(m.group(0)[:4])
        end_token = m.group(2)
        end = datetime.now().year if "present" in end_token else int(end_token)
        years.append(max(0, end - start))

    # pattern: since 2018
    for m in re.finditer(r"(since|from)\s*(19|20)\d{2}", text):
        start = int(m.group(0)[-4:])
        years.append(datetime.now().year - start)

    return sum(years) if years else 0

# -------------------------------
# MAIN PARSER
# -------------------------------
def parse_resume_sections(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    full_text = "\n".join(lines)

    # Extract structured fields
    skills = extract_skills(full_text)
    years_exp = estimate_years_experience(full_text)

    # extract experience section
    exp_section = ""
    exp_m = re.search(
        r"(experience|work experience|employment history)[:\n](.*?)(\neducation[:\n]|\nprojects[:\n]|\Z)",
        full_text, re.S | re.I)
    if exp_m:
        exp_section = exp_m.group(2).strip()

    # extract education section
    edu_section = ""
    edu_m = re.search(
        r"(education|academic qualifications)[:\n](.*?)(\n[A-Z][a-z]+:|\Z)",
        full_text, re.S | re.I)
    if edu_m:
        edu_section = edu_m.group(2).strip()

    return {
        "full_text": full_text,
        "name": extract_name(full_text),
        "email": extract_email(full_text),
        "phone": extract_phone(full_text),
        "linkedin": extract_linkedin(full_text),
        "skills": skills,
        "experience": exp_section,
        "education": edu_section,
        "years_experience": years_exp
    }
