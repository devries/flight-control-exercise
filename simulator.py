#!/usr/bin/env python
import airplane
import vector
import math
import Tkinter

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
        self.canvas = Tkinter.Canvas(self.root,height=300,width=300)
        self.canvas.pack(fill=Tkinter.BOTH,expand=True)

    def go(self):
        self.root.after(100,self.periodicExecution)
        self.root.mainloop()

    def periodicExecution(self):
        pass

if __name__=="__main__":
    main()
