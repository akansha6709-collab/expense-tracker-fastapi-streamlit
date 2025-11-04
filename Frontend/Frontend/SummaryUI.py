# Frontend/SummaryUI.py
import requests
import streamlit as st
import pandas as pd
import datetime as dt

def _api(base: str, path: str) -> str:
    return f"{base}{path}"

def summary_ui(api_base: str) -> None:
    st.subheader("Summary")

    c1, c2 = st.columns(2)
    # give unique keys for this tab
    start = c1.date_input("Start date", dt.date(2024, 9, 1), key="sum_start")
    end   = c2.date_input("End date",   dt.date(2024, 9, 30), key="sum_end")

    if start > end:
        st.error("Start must be <= End")
        return

    url = _api(api_base, f"/summary?start_date={start}&end_date={end}")
    try:
        rows = requests.get(url, timeout=10).json()
        df = pd.DataFrame(rows)
        if df.empty:
            st.info("No data in this range.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load summary: {e}")
