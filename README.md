Flight Control Exercise
=======================

This was an assignment as part of a class I taught at CSU Stanislaus to help
familiarize the students with python in a fun way, as well as a chance to
think about how to solve complex problems. In this exercise the students have
to develop a flight control systems which sends instructions to airplanes so
that they avoid each other in the air, but it seems now to be used to help
train AI models.

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
There are three basic methods of the `airplane.ControllableAirplane` class which allow for tracking:

1. `getName()` - returns a unique identifies as an ASCII string. The string
will include letters and numbers. These are displayed in the simulator above
and to the right of each airplane's position.
2. `getPosition()` - returns a `vector.Threevec` containing the current
position of the aircraft. The coordinates are in meters, with the x-axis
pointed East, the y-axis pointing North, and the z-axis pointing up with z=0
being sea-level.
3. `getVelocity()` - returns a `vector.Threevec` containing the current
velocity of the aircraft. The components are in meters per second with
directions corresponding to those in the `getPosition()` method.  

Airplane Control
----------------
There are several methods of the `airplane.ControllableAirplane` class which
send control commands to the airplanes. They are as follows:

1. `isControllable()` - returns True if the airplane can be controlled. This
will be true for all airplanes in the simulation.
2. `sendHeading(heading)` - commands that the aircraft turn to heading where
heading is an angle in radians that runs from 0 being North, through pi/2
being East, pi being South, and 3pi/2 being West. The aircraft will not
immediately assume this heading, but will turn toward this heading. The
maximum turn rate of these airplanes is 1.5 degrees per second.
3. `sendAltitude(altitude)` - commands the aircraft to climb or descend to
altitude` in meters. The rate of climb and descent is limited by the pitch of
the aircraft above or below the horizon. The maximum rate and which the
airplane can change altitude is at its speed times the sine of the pitch
angle. The maximum pitch angle for these airplanes is 7.5 degrees. The
aircraft is also limited to cruising between 6,000 and 10,000 meters altitude
and will not exceed those bounds.
4. `sendSpeed(speed)` - commands the aircraft to travel at the speed speed in
meters per second. The aircraft is limited to speeds between 215 and 250
meters per second and will not exceed those bounds. 

Airplane Request
----------------
The airplane is trying to get somewhere. In order to do that it will have
available a desired heading, altitude, and speed. These requested parameters
are available using the following methods of `airplane.ControllableAirplane`:

1. `getDesiredHeading()` - returns the desired heading in radians with 0 being North, pi/2 being East, etc. 
2. `getDesiredAltitude()` - returns the desired altitude in meters above sealevel.
3. `getDesiredSpeed()` - returns the desired speed in meters per second.

After dodging any potential aircraft in the way, the airplane should be allowed to resume these settings, but you will have to send it the appropriate commands.

Flight Control
--------------

You will be modifying the `flight_control.py` file, which contains the flight
control system. The system is encapsulated in a class called
`FlightController`. This class is instantiated by the simulator and then every
10 seconds the `executeControl` command is called with a single argument that
contains a list of all airplanes in the simulation. An example is provided in
the source code, which I copy below.

```python
import airplane
import vector
import math

class FlightController(object):
    """This is the flight controller class. Its job is to send commands to
    the airplanes to make sure they don't hit each other
    and get where they are going."""
    def __init__(self):
        """If you need to initialize any data structures do it here."""
        pass

    def executeControl(self,airplane_list):
        """Every 10 seconds a list (airplane_list) of flying objects will be
        passed to you. You can find the positions of the airplanes and issue
        flight control commands to them."""
        for a in airplane_list:
            a.sendHeading(a.getDesiredHeading())
            a.sendAltitude(a.getDesiredAltitude())
            a.sendSpeed(a.getDesiredSpeed())
```

Note that the example only sends airplanes their own desired headings,
altitudes, and speeds. It does not check for or avoid collisions. You will
need to change that by making sure that airplanes do not get too close or
crash.

During the simulation you will receive penalties for airplanes crashing or for
airplanes being too close together. Airplanes crash if they are within 100
meters of one another. Airplane are too close if their altitudes are within
600 meters of another airplane while they are within 10 km of one another. You
will receive a 1000 point penalty for any airplane that crashes and a 100
point penalty every 10 seconds for each airplane that is too close to another.

At the end of the simulation you receive 1000 points for each airplane that is
still flying. You get a bonus of 500 points for each airplane on the right
heading, 250 points for each airplane at the right speed, and 250 more points
for each airplane at the right altitude at the end of the simulation.
