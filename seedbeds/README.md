# Seed Bed Sensors

## Rough design

I'm assuming that we'll have one or more trays or plastic bins of some sort, and they'll have 
So the bins will have to be pretty close to level.

This node needs to: 

Phase 1: 
 1. measure water level in the tray
 2. measure moisture level in a few select seed cups (note: means external ADC, or wiring up one moisture thing to be digital)
 3. report that back to the server, so we can water them when they're dry
 
Phase 2: 
 4. control a solenoid that dispenses water from an elevated bucket

Phase X:
 5. measure light levels (not really necessary, but interesting and easy to do).

Eventually, it could also turn the light on and off, but it's easy enough to do that with a standard ol' timer, so not sure that's worth wiring up.

