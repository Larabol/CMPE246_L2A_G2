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