from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        if not text.strip():
            return None, "The PDF does not contain readable text."

        return text.strip(), None

    except Exception as e:
        return None, f"Unable to read the PDF: {str(e)}"