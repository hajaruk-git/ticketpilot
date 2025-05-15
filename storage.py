import csv
import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

def store_ticket_csv(ticket_data):
    file_path = "tickets.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=ticket_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(ticket_data)

def store_ticket_airtable(ticket_data):
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")

    if not all([api_key, base_id, table_name]):
        raise ValueError("Missing Airtable credentials in .env file")

    table = Table(api_key, base_id, table_name)
    table.create(ticket_data)