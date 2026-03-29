import smbusutils as smbu
from datetime import datetime
import time

addr = 0x0b
cell_capacity = 3350
bus_num = 1

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
    
    return f"time: {timestamp}\nvoltage: {voltage}\ntemperature: {temperature}\ncurrent: {current}"
    

while True:
    print(get_data())
    time.sleep(1)