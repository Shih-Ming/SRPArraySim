import numpy as np
import Globals as gb


class Targ_Point():
    # -----setting--------

    def __init__(self, x, y, z):
        self.aperture = 1
        self.pos = np.array([x, y, z])
        self.received_transmit = []
        self.received_origin = []
        # ---initiate received at time_index=0----
        drone_ant = []
        power_ant = []
        offset_ant = []
        for drone_j in range(len(gb.drones)):
            power_ant.append(gb.drones[drone_j].antsPower)
            drone_ant.append(gb.drones[drone_j].antsPos[0])
            offset_ant.append(gb.drones[drone_j].antsPhase[0])
        self.synthesized_RF(drone_ant, power_ant, offset_ant)

    # antenna pattern from gb
    # simulate isotropic temporarily

    def received_RF(self, ant_pos, power, offset):
        sum_t = 0  # transmit(), with compensation
        sum_o = 0  # without compensation
        for ant_j in range(len(ant_pos)):
            distance = gb.distance_calculate(self.pos, ant_pos[ant_j])

            # print('targ_pt:', self.pos)
            [power_density, phase] = gb.emwave_propagate(
                power, distance, offset)
            sum_t = sum_t + np.sqrt(power_density) * \
                self.aperture * np.e**(1j * phase)
            [power_density, phase] = gb.emwave_propagate(
                power, distance, 0)
            sum_o = sum_o + np.sqrt(power_density) * \
                self.aperture * np.e**(1j * phase)
        return sum_t, sum_o

    # drone[droneA droneB droneC ...],2-dim array
    # droneA[ant1 ant2 ant3 ...]
    # power[pw_of_droneA pw_of_droneB pw_of_droneC ...],2-dim array
    # droneA[pw_of_ant1 pw_of_ant2 pw_of_ant3 ...]
    def synthesized_RF(self, drone, power, offset):
        sum_t = 0
        sum_o = 0
        for drone_j in range(len(drone)):
            sum_t_drone, sum_o_drone = self.received_RF(
                drone[drone_j], power[drone_j], offset[drone_j])
            sum_t = sum_t + sum_t_drone
            sum_o = sum_o + sum_o_drone
        self.received_transmit.append(sum_t)
        self.received_origin.append(sum_o)


# class Target():
#     # input a reference position, generate target points
#     # N: number of target_point
#     # R: radius
#     def __init__(self, N, R, pos):
#         self.target_point = []
#         self.N = N
#         self.R = R
#         self.pos = pos
#         [x, y, z] = pos
#         for pt_j in range(self.N):
#             self.target_point.append(Targ_Point(
#                 x + self.R * np.cos(2 * np.pi / self.N * pt_j), y +
#                 self.R * np.sin(2 * np.pi / self.N * pt_j), z))
#
#     def field_generate(self, drone, power):
#         for pt_j in range(self.N):
#             self.target_point[pt_j].synthesized_RF(drone, power)
#         # setting the axes projection as polar
#         plt.axes(projection='polar')
#
#         # plotting the circle
#         for pt_j in range(self.N):
#             plt.polar(np.angle(self.target_point[pt_j].pos[0] + 1j *
#                                self.target_point[pt_j].pos[1], deg=True), (np.abs(
#                                    self.target_point[pt_j].received)), 'g.')
#             # print(
#             #     np.angle(self.target_point[pt_j].pos[0] + 1j * self.target_point[pt_j].pos[1]) / 2 / np.pi * 360)
#
#         # display the Polar plot
#         plt.show()
