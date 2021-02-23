from mpl_toolkits import mplot3d
from Drone import (Drone, Master, Slave)
import Globals as gb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from Target import Target

time_interval = 0.01
time_index = 0
time = -1  # period=1
Amp = 2.5  # strength of wind
freq = 3e9  # 2.9 GHz

d1 = Drone()
d2 = Drone()
d1.pos_assign(0.025, 0, 0)
d2.pos_assign(-0.025, 0, 0)
# 1000 targ_points, 10m target, ref_pos=[0,0,0]
t1 = Target(1000, 10, [0, 0, 0])
t1.field_generate([d1.antsPos, d2.antsPos], [1, 1])


def distance_calculate(a, b):
    distance = np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 +
                       (a[2] - b[2])**2)
    return distance


# input: source power, freq, distance
# return: received power density, phase
def emwave_propagate(power, distance):
    power_density = power / (4 * np.pi * distance**2)
    phase = np.fmod(2 * np.pi * freq * distance / 3e8, 2 * np.pi)
    return [power_density, phase]


class Drone():
    def __init__(self):
        self.len_mic = 5

        # Position: ideal, actual, estimated
        self.Pos_Ide = np.array([0, 0, 0])
        self.Pos_Act = np.array([[0, 0, 0]])
        self.Pos_Est = np.array([[0, 0, 0]])
        # number of microphones
        self.mic_num = 4
        # relevant position of microphones on drone
        self.micRele = []
        self.micRele.append(np.array([self.len_mic, 0, 0]))
        self.micRele.append(np.array([(-1) * self.len_mic, 0, 0]))
        self.micRele.append(np.array([0, self.len_mic, 0]))
        self.micRele.append(np.array([0, (-1) * self.len_mic, 0]))
        # list of 4(mic_num) of mics, time, position of mic
        # [np.array([[0, 0, 0]]), np.array([[0, 0, 0]]), np.array([[0, 0, 0]]), np.array([[0, 0, 0]])]
        self.micsPos = []
        for mic_j in range(self.mic_num):
            self.micsPos.append(self.Pos_Act[0] + self.micRele[mic_j])
        # number of antenna for beamforming
        self.ant_num = 1
        self.antsPos = [self.Pos_Act[0]]

    # to directly assign the position of the drone and mics
    def pos_assign(self, x, y, z):
        self.Pos_Ide = np.array([x, y, z])
        self.Pos_Act[0] = self.Pos_Ide
        # assign mics position
        for mic_j in range(self.mic_num):
            self.micsPos[mic_j] = self.Pos_Act[0] + self.micRele[mic_j]
        for ant_j in range(self.ant_num):
            self.antsPos[ant_j] = self.Pos_Act[0]

    # update Pos_Act and micsPos, mostly used by vibration()
    def pos_update(self, displacement):
        # current position = previous position + displacement
        # [-1] means the last element

        #displacement = self.Pos_Act + displacement
        # I am not sure if my modification is reasonable,
        # since I pretented that vibration()'s being updated by time
        # means displacement compared to ideal case.

        displacement = self.Pos_Ide + displacement
        self.Pos_Act = np.append(self.Pos_Act, [displacement], axis=0)
        # mics positions
        for mic_j in range(self.mic_num):
            self.micsPos[mic_j] = self.Pos_Act[time_index] + \
                self.micRele[mic_j]
        for ant_j in range(self.ant_num):
            self.antsPos[ant_j] = self.Pos_Act[time_index]

    # updated frame due to vibration
    def vibration(self, type_num):
        Amp
        # No.0: Ideal case. No vibration.
        if(type_num == 0):
            dis = np.array([0, 0, 0])
            self.pos_update(dis)
            # print("vibration zero")

        # No.1: Mechanical vibration. Sine + phi in z-axis.
        elif(type_num == 1):
            # phi: pi/3, why is "2*pi*2*time" ?
            disz = 0.2 * Amp * np.sin(np.pi / 3 + 2 * np.pi * 2 * time)
            dis = np.array([0, 0, disz])
            self.pos_update(dis)
            # print("vibration one")
        # No.2: Damping(Impulse) on x-axis
        elif(type_num == 2):
            # A*e^(-cwt)*cos(sqrt(1-c^2)*wt - phi)
            # c=0.1, sqrt(1-c^2)=0.99498743711, w=6, phi=0, A=2*Amp
            disx = 2 * Amp * \
                np.exp((-0.6) * time) * np.cos(0.99498743711 * 6 * time)
            dis = np.array([disx, 0, 0])
            self.pos_update(dis)
            # print("vibration two")
        # No.3: ellipse
        elif(type_num == 3):
            disx = Amp * np.sin(2 * np.pi * 2 * time)
            disy = Amp * np.sin(np.pi / 4 + 2 * np.pi * 2 * time)
            disz = Amp * np.sin(np.pi / 2 + 2 * np.pi * 2 * time)
            dis = np.array([disx, disy, disz])
            self.pos_update(dis)
            # print("vibration three")


class Targ_Point():
    # -----setting--------

    def __init__(self, x, y, z):
        self.aperture = 1
        self.pos = [x, y, z]
        self.received = -1
    # antenna pattern from gb
    # simulate isotropic temporarily

    def received_RF(self, ant_pos, power):
        sum = 0
        for ant_j in range(len(ant_pos)):
            distance = distance_calculate(self.pos, ant_pos[ant_j])

            # print('targ_pt:', self.pos)
            [power_density, phase] = emwave_propagate(power, distance)
            sum = sum + power_density * \
                self.aperture * np.e**(1j * phase)
        return sum

    # drone[droneA droneB droneC ...],2-dim array
    # droneA[ant1 ant2 ant3 ...]
    # power[pw_of_droneA pw_of_droneB pw_of_droneC ...],2-dim array
    # droneA[pw_of_ant1 pw_of_ant2 pw_of_ant3 ...]
    def synthesized_RF(self, drone, power):
        sum = 0
        for drone_j in range(len(drone)):
            sum = sum + self.received_RF(drone[drone_j], power[drone_j])
        self.received = sum
