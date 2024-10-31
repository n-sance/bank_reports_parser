from app.extractors.tbank_extractor import TBankTransactionExtractor

class TransactionExtractorFactory:
    @staticmethod
    def get_extractor(bank_name, pdf_path, config):
        if bank_name == "TBank":
            return TBankTransactionExtractor(pdf_path, config)
        # elif bank_name == "BankB":
        #     return BankBTransactionExtractor(pdf_path, config)
        else:
            raise ValueError(f"No extractor available for bank: {bank_name}")