import numpy as np
import Globals as gb
import random


class Microphone():
    def __init__(self):
        self.sound = [False]  # time, [whether receive sound]
        self.pos = None

    def receive_sound(self, boo):
        self.sound.append(boo)


class Drone():
    def __init__(self, pos):
        self.dipole = [0]  # received RF power
        # Position: ideal, actual, estimated
        self.Pos_Ide = np.array(pos)
        self.Pos_Act = [self.Pos_Ide]
        self.Pos_Est = [self.Pos_Ide]
        # microphone
        self.len_mic = 0.05
        # number of microphones
        self.mic_num = 4
        self.mics = []
        for mic_j in range(self.mic_num):
            self.mics.append(Microphone())
        # relevant position of microphones on drone
        self.micRele = []
        self.micRele.append(np.array([self.len_mic / 2, self.len_mic / 2, 0]))
        self.micRele.append(
            np.array([(-1) * self.len_mic / 2, self.len_mic / 2, 0]))
        self.micRele.append(
            np.array([(-1) * self.len_mic / 2, (-1) * self.len_mic / 2, 0]))
        self.micRele.append(
            np.array([self.len_mic / 2, (-1) * self.len_mic, 0]))
        # list of 4(mic_num) of mics, time, position of mic
        # [np.array([[0, 0, 0]]), np.array([[0, 0, 0]]), np.array([[0, 0, 0]]), np.array([[0, 0, 0]])]
        self.micsPos = []
        for mic_j in range(self.mic_num):
            self.micsPos.append(self.Pos_Act[0] + self.micRele[mic_j])
        # number of antenna for beamforming
        self.ant_num = 1
        self.antsPower = [1]
        self.antsPos = [[self.Pos_Act[0]]]
        self.antsPhase = [[0]]

    # to directly assign the position of the drone and mics
    def pos_assign(self, x, y, z):
        self.Pos_Ide = np.array([x, y, z])
        self.Pos_Act[0] = self.Pos_Ide
        # assign mics position
        for mic_j in range(self.mic_num):
            self.micsPos[mic_j] = self.Pos_Act[0] + self.micRele[mic_j]
            self.mics[mic_j].pos = self.micsPos[mic_j]
        for ant_j in range(self.ant_num):
            self.antsPos[0][ant_j] = self.Pos_Act[0]

    # update Pos_Act and micsPos, mostly used by vibration()
    def pos_update(self, displacement):
        # current position = previous position + displacement
        # [-1] means the last element
        displacement = self.Pos_Ide + displacement
        self.Pos_Act.append(displacement)
        # mics positions
        for mic_j in range(self.mic_num):
            self.micsPos[mic_j] = self.Pos_Act[gb.time_index] + \
                self.micRele[mic_j]
            self.mics[mic_j].pos = self.micsPos[mic_j]
        antspos = []
        for ant_j in range(self.ant_num):
            antspos.append(self.Pos_Act[gb.time_index])
        self.antsPos.append(antspos)

    # updated frame due to vibration
    def vibration(self, type_num):
        gb.Amp
        # No.0: Ideal case. No vibration.
        if(type_num == 0):
            dis = np.array([0, 0, 0])
            self.pos_update(dis)
            # print("vibration zero")

        # No.1: Mechanical vibration. Sine + phi in z-axis.
        elif(type_num == 1):
            # phi: pi/3, why is "2*pi*2*time" ?
            disy = gb.Amp * np.sin(2 * np.pi / gb.VibPeriod * gb.time)
            # disz = 0.2 * gb.Amp * np.sin(np.pi / 3 + 2 * np.pi * 2 * gb.time)
            # disz = gb.Amp * np.sin(2 * np.pi / gb.Period * gb.time)
            dis = np.array([0, disy, 0])
            self.pos_update(dis)
            # print("vibration one")
        # No.2: Damping(Impulse) on x-axis
        elif(type_num == 2):
            # A*e^(-cwt)*cos(sqrt(1-c^2)*wt - phi)
            # c=0.1, sqrt(1-c^2)=0.99498743711, w=6, phi=0, A=2*gb.Amp
            disx = 2 * gb.Amp * \
                np.exp((-0.6) * gb.time) * np.cos(0.99498743711 * 6 * gb.time)
            dis = np.array([disx, 0, 0])
            self.pos_update(dis)
            # print("vibration two")
        # No.3: ellipse
        elif(type_num == 3):
            disx = gb.Amp * np.sin(2 * np.pi * 2 * gb.time)
            disy = gb.Amp * np.sin(np.pi / 4 + 2 * np.pi * 2 * gb.time)
            disz = gb.Amp * np.sin(np.pi / 2 + 2 * np.pi * 2 * gb.time)
            dis = np.array([disx, disy, disz])
            self.pos_update(dis)
            # print("vibration three")
        # No.4: gaussian
        elif(type_num == 4):
            disx = np.random.normal(0, gb.Amp)
            disy = np.random.normal(0, gb.Amp)
            # disz = np.random.normal(0, gb.Amp)
            disz = 0
            dis = np.array([disx, disy, disz])
            self.pos_update(dis)


