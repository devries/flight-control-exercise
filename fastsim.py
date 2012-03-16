#!/usr/bin/env python
import airplane
import vector
import math
import flight_control
import Tkinter
import numpy.random as random
import sys

RADAR_RADIUS = 70000.0 # range of radar

def main():
    gui = GuiClass()
    gui.go()

def check_proximity(airplane_list):
    warning_list = []
    crash_list = []
    remaining_list = list(airplane_list)

    for i in range(len(remaining_list)):
        o1 = remaining_list.pop()
        for o2 in remaining_list:
            dist = o2.getPosition()-o1.getPosition()
            if abs(dist)<100.0:
                if not o1 in crash_list:
                    crash_list.append(o1)
                if not o2 in crash_list:
                    crash_list.append(o2)
            elif abs(dist.z)<600.0 and (dist.x**2+dist.y**2)<10000.0**2:
                if not o1 in warning_list:
                    warning_list.append(o1)
                if not o2 in warning_list:
                    warning_list.append(o2)

    return crash_list, warning_list

def executeTimestep(airplane_list,deltat):
    for o in airplane_list:
        o.executeTimestep(deltat)

def createAirplaneList():
    names = createNameList()
    p1, p2 = generateCollidingPair(0.0,10000.0,8000.0,names.pop(),names.pop(),200.0)
    p3, p4 = generateCollidingPair(0.0,0.0,8000.0,names.pop(),names.pop(),250.0)
    p5, p6 = generateCollidingPair(10000,0.0,7000.0,names.pop(),names.pop(),300.0)
    p7 = generateRandomPlane(names.pop(),8000.0)
    p8 = generateRandomPlane(names.pop(),7000.0)
    p9 = generateRandomPlane(names.pop(),6000.0)
    p10 = generateRandomPlane(names.pop(),8000.0)

    return [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]
    
def generateCollidingPair(x,y,z,name1,name2,tcollision):
    """Create a set of airplanes which will collide at position x, y, z in tcollision seconds"""
    crashpos = vector.recvec(x,y,z)

    phi1 = -math.pi+random.random_sample()*2.0*math.pi
    phi2 = -math.pi+random.random_sample()*2.0*math.pi
    v = airplane.ControllableAirplane.vcruise

    v1 = vector.sphvec(v,math.pi/2.0,phi1)
    v2 = vector.sphvec(v,math.pi/2.0,phi2)
    pos1 = crashpos-v1*tcollision
    pos2 = crashpos-v2*tcollision

    airplane1 = airplane.ControllableAirplane(name1,pos1,v1)
    airplane2 = airplane.ControllableAirplane(name2,pos2,v2)

    return airplane1, airplane2

def generateRandomPlane(name,altitude):
    phi = -math.pi+random.random_sample()*2.0*math.pi
    dir_flight = phi+3.0*math.pi/4.0+random.random_sample()*math.pi/2.0

    position = vector.cylvec(70000.0,phi,altitude)
    velocity = vector.sphvec(airplane.ControllableAirplane.vcruise,math.pi/2.0,dir_flight)

    return airplane.ControllableAirplane(name,position,velocity)

def createNameList():
    callsigns = ['United','American','Delta','N']
    names=[]
    for i in range(10000):
        names.append(callsigns[i%len(callsigns)]+str(i))

    random.shuffle(names)
    return names

def scoreGame(airplane_list,penalties):
    score = 0
    print penalties,"points to deduct for penalties."
    for a in airplane_list:
        score+=1000 # Airplane is still there
        print a.getName(),
        v = a.getVelocity()
        p = a.getPosition()
        heading = math.pi/2.0-v.phi
        if abs(heading-a.getDesiredHeading())<0.01 or abs(abs(heading-a.getDesiredHeading())-2.0*math.pi)<0.01:
            score+=500 # Airplane on heading
            print "on heading",

        if abs(p.z-a.getDesiredAltitude())<100.0:
            score+=250 # Airplane at altitude
            print "at altitude",
        
        if abs(abs(v)-a.getDesiredSpeed())<1.0:
            score+=250 # Airplane at speed
            print "at speed",

        print

    print "Your score:",score-penalties

class GuiClass(object):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.periodicCount = 0
        self.penalties = 0
        self.count_warnings = False
        airplane_names = createNameList()
        self.airplane_list = createAirplaneList()
        self.warning_list = []
        self.crash_list = []
        self.flightControl = flight_control.FlightController()
        self.flightControl.executeControl(list(self.airplane_list))
        self.canvas = Tkinter.Canvas(self.root,height=300,width=300)
        self.canvas.pack(fill=Tkinter.BOTH,expand=True)
        self.root.bind("<Configure>",self.drawCanvas)
        self.drawCanvas()

    def go(self):
        self.root.after(10,self.periodicExecution)
        self.root.mainloop()

    def periodicExecution(self):
        self.periodicCount+=1
        executeTimestep(self.airplane_list,0.1)
        res = check_proximity(self.airplane_list)
        self.crash_list = res[0]
        self.warning_list = res[1]
        if self.periodicCount%10==0:
            self.drawCanvas()

        for p in self.crash_list:
            print p.getName(),"crashed. 1000 point penalty"
            self.airplane_list.remove(p)
            self.penalties+=1000

        if self.periodicCount==1000:
            self.count_warnings = True
            print "Near-Collisions are now penalized."

        if self.periodicCount%100==0:
            print (6000-self.periodicCount)/10,"seconds remain."
            self.flightControl.executeControl(list(self.airplane_list))
            if self.count_warnings:
                n = len(self.warning_list)
                if n>0:
                    print n,"airplanes are too close."
                    print n*100,"point penalty."
                    self.penalties+=100*n

        if self.periodicCount==6000:
            scoreGame(self.airplane_list,self.penalties)
            sys.exit(0)

        self.root.after(10,self.periodicExecution)
        

    def drawCanvas(self,event=None):
        self.canvas.delete(Tkinter.ALL)
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        circ_radiusa = (width-10)/2
        circ_radiusb = (height-10)/2
        circ_radius = circ_radiusa
        if circ_radius>circ_radiusb:
            circ_radius=circ_radiusb

        self.canvas.create_oval(5,5,5+2*circ_radius,5+2*circ_radius)

        center_x = 5+circ_radius
        center_y = 5+circ_radius
        scale = RADAR_RADIUS/circ_radius

        for o in self.airplane_list:
            pos = o.getPosition()
            land_pos = vector.Threevec(pos.x,pos.y,0.0) # Get the land position
            if abs(land_pos)<RADAR_RADIUS:
                x_pos = land_pos.x/scale+center_x
                y_pos = -land_pos.y/scale+center_y
                color = "black"
                if o in self.crash_list:
                    color = "red"
                elif o in self.warning_list:
                    color = "orange"

                self.canvas.create_oval(x_pos-2,y_pos-2,x_pos+2,y_pos+2,fill=color)
                self.canvas.create_text(x_pos,y_pos,anchor=Tkinter.SW,fill=color,text="  "+o.getName())
                self.canvas.create_text(x_pos,y_pos,anchor=Tkinter.NW,fill=color,text="  %.fm"%pos.z)

if __name__=="__main__":
    main()
