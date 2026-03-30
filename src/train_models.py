from ML_Model import MLModelScript
from smbusutils import BMS
from Data_Preprocessing import DataPreprocessingScript

addr = 0x0b
raw_data_file = "bmsdata.csv"
processed_data_file = "battery_data_processed.csv"

def update_data(self):
        # generate new raw CSV
        bms = BMS(addr)
        bms.write_raw_data(raw_data_file)

        # preprocess latest raw CSV
        preprocessor = DataPreprocessingScript(
            input_file=raw_data_file,
            output_file=processed_data_file,
            battery_capacity_ah = 16.75,  # Specific to battery
            full_charge_voltage = 20.5,  # Specific to battery
            full_charge_current_threshold = 0.2,  ## Specific to battery
        )
        preprocessor.preprocess_data() 

if __name__ == "__main__":
    ml = MLModelScript(
        input_file="battery_data_processed.csv"
    )
    ml.train_models()