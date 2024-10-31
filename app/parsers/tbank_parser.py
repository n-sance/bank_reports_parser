import re
from app.parsers.base_parser import BaseTransactionParser


class TBankTransactionParser(BaseTransactionParser):
    def __init__(self, config):
        self.date_pattern = re.compile(r"\b(\d{2}\.\d{2}\.\d{4})\b.*?\b(\d{2}\.\d{2}\.\d{4})\b")
        self.amount_pattern = re.compile(r"([+-]?\s*\d[\d\s]*[,.]\d{2}\s*₽)")
        self.time_pattern = re.compile(r"(\d{2}:\d{2})\s+(\d{2}:\d{2})")
        self.cards = config['cards']
        self.operation_signatures = config['descriptions']['operation_signatures']
        self.title_mappings = config['descriptions']['title_mappings']

    def parse_date(self, text):
        """Extracts the date from the transaction text."""
        date_match = self.date_pattern.search(text)
        return date_match.group(1) if date_match else ""

    def parse_amount_and_type(self, text):
        """Extracts the amount and determines if it is an income or expense."""
        amount_match = self.amount_pattern.findall(text)
        if amount_match:
            amount_raw = amount_match[0].replace("₽", "").replace(",", ".").replace(" ", "").strip()
            amount = abs(float(amount_raw))
            transaction_type = "доход" if "+" in amount_raw else "расход"
            return amount, transaction_type
        return 0.0, ""

    def parse_time(self, text):
        """Extracts the transaction time in hh:mm format. If multiple times are found, returns the last one."""
        times = re.findall(r"\b\d{2}:\d{2}\b", text)
        return times[-1] if times else ""

    def parse_card(self, description):
        """Finds and identifies the card number in the description text."""
        found_cards = re.findall(r"(?:^|\s)(\d{4})(?=\s|$)", description)
        for card_num in found_cards:
            if card_num in self.cards:
                return card_num, self.cards[card_num]
        return "", "Неизвестная карта"

    def parse_description(self, text):
        """Extracts the description from the transaction text."""
        return text.split("₽")[-1].strip() if "₽" in text else ""

    def determine_operation_type(self, description):
        """Determines the operation type based on keywords in the description."""
        for keyword, operation_type in self.operation_signatures.items():
            if keyword.lower() in description.lower():
                return operation_type
        return "Неизвестный тип"

    def finalize_description(self, description):
        """Replaces parts of the description based on title mappings."""
        for keyword, replacement in self.title_mappings.items():
            if keyword.lower() in description.lower():
                return replacement
        return description

    def parse_transaction(self, text):
        """Parses a full transaction text and returns structured data."""
        date = self.parse_date(text)
        amount, transaction_type = self.parse_amount_and_type(text)
        time = self.parse_time(text)
        description = self.parse_description(text)
        operation_type = self.determine_operation_type(description)
        card_number, card_name = self.parse_card(description)
        final_description = self.finalize_description(description)
        
        return [date, amount, transaction_type, time, card_number, card_name, operation_type, final_description]
