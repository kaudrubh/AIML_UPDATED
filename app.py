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

# Add custom CSS for aesthetics
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f8f9;
        }
        .stSidebar {
            background-color: #001f3d;
        }
        .sidebar .sidebar-content {
            color: white;
        }
        .stButton>button {
            background-color: #0077cc;
            color: white;
            border-radius: 5px;
            height: 40px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #005fa3;
        }
        .stMarkdown {
            font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Add a header with an emoji and banner image
st.title("🛡️ Cyber Threat Prediction")
st.image("https://via.placeholder.com/800x200?text=Cyber+Threat+Prediction", use_column_width=True)

# Main Description
st.markdown("""
    Welcome to the **Cyber Threat Prediction** app! This tool uses machine learning to predict cyber threats based on various factors.  
    Simply input your data below and click the **Predict** button to see the results.
""")

# Sidebar with a background color and instructions
st.sidebar.header("📋 Input Features")
with st.sidebar.expander("ℹ️ Instructions", expanded=True):
    st.write(
        """
        - Enter values for the features.
        - Click **Predict** to view the predicted cyber threat category.
        """
    )

# Collecting user inputs
input_data = {
    "Time": st.sidebar.number_input("Time (in seconds)", value=10, help="Time in seconds."),
    "Protocol": st.sidebar.selectbox("Protocol", list(label_encoders['Protocol'].classes_), help="Select the communication protocol."),
    "Flag": st.sidebar.selectbox("Flag", list(label_encoders['Flag'].classes_), help="Select the packet flag."),
    "Family": st.sidebar.selectbox("Malware Family", list(label_encoders['Family'].classes_)),
    "Clusters": st.sidebar.slider("Clusters", 1, 12, value=1, help="Select cluster count."),
    "Sender Address": st.sidebar.selectbox("Sender Address", list(label_encoders['Sender Address'].classes_)),
    "Exp Address": st.sidebar.selectbox("Receiver Address", list(label_encoders['Exp Address'].classes_)),
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
    for col, le in label_encoders.items():
        if col in input_df:
            input_df[col] = le.transform(input_df[col])
    
    # Scale numerical features
    numerical_columns = input_df.select_dtypes(include="number").columns
    input_df[numerical_columns] = scaler.transform(input_df[numerical_columns])
except Exception as e:
    st.error(f"An error occurred during preprocessing: {e}")

# Prediction button with custom style
if st.button("🔍 Predict"):
    with st.spinner("Processing..."):
        try:
            prediction = rf_model.predict(input_df)
            st.success(
                f"The predicted cyber threat category is: **{le_prediction.inverse_transform(prediction)[0]}**"
            )
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

# Add some charts (e.g., Bar chart or Line chart) to show data or predictions
st.markdown("### 📊 Data Overview")
st.write(input_df)

# Display a basic bar chart or other chart based on predictions or input data
st.bar_chart(input_df["BTC"])  # For illustration, could be any numerical column

# Footer with some credits or notes
st.markdown("---")
st.write("Created with ❤️ by [Your Name]")
st.write("[GitHub](https://github.com/) | [LinkedIn](https://linkedin.com)")
