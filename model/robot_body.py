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
        self.head_side = 200
        self.density = 0.5e-3 #g/mm^3, random
        self.mass_body = self.density * self.height * self.width * self.depth
        self.mass_head = self.density * self.head_side ** 3
        self.x_sensed  = np.zeros(6)
        self.body_corners = np.array([[self.width / 2, self.depth / 2, 0],
                                     [-self.width / 2, -self.depth / 2, self.height]])
   
        self.head_corners = np.array([[self.head_side / 2, self.head_side / 2, self.height],
                                     [-self.head_side / 2, -self.head_side / 2, self.height + self.head_side]])

        self.get_wire_frame()

    def get_wire_frame(self):
        '''gives the array of the edges in ground frame in the order that allows for 
        the plotting of a line to connect the appropriate lines'''
        R = trig.R_zyz(self.x_sensed[3:])
        self.body_points = self.get_line_array(self.body_corners).dot(R) + self.x_sensed[:3]
        self.head_points = self.get_line_array(self.head_corners).dot(R) + self.x_sensed[:3]

    def get_line_array(self, corners):
        '''ordering the corners, overlaps are necessary for this approach'''
        indeces = np.array([[0, 0, 0],
                            [1, 0, 0],
                            [1, 1, 0],
                            [0, 1, 0],
                            [0, 0, 0],
                            [0, 0, 1],
                            [1, 0, 1],
                            [1, 0, 0],
                            [1, 0, 1],
                            [1, 1, 1],
                            [1, 1, 0],
                            [1, 1, 1],
                            [0, 1, 1],
                            [0, 1, 0],
                            [0, 1, 1],
                            [0, 0, 1]])
        return corners[indeces, [0,1,2]]











        