class Master(Drone):
    def __init__(self, pos):
        super().__init__(pos)
        self.phi = np.pi / 2


class Slave(Drone):
    def __init__(self, pos):
        super().__init__(pos)
        # let x axis point toward East, self.phi is the angle from beam direction to x axis
        self.phi = np.pi / 2
        self.trig = False
        self.mic_trig = [False, False, False, False]
        self.start = 0
        self.dis2m = [0, 0, 0, 0]  # distance to master of each mic
        self.d2m = 0
        # let x axis point toward East, theta is the angle from <master-slave> to x axis
        self.theta = np.pi
 # --------------------------------

    def find_set(self):
        # find the mic set that have the smallest and the second smallest dis2m
        micset = (0, 1)
        mini = (0, self.dis2m[0])
        secondmini = (1, self.dis2m[0])
        for i in range(4):
            if self.dis2m[i] < secondmini[1]:
                if self.dis2m[i] < mini[1]:
                    secondmini = mini
                    mini = (i, self.dis2m[i])
                else:
                    secondmini = (i, self.dis2m[i])
            else:
                pass
        if mini[0] < secondmini[0]:
            micset = (mini[0], secondmini[0])
        else:
            micset = (secondmini[0], mini[0])
        return micset

    def dis_calc(self):  # test only (should use utility_func)
        if not self.trig:
            if self.dipole[gb.time_index] is not 0:  # assume received wave as envelope
                self.trig = True
                self.start = gb.time_index
        elif self.trig:
            if self.dipole[gb.time_index] is 0:
                self.trig = False
        else:
            pass
        for mic_j in range(self.mic_num):
            if not self.mic_trig[mic_j]:
                if self.mics[mic_j].sound[gb.time_index]:
                    self.mic_trig[mic_j] = True
                    self.dis2m[mic_j] = (gb.time_index - self.start)\
                        * gb.time_interval * 343
            elif self.mic_trig[mic_j]:
                if not self.mics[mic_j].sound[gb.time_index]:
                    self.mic_trig[mic_j] = False
            else:
                pass

    def positioning(self):
        self.dis_calc()
        (m1, m2) = self.find_set()
        d2 = self.dis2m[m1]
        d1 = self.dis2m[m2]
        d = np.sqrt((d1**2 + d2**2) / 2 - (self.len_mic / 2)**2)
        self.d2m = d
        theta = np.arccos((d**2 + (self.len_mic / 2) **
                           2 - d2**2) / (self.len_mic * d))
        self.theta = theta + m1 * np.pi / 2

    def pos_est(self):  # Pos_Est seems uneeded actually
        # test (fake)
        # self.Pos_Est = self.Pos_Act
        vec = gb.drones[0].Pos_Act[gb.time_index] - self.Pos_Act[gb.time_index]
        self.d2m = np.sqrt(vec.dot(vec))
        self.theta = np.angle(vec[0] + 1j * vec[1])
        # print("pos_est", vec)
        # # real
        # self.positioning()
        # x = self.d2m*np.cos(self.theta)
        # y = self.d2m*np.sin(self.theta)
        # self.Pos_Est.append([x,y,0])

    def phase_compensation(self):
        dr = self.d2m * np.cos(np.pi - self.theta + self.phi)
        phase = (2 * np.pi * gb.freq / 3e8) * dr
        # self.antsPhase = 36 / 360 * 2 * np.pi
        # print("phase_compensation", self.antsPhase)
        return phase
# ------------------------------------------
    # def receive(self): # assume instantaneously
    #     self.phi = master.phi # master = ??
    #     self.dipole.append(master.dipole[gb.time_index]) # master = ??

    def transmit(self):
        phase = []
        for ant_j in range(self.ant_num):
            vec = gb.drones[0].Pos_Act[gb.time_index] - \
                self.antsPos[gb.time_index][ant_j]
            d2m = np.sqrt(vec.dot(vec))
            theta = np.angle(vec[0] + 1j * vec[1])
            dr = d2m * np.cos(np.pi - theta + self.phi)
            phase.append((2 * np.pi * gb.freq / 3e8) * dr)
        self.antsPhase.append(phase)
        # self.antsPhase.append(0)
        # self.antsPhase.append(-38 / 360 * 2 * np.pi)
        # self.pos_est()
        # self.antsPhase.append(self.phase_compensation())
        # self.antsPhase = 0


def drone_generating(num, type):
    gb.drones.append(Master([0, 0, 0]))
    for num_j in range(num - 1):
        gb.drones.append(Slave([0, 0, 0]))

    if(type == 'linear'):
        xmin = -0.5*(gb.speed_em/gb.freq)*gb.spacing_lambda
        for num_j in range(num):
            gb.drones[num_j].pos_assign(xmin+ num_j * ((gb.speed_em/gb.freq)*gb.spacing_lambda), 0, 0)
    elif(type == 'manual'):
        gb.drones[0].pos_assign(-0.025 / np.sqrt(2), 0.025 / np.sqrt(2), 0)
        gb.drones[1].pos_assign(0.025 / np.sqrt(2), -0.025 / np.sqrt(2), 0)
    else:
        print("assigned parameter type is invalid for drone_generating().")
