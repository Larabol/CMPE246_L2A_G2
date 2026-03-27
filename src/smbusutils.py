import smbus2

class BMS:
    def __init__(self, addr, cell_capacity=3350, bus_num=1):
        self.bus = smbus2.SMBus(bus_num)
        self.addr = addr
        self.capacity = cell_capacity

    def check_bit(num, pos):
        mask = 1 << pos
        return (num & mask) != 0
    
    def get_cell_voltage(self, cell):
        if cell >= 1 and cell <= 3:
            cell_reg = 0x40-cell
            return self.bus.read_word_data(self.addr, cell_reg)
        elif cell == 4 or cell == 5:
            cell_reg = 0x43-cell
            return self.bus.read_word_data(self.addr, cell_reg)
        
    def get_pack_voltage(self):
        return sum(self.bus.read_word_data(self.addr, 0x3F)+self.bus.read_word_data(self.addr, 0x3E)+self.bus.read_word_data(self.addr, 0x3D))*(5/3)
    
    def get_current(self):
        return self.bus.read_word_data(self.addr, 0x0A)
    
    def get_temperature(self):
        return self.bus.read_word_data(self.addr, 0x08)

    def get_coulombs(self):
        return (100 - self.bus.read_word_data(self.addr, 0x0E))*self.capacity*3.6
    
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
        
        if self.check_bit(status_in, 10):
            status_out[3] = "critical low battery"
        else:
            status_out[3] = "pack charged"
        
        if self.check_bit(status_in, 12):
            status_out[4] = "permanent fail"
        else:
            status_out[4] = "no fails"
        
        if self.check_bit(status_in, 23):
            status_out[5] = "sleeping"
        else:
            status_out[5] = "awake"
        
        if self.check_bit(status_in, 11):
            status_out[6] = "unsafe condition"
        else:
            status_out[6] = "safe"

        return status_out
