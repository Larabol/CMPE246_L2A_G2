import pandas as pd
import joblib
from Data_Preprocessing import DataPreprocessingScript
import json


class RunBMSScripts:
    def __init__(self, raw_data_file, processed_data_file, fault_model_file, temp_model_file):
        self.raw_data_file = raw_data_file
        self.processed_data_file = processed_data_file
        self.fault_model = joblib.load(fault_model_file)
        self.temp_model = joblib.load(temp_model_file)

        self.feature_columns = [
            "voltage",
            "current",
            "temperature",
            "cumulative_coulombs",
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

    def run_predictions(self):
        # preprocess latest raw CSV first
        preprocessor = DataPreprocessingScript(
            input_file=self.raw_data_file,
            output_file=self.processed_data_file,
            battery_capacity_ah = 16.75,  # Specific to battery
            full_charge_voltage = 20.5,  # Specific to battery
            full_charge_current_threshold = 0.2,  ## Specific to battery
        )
        preprocessor.preprocess_data()

        # read processed CSV
        df = pd.read_csv(self.processed_data_file)
        df = df.dropna(subset=self.feature_columns).copy()

        if len(df) == 0:
            print("No usable data available.")
            return

        latest_row = df.iloc[-1]
        latest_features = df.iloc[[-1]][self.feature_columns]

        fault_prediction = self.fault_model.predict(latest_features)[0]
        fault_probability = self.fault_model.predict_proba(latest_features)[0][1]
        predicted_future_temp = self.temp_model.predict(latest_features)[0]

        print("Latest Battery Status")
        print("-" * 40)
        print(f"Timestamp: {latest_row['timestamp']}")
        print(f"Voltage: {latest_row['voltage']:.2f} V")
        print(f"Current: {latest_row['current']:.2f} A")
        print(f"Temperature: {latest_row['temperature']:.2f} C")
        print(f"State of Charge: {latest_row['soc']:.2f} %")

        if pd.notna(latest_row["runtime_left_minutes"]):
            print(f"Estimated Runtime Left: {latest_row['runtime_left_minutes']:.2f} minutes")
        else:
            print("Estimated Runtime Left: N/A")

        print(f"Fault Prediction: {fault_prediction}")
        print(f"Fault Probability: {fault_probability * 100:.2f}%")
        print(f"Predicted Future Temperature: {predicted_future_temp:.2f} C")
        print("-" * 40)

        # save latest output to JSON
        latest_output = {
            "Timestamp": str(latest_row["timestamp"]),
            "Voltage": float(latest_row["voltage"]),
            "Current": float(latest_row["current"]),
            "Temperature": float(latest_row["temperature"]),
            "SoC": float(latest_row["soc"]),
            "Runtime_Minutes_Left": None if pd.isna(latest_row["runtime_left_minutes"]) else float(latest_row["runtime_left_minutes"]),
            "Fault_Prediction": int(fault_prediction),
            "Fault_Probability_Percent": float(fault_probability * 100),
            "Predicted_Future_Temp": float(predicted_future_temp)
        }

        with open("latest_status.json", "w") as f:
            json.dump(latest_output, f, indent=4)


if __name__ == "__main__":
    runner = RunBMSScripts(
        raw_data_file="battery_data.csv",
        processed_data_file="battery_data_processed.csv",
        fault_model_file="fault_model.joblib",
        temp_model_file="temp_model.joblib"
    )
    runner.run_predictions()
