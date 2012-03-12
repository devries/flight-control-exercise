"""Airplane Library. Contains things that fly through the sky."""
import vector
import math

class FlyingObject(object):
    def __init__(self,name,position=vector.Threevec(),velocity=vector.Threevec()):
        self.name = name
        self.position = position
        self.velocity = velocity

    def getPosition(self):
        """The position of the aircraft is returned as a vector.Threevec.
        The components are all in meters. The x-direction is East, the 
        y-direction is North, and the z-direction is altitude from sealevel."""
        return self.position.copy()

    def getVelocity(self):
        """The velocity of the aircraft is returned as a vector.Threevec.
        The components are all in meters per second. The x-direction is
        East, the y-direction is North, and the z-direction is up."""
        return self.velocity.copy()

    def isControllable(self):
        return False

    def getName(self):
        """The unique name of the aircraft is returned by this method."""
        return self.name

    def executeTimestep(self,deltat):
        self.position += self.velocity*deltat

class ControllableAirplane(FlyingObject):
    """An airplane which is controllable using the flight control system."""
    vmin = 215.0 # meters per second
    vmax = 250.0 # meters per second
    vcruise = 230.0 # Meters per second
    alt_min = 6000.0 # meters
    alt_max = 10000.0 # meters
    alt_cruise = 8000.0 # meters
    turn_rate = 1.5 * math.pi/180.0 # radians per second
    max_tilt = 7.5 * math.pi/180.0 # radians

    def __init__(self,name,position=vector.Threevec(),velocity=vector.Threevec()):
        FlyingObject.__init__(self,name,position,velocity)

        heading = math.pi/2.0-velocity.phi
        if heading<0.0:
            heading+=2.0*math.pi

        # Set the command info from current parameters
        self.commandHeading = heading
        self.commandSpeed = abs(velocity)
        self.commandAltitude = position.z

        # Set the desired info from current parameters, except speed.
        self.desiredHeading = heading
        self.desiredSpeed = ControllableAirplane.vcruise
        self.desiredAltitude = ControllableAirplane.alt_cruise

    def isControllable(self):
        """This will return True if you can send commands to the plane."""
        return True

    def sendHeading(self,heading):
        """Send the heading you would like the plane to turn to. The plane is
        limited to turn at a rate of 1.5 degrees per second. Note that the
        heading is given in radians with 0.0 being North, pi/2 is East, pi
        is South, and 3pi/2 is West."""
        self.commandHeading = heading

    def sendAltitude(self,altitude):
        """Send the altitude you would like the airplane to reach in meters. 
        Note that the airplane is limited to an up or down pitch of up to 7.5
        degrees, which means its maximum rate of altitude change is its speed
        times the sine of 7.5 degrees. The airplane is limited to altitudes
        between 6,000 and 10,000 meters. If you ask it to exceed its maximum
        altitude or drop below its minimum altitude, it will stay at the
        closest safe altitude."""
        self.commandAltitude = altitude

    def sendSpeed(self,speed):
        """Send the speed you would like the airplane to travel in meters per
        second. Note that the airplane is limited to speeds between 215 and
        250 meters per second. If you ask for a speed outside of this range, 
        the airplane will travel at the closest safe speed."""
        self.commandSpeed = speed

    def getDesiredHeading(self):
        """The desired heading of the aircraft is returned by this method
        (in radians, with 0 being North and pi/2 being East).
        The airplane should resume this heading after avoiding other 
        aircraft."""
        return self.desiredHeading

    def getDesiredSpeed(self):
        """The desired speed of the aircraft is returned by this method in
        meters per second. The aircraft should resume this speed after
        avoiding other aircraft."""
        return self.desiredSpeed

    def getDesiredAltitude(self):
        """The desired altitude of the aircraft is returned by this method in
        meters. The aircraft should resume this altitude after avoiding other
        aircraft."""
        return self.desiredAltitude

    def executeTimestep(self,deltat):
        """This method is called by the simulator to advance the aircraft
        through time by an amount deltat (in seconds). The aircraft tries
        to acommodate the commands given to it."""
        speed = self.commandSpeed

        if speed>ControllableAirplane.vmax:
            speed = ControllableAirplane.vmax
        elif speed<ControllableAirplane.vmin:
            speed = ControllableAirplane.vmin

        max_delta_altitude = speed*math.sin(ControllableAirplane.max_tilt)*deltat

        altitude = self.commandAltitude

        if altitude>ControllableAirplane.alt_max:
            altitude = ControllableAirplane.alt_max
        elif altitude<ControllableAirplane.alt_min:
            altitude = ControllableAirplane.alt_min

        current_heading = math.pi/2.0-self.velocity.phi
        # headings are between 0 and 2pi
        if current_heading < 0.0:
            current_heading += 2.0*math.pi
        current_altitude = self.position.z

        tilt_set = 0.0
        delta_altitude = altitude - current_altitude

        if delta_altitude > max_delta_altitude:
            tilt_set = ControllableAirplane.max_tilt
        elif delta_altitude < max_delta_altitude and delta_altitude > -max_delta_altitude:
            tilt_set = math.asin(delta_altitude/speed/deltat)
        else:
            tilt_set = -ControllableAirplane.max_tilt

        heading_set = current_heading
        delta_heading = self.commandHeading - current_heading

        # Adjust turn so it can go through 2pi
        if delta_heading > math.pi:
            delta_heading -= 2.0*math.pi
        elif delta_heading < -math.pi:
            delta_heading += 2.0*math.pi

        max_delta_heading = ControllableAirplane.turn_rate*deltat

        if delta_heading > max_delta_heading:
            heading_set += max_delta_heading
        elif delta_heading < max_delta_heading and delta_heading > -max_delta_heading:
            heading_set += delta_heading
        else:
            heading_set -= max_delta_heading

        new_velocity = vector.sphvec(speed,math.pi/2.0-tilt_set,math.pi/2.0-heading_set)

        new_position = self.position+(self.velocity/2.0+new_velocity/2.0)*deltat

        self.velocity = new_velocity
        self.position = new_position

