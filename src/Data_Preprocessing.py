import pandas as pd
import numpy as np
import json


class DataPreprocessingScript:
    def __init__(
        self,
        input_file,
        output_file,
        battery_capacity_ah=16.75, ## Specific to battery
        full_charge_voltage=20.5, ## Specific to battery
        full_charge_current_threshold=0.2, ## Specific to battery
    ):
        self.input_file = input_file
        self.output_file = output_file

        # Battery / SoC settings
        self.battery_capacity_ah = battery_capacity_ah
        self.initial_soc = initial_soc
        self.full_charge_voltage = full_charge_voltage
        self.full_charge_current_threshold = full_charge_current_threshold
        self.enable_full_charge_reset = enable_full_charge_reset

    def is_full_charge_condition(self, voltage, current):
        if not self.enable_full_charge_reset:
            return False

        return (
            voltage >= self.full_charge_voltage and
            abs(current) <= self.full_charge_current_threshold
        )

    def calculate_soc(self, df):
        soc = self.initial_soc
        soc_values = []

        for _, row in df.iterrows():
            current = row["current"]        # positive = discharge
            dt_seconds = row["dt_seconds"]
            voltage = row["voltage"]

            if self.is_full_charge_condition(voltage, current):
                soc = 100.0
            else:
                delta_ah = current * dt_seconds / 3600.0
                soc = soc - (delta_ah / self.battery_capacity_ah) * 100.0

            soc = max(0.0, min(100.0, soc))
            soc_values.append(soc)

        df["soc"] = soc_values
        return df

    def calculate_runtime_left(self, df):
        runtime_left_minutes = []

        for _, row in df.iterrows():
            current = row["current"]
            soc = row["soc"]

            if current > 0.05:
                remaining_capacity_ah = (soc / 100.0) * self.battery_capacity_ah
                runtime_hours = remaining_capacity_ah / current
                runtime_minutes = runtime_hours * 60.0
            else:
                runtime_minutes = np.nan

            runtime_left_minutes.append(runtime_minutes)

        df["runtime_left_minutes"] = runtime_left_minutes
        return df

    def preprocess_data(self):
        df = pd.read_csv(self.input_file)

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)

        df["dt_seconds"] = df["timestamp"].diff().dt.total_seconds()
        df["dt_seconds"] = df["dt_seconds"].fillna(1.0)

        df = self.calculate_soc(df)
        df = self.calculate_runtime_left(df)

        
        df["abs_current"] = df["current"].abs()
        df["power"] = df["voltage"] * df["current"]

        df["voltage_lag1"] = df["voltage"].shift(1)
        df["current_lag1"] = df["current"].shift(1)
        df["temperature_lag1"] = df["temperature"].shift(1)

        df["avg_voltage_5"] = df["voltage"].rolling(5).mean()
        df["avg_current_5"] = df["current"].rolling(5).mean()
        df["avg_temp_5"] = df["temperature"].rolling(5).mean()

        df["d_voltage"] = df["voltage"].diff()
        df["d_current"] = df["current"].diff()
        df["d_temperature"] = df["temperature"].diff()

        df.to_csv(self.output_file, index=False)
        print(f"Preprocessed data saved to {self.output_file}")


if __name__ == "__main__":
    preprocessor = DataPreprocessingScript(
        input_file="battery_data.csv",
        output_file="battery_data_processed.csv",
        battery_capacity_ah = 16.75, ## Specific to battery
        full_charge_voltage = 20.5, ## Specific to battery
        full_charge_current_threshold = 0.2, ## Specific to battery
    )
    preprocessor.preprocess_data()
