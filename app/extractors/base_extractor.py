import pdfplumber

class BaseTransactionExtractor:
    def __init__(self, pdf_path, config):
        self.pdf_path = pdf_path
        self.config = config
        self.all_text = ""

    def extract_text_from_pdf(self):
        """Extracts text from all pages of the PDF."""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                self.all_text += page.extract_text() + "\n"

    def filter_transactions(self):
        """Filters and processes transaction lines from the extracted text."""
        raise NotImplementedError("Must implement filter_transactions method.")

    def parse_transactions(self, transactions):
        """Parses filtered transactions and returns structured data."""
        raise NotImplementedError("Must implement parse_transactions method.")
