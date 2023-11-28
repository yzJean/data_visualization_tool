import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import math

# painting a plot


class Painter:
    def __init__(self):
        self.fig = plt.figure()
        # marker ref: https://matplotlib.org/stable/api/markers_api.html
        # length = 8
        self.marker_list = ['x', 'o', '^', '8',
                            's', '*', 'D', 'P']

        # color ref: https://matplotlib.org/stable/gallery/color/named_colors.html
        # length = 16
        self.color_list = ['b', 'r', 'g', 'c', 'm', 'y',
                           # blue, green, red, cyan, magenta, yellow
                           'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
                           'tab:brown', 'tab:pink', 'darkcyan', 'tab:olive', 'tab:cyan']
        # length = 5
        self.verticalalignment = ['bottom', 'top',
                                  'center', 'center_baseline', 'baseline']

    def setup_ax_subplot(self, ax_subplot, subplot_info):
        ax_subplot.grid(True)
        ax_subplot.set_xlabel(subplot_info["xlabel"])
        ax_subplot.set_ylabel(subplot_info["ylabel"])
        ax_subplot.set_title(subplot_info["title"])

    # TODO: not work
    def set_ticks(self, ax_subplot, xdata=None, ydata=None):
        if (xdata and len(xdata) >= 2):
            xinterval = xdata[1] - xdata[0]
            ax_subplot.set_xticks(
                np.arange(min(xdata), max(xdata)+xinterval, xinterval))
        if (ydata and len(ydata) >= 2):
            yinterval = ydata[1] - ydata[0]
            ax_subplot.set_yticks(
                np.arange(min(ydata), max(ydata)+yinterval, yinterval))
    def set_aspect(self, ax_subplot):
        # ax_subplot.set_aspect('equal', adjustable='box')
        ax_subplot.axis('scaled')

    def get_color_with_index(self, index):
        return self.color_list[index % len(self.color_list)]

    def get_marker_with_index(self, index):
        return self.marker_list[index % len(self.marker_list)]

    def add_annotate(self, ax_subplot, display_str, pose, annot_face_color, pose_switch_index = 0):
        x = pose[0]
        y = pose[1]
        annot_offset = 0.0003 * pow(-1, pose_switch_index)
        ax_subplot.annotate(display_str, xy=(x, y), xytext=(x + annot_offset, y + annot_offset),
                            # textcoords='offset points', ha='center', va='bottom',
                            # ha='center', va='bottom',
                            # arrowprops=dict(
                            #     facecolor=annot_face_color, shrink=0.05),
                            arrowprops=dict(
                                color=annot_face_color, arrowstyle='<|-', connectionstyle='arc3,rad=0.1'),
                            bbox=dict(color=annot_face_color, alpha=0.5, boxstyle='round,pad=0.2'))

    def add_arrow(self, ax_subplot, v4, arrow_color, f=1):
        x0, y0, x1, y1 = v4
        f = max(f, .0001)
        scale = 1e-5
        dx = (x1-x0)*f
        dy = (y1-y0)*f
        ax_subplot.arrow(x0, y0, dx, dy,
                         fc=arrow_color,
                         ec='k',
                         head_width=scale, head_length=scale, width=scale,
                         length_includes_head=True, overhang=0)

    # theta: degree
    def add_heading(self, ax_subplot, v2_pose, arrow_color, arrow_len, theta=0):
        x, y = v2_pose
        # pose under visualization coord which is : East-North-Up
        dx = arrow_len*math.cos(math.radians(theta)) + x
        dy = arrow_len*math.sin(math.radians(theta)) + y
        v4 = [x, y, dx, dy]
        self.add_arrow(ax_subplot, v4, arrow_color)

    def add_text(self, ax_subplot, text_str, pose, color, display_bbox=False):
        if (display_bbox):
            ax_subplot.text(pose[0], pose[1], text_str,
                            horizontalalignment='center', verticalalignment='center_baseline',
                            bbox=dict(facecolor=color, alpha=0.5))
        else:
            ax_subplot.text(pose[0], pose[1], text_str)
            # horizontalalignment='center', verticalalignment='center_baseline')

    def display(self):
        plt.show()
