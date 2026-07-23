import fitz
from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF.
    """

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def create_cover_letter_pdf(cover_letter):
    """
    Create a professional PDF cover letter.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    body_style = styles["BodyText"]
    body_style.leading = 24

    story = []

    story.append(
        Paragraph(
            "Professional Cover Letter",
            title_style
        )
    )

    story.append(
        Paragraph("<br/><br/>", body_style)
    )

    for line in cover_letter.split("\n"):

        if line.strip():

            story.append(
                Paragraph(line, body_style)
            )

        else:

            story.append(
                Paragraph("<br/>", body_style)
            )

    document.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf