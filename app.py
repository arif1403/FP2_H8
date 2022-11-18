import streamlit as st
import pandas as pd
import pickle
from PIL import Image

model1 = pickle.load(open('model/classifier_logreg','rb'))
# model2 = pickle.load(open('model/classifier_svm','rb'))

img = Image.open('img/favicon.ico')
im = Image.open('img/favicon-sunny.ico')
st.set_page_config(page_title="Rainfall Prediction App",page_icon=img,layout="centered",initial_sidebar_state="expanded")

html_temp = """ 
    <div style ="background-color:#bd0d21;padding:13px"> 
    <h1 style ="color:white;text-align:center;">Rainfall Prediction in Australia</h1> 
    </div> 
    """
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html=True)

st.write("""
---

""")

def user_input_parameters():
    min_temp = st.number_input("Minimum Temperature °C:")
    max_temp = st.number_input("Maximum Temperature °C:")
    rainfall = st.number_input("Rainfall (in mm) :")
    wind_gust_dir = st.selectbox('Wind Gust Direction : ',['West Wind','West-Northwest Wind','West-Southwest Wind','Northeast Wind','North-Northwest Wind',
                                                           'North Wind','North-Northeast Wind','Southwest Wind','East-Northeast Wind','South-Southeast Wind',
                                                           'South Wind','Northwest Wind','Southeast Wind','East-Southeast Wind','East Wind','South-Southwest Wind'])
    wind_gust_speed = st.slider('Wind Gust Speed :',0,150,45)
    wind_speed_9am = st.slider('Wind Speed at 9 am :',0,150,20)
    humidity_9am = st.slider('Humidity at 9 am (%):',0,150,77)
    humidity_3pm = st.slider('Humidity at 3 pm (%):',0,150,77)
    pressure_9am = st.number_input('Pressure at 9 am :')
    temp_9am = st.number_input('Temperature at 9 am :')
    temp_3pm = st.number_input('Temperature at 3 pm :')
    rain_today = st.radio('Rain Today ?', ['Yes','No'])


    #Logic Wind direction
    if wind_gust_dir == 'West Wind':
        wind_gust_dir = 0
    elif wind_gust_dir == 'West-Northwest Wind':
        wind_gust_dir = 1
    elif wind_gust_dir == 'West-Southwest Wind':
        wind_gust_dir = 2
    elif wind_gust_dir == 'Northeast Wind':
        wind_gust_dir = 3
    elif wind_gust_dir == 'North-Northwest Wind':
        wind_gust_dir = 4
    elif wind_gust_dir == 'North Wind':
        wind_gust_dir = 5
    elif wind_gust_dir == 'North-Northeast Wind':
        wind_gust_dir = 6
    elif wind_gust_dir == 'Southwest Wind':
        wind_gust_dir = 7
    elif wind_gust_dir == 'East-Northeast Wind':
        wind_gust_dir = 8
    elif wind_gust_dir == 'South-Southeast Wind':
        wind_gust_dir = 9
    elif wind_gust_dir == 'South Wind':
        wind_gust_dir = 10
    elif wind_gust_dir == 'Northwest Wind':
        wind_gust_dir = 11
    elif wind_gust_dir == 'Southeast Wind':
        wind_gust_dir = 12
    elif wind_gust_dir == 'East-Southeast Wind':
        wind_gust_dir = 13
    elif wind_gust_dir == 'East Wind':
        wind_gust_dir = 14
    else:
        wind_gust_dir = 15

    #Logic rain today
    if rain_today == 'Yes':
        rain_today = 1
    elif rain_today == 'No':
        rain_today = 0

    #Logic weather
    st.sidebar.title('Weather Metrics')
    if wind_gust_speed > wind_speed_9am :
        st.sidebar.metric(label="Temperature", value=f'{max_temp} °C', delta=f'{-min_temp} °C')
        st.sidebar.metric(label="Wind", value=f'{wind_gust_speed} mph', delta=f'{-wind_speed_9am} mph')
        st.sidebar.metric(label="Humidity", value=f'{humidity_9am} %', delta=f'{-humidity_3pm} %')
    elif wind_gust_speed < wind_speed_9am :
        st.sidebar.metric(label="Temperature", value=f'{max_temp} °C', delta=f'{min_temp} °C')
        st.sidebar.metric(label="Wind", value=f'{wind_gust_speed} mph', delta=f'{wind_speed_9am} mph')
        st.sidebar.metric(label="Humidity", value=f'{humidity_9am} %', delta=f'{humidity_3pm} %')
    elif humidity_9am > humidity_3pm:
        st.sidebar.metric(label="Temperature", value=f'{max_temp} °C', delta=f'{-min_temp} °C')
        st.sidebar.metric(label="Wind", value=f'{wind_gust_speed} mph', delta=f'{-wind_speed_9am} mph')
        st.sidebar.metric(label="Humidity", value=f'{humidity_9am} %', delta=f'{-humidity_3pm} %')
    elif humidity_9am < humidity_3pm:
        st.sidebar.metric(label="Temperature", value=f'{max_temp} °C', delta=f'{min_temp} °C')
        st.sidebar.metric(label="Wind", value=f'{wind_gust_speed} mph', delta=f'{wind_speed_9am} mph')
        st.sidebar.metric(label="Humidity", value=f'{humidity_9am} %', delta=f'{humidity_3pm} %')

    data = {
        'MinTemp':min_temp,
        'MaxTemp':max_temp,
        'Rainfall':rainfall,
        'WindGustDir':wind_gust_dir,
        'WindGustSpeed':wind_gust_speed,
        'WindSpeed9am':wind_speed_9am,
        'Humidity9am':humidity_9am,
        'Humidity3pm':humidity_3pm,
        'Pressure9am':pressure_9am,
        'Temp9am':temp_9am,
        'Temp3pm':temp_3pm,
        'RainToday':rain_today}

    features = pd.DataFrame(data,index=[0])
    return  features

input_df = user_input_parameters()

st.subheader('User Input Parameters')
st.write(input_df)

prediction = model1.predict(input_df)
prediction_proba = model1.predict_proba(input_df)

if st.button("Predict"):
    if prediction[0] == 0:
        st.subheader('Prediction')
        st.write(prediction)
        st.subheader('Prediction Probability')
        st.write(prediction_proba)
        st.image(im)
        st.success('Chances of not Rain Tomorrow')


    else:
        st.subheader('Prediction')
        st.write(prediction)
        st.subheader('Prediction Probability')
        st.write(prediction_proba)
        st.image(img)
        st.error('Warning! Chances of Rain Tomorrow')


