import smbus2

class BMS:
    def __init__(self, addr, cell_capacity=3350, bus_num=1):
        self.bus = smbus2.SMBus(bus_num)
        self.addr = addr
        self.capacity = cell_capacity

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
