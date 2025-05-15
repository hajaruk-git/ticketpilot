# 🎫 TicketPilot

TicketPilot is a simple internal support ticketing app built with Streamlit, OpenAI, and Airtable or CSV.  
It allows employees to submit issues and routes them automatically to the relevant department, while detecting urgency via GPT.

---

## 🚧 Project Status

This project is a work in progress. More AI-driven features are planned.

---

## 🚀 Features

- ✍️ Employee form: Name, Email, Category, Message
- 🤖 GPT-powered urgency detection (`High`, `Medium`, `Low`)
- 📬 Email confirmation upon ticket submission
- ☁️ Airtable or local CSV storage (configurable)
- 🛠️ Easy to extend with admin interface or automation
- 📦 Ready to deploy with `.env` configuration

---

## ⚙️ Technologies

- [Streamlit](https://streamlit.io/) — UI
- [OpenAI GPT](https://platform.openai.com/docs) — urgency classification
- [Airtable API](https://airtable.com/developers) — optional backend
- `Python`, `dotenv`, `smtplib`, `pyairtable`

---

## 🧪 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/hajaruk-git/ticketpilot.git
cd ticketpilot
```

### 2. Create and activate virtual env

```bash
python -m venv env
env\Scripts\activate    # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory using `.env.example` as reference.

---

## 📄 Example .env

```env
OPENAI_API_KEY=your_openai_key

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password

# Only required if using Airtable
AIRTABLE_API_KEY=your_airtable_token
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_NAME=tickets
```

---

## 🛠️ Configuration

In `config.py`, you can change:

- `STORAGE_MODE = "csv"` or `"airtable"`
- Available categories, statuses, urgency levels