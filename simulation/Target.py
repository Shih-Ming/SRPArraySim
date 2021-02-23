from Targ_Point import Targ_Point
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import Globals as gb


class Target():
    # input a reference position, generate target points
    # N: number of target_point
    # R: radius
    def __init__(self, N, R, pos, axis):
        self.target_point = []
        self.N = N
        self.R = R
        self.pos = pos
        self.axis = axis
        # self.plot
        [x, y, z] = pos
        if (axis == 'xy'):
            for pt_j in range(self.N):
                self.target_point.append(Targ_Point(
                    x + self.R * np.cos(2 * np.pi / self.N * pt_j), y +
                    self.R * np.sin(2 * np.pi / self.N * pt_j), z))
        elif (axis == 'yz'):
            for pt_j in range(self.N):
                self.target_point.append(Targ_Point(
                    x, y + self.R * np.cos(2 * np.pi / self.N * pt_j), z +
                    self.R * np.sin(2 * np.pi / self.N * pt_j)))

        elif (axis == 'xz'):
            for pt_j in range(self.N):
                self.target_point.append(Targ_Point(
                    x + self.R * np.cos(2 * np.pi / self.N * pt_j), y, z +
                    self.R * np.sin(2 * np.pi / self.N * pt_j)))
        else:
            print("assigned axis parameter is invalid for Target.")

    def field_generating(self):
        # drone_ant stores antenna pos of each drone
        drone_ant = []
        power_ant = []
        offset_ant = []
        for drone_j in range(len(gb.drones)):
            power_ant.append(gb.drones[drone_j].antsPower)
            drone_ant.append(gb.drones[drone_j].antsPos[gb.time_index])
            if(drone_j == 0):  # master
                offset_ant.append(gb.drones[drone_j].antsPhase[0])
            else:  # slave
                offset_ant.append(gb.drones[drone_j].antsPhase[gb.time_index])
        for pt_j in range(self.N):
            self.target_point[pt_j].synthesized_RF(
                drone_ant, power_ant, offset_ant)
        # setting the axes projection as polar
        # gb.plot

    # ---------------plot ideal field-------------------

    def field_plotting(self, type, index, title, ylims):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        if(type == 'mag'):
            if (self.axis == 'xy'):
                data_x = []
                data_y = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y.append(10 * np.log(np.abs(
                        self.target_point[pt_j].received_transmit[index])))
                data_y_max = max(data_y)
                for pt_j in range(self.N):
                    data_y[pt_j] = data_y[pt_j] - data_y_max

                plt.title(title)
                line0, = plt.polar(data_x, data_y, 'g-')
                # ax.legend((line0), ('time_index=0'))
                ax.set_ylim(ylims)
                ax.set_rticks([-30, -20, -10, 0])
                # plt.show()
                plt.savefig('./figure/' + title + '.png')
                # return([data_x, data_y, "magnitude in xy-plane"])
            elif (self.axis == 'yz'):
                print("not yet written!")
            elif (self.axis == 'xz'):
                print("not yet written!")
            else:
                print("assigned axis parameter is invalid for field_generating().")
        elif(type == 'angle'):
            print("not yet written!")
        else:
            print("assigned type parameter is invalid for field_generating()")

    # ---------------plot vibrated field-----------------

    def field_plotting_overlay(self, type, index1, index2, index3, index4, title):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        if(type == 'mag'):
            if (self.axis == 'xy'):
                # index1
                data_x = []
                data_y = []
                ax.set_ylim(-30, 0)
                ax.set_rticks([-30, -20, -10, 0])
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y.append(10 * np.log(np.abs(
                        self.target_point[pt_j].received_transmit[index1])))
                data_y_max = max(data_y)
                for pt_j in range(self.N):
                    data_y[pt_j] = data_y[pt_j] - data_y_max
                line1, = plt.polar(data_x, data_y, 'g.')
                # index2
                data_x = []
                data_y = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y.append(10 * np.log(np.abs(
                        self.target_point[pt_j].received_transmit[index2])))
                data_y_max = max(data_y)
                for pt_j in range(self.N):
                    data_y[pt_j] = data_y[pt_j] - data_y_max
                line2, = plt.polar(data_x, data_y, 'y.')
                # index3
                data_x = []
                data_y = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y.append(10 * np.log(np.abs(
                        self.target_point[pt_j].received_transmit[index3])))
                data_y_max = max(data_y)
                for pt_j in range(self.N):
                    data_y[pt_j] = data_y[pt_j] - data_y_max
                line3, = plt.polar(data_x, data_y, 'r.')
                # index4
                data_x = []
                data_y = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y.append(10 * np.log(np.abs(
                        self.target_point[pt_j].received_transmit[index4])))
                data_y_max = max(data_y)
                for pt_j in range(self.N):
                    data_y[pt_j] = data_y[pt_j] - data_y_max
                line4, = plt.polar(data_x, data_y, 'b.')

                ax.legend((line1, line2, line3, line4), ('time_index1',
                                                         'time_index2', 'time_index3', 'time_index4'), loc='lower right')
                plt.title(title)
                # plt.show()
                plt.savefig('./figure/' + title + '.png')
                # return([data_x, data_y, "magnitude in xy-plane"])

    # ---plot summed field---
    def field_plotting_summed(self, type, title, compensation):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        ax.set_ylim(-30, 0)
        ax.set_rticks([-30, -20, -10, 0])
        if(type == 'mag'):
            if (self.axis == 'xy'):
                data_x = []
                data_y = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y.append(0)
                for index in range(1, gb.times+1):
                    for pt_j in range(self.N):
                        if(compensation == True):
                            data_y[pt_j] = data_y[pt_j] + \
                                abs(self.target_point[pt_j].received_transmit[index])
                        else:
                            data_y[pt_j] = data_y[pt_j] + \
                                abs(self.target_point[pt_j].received_origin[index])
                for pt_j in range(self.N):
                    data_y[pt_j] = 10 * np.log(data_y[pt_j] / 100.)
                data_y_max = max(data_y)
                for pt_j in range(self.N):
                    data_y[pt_j] = data_y[pt_j] - data_y_max

                plt.title(title)
                line0, = plt.polar(data_x, data_y, 'b-')
                # ax.legend((line0), ('time_index=0'))
                # plt.show()
                plt.savefig('./figure/' + title + '.png')
                # return([data_x, data_y, "magnitude in xy-plane"])
            elif (self.axis == 'yz'):
                print("not yet written!")
            elif (self.axis == 'xz'):
                print("not yet written!")
            else:
                print("assigned axis parameter is invalid for field_generating().")
        elif(type == 'angle'):
            print("not yet written!")
        else:
            print("assigned type parameter is invalid for field_generating()")
        # display the Polar plot
        # plt.show()

    # ---plot extreme field---
    def field_plotting_extreme(self, type, title, compensation):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        ax.set_ylim(-30, 0)
        ax.set_rticks([-30, -20, -10, 0])
        if(type == 'mag'):
            if (self.axis == 'xy'):
                data_x = []
                data_y_max = []
                data_y_min = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y_max.append(0)
                    data_y_min.append(0)

                for pt_j in range(self.N):
                    temp = []
                    for index in range(1, gb.times+1):
                        if(compensation == True):
                            temp.append(
                                abs(self.target_point[pt_j].received_transmit[index]))
                        else:
                            temp.append(
                                abs(self.target_point[pt_j].received_origin[index]))
                    min_ = min(temp)
                    max_ = max(temp)
                    data_y_min[pt_j] = 10 * np.log(min_)
                    data_y_max[pt_j] = 10 * np.log(max_)
                    if (min_ > max_):
                        print("strange")

                DATA_Y_MAX = max(data_y_max)
                for pt_j in range(self.N):
                    data_y_min[pt_j] = data_y_min[pt_j] - DATA_Y_MAX
                    data_y_max[pt_j] = data_y_max[pt_j] - DATA_Y_MAX
                    if (data_y_min[pt_j] > data_y_max[pt_j]):
                        print("strange")
                plt.title(title)
                if(compensation == True):
                    line0, = plt.polar(data_x, data_y_min, 'y-')
                    line1, = plt.polar(data_x, data_y_max, 'g-')
                else:
                    line0, = plt.polar(data_x, data_y_min, 'y--')
                    line1, = plt.polar(data_x, data_y_max, 'g--')
                ax.legend((line0, line1), ('min', 'max'), loc=1)
                # plt.show()
                plt.savefig('./figure/' + title + '.png')
                # return([data_x, data_y, "magnitude in xy-plane"])
            elif (self.axis == 'yz'):
                print("not yet written!")
            elif (self.axis == 'xz'):
                print("not yet written!")
            else:
                print("assigned axis parameter is invalid for field_generating().")
        elif(type == 'angle'):
            print("not yet written!")
        else:
            print("assigned type parameter is invalid for field_generating()")
        # display the Polar plot
        # plt.show()

    # ---plot rms error---
    def field_plotting_error(self, type, title, compensation):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        if(type == 'mag'):
            if (self.axis == 'xy'):
                data_x = []
                data_y = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y.append(0)

                for pt_j in range(self.N):
                    temp = []
                    for index in range(1, gb.times+1):
                        if(compensation == True):
                            temp.append(
                                (abs(self.target_point[pt_j].received_transmit[index]) - abs(self.target_point[pt_j].received_transmit[0]))**2)
                        else:
                            temp.append(
                                (abs(self.target_point[pt_j].received_origin[index]) - abs(self.target_point[pt_j].received_transmit[0]))**2)
                    temp = np.array(temp)
                    data_y[pt_j] = np.sqrt(temp.sum())

                plt.title(title)
                if(compensation == True):
                    line0, = plt.polar(data_x, data_y, 'b-')
                else:
                    line0, = plt.polar(data_x, data_y, 'b--')
                # plt.show()
                plt.savefig('./figure/' + title + '.png')
                # return([data_x, data_y, "magnitude in xy-plane"])
            elif (self.axis == 'yz'):
                print("not yet written!")
            elif (self.axis == 'xz'):
                print("not yet written!")
            else:
                print("assigned axis parameter is invalid for field_generating().")
        elif(type == 'angle'):
            print("not yet written!")
        else:
            print("assigned type parameter is invalid for field_generating()")
        # display the Polar plot
        # plt.show()

    # ---plot rms error---
    def field_plotting_error_overlay(self, type, title):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        if(type == 'mag'):
            if (self.axis == 'xy'):
                data_x = []
                data_y_t = []
                data_y_o = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y_t.append(0)
                    data_y_o.append(0)
                for pt_j in range(self.N):
                    temp_t = []
                    temp_o = []
                    for index in range(1, gb.times+1):
                        temp_t.append(
                            (abs(self.target_point[pt_j].received_transmit[index]) - abs(self.target_point[pt_j].received_transmit[0]))**2)
                        temp_o.append(
                            (abs(self.target_point[pt_j].received_origin[index]) - abs(self.target_point[pt_j].received_transmit[0]))**2)
                    temp_t = np.array(temp_t)
                    temp_o = np.array(temp_o)
                    data_y_t[pt_j] = np.sqrt(temp_t.sum())/gb.times
                    data_y_o[pt_j] = np.sqrt(temp_o.sum())/gb.times
                plt.title(title)
                line_t, = plt.polar(data_x, data_y_t, 'b-')
                line_o, = plt.polar(data_x, data_y_o, 'b--')
                # plt.show()
                ax.legend((line_t, line_o), ('with compensation',
                                             'without compensation'), loc=4)
                plt.savefig('./figure/' + title + '.png')
                # return([data_x, data_y, "magnitude in xy-plane"])
            elif (self.axis == 'yz'):
                print("not yet written!")
            elif (self.axis == 'xz'):
                print("not yet written!")
            else:
                print("assigned axis parameter is invalid for field_generating().")
        elif(type == 'angle'):
            print("not yet written!")
        else:
            print("assigned type parameter is invalid for field_generating()")
        # display the Polar plot
        # plt.show()
    def field_plotting_ideal_plus_rms(self, type, title, ylims, bool_compen, bool_noncompen):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')
        max_ideal = 0
        if(type == 'mag'):
            if (self.axis == 'xy'):
                data_x = []
                data_y_t_plus = []
                data_y_t_minus = []
                data_y_o_plus = []
                data_y_o_minus = []
                data_y_ideal = []
                for pt_j in range(self.N):
                    data_x.append(np.angle(self.target_point[pt_j].pos[0] + 1j *
                                           self.target_point[pt_j].pos[1]))
                    data_y_t_plus.append(0)
                    data_y_t_minus.append(0)
                    data_y_o_plus.append(0)
                    data_y_o_minus.append(0)
                    data_y_ideal.append(0)
                for pt_j in range(self.N):
                    temp_t = []
                    temp_o = []
                    if max_ideal < abs(self.target_point[pt_j].received_transmit[0]):
                        max_ideal = abs(self.target_point[pt_j].received_transmit[0])
                    for index in range(1, gb.times+1):
                        temp_t.append(
                            (abs(self.target_point[pt_j].received_transmit[index]) - abs(self.target_point[pt_j].received_transmit[0]))**2)
                        temp_o.append(
                            (abs(self.target_point[pt_j].received_origin[index]) - abs(self.target_point[pt_j].received_transmit[0]))**2)
                    temp_t = np.array(temp_t)
                    temp_o = np.array(temp_o)
                    rms_t = np.sqrt(temp_t.sum()/gb.times)
                    rms_o = np.sqrt(temp_o.sum()/gb.times)
                    data_y_t_plus[pt_j] =abs(self.target_point[pt_j].received_transmit[0])+rms_t
                    data_y_t_minus[pt_j] =abs(self.target_point[pt_j].received_transmit[0])-rms_t
                    data_y_o_plus[pt_j] = abs(self.target_point[pt_j].received_transmit[0])+rms_o
                    data_y_o_minus[pt_j] = abs(self.target_point[pt_j].received_transmit[0])-rms_o
                    data_y_ideal[pt_j] =  abs(self.target_point[pt_j].received_transmit[0])
                plt.title(title)
                line_group = []
                if bool_compen == 1:
                # line_t_plus represent the compensated field plus the rms error
                # line_t_minus represent the compensated field minus the rms error
                # line_t_plus represent the non-compensated field plus the rms error
                # line_t_minus represent the non-compensated field minus the rms error
                    line_t_plus, = plt.polar(data_x, 20*np.log10(data_y_t_plus/max_ideal), 'r-', label='Phase Compensation plus RMS')
                    line_t_minus, = plt.polar(data_x, 20*np.log10(data_y_t_minus/max_ideal), 'b-', label='Phase Compensation minus RMS')
                    line_group.append([line_t_plus,line_t_minus])
                if bool_noncompen == 1:
                    line_o_plus, = plt.polar(data_x, 20*np.log10(data_y_o_plus/max_ideal), 'r--', label='W/O Compensation plus RMS')
                    line_o_minus, = plt.polar(data_x, 20*np.log10(data_y_o_minus/max_ideal), 'b--', label='W/O Compensation minus RMS')
                    line_group.append([line_o_plus,line_o_minus])
                line_ideal, = plt.polar(data_x, 20*np.log10(data_y_ideal/max_ideal), 'g-', label='Ideal Field')
                line_group.append(line_ideal)
                # plt.show()
                ax.set_ylim(ylims)
#                ax.legend(bbox_to_anchor = (1,1.05))
                # return([data_x, data_y, "magnitude in xy-plane"])
            elif (self.axis == 'yz'):
                print("not yet written!")
            elif (self.axis == 'xz'):
                print("not yet written!")
            else:
                print("assigned axis parameter is invalid for field_generating().")
        elif(type == 'angle'):
            print("not yet written!")
        else:
            print("assigned type parameter is invalid for field_generating()")
        # display the Polar plot
        # plt.show()

    def field_show(self):
        plt.show()

    def plot_targ_points(self):

        # #plot 3D
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        xdata = []
        ydata = []
        zdata = []
        for pt_j in range(self.N):
            xdata.append(self.target_point[pt_j].pos[0])
            ydata.append(self.target_point[pt_j].pos[1])
            zdata.append(self.target_point[pt_j].pos[2])

        # ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
        ax.scatter3D(xdata, ydata, zdata)
        plt.show()
