import streamlit as st
import pandas as pd
import joblib

# Load pre-trained model and preprocessing tools
rf_model = joblib.load('random_forest_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')
target_encoder = joblib.load('target_encoder.pkl')

# Set Page Configuration
st.set_page_config(
    page_title="Cyber Threat Prediction",
    page_icon="🛡️",
    layout="wide"
)

# Add a header
st.title("🔒 Cyber Threat Prediction")
st.markdown("""
<style>
    .stSidebar {background-color: #f0f2f6;}
</style>
""", unsafe_allow_html=True)

st.write(
    "Upload your data or fill in the fields below to predict **cyber threat categories**. 🕵️‍♂️"
)

# Sidebar for feature inputs
st.sidebar.header("📋 Input Features")
with st.sidebar.expander("ℹ️ Instructions"):
    st.write(
        """
        - Provide numerical and categorical inputs.
        - Click **Predict** to see the result.
        """
    )

# Collecting user inputs
input_data = {
    "Time": st.sidebar.number_input("Time (in seconds)", value=10, help="Time in seconds."),
    "Protcol": st.sidebar.selectbox("Protocol", list(label_encoders['Protcol'].classes_), help="Select the communication protocol."),
    "Flag": st.sidebar.selectbox("Flag", list(label_encoders['Flag'].classes_), help="Select the packet flag."),
    "Family": st.sidebar.selectbox("Malware Family", list(label_encoders['Family'].classes_)),
    "Clusters": st.sidebar.slider("Clusters", 1, 12, value=1, help="Select cluster count."),
    "SeddAddress": st.sidebar.selectbox("Sender Address", list(label_encoders['SeddAddress'].classes_)),
    "ExpAddress": st.sidebar.selectbox("Receiver Address", list(label_encoders['ExpAddress'].classes_)),
    "BTC": st.sidebar.number_input("BTC Amount", value=1),
    "USD": st.sidebar.number_input("USD Amount", value=500),
    "Netflow_Bytes": st.sidebar.number_input("Netflow Bytes", value=500),
    "IPaddress": st.sidebar.selectbox("IP Address", list(label_encoders['IPaddress'].classes_)),
    "Threats": st.sidebar.selectbox("Threat Type", list(label_encoders['Threats'].classes_)),
    "Port": st.sidebar.slider("Port", 5061, 5068, value=5061),
}

# Convert input data to a DataFrame
input_df = pd.DataFrame([input_data])

# Preprocess the input
try:
    # Apply label encoding for categorical variables
    for col, le in label_encoders.items():
        if col in input_df:
            input_df[col] = le.transform(input_df[col])
    
    # Scale numerical features
    numerical_columns = input_df.select_dtypes(include="number").columns
    input_df[numerical_columns] = scaler.transform(input_df[numerical_columns])
except Exception as e:
    st.error(f"An error occurred during preprocessing: {e}")

# Prediction button
if st.button("🔍 Predict"):
    with st.spinner("Processing..."):
        try:
            # Make the prediction using the model
            prediction = rf_model.predict(input_df)
            
            # Convert the predicted label back to the original category
            predicted_label = le_prediction.inverse_transform(prediction)[0]
            st.success(f"The predicted cyber threat category is: **{predicted_label}**")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

# Footer with some credits or notes
st.markdown("---")
st.write("Created with ❤️ by [Your Name]")
st.write("[GitHub](https://github.com/) | [LinkedIn](https://linkedin.com)")
