# Frontend/ViewDeleteUI.py
import datetime as dt
import requests
import streamlit as st
import pandas as pd

def _api(base: str, path: str) -> str:
    return f"{base}{path}"

def view_delete_ui(api_base: str) -> None:
    st.subheader("View / Delete")

    # Unique key so it doesn't clash with date_inputs in other tabs
    date = st.date_input("Date", dt.date.today(), key="vd_date")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Load", type="primary", key="vd_load"):
            try:
                url = _api(api_base, f"/expenses?expense_date={date}")
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                rows = resp.json()
                if not rows:
                    st.info("No expenses for this date.")
                    st.session_state["vd_rows"] = []
                else:
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True)
                    st.session_state["vd_rows"] = rows
                    st.success(f"Loaded {len(rows)} row(s) for {date}")
            except Exception as e:
                st.error(f"Fetch failed: {e}")

    with c2:
        if st.button("Delete ALL rows for this date", key="vd_delete"):
            try:
                del_url = _api(api_base, f"/expenses?expense_date={date}")
                resp = requests.delete(del_url, timeout=10)
                resp.raise_for_status()
                st.success(f"Deleted all rows for {date}")
                st.session_state["vd_rows"] = []
            except Exception as e:
                st.error(f"Delete failed: {e}")

    # Show last loaded rows (if any) below the buttons too
    rows = st.session_state.get("vd_rows", [])
    if rows:
        st.write("Last loaded rows:")
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
