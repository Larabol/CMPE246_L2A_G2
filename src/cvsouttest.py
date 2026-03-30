import smbusutils as smbu
import pandas as pd
from collections import deque
import time
from datetime import datetime

addr = 0x0b
cell_capacity = 3350
bus_num = 1

max_points = 1000
buffer = deque(maxlen=max_points)

bms = smbu.BMS(addr, cell_capacity, bus_num)

def get_data():
    timestamp = datetime.now().isoformat()
    time.sleep(0.1)
    voltage = bms.get_pack_voltage()
    time.sleep(0.1)
    temperature = bms.get_temperature()
    time.sleep(0.1)
    current = -1*bms.get_current()
    time.sleep(0.1)

    return {
        "timestamp": timestamp,
        "voltage": voltage,
        "temperature": temperature,
        "current": current,
    }

while True:
    buffer.append(get_data())
    df = pd.DataFrame(buffer)
    print(df)
    df.to_csv("bmsdata.csv", index=False)
    time.sleep(5)