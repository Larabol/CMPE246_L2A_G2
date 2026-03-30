import smbus2
import time
import datetime
import pandas as pd
from collections import deque

class BMS:
    def __init__(self, addr, cell_capacity=3350, bus_num=1):
        self.bus = smbus2.SMBus(bus_num)
        self.addr = addr
        self.capacity = cell_capacity
        self.max_points = 1000
        self.buffer = deque(maxlen=self.max_points)

    def twos_complement(self, value, bits):
        if value & (1 << (bits - 1)):
            value -= (1 << bits)
        return value

    def check_bit(self, num, pos):
        mask = 1 << pos
        return (num & mask) != 0
    
    def get_cell_voltage(self, cell):
        if cell >= 1 and cell <= 5:
            cell_reg = 0x40-cell
            return self.bus.read_word_data(self.addr, cell_reg)
        else: 
            return 0
        
    def get_pack_voltage(self):
        return self.bus.read_word_data(self.addr, 0x09)
    
    def get_current(self):
        raw = self.bus.read_word_data(self.addr, 0x0B)
        raw = ((raw & 0xFF) << 8) | (raw >> 8)
        current = self.twos_complement(raw, 16) / 100
        return current
    
    def get_temperature(self):
        return self.bus.read_word_data(self.addr, 0x08)*0.1 - 273

    def get_soc(self):
        return self.bus.read_word_data(self.addr, 0x0E)
    
    def get_data(self):
        timestamp = datetime.now().isoformat()
        time.sleep(0.1)
        voltage = self.get_pack_voltage()
        time.sleep(0.1)
        temperature = self.get_temperature()
        time.sleep(0.1)
        current = -1*self.get_current()
        time.sleep(0.1)
        soc = bms.get_soc()

        return {
            "timestamp": timestamp,
            "voltage": voltage,
            "temperature": temperature,
            "current": current,
            "soc": soc
        }
    
    def write_raw_data(self, csv):
        self.csv = csv
        self.buffer.append(self.get_data())
        df = pd.DataFrame(self.buffer)
        df.to_csv("bmsdata.csv", index=False)



    def get_operation_status(self):
        status_out = ["", "", "", "", "", ""]
        status_in = self.bus.read_word_data(self.addr, 0x54)
        
        if self.check_bit(status_in, 1):
            status_out[0] = "charging"
        elif self.check_bit(status_in, 2):
            status_out[0] = "discharging"
        else:
            status_out[0] = "idle"
        
        if not self.check_bit(status_in, 9):
            status_out[1] = "full access"
        else:
            if self.check_bit(status_in, 8):
                status_out[1] = "sealed"
            else:
                status_out[1] = "unsealed"
        
        if not self.check_bit(status_in, 10):
            status_out[2] = "critical low battery"
        else:
            status_out[2] = "pack charged"
        
        if self.check_bit(status_in, 12):
            status_out[3] = "permanent fail"
        else:
            status_out[3] = "no fails"
        
        if self.check_bit(status_in, 23):
            status_out[4] = "sleeping"
        else:
            status_out[4] = "awake"
        
        if self.check_bit(status_in, 11):
            status_out[5] = "unsafe condition"
        else:
            status_out[5] = "safe"

        return status_out

if __name__ == "__main__":
    bms = BMS(0x0b)
    cell_1 = bms.get_cell_voltage(1)
    cell_2 = bms.get_cell_voltage(2)
    cell_3 = bms.get_cell_voltage(3)
    cell_4 = bms.get_cell_voltage(4)
    cell_5 = bms.get_cell_voltage(5)
    print(f"V1: {cell_1}\nV2: {cell_2}\nV3: {cell_3}\nV4: {cell_4}\nV5: {cell_5}")
    print(bms.get_operation_status())