import streamlit as st
import pandas as pd
import joblib

# Load saved model and encoders
model = joblib.load('random_forest_model.pkl')
label_encoders = joblib.load('label_encoders.pkl')
target_encoder = joblib.load('target_encoder.pkl')

# Set page configuration
st.set_page_config(
    page_title="Cyber Threat Detection",
    page_icon="🛡️",
    layout="wide"
)



# Title and description
st.title("🛡️ Cyber Threat Detection")
st.markdown("""
    Welcome to the **Cyber Threat Detection** app! This app uses machine learning to predict cyber threats based on various features.
    Enter the data in the sidebar and click **Predict** to get the result.
""")

# Sidebar for feature inputs
st.sidebar.header("📋 Input Features")
with st.sidebar.expander("ℹ️ Instructions", expanded=True):
    st.write("""
        - Fill in the fields below with the respective information.
        - Click **Predict** to see the cyber threat category.
    """)

# Input fields for features
features = {
    "Time": st.sidebar.number_input("Time (in seconds)", min_value=0, value=10, help="Enter time in seconds."),
    "Protcol": st.sidebar.selectbox("Protocol", list(label_encoders['Protcol'].classes_)),
    "Flag": st.sidebar.selectbox("Flag", list(label_encoders['Flag'].classes_)),
    "Family": st.sidebar.selectbox("Family", list(label_encoders['Family'].classes_)),
    "Clusters": st.sidebar.number_input("Clusters", min_value=0, value=1),
    "SeddAddress": st.sidebar.selectbox("Sender Address", list(label_encoders['SeddAddress'].classes_)),
    "ExpAddress": st.sidebar.selectbox("Receiver Address", list(label_encoders['ExpAddress'].classes_)),
    "BTC": st.sidebar.number_input("BTC Amount", min_value=0, value=1),
    "USD": st.sidebar.number_input("USD Amount", min_value=0, value=500),
    "Netflow_Bytes": st.sidebar.number_input("Netflow Bytes", min_value=0, value=500),
    "IPaddress": st.sidebar.selectbox("IP Address", list(label_encoders['IPaddress'].classes_)),
    "Threats": st.sidebar.selectbox("Threat Type", list(label_encoders['Threats'].classes_)),
    "Port": st.sidebar.number_input("Port", min_value=0, value=5061),
}

# Convert categorical inputs using label encoders
for key in features:
    if key in label_encoders:
        features[key] = label_encoders[key].transform([features[key]])[0]

# Predict button
if st.button("🔍 Predict", use_container_width=True):
    with st.spinner("Processing..."):
        input_data = pd.DataFrame([features])
        prediction = model.predict(input_data)
        prediction_label = target_encoder.inverse_transform(prediction)[0]
        st.success(f"The predicted cyber threat is: **{prediction_label}**")

# Footer with credits
st.markdown("---")
st.markdown("Created with ❤️ by [Your Name]")
st.markdown("[GitHub](https://github.com/) | [LinkedIn](https://linkedin.com)")

