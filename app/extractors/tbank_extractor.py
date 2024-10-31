from app.extractors.base_extractor import BaseTransactionExtractor
from app.parsers.factory import TransactionParserFactory

class TBankTransactionExtractor(BaseTransactionExtractor):
    def __init__(self, pdf_path, config):
        super().__init__(pdf_path, config)
        self.parser = TransactionParserFactory.get_parser("TBank", config)

    def filter_transactions(self):
        """Bank-specific logic to filter transaction lines from extracted text."""
        transactions = []
        lines = self.all_text.splitlines()
        i = 0

        while i < len(lines):
            date_match = self.parser.parse_date(lines[i])
            if date_match:
                transaction = lines[i]
                
                # Append the next line if it's part of the transaction
                if i + 1 < len(lines):
                    transaction += " " + lines[i + 1]
                    i += 1
                
                transactions.append(transaction)
            i += 1
        return transactions

    def parse_transactions(self, transactions):
        """Uses the bank-specific parser to parse each transaction."""
        parsed_transactions = []
        for transaction in transactions:
            parsed_transactions.append(self.parser.parse_transaction(transaction))
        return parsed_transactions