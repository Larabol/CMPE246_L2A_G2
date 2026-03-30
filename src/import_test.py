from smbusutils import BMS

bms = BMS(0x0b, 3350, 1)

print(bms.get_data())

bms.write_raw_data("bmsdata.csv")