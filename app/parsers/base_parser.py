class BaseTransactionParser:
    def __init__(self, config):
        self.config = config
    
    def parse_date(self, text):
        raise NotImplementedError("Must implement parse_date method.")
    
    def parse_amount_and_type(self, text):
        raise NotImplementedError("Must implement parse_amount_and_type method.")
    
    def parse_time(self, text):
        raise NotImplementedError("Must implement parse_time method.")
    
    def parse_card(self, description):
        raise NotImplementedError("Must implement parse_card method.")
    
    def parse_description(self, text):
        raise NotImplementedError("Must implement parse_description method.")
    
    def parse_transaction(self, text):
        date = self.parse_date(text)
        amount, transaction_type = self.parse_amount_and_type(text)
        time = self.parse_time(text)
        description = self.parse_description(text)
        card_number, card_name = self.parse_card(description)
        
        return [date, amount, transaction_type, time, card_number, card_name, description]
