# Frontend/app.py
import streamlit as st

from AddUpdateUI import add_update_ui
from ViewDeleteUI import view_delete_ui
from SummaryUI import summary_ui
from AnalyticsUI import analytics_ui

st.set_page_config(page_title="Expense Tracker", layout="wide")

def main() -> None:
    st.title("Expense Tracking System")

    # Render this ONCE and pass it to the tabs
    api_base = st.sidebar.text_input(
        "API base URL",
        value="http://127.0.0.1:8000",
        key="api_base",              # ensure a stable key
    ).rstrip("/")
    st.session_state["API_BASE"] = api_base  # optional convenience

    tab1, tab2, tab3, tab4 = st.tabs(["Add / Update", "View / Delete", "Summary", "Analytics"])

    with tab1:
        add_update_ui(api_base)

    with tab2:
        view_delete_ui(api_base)

    with tab3:
        summary_ui(api_base)

    with tab4:
        analytics_ui(api_base)

if __name__ == "__main__":
    main()
