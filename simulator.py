#!/usr/bin/env python
import airplane
import vector
import math
import Tkinter

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
                crash_list.append(o1)
                crash_list.append(o2)
            elif abs(dist.z)<200.0 and (dist.x**2+dist.y**2)<1000.0**2:
                warning_list.append(o1)
                warning_list.append(o2)

    return crash_list, warning_list

def executeTimestep(airplane_list,deltat):
    for o in airplane_list:
        o.executeTimestep(deltat)

class GuiClass(object):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.periodicCount = 0
        self.airplane_list = [airplane.ControlableAirplane("Test Craft",vector.recvec(20000.0,20000.0,4000.0),vector.recvec(250.0,0.0,0.0))]
        self.warning_list = []
        self.crash_list = []
        self.canvas = Tkinter.Canvas(self.root,height=300,width=300)
        self.canvas.pack(fill=Tkinter.BOTH,expand=True)
        self.root.bind("<Configure>",self.drawCanvas)
        self.drawCanvas()

    def go(self):
        self.root.after(100,self.periodicExecution)
        self.root.mainloop()

    def periodicExecution(self):
        self.periodicCount+=1
        executeTimestep(self.airplane_list,0.1)
        res = check_proximity(self.airplane_list)
        self.crash_list = res[0]
        self.warning_list = res[1]
        if self.periodicCount%10==0:
            self.drawCanvas()

        if self.periodicCount%100==0:
            # insert control code here
            pass

        self.root.after(100,self.periodicExecution)
        

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
                self.canvas.create_text(x_pos,y_pos,anchor=Tkinter.SW,text="  "+o.getName())
                self.canvas.create_text(x_pos,y_pos,anchor=Tkinter.NW,text="  %.fm"%pos.z)

if __name__=="__main__":
    main()
