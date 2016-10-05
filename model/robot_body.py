'''
Author: Jake Sganga
Date: 8/3/16

robot_body gives the shape of the simple robot body (cube for now) and 
the positions and orientations of the catheter arms to be used in the visualizations

'''
import sys, time
import numpy as np
import functions.trig as trig

class robot_body(object):
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
        self.R         = trig.R_zyz(self.x_sensed[3:])
        self.body_corners = np.array([[self.width / 2, self.depth / 2, 0],
                                     [-self.width / 2, -self.depth / 2, self.height]])
   
        self.head_corners = np.array([[self.head_side / 2, self.head_side / 2, self.height],
                                     [-self.head_side / 2, -self.head_side / 2, self.height + self.head_side]])

        self.arm_bases = np.array([[self.width / 2,  0, (2 / 3) * self.height, 0,     np.pi / 2, 0],
                                   [-self.width / 2, 0, (2 / 3) * self.height, np.pi, np.pi / 2, 0]])

        self.get_wire_frame()


    def set_position(self, x_set):
        self.x_sensed = x_set.copy()
        self.R        = trig.R_zyz(self.x_sensed[3:])

    def get_position(self):
        return self.x_sensed.copy()

    def get_arm_bases(self):
        x_arm = self.arm_bases[:,:3].dot(self.R.T)
        R_right = self.R.dot(trig.R_zyz(self.arm_bases[0,3:]))
        R_left  = self.R.dot(trig.R_zyz(self.arm_bases[1,3:]))
        P_right = np.hstack((R_right, x_arm[0,:]))
        P_left  = np.hstack((R_left,  x_arm[1,:]))
        return P_right, P_left

    def get_wire_frame(self):
        '''gives the array of the edges in ground frame in the order that allows for 
        the plotting of a line to connect the appropriate lines'''
        self.body_points = self.get_vertices(self.body_corners).dot(self.R) + self.x_sensed[:3]
        self.head_points = self.get_vertices(self.head_corners).dot(self.R) + self.x_sensed[:3]

        self.body_faces = self.get_face_tuples(self.body_points)
        self.head_faces = self.get_face_tuples(self.head_points)

    def get_vertices(self, corners):
        '''gets the corners'''
        indeces = np.array([[0, 0, 0],
                            [1, 0, 0],
                            [1, 1, 0],
                            [0, 1, 0],
                            [0, 0, 1],
                            [1, 0, 1],
                            [1, 1, 1],
                            [0, 1, 1]])
        return corners[indeces, [0,1,2]]

    def get_face_tuples(self, points):
        '''groups the corner tuples as 6 faces'''
        face_indeces = np.array([[0, 1, 2, 3],
                                 [4, 5, 6, 7],
                                 [0, 1, 5, 4],
                                 [1, 2, 6, 5],
                                 [2, 3, 7, 6],
                                 [3, 0, 4, 7]])
        tuple_list = list(zip(points[:,0], points[:,1], points[:,2]))
        # faces = []
        # for i_face in range(len(face_indeces)):
        #     for i_tuple in range(len(face_indeces[0])):
        #         faces.append(tupleList[face_indeces[i_face, i_tuple]])
        faces = [[tuple_list[face_indeces[ix][iy]] for iy in range(len(face_indeces[0]))] for ix in range(len(face_indeces))]
        return faces












        

