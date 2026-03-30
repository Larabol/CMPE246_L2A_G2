from ML_Model import MLModelScript

raw_data_file = "raw_training_data.csv"
processed_data_file = "processed_training_data.csv"

if __name__ == "__main__":
    ml = MLModelScript(
        input_file="battery_data_processed.csv"
    )
    ml.train_models()