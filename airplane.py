"""Airplane Library. Contains things that fly through the sky."""
import vector
import math

class FlyingObject(object):
    def __init__(self,name,position=vector.Threevec(),velocity=vector.Threevec()):
        self.name = name
        self.position = position
        self.velocity = velocity

    def getPosition(self):
        return self.position

    def getVelocity(self):
        return self.velocity

    def isControlable(self):
        return False

    def getName(self):
        return self.name

    def executeTimestep(self,deltat):
        self.position += self.velocity*deltat

class ControlableAirplane(FlyingObject):
    vmin = 215.0 # meters per second
    vmax = 250.0 # meters per second
    vcruise = 230.0 # Meters per second
    alt_min = 2000.0 # meters
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
        self.desiredSpeed = ControlableAirplane.vcruise
        self.desiredAltitude = ControlableAirplane.alt_cruise

    def isControlable(self):
        return True

    def sendHeading(self,heading):
        self.commandHeading = heading

    def sendAltitude(self,altitude):
        self.commandAltitude = altitude

    def sendSpeed(self,speed):
        self.commandSpeed = speed

    def getDesiredHeading(self):
        return self.desiredHeading

    def getDesiredSpeed(self):
        return self.desiredSpeed

    def getDesiredAltitude(self):
        return self.desiredAltitude

    def executeTimestep(self,deltat):
        speed = self.commandSpeed

        if speed>ControlableAirplane.vmax:
            speed = ControlableAirplane.vmax
        elif speed<ControlableAirplane.vmin:
            speed = ControlableAirplane.vmin

        max_delta_altitude = speed*math.sin(ControlableAirplane.max_tilt)*deltat

        altitude = self.commandAltitude

        if altitude>ControlableAirplane.alt_max:
            altitude = ControlableAirplane.alt_max
        elif altitude<ControlableAirplane.alt_min:
            altitude = ControlableAirplane.alt_min

        current_heading = math.pi/2.0-self.velocity.phi
        # headings are between 0 and 2pi
        if current_heading < 0.0:
            current_heading += 2.0*math.pi
        current_altitude = self.position.z

        tilt_set = 0.0
        delta_altitude = altitude - current_altitude

        if delta_altitude > max_delta_altitude:
            tilt_set = ControlableAirplane.max_tilt
        elif delta_altitude < max_delta_altitude and delta_altitude > -max_delta_altitude:
            tilt_set = math.asin(delta_altitude/speed/deltat)
        else:
            tilt_set = -ControlableAirplane.max_tilt

        heading_set = current_heading
        delta_heading = self.commandHeading - current_heading

        # Adjust turn so it can go through 2pi
        if delta_heading > math.pi:
            delta_heading -= 2.0*math.pi
        elif delta_heading < -math.pi:
            delta_heading += 2.0*math.pi

        max_delta_heading = ControlableAirplane.turn_rate*deltat

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

