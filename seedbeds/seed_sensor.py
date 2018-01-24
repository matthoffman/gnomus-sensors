import machine
import time
import ds18x20
import onewire

from machine import Pin


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



