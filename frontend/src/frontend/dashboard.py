import streamlit as st
import httpx
import pandas as pd
import os 

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def main():
    st.markdown("# EclipseBord Dashboard")
    st.write(f"Ansluter till backend: {BASE_URL}")

    st.markdown("Allt du behöver veta om sol och måndata")

    # Hämta och visa Solar-data
    st.markdown("## Solar Data")
    try:
        solar_response = httpx.get(f"{BASE_URL}/solar")
        if solar_response.status_code == 200:
            solar_data = solar_response.json()
            df_solar = pd.DataFrame(solar_data)
            st.dataframe(df_solar)
        else:
            st.error("Kunde inte hämta sol-data från backenden.")
    except Exception as e:
        st.error(f"Kunde inte ansluta till servern: {e}")

    # Hämta och visa Lunar-data (Detta lägger du till)
    st.markdown("## Lunar Data")
    try:
        lunar_response = httpx.get(f"{BASE_URL}/lunar")
        if lunar_response.status_code == 200:
            lunar_data = lunar_response.json()
            df_lunar = pd.DataFrame(lunar_data)
            st.dataframe(df_lunar)
        else:
            st.error("Kunde inte hämta måndata från backenden.")
    except Exception as e:
        st.error(f"Kunde inte ansluta till servern: {e}")

if __name__ == "__main__":
    main()