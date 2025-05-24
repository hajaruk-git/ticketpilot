import random
import os
from datetime import datetime, timedelta
from uuid import uuid4
from faker import Faker
from dotenv import load_dotenv
from config import STORAGE_MODE
import pytz

load_dotenv()

fake = Faker()
Faker.seed(42)

CATEGORIES = ["IT"]
URGENCY_LEVELS = ["High", "Medium", "Low"]
STATUSES = ["Open", "In Progress", "Resolved"]

messages = [
    "Can't connect to VPN",
    "Forgotten password",
    "Outlook keeps crashing",
    "Slow Wi-Fi in the office",
    "Printer not responding",
    "Blue screen error on startup",
    "Unable to access shared drive",
    "Teams app not opening",
    "Computer won't boot",
    "Keyboard unresponsive"
]

def generate_ticket():
    created_at = datetime.now() - timedelta(days=random.randint(0, 120))
    created_at = created_at.replace(tzinfo=pytz.UTC)
    return {
        "Name": fake.name(),
        "TicketID": f"TICKET-{uuid4().hex[:8].upper()}",
        "CreatedAt": created_at.isoformat(),
        "Email": fake.email(),
        "Category": random.choice(CATEGORIES),
        "Message": random.choice(messages),
        "Urgency": random.choice(URGENCY_LEVELS),
        "Status": random.choice(STATUSES)
    }

def store_ticket_csv(ticket_data):
    import csv
    file_path = "tickets.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=ticket_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(ticket_data)

def store_ticket_airtable(ticket_data):
    from pyairtable import Table

    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")

    if not all([api_key, base_id, table_name]):
        raise ValueError("Missing Airtable credentials in .env file")

    table = Table(api_key, base_id, table_name)
    table.create(ticket_data)

for i in range(100):
    ticket = generate_ticket()

    try:
        if STORAGE_MODE == "csv":
            store_ticket_csv(ticket)
        elif STORAGE_MODE == "airtable":
            store_ticket_airtable(ticket)
        else:
            raise ValueError("Invalid STORAGE_MODE in config.py")
    except Exception as e:
        print(f"Error creating ticket {ticket['TicketID']}: {e}")

print("\u2705 100 dummy tickets generated and stored.")
