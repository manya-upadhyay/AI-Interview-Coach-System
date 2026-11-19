import fitz

def extract_text(file_path):
    if file_path.lower().endswith(".docx"):
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs if p.text])
        except Exception as e:
            return f"Error reading DOCX: {e}"
    else:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
