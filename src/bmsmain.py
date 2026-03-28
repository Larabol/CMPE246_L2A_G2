import src.smbusutils as smbu
import pandas as pd
from collections import deque
import time
from datetime import datetime
import Data_Preprocessing
import ML_Model

addr = 0x0b
cell_capacity = 3350
bus_num = 1

max_points = 1000
buffer = deque(maxlen=max_points)

bms = smbu.BMS(addr, cell_capacity, bus_num)

preprocessor = Data_Preprocessing.DataPreprocessingScript(
    "bmsdata.csv",
    "processedbmsdata.csv"
)

def get_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "voltage": bms.get_pack_voltage(),
        "temperature": bms.get_temperature(),
        "current": -1*bms.get_current(),
    }

while True:
    buffer.append(get_data())
    df = pd.DataFrame(buffer)
    df.to_csv("bmsdata.csv", index=False)
    if len(buffer) % 50 == 0:
        preprocessor.preprocess_data()

    time.sleep(1)