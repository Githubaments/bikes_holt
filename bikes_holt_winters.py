import streamlit as st
import requests
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Dublin Bikes API endpoint
API_ENDPOINT = 'https://api.jcdecaux.com/vls/v1/stations/{}'

# API key (replace with your own key)
API_KEY = 'your_api_key'

# Station number
station_number = st.text_input('Enter the station number')

# Time (in minutes from now)
time = st.number_input('Enter the time (in minutes from now)')

if station_number and time:
    # Get station information from the API
    response = requests.get(API_ENDPOINT.format(station_number), params={'apiKey': API_KEY})
    station = response.json()

    # Get available bikes
    available_bikes = station['available_bikes']

    # Create Holt-Winters model
    model = ExponentialSmoothing(available_bikes)

    # Fit model
    model = model.fit()

    # Make predictions
    predictions = model.predict(len(available_bikes), len(available_bikes) + time)

    st.write('Predicted number of bikes at time {}: {}'.format(time, predictions[-1]))
