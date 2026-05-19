import streamlit as st

from utils.logger import log_event
from automations.motivational_quotes import get_motivational_quote

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