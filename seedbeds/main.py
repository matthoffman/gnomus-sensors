import machine
import time
import ds18x20
import onewire
import config
import uhttp
from machine import Pin
from micropython import alloc_emergency_exception_buf

POLL_INTERVAL = 60
alloc_emergency_exception_buf(100)


def read_soil_moisture():
    adc = machine.ADC(0)
    return {"internal": adc}


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
    try:
        # read the sensors
        moisture = read_soil_moisture()
        temp = read_temperature()
        # post it to the server
        resp = uhttp.post(config.SERVER_URL, {"id": machine.unique_id(),
                                              "moisture": moisture,
                                              "temp": temp})
        # now maybe do something with the result?
    except Exception as e:
        print("Exception in main loop: {}".format(e))

    # sleep until we try again. TODO: this will be deep sleep eventually...
    time.sleep(POLL_INTERVAL)
