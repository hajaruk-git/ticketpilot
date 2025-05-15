
import streamlit as st
from datetime import datetime
from uuid import uuid4
from config import CATEGORIES, URGENCY_LEVELS, STATUSES, STORAGE_MODE
from storage import store_ticket_csv, store_ticket_airtable
import openai
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(to, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

st.set_page_config(page_title="TicketPilot", page_icon="🎫")
st.title("🎫 TicketPilot - Submit a Support Ticket")

with st.form("ticket_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    category = st.selectbox("Category", CATEGORIES)
    message = st.text_area("Describe your issue")

    submitted = st.form_submit_button("Submit Ticket")

if submitted:
    ticket_id = f"TICKET-{uuid4().hex[:8].upper()}"
    created_at = datetime.now().isoformat()

    prompt = f"""
You are a support assistant. Classify the urgency of the following message into one of three levels:
- High: system is unusable, work is blocked
- Medium: disruptive but a workaround exists
- Low: minor inconvenience

Message:
```{message}```

Respond with only one word: High, Medium, or Low.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1,
            temperature=0
        )
        urgency = response["choices"][0]["message"]["content"].strip()
        if urgency not in URGENCY_LEVELS:
            urgency = "Medium"
    except Exception as e:
        st.error(f"Error detecting urgency: {e}")
        urgency = "Medium"

    ticket_data = {
        "Name": name,
        "TicketID": ticket_id,
        "CreatedAt": created_at,
        "Email": email,
        "Category": category,
        "Message": message,
        "Urgency": urgency,
        "Status": "Open"
    }

    try:
        if STORAGE_MODE == "csv":
            store_ticket_csv(ticket_data)
        elif STORAGE_MODE == "airtable":
            store_ticket_airtable(ticket_data)
        else:
            raise ValueError("Invalid STORAGE_MODE in config.py")

        st.success(f"✅ Ticket submitted successfully! Your ID is {ticket_id}")

        # Email confirmation after submission
        email_subject = f"🎫 Ticket {ticket_id} Received"
        email_body = f"""
Hello {name},

Your support ticket has been received and routed to the appropriate service.

Ticket ID: {ticket_id}
Category: {category}
Urgency: {urgency}

Message:
{message}

We will get back to you as soon as possible.

- TicketPilot
"""
        send_email(email, email_subject, email_body)

    except Exception as e:
        st.error(f"❌ Failed to store ticket or send confirmation: {e}")
