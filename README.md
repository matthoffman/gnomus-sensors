# Gnomus sensors

This is the code for sensors based around ESP8266 modules running Micropython. They're designed to communicate with a server
running [gnomus-server](https://github.com/matthoffman/gnomus-server).

They're designed to help with various things around the garden. I enjoy gardening, but I'm not great at remembering to 
check on my seed trays every day, or remembering to water the various beds. So these are a simple(-ish) way to track things
like soil moisture, temperature, humidity, light exposure, and so on, and make it easy to see. 

This is particularly important for seedlings and tree cuttings, since in my current house they are stored out of my main 
living area, so they're easy to forget about for a bit too long.

It's also an excuse to play with sensors and Micropython, which is a lot of fun. 

This is very much a work in progress.  You'll notice, at this point in early development, that there's some excessively detailed design notes strewn about in files like this one.
That's because I find time to work on this in small increments, so it helps me to be overly explicit with what I'm thinking so that I can pick it up again later when I have a bit of time.

## Gnomus?

A word invented by Paracelsus in the 18th century to describe small earth-dwelling creatures; it became the English "gnome". 
The plan is for this server to manage sensors that are deployed in various places in the garden inside plastic garden gnomes, so the name seems appropriate.

## TODO: 


- [ ] write first cut: something that stays connected, polls a thermometer and soil moisture sensor every hour, and sends the data to a given URL.
- [ ] write a manage.py or similar that will pull in a non-source-controlled config.py (secret.py?) with network SSID and password (and any other private info) and then flash them to the board. Might want "manage.py flash seed_sensor", etc. to tell it which files to pull.
    - [ ] bonus points: open a REPL?
- [ ] implement deep sleep between polls

It makes me sad to have sensor-reading code copied and pasted here, but some of the sensor code for ESP8266 isn't available in a repo. So here they are, for now.
