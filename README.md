Flight Control Exercise
=======================

This was an assignment as part of a class I taught at CSU Stanislaus to help
familiarize the students with python in a fun way, as well as a chance to
think about how to solve complex problems. In this exercise the students have
to develop a flight control systems which sends instructions to airplanes so
that they avoid each other in the air.

There are two simulators for watching the result of the exercise:
`simulator.py` will run a real-time simulation of the airplanes showing their
positions on the screen along with an altitude for each one. The `fastsim.py`
program runs a faster simulation, suitable for debugging.

Each airplane has a desired heading and altitude, however they will obey any
commands given by the flight controller. If airplanes come within 100 meters
of each other they are assumed to have crashed and the simulator will register
a penalty. If airplanes come within 10km of one another in horizontal distance
and within 600 meters in altitude they are assumed to be too close and the
simulator will register a penalty.

Airplane Characteristics
------------------------
The airplanes themselves are not very maneuverable. The airplanes have the
following limitations:

- Maximum turn rate: 1.5 degrees per second
- Maximum incline: +/- 7.5 degrees from level
- Maximum altitude: 10,000 meters
- Minimum altitude: 6,000 meters
- Maximum speed: 250 meters per second
- Minimum speed: 215 meters per second

These limits are designed to make the problem fairly challenging.

The Flight Control System
-------------------------
The flight control system is in the module `flight_control.py`, which contains
a class called `FlightController`. This is the class you should modify to
create your own flight control system. This class is initialized when the
simulations begins, then every 10 seconds the `executeControl` method of the
`FlightController` class is called. The only argument included is a list of
airplanes. Each member of the list is an object of the type
`airplane.ControllableAirplane` which has methods to both let you find its
current position and speed, and to send it commands.

Included, as a sample, is a `flight_control.py` module which sends the
instruction to each airplane to remain on its desired heading at its desired
altitude and speed. 

Airplane Tracking
-----------------
 
