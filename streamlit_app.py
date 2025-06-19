
import streamlit as st
import json
import openai
import pandas as pd
import random

from agent.validator_agent import suggest_next_tests

st.set_page_config(page_title="SensusAI", layout="centered")

st.title("🔍 SensusAI – AI-Powered Sensor Validation Assistant")
st.markdown("Upload your sensor test logs or select a sensor type to simulate test results. Then let the AI agent analyze and recommend next steps.")

# Simulated data selector
sensor_type = st.selectbox("Select Sensor Type", ["Camera", "Lidar", "Fusion"])

# Generate mock data
def generate_mock_data(sensor):
    if sensor == "Camera":
        return {
            "sharpness": random.choice(["low", "medium", "high"]),
            "hdr": random.choice(["low", "medium", "high"]),
            "color_accuracy": random.choice(["poor", "good", "excellent"])
        }
    elif sensor == "Lidar":
        return {
            "range_accuracy": random.choice(["low", "medium", "high"]),
            "reflectivity": random.choice(["poor", "good", "great"]),
            "interference": random.choice(["none", "moderate", "high"])
        }
    elif sensor == "Fusion":
        return {
            "time_sync_error_ms": random.randint(0, 100),
            "alignment_score": random.choice(["low", "acceptable", "high"]),
            "gps_drift_m": random.uniform(0, 2.0)
        }

# Upload or generate data
uploaded_file = st.file_uploader("📤 Upload your test results (JSON)", type="json")

if uploaded_file:
    test_data = json.load(uploaded_file)
    st.success("File uploaded and parsed successfully.")
else:
    if st.button("Generate Mock Test Data"):
        test_data = {sensor_type.lower(): generate_mock_data(sensor_type)}
        st.json(test_data)

# Visualize simulated metric
if "test_data" in locals():
    st.subheader("📈 Simulated Sensor Metric Chart")
    df = pd.DataFrame({
        'Sample': list(range(10)),
        'Metric Value': [random.randint(60, 100) for _ in range(10)]
    })
    st.line_chart(df)

    if st.button("🧠 Run AI Agent on Data"):
        try:
            result = suggest_next_tests(test_data)
            st.subheader("💡 AI Agent Suggestion")
            st.write(result)

            if st.checkbox("🔎 Generate OpenAI LLM Suggestion"):
                openai.api_key = st.text_input("Enter your OpenAI API key", type="password")
                if openai.api_key:
                    user_prompt = f"Given this sensor test data: {test_data}, what should be tested next?"
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    st.success("✅ OpenAI Suggestion:")
                    st.write(response['choices'][0]['message']['content'])
        except Exception as e:
            st.error(f"Error: {e}")
