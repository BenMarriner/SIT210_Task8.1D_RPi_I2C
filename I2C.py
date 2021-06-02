import smbus
import time

# Sensor configuration
SENSOR = 0x23
POWER_DOWN = 0x00
POWER_UP = 0x01
RESET = 0x07
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# Light level thresholds
THRESHOLDS = [600, 1200, 1800, 2400, 3000]
THRESHOLD_MSG = ["Too Dark", "Dark", "Medium", "Bright", "Too Bright"]

bus = smbus.SMBus(1)

def convertToNumber(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return result

def readLight(addr=SENSOR):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)

def getLightThreshold(lux):
    for i in range(len(THRESHOLDS)):
        if lux < THRESHOLDS[i]:
            return THRESHOLD_MSG[i]
    
    # Return the last threshold message since the light level would be too bright
    return THRESHOLD_MSG[len(THRESHOLD_MSG) - 1]


while True:
    lightLevel = readLight()
    print(getLightThreshold(lightLevel))
    time.sleep(0.5)