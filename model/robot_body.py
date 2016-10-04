'''
Author: Jake Sganga
Date: 8/3/16

robot_body gives the shape of the simple robot body (cube for now) and 
the positions and orientations of the catheter arms to be used in the visualizations

'''
import sys, time
import numpy as np
import functions.trig as trig

class body(object):
    """Everything in mm and rad.
    origin at base, +Z pointing up toward head, +X is right arm, +Y is front
    3 Euler angles, ZYZ"""
    def __init__(self):
        self.height  = 1000
        self.width   = 500
        self.depth   = 250
        self.head_side = 20
        self.density = 0.5e-3 #g/mm^3, random
        self.mass_body = self.density * self.height * self.width * self.depth
        self.mass_head = self.density * self.head_side ** 3
        self.x_sensed  = np.zeros(6)

    def get_wire_frame(self, n = 20):
        '''gives the n x 3 array of the edges in ground frame'''
        R = trig.R_zyz(self.x_sensed[3:])
        

