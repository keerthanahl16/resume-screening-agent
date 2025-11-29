# app/utils.py
from pathlib import Path
from app.resume_parser import load_resume_text, parse_resume_sections
from app.embedder import embed_texts
from app.search import create_index

def build_index_from_folder(folder="data/resumes"):
    folder = Path(folder)
    files = sorted([f for f in folder.iterdir() if f.is_file()])
    docs = []
    metas = []
    for f in files:
        text = load_resume_text(f)
        parsed = parse_resume_sections(text)
        # Create search_text containing skills + experience + education
        search_text = " ".join([
            " ".join(parsed.get("skills", [])),
            parsed.get("experience", ""),
            parsed.get("education", "")
        ]).strip()
        if not search_text:
            search_text = parsed["full_text"][:2000]
        docs.append(search_text)
        metas.append({
            "file": f.name,
            "full_text": parsed["full_text"],
            "skills": parsed.get("skills", []),
            "years_experience": parsed.get("years_experience", 0)
        })
    if not docs:
        return 0
    embeddings = embed_texts(docs)
    create_index(embeddings, metas)
    return len(docs)
