import pandas as pd
import joblib
from xgboost import XGBClassifier, XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error


class MLModelScript:
    def __init__(self, input_file):
        self.input_file = input_file

        
        self.min_voltage = 17.5 ## Specific to battery
        self.max_voltage = 20.5 ## Specific to battery
        self.max_current = 4.875 ## Specific to battery
        self.max_temperature = 333.0 ## Specific to battery

        self.temp_lookahead_steps = 10

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

    def create_fault_labels(self, df):
        df["fault_label"] = (
            (df["voltage"] < self.min_voltage) |
            (df["voltage"] > self.max_voltage) |
            (df["current"].abs() > self.max_current) |
            (df["temperature"] > self.max_temperature)
        ).astype(int)
        return df

    def create_future_temperature_target(self, df):
        df["temp_future"] = df["temperature"].shift(-self.temp_lookahead_steps)
        return df

    def train_models(self):
        df = pd.read_csv(self.input_file)

        df = self.create_fault_labels(df)
        df = self.create_future_temperature_target(df)

        df = df.dropna(subset=self.feature_columns + ["fault_label", "temp_future"]).copy()

        ## Fault model
        X_fault = df[self.feature_columns]
        y_fault = df["fault_label"]

        X_train_fault, X_test_fault, y_train_fault, y_test_fault = train_test_split(
            X_fault, y_fault, test_size=0.2, random_state=42, stratify=y_fault
        )

        fault_model = XGBClassifier(
            objective = "binary:logistic",
            eval_metric = "logloss",
            n_estimators = 150,
            max_depth = 4,
            learning_rate = 0.05,
            random_state = 42
        )

        fault_model.fit(X_train_fault, y_train_fault)
        fault_predictions = fault_model.predict(X_test_fault)

        print("Fault Model Accuracy:", accuracy_score(y_test_fault, fault_predictions))

        ## Future temperature model
        X_temp = df[self.feature_columns]
        y_temp = df["temp_future"]

        X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(
            X_temp, y_temp, test_size=0.2, random_state=42
        )

        temperature_model = XGBRegressor(
            objective = "reg:squarederror",
            n_estimators = 200,
            max_depth = 4,
            learning_rate = 0.05,
            random_state = 42
        )

        temperature_model.fit(X_train_temp, y_train_temp)
        temp_predictions = temperature_model.predict(X_test_temp)

        print("Future Temperature Model MAE:", mean_absolute_error(y_test_temp, temp_predictions))

        joblib.dump(fault_model, "fault_model.joblib")
        joblib.dump(temperature_model, "temp_model.joblib")

        print("Saved fault_model.joblib")
        print("Saved temp_model.joblib")


if __name__ == "__main__":
    model_script = MLModelScript("battery_data_processed.csv")
    model_script.train_models()
