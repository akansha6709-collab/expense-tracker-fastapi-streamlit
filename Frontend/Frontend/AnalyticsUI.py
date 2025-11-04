# Frontend/Frontend/AnalyticsUI.py
import requests
import streamlit as st
import pandas as pd
import datetime as dt

def _api(base: str, path: str) -> str:
    return f"{base}{path}"

def analytics_ui(api_base: str) -> None:
    st.subheader("Analytics")

    c1, c2 = st.columns(2)
    # UNIQUE KEYS -> prevent duplicate element id across tabs
    start = c1.date_input("Start date", dt.date(2024, 9, 1), key="an_start")
    end   = c2.date_input("End date",   dt.date(2024, 9, 30), key="an_end")

    if start > end:
        st.error("Start must be <= End")
        return

    st.markdown("#### Category totals")
    try:
        rows = requests.get(
            _api(api_base, f"/analytics/categories?start_date={start}&end_date={end}"),
            timeout=10
        ).json()
        df = pd.DataFrame(rows)
        if df.empty:
            st.info("No data.")
        else:
            df = df.sort_values("total", ascending=False).reset_index(drop=True)
            df["percent"] = (df["total"] / df["total"].sum() * 100).round(1)
            st.bar_chart(df.set_index("category")["total"])
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load category totals: {e}")
        return

    st.divider()

    st.markdown("#### Category trend (daily)")
    try:
        options = sorted({r["category"] for r in rows} or {"Food"})
        # UNIQUE KEY for selectbox too
        category = st.selectbox("Category", options=options, index=0, key="an_category")

        trows = requests.get(
            _api(api_base, f"/analytics/category-trend?category={category}&start_date={start}&end_date={end}"),
            timeout=10
        ).json()
        tdf = pd.DataFrame(trows)
        if tdf.empty:
            st.info("No trend data.")
        else:
            tdf["day"] = pd.to_datetime(tdf["day"])
            tdf = tdf.sort_values("day").set_index("day")
            st.line_chart(tdf["total"])
            st.dataframe(tdf.reset_index(), use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load trend: {e}")
