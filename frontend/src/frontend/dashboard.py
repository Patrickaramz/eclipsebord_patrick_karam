import streamlit as st
import httpx
import pandas as pd
import os 

# Sätt sidkonfiguration för en snyggare look
st.set_page_config(
    page_title="EclipseBord Dashboard",
    layout="wide"
)

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def main():
    # Sidofält med inställningar och sökfilter
    st.sidebar.markdown("# Inställningar")
    st.sidebar.write(f"Ansluter till backend:")
    st.sidebar.code(BASE_URL)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("# Sökfilter")
    search_query = st.sidebar.text_input("Sök i tabellerna (t.ex. år eller månad):", "")

    # Huvudtitel
    st.markdown("# EclipseBord Dashboard")
    st.markdown("Välkommen till din central för sol och måndata.")
    st.markdown("---")

    # Hämta och visa Solar data
    try:
        solar_response = httpx.get(f"{BASE_URL}/solar")
        if solar_response.status_code == 200:
            solar_data = solar_response.json()
            df_solar = pd.DataFrame(solar_data)

            # Filtrera data om användaren har skrivit något i sökfältet
            if search_query:
                # Konvertera alla kolumner till strings för enklare matchning
                mask = df_solar.astype(str).apply(lambda col: col.str.contains(search_query, case=False, na=False)).any(axis=1)
                df_solar_filtered = df_solar[mask]
            else:
                df_solar_filtered = df_solar
            
            # Visa KPI mätare
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Visade solförmörkelser", value=len(df_solar_filtered), delta=f"Totalt: {len(df_solar)}")
            
            st.markdown("## Solar Data")
            st.dataframe(df_solar_filtered, use_container_width=True)
        else:
            st.error("Kunde inte hämta sol-data från backenden.")
    except Exception as e:
        st.error(f"Kunde inte ansluta till servern: {e}")

    st.markdown("---")

    # Hämta och visa Lunar data
    try:
        lunar_response = httpx.get(f"{BASE_URL}/lunar")
        if lunar_response.status_code == 200:
            lunar_data = lunar_response.json()
            df_lunar = pd.DataFrame(lunar_data)

            # Filtrera data om användaren har skrivit något i sökfältet
            if search_query:
                mask = df_lunar.astype(str).apply(lambda col: col.str.contains(search_query, case=False, na=False)).any(axis=1)
                df_lunar_filtered = df_lunar[mask]
            else:
                df_lunar_filtered = df_lunar
            
            # Visa KPI-mätare
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Visade månförmörkelser", value=len(df_lunar_filtered), delta=f"Totalt: {len(df_lunar)}")

            st.markdown("## Lunar Data")
            st.dataframe(df_lunar_filtered, use_container_width=True)
        else:
            st.error("Kunde inte hämta måndata från backenden.")
    except Exception as e:
        st.error(f"Kunde inte ansluta till servern: {e}")

if __name__ == "__main__":
    main()