import streamlit as st 
from datetime import date
import yfinance as yf 
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go 
from plotly.subplots import make_subplots





START = "2022-01-01" 
TODAY = date.today().strftime("%Y-%m-%d")
st.title("USD/KES Analysis App" )

Currency = ["KES=X"]
selected_currency = st.selectbox("Select Currency", Currency)

n_years = st.slider("Years of Prediction",1,5)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace= True)
    return data

data_load_state = st.text("Load data...")
data = load_data(selected_currency)
data_load_state.text("Loading data...Done!")


st.subheader('Raw data')
st.write(data.tail())


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Currency Open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Currency Close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()   

#Forecasting
df_train = data[['Date','Close']]
df_train= df_train.rename(columns={"Date":"ds","Close":"y"})


m=Prophet()
m.fit(df_train)
fututre = m.make_future_dataframe(periods=period)
forecast = m.predict(fututre)

st.subheader('Forecast Data')
st.write(data.tail())



