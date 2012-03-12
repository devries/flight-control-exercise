import airplane
import vector
import math

class FlightController(object):
    """This is the flight controller class. It's job is to send commands to
    send commands to the airplanes to make sure they don't hit each other
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
