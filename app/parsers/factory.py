from app.parsers.tbank_parser import TBankTransactionParser


class TransactionParserFactory:
    @staticmethod
    def get_parser(bank_name, config):
        if bank_name == "TBank":
            return TBankTransactionParser(config)
        # elif bank_name == "BankB":
        #     return BankBTransactionParser(config)
        # else:
            raise ValueError(f"No parser available for bank: {bank_name}")
