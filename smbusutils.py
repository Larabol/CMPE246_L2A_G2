import smbus2
import time

BUS_NUM = 1
BQ_ADDR = 0xb

bus = smbus2.SMBus(BUS_NUM)