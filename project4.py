import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.graph_objects as go 
import plotly.express as px
import datetime
from datetime import date, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm 
from statsmodels.tsa.stattools import adfuller
from importlib import reload
st = reload(st)


app_name ='Analysis Page'
st.title(app_name)



st.sidebar.header('Select the parameter from below')

START =st.sidebar.date_input('Start Date', date(2022,1,1)) 
TODAY = st.sidebar.date_input('Today', date.today())
Currency = ["KES=X"]

ticker = st.sidebar.selectbox('Select Symbol', Currency)

data = yf.download(ticker, START, TODAY)

st.subheader('Raw data')
st.write('Data From',START, 'to', TODAY)
st.write(data.tail())
st.write(data.head())

st.header(':blue[DATA VISUALIZATION]')
st.subheader(':blue[Plot of the Data]')
st.write(':red[**Note:** Select your specific data range from the sidebar, or zoom in on the plot and select your specific column]')
data.insert(0,'Date',data.index,True)
fig = px.line(data, x= 'Date', y= data.columns, title ='Closing price of the currency,', width=800, height=600)
st.plotly_chart(fig)

column= st.selectbox('Select the column to be used', data.columns[1:])

#subsetting the data
data = data[['Date',column]]
st.write("Selected data")
st.write(data)


#Test to see if the data is stationary using ADF
#st.header('Is data Stationary?')
st.warning(':red[**Note:** If p-value is less than 0.05, then data is stationary]')
st.write(adfuller(data[column])[1]<0.05)

#Decomposition of the data
st.header('Data Decomposition')
decomposition = seasonal_decompose(data[column], model='additive', period=12)
st.write(decomposition.plot())

# Plot each component separately
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

ax1.set_title('Original Data')
ax1.plot(data[column])

ax2.set_title('Trend Component')
ax2.plot(decomposition.trend)

ax3.set_title('Seasonal Component')
ax3.plot(decomposition.seasonal)

ax4.set_title('Residual Component')
ax4.plot(decomposition.resid)

# Adjust layout to prevent clipping of titles
plt.tight_layout()

# Display the plot using Streamlit
st.pyplot(fig)


#Running a model
# User input for three parameters of the model and seasonal order
p = st.slider('Select the value of p', 0,5,2)
d = st.slider('Select the value of d', 0,5,1)
q = st.slider('Select the value of q', 0,5,2)
seasonal_order =st.number_input('Select the value of seasonal p', 0 ,24, 12)

model = sm.tsa.statespace.SARIMAX(data[column],order= (p,d,q), seasonal_order=(p,d,q,seasonal_order))
model= model.fit()

#print model summary
st.header('Model Summary')
st.write(model.summary())
st.write("---")


#predict future values
st.write("<p style='color:green; font-size: 50px; font-weight:bold;'>Forecasting the data</p>", unsafe_allow_html=True)
forecast_period = st.number_input('Select the number of days to forecast', 1,365,10)

#predict the future values
predictions = model.get_prediction(start= len(data), end= len(data)+forecast_period)


predictions =predictions.predicted_mean
end_date = data.index[-1]
# Add a datetime index to the predictions with the same frequency as the original data
predictions.index = pd.date_range(start=end_date, periods=len(predictions), freq=data.index.freq)

#st.write(predictions)

# add index to the prediction

predictions.index = pd.date_range(start=end_date, periods=len(predictions), freq ='D')
predictions = pd.DataFrame(predictions)

st.write('Predictions', predictions)
st.write('Actual Data', data.tail())
st.write("---")


#plot the data
fig = go.Figure()
#add 'actual data '
fig.add_trace(go.Scatter(x=data['Date'],y=data[column], mode='lines',name='Actual', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=predictions['Date'],y=predictions['predicted_mean'], mode='lines',name='Predicted', line=dict(color='red')))
fig.update_layout(title='Actual vs Predicted', xaxis_title='Date', yaxis_title='Price', width=800, height=400)
#display the plot
st.plotly_chart(fig)


