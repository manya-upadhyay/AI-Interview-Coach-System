import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def _safe(value):
    return str(value if value is not None else "").strip()


def generate_pdf(report_text):
    os.makedirs("reports", exist_ok=True)
    file_path = "reports/interview_report.pdf"

    doc = SimpleDocTemplate(
        file_path, pagesize=A4, rightMargin=42, leftMargin=42,
        topMargin=42, bottomMargin=42
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=20, leading=24, alignment=TA_CENTER, spaceAfter=16,
        textColor=colors.HexColor("#1D4ED8")
    )
    heading = ParagraphStyle(
        "Heading", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, leading=16, spaceBefore=10, spaceAfter=6,
        textColor=colors.HexColor("#111827")
    )
    body = ParagraphStyle(
        "Body", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=10.5, leading=15, spaceAfter=5, textColor=colors.HexColor("#1F2937")
    )

    story = [Paragraph("AI Interview Performance Report", title_style)]

    if isinstance(report_text, dict):
        r = report_text
        score = _safe(r.get("overall_score", 0))
        story.append(Paragraph(f"Overall Score: <b>{score}/10</b>", heading))

        rows = [["Category", "Score"]]
        for key, label in [("technical", "Technical"), ("communication", "Communication"),
                           ("problem_solving", "Problem Solving"), ("confidence", "Confidence")]:
            if key in r:
                rows.append([label, _safe(r.get(key))])
        if len(rows) > 1:
            table = Table(rows, colWidths=[250, 150])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E0E7FF")),
                ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#1E3A8A")),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0,0), (-1,-1), 7),
            ]))
            story += [table, Spacer(1, 10)]

        for key, label in [("strengths", "Strengths"), ("weaknesses", "Areas for Improvement"),
                           ("suggestions", "Recommendations")]:
            value = r.get(key, [])
            story.append(Paragraph(label, heading))
            if isinstance(value, list):
                for item in value:
                    story.append(Paragraph("• " + _safe(item), body))
            else:
                story.append(Paragraph(_safe(value), body))

        if r.get("final_recommendation"):
            story.append(Paragraph("Final Recommendation", heading))
            story.append(Paragraph(_safe(r["final_recommendation"]), body))
    else:
        for part in _safe(report_text).splitlines():
            if part.strip():
                story.append(Paragraph(part.replace("&", "&amp;"), body))

    doc.build(story)
    return file_path
