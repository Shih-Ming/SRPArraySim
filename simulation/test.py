import matplotlib.pyplot as plt
from Drone import (Drone, Master, Slave)
import Globals as gb
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
from scipy import signal


# #plot 3D
# from mpl_toolkits import mplot3d
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
# plt.show()

# class Person():
#     def __init__(self, pos):
#         self.kk = pos
#         self.pp = 3
#
#
# class Student(Person):
#     def __init__(self, pos):
#         super().__init__(pos)
#
#
# s1 = Student(1)
# print(s1.pp)
a = "aa"
b = "bb"
c = a + b
print(c)
"""
plot.axes(projection='polar')

# Set the title of the polar plot
plot.title('Circle in polar format:r=R')

# Plot a circle with radius 2 using polar form
rads = np.arange(0, (2 * np.pi), 0.01)

for radian in rads:
    plot.polar(radian, radian * 2, '.')

# Display the Polar plot
plot.show()


Bob = Master()
Bob.pos_assign(1, 3, -4)
vib = 3  # vibration type 0-3
while(gb.time_index < 1000):
    Bob.vibration(vib)
    gb.time_index = gb.time_index + 1
    gb.time = gb.time_index * gb.time_interval
if vib == 0:
    plt.title("ideal")
    plt.xlabel("time")
    plt.ylabel("x axis")
    plt.plot(Bob.Pos_Act[:, 0])
    plt.show()
elif vib == 1:
    plt.title("sin")
    plt.xlabel("time")
    plt.ylabel("z axis")
    plt.plot(Bob.Pos_Act[1:, 2])
    plt.show()
elif vib == 2:
    plt.title("damping")
    plt.xlabel("time")
    plt.ylabel("x axis")
    plt.plot(Bob.Pos_Act[:, 0])
    plt.show()
elif vib == 3:
    plt.title("ellipse")
    plt.xlabel("x axis")
    plt.ylabel("y axis")
    plt.plot(Bob.Pos_Act[1:, 0], Bob.Pos_Act[1:, 1])
    plt.show()
else:
    pass
"""
