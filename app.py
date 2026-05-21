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
    get_all_events,
    process_reminders
)

st.markdown("## Dashboard Navigation")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Quotes"):
        st.markdown('<a href="#motivational-quotes"></a>', unsafe_allow_html=True)

with col2:
    if st.button("Email"):
        st.markdown('<a href="#email-analysis"></a>', unsafe_allow_html=True)

with col3:
    if st.button("Profiles"):
        st.markdown('<a href="#profile-generation"></a>', unsafe_allow_html=True)

with col4:
    if st.button("Events"):
        st.markdown('<a href="#event-system"></a>', unsafe_allow_html=True)

with col5:
    if st.button("Analytics"):
        st.markdown('<a href="#system-analytics-overview"></a>', unsafe_allow_html=True)

st.markdown("""
<script>
const anchors = document.querySelectorAll("a");
anchors.forEach(a => a.click());
</script>
""", unsafe_allow_html=True)

process_reminders()

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
st.markdown('<a id="motivational-quotes"></a>', unsafe_allow_html=True)

if st.button("Generate AI Quote"):
    with st.spinner("Generating quote..."):
        quote = get_motivational_quote()

        st.info(quote)

st.header("Email Analysis System")
st.markdown('<a id="email-analysis"></a>', unsafe_allow_html=True)

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
st.markdown('<a id="profile-generation"></a>', unsafe_allow_html=True)

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

st.header("Event System")
st.markdown('<a id="event-system"></a>', unsafe_allow_html=True)

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
            st.markdown(f"""
            ### {e['title']}
            - Date: {e['date']}
            - Reminder Enabled: {"Yes" if e.get("reminder_enabled") else "No"}
            """)
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

    set_reminder = st.checkbox("Set Reminder")

    event_email = None

    if set_reminder:
        event_email = st.text_input("Reminder Email")

    if st.button("Add Event"):
        if event_title.strip() and event_date.strip():

            result = add_event(
                event_title,
                event_date,
                event_email if set_reminder else None,
                set_reminder
            )

            st.success(result)

        else:
            st.warning("Please enter both title and date.")

# Edit Events

if st.session_state.show_edit:

    st.subheader("Edit Existing Event")

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

        st.write("### Event Details")

        updated_title = st.text_input(
            "Event Title",
            value=selected_data["title"]
        )

        updated_date = st.text_input(
            "Event Date (YYYY-MM-DD)",
            value=selected_data["date"]
        )

        reminder_enabled = st.checkbox(
            "Set Reminder",
            value=selected_data.get("reminder_enabled", False)
        )

        updated_email = None

        if reminder_enabled:
            updated_email = st.text_input(
                "Reminder Email",
                value=selected_data.get("email", "")
            )

        col1, col2 = st.columns(2)


        with col1:

            if st.button("Save Changes"):

                result = edit_event(
                    selected_data["title"],
                    selected_data["date"],
                    updated_title,
                    updated_date,
                    reminder_enabled,
                    updated_email if reminder_enabled else None
                )

                st.success(result)

        with col2:

            if st.button("Delete Event"):

                result = delete_event(
                    selected_data["title"],
                    selected_data["date"],
                )

                st.success(result)

    else:
        st.info("No events available.")

st.subheader("System Analytics Overview")
st.markdown('<a id="system-analytics-overview"></a>', unsafe_allow_html=True)

metrics = get_summary_metrics()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Actions Logged", metrics["total_events"])
col2.metric("Success", metrics["success_count"])
col3.metric("Fallbacks", metrics["fallback_count"])
col4.metric("Errors", metrics["error_count"])