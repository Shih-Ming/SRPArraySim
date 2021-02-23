from mpl_toolkits import mplot3d
from Drone import (Drone, Master, Slave, drone_generating)
import Globals as gb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from Target import Target


gb.freq = 3.5e9
drone_generating(num=4, type='linear')
# 1000 targ_points, 10m target radius, ref_pos=[0,0,0]
t1 = Target(N=1000, R=100, pos=[0, 0, 0], axis='xy')
vib = 4  # vibration type, gaussian
gb.Amp = 0.2*(gb.speed_em/gb.freq)
while(gb.time_index < gb.times):
    # if(gb.time_index == 0):
    #     [data_x, data_y, title] = t1.field_generating(
    #         type='mag', color='g.')
    #     line0, = plt.polar(data_x, data_y, 'g.')
    gb.update_frame()
    for drone_j in range(len(gb.drones)):
        gb.drones[drone_j].vibration(vib)
        if(drone_j != 0):
            gb.drones[drone_j].transmit()
    t1.field_generating()

# ---plot ideal field---
# t1.field_plotting(type='mag', index=0,
#                   title="Beamforming in Ideal Case",ylims = [-10,3])

# ---plot extreme field---
# t1.field_plotting_extreme(type='mag', compensation=False,
#                           title="Max and Min Value of the Beam without Phase Compensation")  # origin, without compensation
# t1.field_plotting_extreme(type='mag', compensation=True,
#                           title="Max and Min Value of the Beam with Phase Compensation")  # transmit(), with compensation
# ---plot the expected field plus/minus RMS error
t1.field_plotting_ideal_plus_rms(type='mag', title="", ylims = [-20,6], bool_compen=0, bool_noncompen=0)
t1.field_plotting_ideal_plus_rms(type='mag', title="", ylims = [-20,6], bool_compen=0, bool_noncompen=1)
t1.field_plotting_ideal_plus_rms(type='mag', title="", ylims = [-20,6], bool_compen=1, bool_noncompen=0)
t1.field_plotting_ideal_plus_rms(type='mag', title="", ylims = [-20,6], bool_compen=1, bool_noncompen=1)
plt.show()
# ---plot error---
# t1.field_plotting_error(type='mag', compensation=False,
#                         title="RMS Error of the Beam without Phase Compensation")  # origin, without compensation
# t1.field_plotting_error(type='mag', compensation=True,
#                         title="RMS Error of the Beam with Phase Compensation")  # transmit(), with compensation
# t1.field_plotting_error_overlay(type='mag',
#                                 title="RMS Error of the Beam")
# plt.show()
# t1.field_plotting_summed(type='mag',
#                          title="Sum ")

# # ---plot summed field---
# t1.field_plotting_overlay(type='mag', index1=1, index2=2, index3=3, index4=4,
#                           title="magnitude in xy-plane with viberation (index=1, 2, 3, 4)")
# t1.field_plotting_summed(type='mag', index1=1, index2=2, index3=3, index4=4,
#                          title="extreme magnitude in xy-plane with vibration (index=1, 2, 3, 4)")
#
# t1.field_plotting_overlay(type='mag', index1=11, index2=12, index3=13, index4=14,
#                           title="magnitude in xy-plane with viberation (index=11, 12, 13, 14)")
# t1.field_plotting_summed(type='mag', index1=11, index2=12, index3=13, index4=14,
#                          title="average magnitude in xy-plane with viberation (index=11, 12, 13, 14)")
#
# t1.field_plotting_overlay(type='mag', index1=51, index2=52, index3=53, index4=54,
#                           title="magnitude in xy-plane with viberation (index=51, 52, 53, 54)")
# t1.field_plotting_summed(type='mag', index1=51, index2=52, index3=53, index4=54,
#                          title="average magnitude in xy-plane with viberation (index=51, 52, 53, 54)")
#
# t1.field_plotting_overlay(type='mag', index1=91, index2=92, index3=93, index4=94,
#                           title="magnitude in xy-plane with viberation (index=91, 92, 93, 94)")
# t1.field_plotting_summed(type='mag', index1=91, index2=92, index3=93, index4=94,
#                          title="average magnitude in xy-plane with viberation (index=91, 92, 93, 94)")


def plot_drones():
    vib = 4  # vibration type, gaussian
    gb.Amp = 0.025
    ax = plt.axes(projection='3d')
    gb.time_index = 0
    while(gb.time_index < 1000):
        if(gb.time_index == 0):
            x_data = []
            y_data = []
            z_data = []
            for i in range(len(gb.drones)):
                x_data.append(gb.drones[i].Pos_Act[gb.time_index][0])
                y_data.append(gb.drones[i].Pos_Act[gb.time_index][1])
                z_data.append(gb.drones[i].Pos_Act[gb.time_index][2])
            line0 = ax.scatter3D(x_data, y_data, z_data, c='g')
            # line0, = plt.polar(data_x, data_y, 'g.')
        gb.time_index = gb.time_index + 1
        gb.time = gb.time_index * gb.time_interval
        for drone_j in range(len(gb.drones)):
            gb.drones[drone_j].vibration(vib)
        if(gb.time_index == 100):
            x_data = []
            y_data = []
            z_data = []
            for i in range(len(gb.drones)):
                x_data.append(gb.drones[i].Pos_Act[gb.time_index][0])
                y_data.append(gb.drones[i].Pos_Act[gb.time_index][1])
                z_data.append(gb.drones[i].Pos_Act[gb.time_index][2])
            line100 = ax.scatter3D(x_data, y_data, z_data, c='b')
        if(gb.time_index == 500):
            x_data = []
            y_data = []
            z_data = []
            for i in range(len(gb.drones)):
                x_data.append(gb.drones[i].Pos_Act[gb.time_index][0])
                y_data.append(gb.drones[i].Pos_Act[gb.time_index][1])
                z_data.append(gb.drones[i].Pos_Act[gb.time_index][2])
            line200 = ax.scatter3D(x_data, y_data, z_data, c='y')
        if(gb.time_index == 999):
            x_data = []
            y_data = []
            z_data = []
            for i in range(len(gb.drones)):
                x_data.append(gb.drones[i].Pos_Act[gb.time_index][0])
                y_data.append(gb.drones[i].Pos_Act[gb.time_index][1])
                z_data.append(gb.drones[i].Pos_Act[gb.time_index][2])
            line300 = ax.scatter3D(x_data, y_data, z_data, c='r')
    ax.legend((line0, line100, line200, line300), ('time_index = 0',
                                                   'time_index = 100', 'time_index = 200', 'time_index = 300'), loc='upper left')
    plt.show()


# plot_drones()

# t1.field_generating(type='mag')

# --------------test--------------
"""
# read antenna


# update new frame
Bob = Master()
Bob.pos_assign(1, 3, -4)
while(gb.time_index < 1000):
    vib = 1  # vibration type
    gb.time_index = gb.time_index + 1
    gb.time = gb.time_index * gb.time_interval
    Bob.vibration(vib)
fig, (ax1, ax2, ax3) = plt.subplots(3)

ax1.plot(Bob.Pos_Act[1:, 0])  # x-axis
ax2.plot(Bob.Pos_Act[1:, 1])  # y-axis
ax3.plot(Bob.Pos_Act[1:, 2])  # z-axis
plt.show()
parsing_file('2.9GHz_3D_pattern.csv')

d = Drone()
d.pos_assign(1, 2, 3)
print(d.Pos_Ide)
"""
