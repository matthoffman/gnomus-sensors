from machine import ADC, I2C, unique_id, Pin
from dht import DHT22
from ads1x15 import ADS1115
import bme280
import time
import ds18x20
import onewire
import config
import urest
from micropython import alloc_emergency_exception_buf

POLL_INTERVAL = 60
alloc_emergency_exception_buf(100)


def initialize_i2c():
    # construct an I2C bus
    i2c = I2C(scl=Pin(12), sda=Pin(14))
    print("Initialized I2C bus. Has the following devices attached: ".format(i2c.scan()))
    return i2c


def read_soil_moisture_adc():
    adc = ADC(0).read()
    return [{"id": "internal_adc",
             "value": adc,
             "type": "soil moisture"}]


def read_soil_moisture_i2c(i2c):
    """The ADS1115 4-channel ADC converter is somewhere between 0x48-0x4B. Ours is
      on the default. We're assuming we're only hooking soil sensors to it."""
    addr = 72
    adc = ADS1115(i2c, addr, 0)
    ret = []
    for i in range(0, 3):
        val = adc.read(0, i)
        if val < 3130 or val > 3150:
            ret.append({"id": "adc_{}_{}".format(addr, i),
                        "type": "soil moisture",
                        "value": val})

    return ret


def read_humidity_i2c(i2c):
    """The BME280 temp/humidity sensor is usually on 0x76"""
    bme = bme280.BME280(i2c=i2c)
    print(bme.values)
    (temp, pressure, humidity) = bme.read_compensated_data()
    return [{"id": "bme280_0x76_temp",
             "value": temp / 100.0,
             "type": "temperature"},
            {"id": "bme280_0x76_pressure",
             "type": "pressure",
             "value": pressure / 256.0},
            {"id": "bme280_0x76_humidity",
             "value": humidity / 1024.0,
             "type": "humidity"}]


def read_dht22():
    pin = 0
    dht = DHT22(Pin(pin))
    dht.measure()
    return [{"id": "dht22_{}_temp".format(pin),
             "value": dht.temperature(),
             "type": "temperature"},
            {"id": "dht22_{}_humidity".format(pin),
             "value": dht.humidity(),
             "type": "humidity"}]


def read_luminosity_i2c(i2c):
    """The TSL2561 luminosity sensor might be listening on 0x39, 0x29, or 0x49 """
    pass


def bytearray_to_str(b):
    return "".join("{:02x}".format(x) for x in b)


def read_temperature():
    ow = onewire.OneWire(Pin(13, Pin.IN, Pin.PULL_UP))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    temps = []
    for rom in roms:
        rom_str = bytearray_to_str(rom)
        temps.append({"id": rom_str,
                      "type": "temperature",
                      "value": ds.read_temp(rom)})
    print("Found temps: {}".format(temps))
    return temps


# main loop
while True:
    try:
        # read the sensors
        i2c = initialize_i2c()
        moisture = read_soil_moisture_i2c(i2c)
        # moisture2 = read_soil_moisture_adc()
        temp = read_temperature()
        humidity = read_humidity_i2c(i2c)
        dht_temp = read_dht22()

        readings = moisture + temp + humidity + dht_temp

        # post it to the server
        resp = urest.post(config.SERVER_URL, {"id": bytearray_to_str(unique_id()),
                                              "version": 1,
                                              "readings": readings})
        # now maybe do something with the result from that POST?
        # Maybe it told us to do something?
    except Exception as e:
        print("Exception in main loop: {}".format(e))

    # sleep until we try again. TODO: this will be deep sleep eventually...
    time.sleep(POLL_INTERVAL)
