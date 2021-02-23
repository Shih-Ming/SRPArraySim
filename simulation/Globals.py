import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

time_interval = 0.01
time_index = 0
time = -1
Amp = 0.05   # strength of wind
VibPeriod = 7.88  # T of sine vibration
freq = 1e6  # 2.9 GHz
times = 100 # times of iteration
spacing_lambda = 0.5  # spacing of drones with __ lambda
speed_em = 3e8        # speed of light
speed_us = 346.45     # speed of ultrasound
drones = []
# plot = plt.axes(projection='polar')


def update_frame():
    global time_index, time
    time_index = time_index + 1
    time = time_index * time_interval


def plot_drones():

    # #plot 3D
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    xdata = []
    ydata = []
    zdata = []
    for pt_j in range(len(drones)):
        xdata.append(drones[pt_j].Pos_Act[time_index][0])
        ydata.append(drones[pt_j].Pos_Act[time_index][1])
        zdata.append(drones[pt_j].Pos_Act[time_index][2])

    # ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
    ax.scatter3D(xdata, ydata, zdata)
    # plt.show()


def distance_calculate(a, b):
    distance = np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 +
                       (a[2] - b[2])**2)
    return distance


# input: source power, freq, distance
# return: received power density, phase
def emwave_propagate(power, distance, offset):
    power_density = power / (4 * np.pi *(distance**2))
    phase = np.fmod(2 * np.pi * freq * distance / speed_em + offset, 2 * np.pi)
    return [power_density, phase]


def position_error_estimate():
    pass


def data_visualize():
    pass


def beam_visualize():
    pass


def parsing_file(Filename):
    ant_df = pd.read_csv(Filename, encoding='shift-jis')
    Phi = ant_df['Phi[deg]']
    Theta = ant_df['Theta[deg]']
    dB = ant_df['dB(RealizedGainTotal)']
