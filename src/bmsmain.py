import smbus2
import src.smbusutils as smbu
import pandas as pd
from collections import deque
import time

addr = 0xb
cell_capacity = 3350
bus_num = 1

max_points = 1000
buffer = deque(maxlen=max_points)

bms = smbu.BMS(addr, cell_capacity, bus_num)

def get_data():
    return {
        "time": time.time(),
        "voltage": bms.get_pack_voltage(),
        "temperature": bms.get_temperature(),
        "current": bms.get_current(),
        "coulomb_count": bms.get_coulombs()
    }

#jacob was here
while True:
    buffer.append(get_data())
    df = pd.dataFrame(buffer)
    df.to_csv("bmsdata.csv", index=False)

    time.sleep(1)