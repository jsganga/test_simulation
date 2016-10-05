
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import random

from functions import low_pass_filter as f
import functions.trig as trig

from model.robot_body import body

a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([[0, 1, 0], [1, 0, 0]])
