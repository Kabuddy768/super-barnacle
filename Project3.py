import streamlit as st
import requests
import time

# Alpha Vantage API key (replace with your own)
api_key = "KVXS88KQTDFM2MCL"

# Function to fetch real-time currency data from Alpha Vantage
def get_currency_data(from_currency, to_currency):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

# Main app logic
st.title("Real-Time KES/USD Exchange Rate (Alpha Vantage)")

current_rate = get_currency_data("USD", "KES")
st.metric("Current Rate", current_rate, f"USD 1 = {current_rate:.4f} KES")

# Simulate interval behavior using query parameters
#query_params = st.experimental_get_query_params()
#query_params = st.query_params()
#refreshed = st.button("Refresh Data")
# Simulate interval behavior using session state
refreshed = st.button("Refresh Data")
if 'refreshed' not in st.session_state:
    st.session_state.refreshed = False

while True:
    if refreshed:
        current_rate = get_currency_data("USD", "KES")
        st.metric("Current Rate", current_rate, f"USD 1 = {current_rate:.4f} KES")
        st.session_state.refreshed = False
        #st.query_params(refreshed=False)
        #st.experimental_set_query_params(refreshed=False)
    time.sleep(60)
