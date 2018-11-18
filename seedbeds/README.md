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

Currently, the sensors post JSON in a format like the following: 

```json
    { "temperature": [
        { "foo_1": 0.23}, 
        { "foo_2": 0.24}],
      "soil_moisture": [
        { "foo_3": 432} ]
    }  
```

In this case, `foo_x` is the ID of individual sensors. 
