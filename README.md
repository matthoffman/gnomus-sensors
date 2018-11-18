It makes me sad to have sensor-reading code copied and pasted here, but some of the sensor code for ESP8266 isn't available in a repo. So here they are.

TODO: 

- [ ] write first cut: something that stays connected, polls a thermometer and soil moisture sensor every hour, and sends the data to a given URL.
- [ ] write a manage.py or similar that will pull in a non-source-controlled config.py (secret.py?) with network SSID and password (and any other private info) and then flash them to the board. Might want "manage.py flash seed_sensor", etc. to tell it which files to pull.
    - [ ] bonus points: open a REPL?
- [ ] implement deep sleep between polls

