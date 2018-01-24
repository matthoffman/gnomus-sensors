from config import secrets
import machine


def do_connect():
    import network
    ap_if = network.WLAN(network.AP_IF)
    # Turn off the AP if it's on
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets["ssid"], secrets["network_password"])
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')

