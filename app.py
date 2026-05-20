import streamlit as st

from utils.logger import log_event
from automations.motivational_quotes import get_motivational_quote
from analytics.log_analyzer import get_summary_metrics
from email_system.email_summarizer import summarize_email
from profile_system.profile_generator import generate_profile
from reminders.reminder_system import (
    add_event,
    check_reminders,
    delete_event,
    edit_event,
    get_all_events
)

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

st.header("AI Motivational Quote Generator")

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

st.header("Profile Generation System")

name_input = st.text_input("Enter Name")

background_input = st.text_area(
    "Enter Background Information",
    height=150,
    placeholder="e.g. Python Developer, intern, interested in AI systems..."
)

if st.button("Generate Profile"):
    if name_input.strip() and background_input.strip():
        with st.spinner("Generating profile..."):
            profile = generate_profile(name_input, background_input)

        st.success("Profile Generated")
        st.write(profile)

    else:
        st.warning("Please enter both name and background information.")

st.header("Email Reminder System")

for key in [
    "show_view",
    "show_manage",
    "show_add",
    "show_edit"
]:
    if key not in st.session_state:
        st.session_state[key] = False

# View Events

if st.button("View Events"):
    st.session_state.show_view = not st.session_state.show_view

if st.session_state.show_view:

    st.subheader("All Events")

    events = get_all_events()

    if events:
        for e in events:
            st.write(f"{e['title']} - {e['date']}")
    else:
        st.info("No events found.")

# Manage Events

if st.button("Manage Events"):
    st.session_state.show_manage = not st.session_state.show_manage

if st.session_state.show_manage:

    st.subheader("Manage Existing Events")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add"):
            st.session_state.show_add = not st.session_state.show_add

    with col2:
        if st.button("Edit"):
            st.session_state.show_edit = not st.session_state.show_edit

# Add Events

if st.session_state.show_add:

    st.write("### Add New Event")

    event_title = st.text_input("Event Title")
    event_date = st.text_input("Event Date (YYYY-MM-DD)")

    if st.button("Add Event"):
        if event_title.strip() and event_date.strip():
            result = add_event(event_title, event_date)
            st.success(result)
        else:
            st.warning("Please enter both title and date.")

# Edit Events

if st.session_state.show_edit:

    events = get_all_events()

    if events:

        event_options = [
            f"{e['title']} ({e['date']})"
            for e in events
        ]

        selected_event = st.selectbox(
            "Select Event",
            event_options
        )

        selected_index = event_options.index(selected_event)
        selected_data = events[selected_index]

        col1, col2 = st.columns(2)

        # Delete

        with col1:
            if st.button("Delete Event"):
                result = delete_event(
                    selected_data["title"],
                    selected_data["date"]
                )
                st.success(result)

        # Edit

        with col2:

            if st.button("Edit Selected Event"):
                st.session_state.show_edit_fields = True

        if "show_edit_fields" not in st.session_state:
            st.session_state.show_edit_fields = False

        if st.session_state.show_edit_fields:

            new_title = st.text_input(
                "New Title",
                value=selected_data["title"]
            )

            new_date = st.text_input(
                "New Date",
                value=selected_data["date"]
            )

            if st.button("Update Event"):

                result = edit_event(
                    selected_data["title"],
                    selected_data["date"],
                    new_title,
                    new_date
                )

                st.success(result)

    else:
        st.info("No events available.")

st.subheader("System Analytics Overview")

metrics = get_summary_metrics()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", metrics["total_events"])
col2.metric("Success", metrics["success_count"])
col3.metric("Fallbacks", metrics["fallback_count"])
col4.metric("Errors", metrics["error_count"])