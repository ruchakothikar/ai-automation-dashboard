# AI Automation Dashboard

An AI-powered operations dashboard built with Python and Streamlit that automates workflow tasks including email summarization, profile generation, event reminder automation, quote generation, analytics tracking, and AI-generated content workflows.

---

# Overview

AI Automation Dashboard is a centralized automation platform designed to streamline repetitive operational workflows using GPT-powered AI systems and Python-based automation pipelines.

The platform integrates multiple AI-assisted utilities into a single dashboard interface, including:

- AI email summarization
- AI profile generation
- Automated event reminder workflows
- Real email notification system
- AI motivational quote generation
- System logging and analytics monitoring

The project demonstrates practical integration of AI-driven automation into business-style workflows using modular Python architecture.

---

# Features

## AI Motivational Quote Generator
- Generates AI-powered motivational quotes using GPT models
- Demonstrates AI text generation workflows
- Includes system logging and monitoring

## Email Analysis System
- Summarizes long-form email content using AI
- Converts unstructured text into concise summaries
- Handles API failures with fallback logging

## Profile Generation System
- Generates structured professional profiles from background information
- Produces formatted summaries, descriptions, and key traits
- Demonstrates AI-assisted content generation workflows

## Event Reminder Automation
- Add, edit, and delete events
- Optional reminder email configuration
- Automated reminder triggering within 5 days of events
- Real SMTP email integration using Gmail App Passwords
- Persistent JSON-based event storage

## System Analytics
- Tracks:
  - total logged actions
  - successful operations
  - fallback responses
  - system errors
- Reads analytics directly from automation logs

---

# System Architecture

The project follows a modular architecture:

```text
app.py
│
├── analytics/
│   └── log_analyzer.py
│
├── automations/
│   └── motivational_quotes.py
│
├── email_system/
│   ├── email_sender.py
│   └── email_summarizer.py
│
├── logs/
│   └── automation_logs.csv
│
├── profile_system/
│   └── profile_generator.py
│
├── reminders/
│   └── reminder_system.py
│
├── services/
│   └── openai_service.py
│
├── utils/
│   └── logger.py
│
└── app.py
```

---

# Technologies Used

- Python
- Streamlit
- OpenAI API
- Pandas
- SMTP Email Automation
- JSON Storage
- dotenv
- CSV Logging System

---

# Installation & Setup

## Clone Repository

```bash
git clone https://github.com/ruchakothikar/ai-automation-dashboard.git
cd ai-automation-dashboard
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key

SENDER_EMAIL=your_demo_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

---

# Running the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

---

# Logging & Analytics

The platform includes centralized logging through:

```text
logs/automation_logs.csv
```

Tracked information includes:
- timestamps
- task names
- success/failure status
- automation details
- fallback events
- reminder activity

Analytics are displayed directly inside the dashboard UI.