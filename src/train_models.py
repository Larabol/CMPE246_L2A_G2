import time
from smbusutils import BMS
from Data_Preprocessing import DataPreprocessingScript

addr = 0x0b
raw_data_file = "bmsdata.csv"
processed_data_file = "battery_data_processed.csv"


def update_data():
        # generate new raw CSV
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
    for i in range(1000):
        bms = BMS(addr)
        update_data()
        print("updated data") 
        time.sleep(5)