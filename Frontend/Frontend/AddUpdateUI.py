import streamlit as st
import requests
import datetime as dt
import pandas as pd

def _api(base: str, path: str) -> str:
    return f"{base}{path}"

def add_update_ui(api_base: str):
    st.subheader("Add / Update")

    # Date input with unique key
    date = st.date_input("Date", dt.date.today(), key="add_date")

    # Editable grid for multiple rows
    df = pd.DataFrame(
        {"amount": [0.0], "category": ["Food"], "notes": [""]}
    )
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        key="add_editor"
    )

    if st.button("Submit", key="add_submit"):
        rows = []
        for _, row in edited_df.iterrows():
            if float(row["amount"]) > 0:
                rows.append({
                    "date": str(date),
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "notes": row["notes"]
                })

        if not rows:
            st.warning("Nothing to save.")
            return

        url = _api(api_base, "/expenses/bulk")
        res = requests.post(url, json={"items": rows}, timeout=10)

        if res.status_code == 200:
            st.success("Saved successfully!")
        else:
            st.error(f"Failed: {res.text}")
