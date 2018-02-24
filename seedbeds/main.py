from machine import ADC, I2C, unique_id, Pin
from dht import DHT22
import time
import ds18x20
import onewire
import config
import uhttp
from micropython import alloc_emergency_exception_buf


POLL_INTERVAL = 60
alloc_emergency_exception_buf(100)


def initialize_i2c():
    # construct an I2C bus
    i2c = I2C(scl=Pin(12), sda=Pin(14), freq=100000)
    print("Initialized I2C bus. Has the following devices attached: ".format(i2c.scan()))
    return i2c


def read_soil_moisture_adc():
    return ADC(0).read()


def read_soil_moisture_i2c(i2c):
    """The ADS1115 4-channel ADC converter is somewhere between 0x48-0x4B"""
    i2c.read("0x48")
    pass


def read_soil_moisture():
    adc = read_soil_moisture_adc()
    return {"internal": adc}


def bytearray_to_str(b):
    return "".join("{:02x}".format(x) for x in b)


def read_humidity_i2c(i2c):
    """The BME280 temp/humidity sensor is usually on 0x76"""
    pass

def read_dht22():
    dht = DHT22(Pin(0))
    d.measure()
    d.temperature()
    d.humidity()


def read_luminosity_i2c(i2c):
    """The TSL2561 luminosity sensor might be listening on 0x39, 0x29, or 0x49 """
    pass


def read_temperature():
    ow = onewire.OneWire(Pin(13, Pin.IN, Pin.PULL_UP))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    temps = {}
    for rom in roms:
        rom_str = bytearray_to_str(rom)
        temps[rom_str] = ds.read_temp(rom)
    print("Found temps: {}".format(temps))
    return temps


# main loop
while True:
    try:
        # read the sensors
        moisture = read_soil_moisture()
        temp = read_temperature()
        i2c = initialize_i2c()
        # post it to the server
        resp = uhttp.post(config.SERVER_URL, {"id": unique_id(),
                                              "version": 1,
                                              "readings": {
                                                  "moisture": moisture,
                                                  "temp": temp}})
        # now maybe do something with the result?
    except Exception as e:
        print("Exception in main loop: {}".format(e))

    # sleep until we try again. TODO: this will be deep sleep eventually...
    time.sleep(POLL_INTERVAL)
