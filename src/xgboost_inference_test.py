import pandas as pd
import numpy as np
from xgboost import XGBClassifier, XGBRegressor

MODEL_FAULT_PATH = "fault_model.json"
MODEL_TEMP_PATH = "temp_model.json"
DATA_PATH = "battery_data_processed.csv"

feature_columns = [
    "voltage",
    "current",
    "temperature",
    "soc",
    "abs_current",
    "power",
    "voltage_lag1",
    "current_lag1",
    "temperature_lag1",
    "avg_voltage_5",
    "avg_current_5",
    "avg_temp_5",
    "d_voltage",
    "d_current",
    "d_temperature",
]

def test_inference():
    print("Loading models...")

    try:
        fault_model = XGBClassifier()
        fault_model.load_model(MODEL_FAULT_PATH)

        temp_model = XGBRegressor()
        temp_model.load_model(MODEL_TEMP_PATH)

        print("✅ Models loaded successfully")

    except Exception as e:
        print("❌ Model loading failed:", e)
        return

    print("\nLoading data...")

    try:
        df = pd.read_csv(DATA_PATH)
        df = df.dropna(subset=feature_columns)

        if df.empty:
            print("❌ No valid data after dropping NaNs")
            return

        latest = df.iloc[[-1]][feature_columns]

        print("✅ Data loaded, shape:", latest.shape)

    except Exception as e:
        print("❌ Data loading failed:", e)
        return

    print("\nRunning inference...")

    try:
        fault_pred = fault_model.predict(latest)[0]
        fault_prob = fault_model.predict_proba(latest)[0][1]
        temp_pred = temp_model.predict(latest)[0]

        print("✅ Inference successful\n")
        print("Fault Prediction:", fault_pred)
        print("Fault Probability:", round(fault_prob * 100, 2), "%")
        print("Predicted Future Temp:", round(temp_pred, 2), "C")

    except Exception as e:
        print("❌ Inference failed:", e)
        return


if __name__ == "__main__":
    test_inference()