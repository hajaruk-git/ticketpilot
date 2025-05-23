# 🎫 TicketPilot

TicketPilot is a lightweight internal ticketing system built with Streamlit, OpenAI, and Airtable (or CSV).  
It allows employees to submit IT support requests while integrating AI to enhance ticket management.

GPT is used to:
- Automatically classify the urgency level of each ticket (High, Medium, Low)
- Generate quarterly analytical reports identifying the most frequent issues and improvement areas

---

## 🚧 Project Status

This project is a work in progress.

---

## 🚀 Features

- ✍️ Employee ticket submission form (Name, Email, Category, Message)
- 🤖 Automatic urgency classification powered by GPT-3.5 (`High`, `Medium`, `Low`)
- 📬 Email confirmation sent to the user upon ticket creation
- ☁️ Flexible data storage: Airtable or local CSV (configurable)
- 📊 **Quarterly analysis module** powered by GPT-4:
  - Identifies the most frequent IT issues over a selected quarter
  - Categorizes problems by theme (network, access, hardware…)
  - Outputs a structured markdown report for internal review

---

## ⚙️ Technologies

- [Streamlit](https://streamlit.io/) — UI
- [OpenAI GPT](https://platform.openai.com/docs) — urgency classification and quarterly analysis
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