import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_pdf(report_text):
    os.makedirs("reports", exist_ok=True)
    file_path = "reports/interview_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    story = []

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1D4ED8')
    )

    story.append(Paragraph("🎯 AI Interview Performance Report", title_style))
    story.append(Spacer(1, 15))

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#1F2937')
    )

    formatted_text = report_text.replace("\n", "<br/>")
    story.append(Paragraph(formatted_text, body_style))

    doc.build(story)

    return file_path