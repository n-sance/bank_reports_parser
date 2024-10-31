import yaml
import csv
from app.extractors.factory import TransactionExtractorFactory

def load_config(config_path):
    """Loads configuration from a YAML file."""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Основные настройки
pdf_path = '/Users/nsance/code/finance_parser/test_data/tbank1.pdf'
config_path = 'config.yml'
bank_name = "TBank"  # Укажите банк

# Загрузка конфигурации
config = load_config(config_path)

# Получение экстрактора и запуск процесса
transaction_extractor = TransactionExtractorFactory.get_extractor(bank_name, pdf_path, config)
transaction_extractor.extract_text_from_pdf()
transactions = transaction_extractor.filter_transactions()
parsed_transactions = transaction_extractor.parse_transactions(transactions)

# Сохранение результата в CSV
output_csv_path = config['output']['csv_path']
with open(output_csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Дата", "Сумма", "Расход/Доход", "Время", "Последние 4 цифры карты", "Название карты", "Описание"])
    writer.writerows(parsed_transactions)
print(f"Structured transaction data has been saved to {output_csv_path}")
