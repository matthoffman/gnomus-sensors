import machine
import time
import ds18x20
import onewire
import config
from machine import Pin
import uhttp


def read_soil_moisture():
    adc = machine.ADC(0)
    return adc


def read_temperature():
    ow = onewire.OneWire(Pin(13, Pin.IN, Pin.PULL_UP))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    ds.convert_temp()
    time.sleep_ms(750)
    temps = {}
    for rom in roms:
        temps[rom] = ds.read_temp(rom)
    print("Found temps: {}".format(temps))
    return temps


# main loop
while True:

    # read the sensors
    moisture = read_soil_moisture()
    temp = read_temperature()

    # post it to the server
    resp = uhttp.post(config.SERVER_URL, {"id": machine.unique_id(),
                                  "moisture": moisture,
                                  "temp": temp})
    # now maybe do something with the result?

    # sleep until we try again. TODO: this will be deep sleep eventually...
    time.sleep(60)

