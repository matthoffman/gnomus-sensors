# Seed Bed Sensors

## Rough design

I'm assuming that we'll have one or more trays or plastic bins of some sort, and they'll have little cups inside them 
filled with soil. Then the bottoms of the bins or trays will be filled with water (so bottom-watering, more or less).

So the bins will have to be pretty close to level.

This node needs to: 

Phase 1: 
 1. measure water level in the tray
 2. measure moisture level in a few select seed cups
 3. report that back to the server, so we can water them when they're dry
 
Phase 2: 
 4. control a solenoid that dispenses water from an elevated bucket

Phase X:
 5. measure light levels (not really necessary, but interesting and easy to do).

Eventually, it could also turn the light on and off, but it's easy enough to do that with a standard ol' timer, so not sure that's worth wiring up.


# Post format: 

I'm not really sure what the format should look like.

## Sensor IDs
ESP8266's have a built-in ID concept for the module as a whole.
In some cases (1-wire, in particular) we have a sensor ID too. Most others don't, but they generally do have an address 
that corresponds to where they were plugged in.

So I think we need a "sensor address" and a "sensor ID" as separate things. 

An address might be `module1.adc`, or `module1.0x76.1`. Then on the server we associate that with an actual sensor ID. 
Then we could choose to make sensor ID unique, even unique to a location if we wanted.
Or we could hedge a bit and record both sensor ID and location ID, just in case the sensor moves. Maybe it's actually a moving sensor? Robot? Drone? Who knows...
 
Ok, I like that: 
- sensor address is distinct from sensor ID
- sensor ID is unique to a particular sensor attached to a particular module. Replace a moisture meter with a temperature or other meter on a given ADC port and it gets a new ID
- modules only know their addresses and the readings from those addresses
- maybe sensor IDs can move, maybe not... not sure. But I'll go ahead and say probably they can. They have a current location, though.
- record both sensor ID and location in readings.

So perhaps it looks like:

```json
    { "abc123.adc.1": {"value": 0.23}, 
      "abc123.adc.2": {"value": 0.31},
      "abc123.adc.3": {"value": 334}, 
      "abc123.0x76": {"value": 432}
    }  
```

Now, in this example, the module really doesn't know anything at all about what's connected to it. Which is probably overkill, but it's an option for sure.

But honestly, the thing almost always needs to know what's connected to it anyway. The example of interchangeable things on an ADC port is interesting, but in practice... I only have 1 thing that connects there (soil moisture). Everything else needs explicit code to read it. And I'm going to have different files to load on each different module corresponding to what sensors I'm attaching; I'm not hot-plugging sensors willy-nilly on these things.
The chances that I'll want to unplug something from an ADC, plug in a different kind of sensor, and won't be able to do a quick update on the code on the sensor is pretty slim. 
But being able to set up a new sensor and have it just work without needing new config is kind of nice. Of course I wouldn't know the location of it upfront, but ...

What if sensor IDs are a concatenation of the two:
module_id.some_sensor_id ? 

Perhaps for addressable (IPC? what's it called) sensors, it might look like: 
`module_id.0x76.1` for the first connected soil sensor to a 4-channel ADC.
But then, of course, if I changed what was connected to that ADC, then what? It's not really unique to a particular sensor.

So, root issue: Do I want a sensorID to be absolutely unique? Who manages that? The module itself? That code then gets specific to that location, which we don't want. 
All it knows is readings from somewhere, it doesn't really know what it's reading. In the case of an ADC, it really doesn't even know what the type is, either.




Options:
1. device sends just sensor IDs and values, and backend has to pre-understand those sensors are to tie them to a location and a reading type.
2. device registers sensors on startup: "sensor ID foo is of type X" (and location?)
3. device sends it all with every post: sensor ID is of type X and has reading Y

Maybe location is still pre-understood?

Note that a sensor can measure more than one thing (temp/humidity/pressure sensors) but we could split that into several.


Here's what option #3 might look like: 

```json
     [
         {
             "sensor_id": "foo_1",
             "type": "temperature", 
             "value": 0.23
         },
         {
             "sensor_id": "foo_2",
             "type": "humidity", 
             "value": 0.23
         },
         {
             "sensor_id": "foo_3",
             "type": "soil moisture", 
             "value": 0.23
         }
     ]
``` 
    
Or, in a form that would be a bit easier for sensors to produce: 

```json
    { "temperature": [
        { "id": "foo_1", "value": 0.23}, 
        { "id": "foo_2", "value": 0.24}],
      "soil_moisture": [
        { "id": "foo_3", "value": 432} ]
    }  
```

And sure enough, here's what they're actually producing, when I sketched this out last week: 

```json
    { "temperature": [
        { "foo_1": 0.23}, 
        { "foo_2": 0.24}],
      "soil_moisture": [
        { "foo_3": 432} ]
    }  
```

Eh, just version the protocol and don't worry about it. Make sure to send `"version": 1` to start with.
