import streamlit as st

from utils.logger import log_event
from automations.motivational_quotes import get_motivational_quote
from analytics.log_analyzer import get_summary_metrics
from email_system.email_summarizer import summarize_email

st.set_page_config(page_title="AI Automation Dashboard")

st.title("AI Operations Automation Dashboard")

st.markdown("""
This system demonstrates AI-powered automation workflows including:
            
            -Email summarization pipeline
            -Reminder automation system
            -Motivational quote generator
            -Workflow logging and monitoring
            -Dashboard analytics and trend tracking
"""
           )

st.success("System initialized successfully.")

st.subheader("AI Motivational Quote Generator")

if st.button("Generate AI Quote"):
    with st.spinner("Generating quote..."):
        quote = get_motivational_quote()

        st.info(quote)

st.header("Email Analysis System")

email_input = st.text_area(
    "Paste Email Content",
    height=200,
    placeholder="Paste email text here..."
)

if st.button("Generate Email Summary"):
    if email_input.strip():
        with st.spinner("Summarizing email..."):
            summary = summarize_email(email_input)

        st.success("Summary Generated")
        st.write(summary)

    else:
        st.warning("Please paste email content first.")

st.subheader("System Analytics Overview")

metrics = get_summary_metrics()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", metrics["total_events"])
col2.metric("Success", metrics["success_count"])
col3.metric("Fallbacks", metrics["fallback_count"])
col4.metric("Errors", metrics["error_count"])