import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle


model = tf.keras.models.load_model('model.h5')

with open('onehotencoder_Geo.pkl','rb') as file:
    onehotencoder_Geo=pickle.load(file)

with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender=pickle.load(file)

with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)


# Streamlit APP
st.title('Customer churn Prediction')

#input

geography = st.selectbox('Geography',onehotencoder_Geo.categories_[0])
gender = st.selectbox('Gender',label_encoder_gender.classes_)
age = st.slider('Age',18,92)
balance = st.number_input('Balance')
credit_score = st.number_input('credit_score')
estimated_salary = st.number_input('Estimated_salary')
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider('Number of Products',1,4)
has_cr_card = st.selectbox('Has Credit card',[0,1])
is_active_member = st.selectbox('Is Active member',[0,1])

#Prepare the input data

input_data = pd.DataFrame({
    'CreditScore' : [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age' : [age],
    'Tenure' :[tenure],
    'Balance' : [balance],
    'NumOfProducts' : [num_of_products],
    'HasCrCard' : [has_cr_card],
    'IsActiveMember' : [is_active_member],
    'EstimatedSalary' : [estimated_salary]
})

geo_encoded = onehotencoder_Geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded,columns=onehotencoder_Geo.get_feature_names_out(['Geography']))

#Combine one-hot encooded data
input_data = pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)

#sacle the dta
input_data_scaled = scaler.transform(input_data)

#Predict Churn
prediction = model.predict(input_data_scaled)
prediction_prob = prediction[0][0]

st.write(f'Churn Probability: {prediction_prob:.2f}')

if prediction_prob > 0.5:
    st.write('The customer is likey to churn')
else:
    st.write('The customer is not likey to churn')


