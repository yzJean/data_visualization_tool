#!/usr/bin/python3

import tkinter
from tokenize import Double
import matplotlib.pyplot as plt
import optparse      # file parser
import numpy as np
import os
import matplotlib
matplotlib.use('TkAgg')
import math
from scipy.spatial.transform import Rotation as R

import tool_reader as tl_reader
import tool_painter as tl_painter

help_msg = """
Version: At least Python3
Dependencies: matplotlib, numpy, os, optparse
Purpose: This tool aims at visualizing raw sdmap and sdmap handler query results.
Expected results: A figure containing the above information.

Command:
python3 main_vis_sdmap_query.py -i <dir-to-sdmap_*.csv> -u <dir-to-*VehRoadData.csv>

For example,
python3 main_vis_sdmap_query.py -i ../test/test_map_data/20230605_TPE2_autopipe/sdmap/sdmap_20230605_TPE2_pt1_pt5_all.csv -u ../test/test_map_data/20230605_TPE2_autopipe/20230605_TPE2_autopipe_VehRoadData.csv
"""

# ========================
# parsing options setup
# ========================
def numb_to_bool(option_numb):
    if int(option_numb) == 1:
        return True
    else:
        return False

def options():
    p = optparse.OptionParser(usage=help_msg)
    p.add_option('--in_sdmap_dir', '-i', default='./sdmap_20230605_TPE2_pt1_pt5_all.csv',
                 help='This is a mandatory option. It is recommended to use with the NRU110V/<route-data>/sdmap_*.csv')
    p.add_option('--in_vehroaddata_dir', '-u', default='',
                 help='This is an optional option. It is recommended to use with the NRU110V/<route-data>/*VehRoadData.csv')
    p.add_option('--is_show_start_timestamp', '--show-start-timestamp', default = -1.0, help='This is a optional option. Default: 0. Show Start Timestamp: 1. The rest of value could be treated as False.')
    p.add_option('--is_show_lane_count', '--show-lane-count', default = -1.0, help='This is a optional option. Default: 0. Show Start Lane Count: 1. The rest of value could be treated as False.')
    p.add_option('--start_timestamp', '-s', default= -1,
                 help='This is an optional option. Input digit number should be consistent with actual time period.')
    p.add_option('--end_timestamp', '-e', default= -1,
                 help='This is an optional option. Input digit number should be consistent with actual time period.')
    p.add_option('--sampling_rate', '--smapling-rate', default= 10,
                 help='This is an optional option. 10 is default')
    p.add_option('--is_show_frd_coord', '--show-frd-coord', default= 0,
                 help='This is an optional option. 0 is default')
    options, arguments = p.parse_args()

    in_sdmap_dir = options.in_sdmap_dir
    in_vehroaddata_dir = options.in_vehroaddata_dir
    is_show_start_timestamp = options.is_show_start_timestamp
    is_show_lane_count = options.is_show_lane_count
    start_timestamp = float(options.start_timestamp)
    end_timestamp = float(options.end_timestamp)
    sampling_rate = int(options.sampling_rate)
    is_show_frd_coord = options.is_show_frd_coord
    display_modes_list = [numb_to_bool(is_show_start_timestamp), numb_to_bool(is_show_lane_count), numb_to_bool(is_show_frd_coord)]
    if (start_timestamp > end_timestamp):
        start_timestamp, end_timestamp = swap(start_timestamp, end_timestamp)
    time_period = [start_timestamp, end_timestamp]
    # check input arguments
    if (not in_sdmap_dir):
        p.error("Directory to sdmap_*.csv is empty, return")
        return None, None, None, None

    return in_sdmap_dir, in_vehroaddata_dir, display_modes_list, time_period, sampling_rate

# ========================
# reader
# ========================
def read_from_directories(dirs, header_list):
    multiple_reading_results =[]
    for idx, item_dir in enumerate(dirs):
        if (item_dir == ""):
            continue
        print("\nReading a file under: ", item_dir)
        reading = read_from_file(item_dir, header_list[idx])
        multiple_reading_results.append(reading)
    return multiple_reading_results

def read_from_file(dir, header_list):
    reader = tl_reader.Reader(dir, header_list)
    return reader.read_file()

# ========================
# utils
# ========================
def swap(a, b):
    tmp = b
    b = a
    a = tmp
    return a, b

def is_in_range(range, value):
    start = range[0]
    end = range[1]
    if (start > end):
        start, end = swap(range[0], range[1])
    return (start <= value and value <= end)

# ========================
# painter
# ========================
def parse_reading_dict_to_list(reading, header_dict):
    ret_list = []
    for header in header_dict.keys():
        if reading.get(header) is not None:
            ret_list.append(reading[header])
    return ret_list

# =========================
# Transform
# =========================


def draw(filename, header_list, readings, display_modes_list, time_period, sampling_rate = 20):
    # ----- Read from sdmap -----
    sdmap_reading = readings[0]
    sdmap_header_dict = header_list[0]
    sd_info_list = parse_reading_dict_to_list(sdmap_reading, sdmap_header_dict)
    sd_road_id_list = sd_info_list[0]         # road_id
    sd_lane_count_list = sd_info_list[1]      # lane_count
    sd_longitude_start_list = sd_info_list[2] # longitude_start
    sd_latitude_start_list = sd_info_list[3]  # latitude_start
    sd_longitude_end_list = sd_info_list[4]   # longitude_end
    sd_latitude_end_list = sd_info_list[5]    # latitude_end

    # ----- Read from vehicle road data -----
    is_veh_road_data_imported = len(readings) >= 2
    # TODO: be more flexible
    if (is_veh_road_data_imported):
        vehroaddata_reading = readings[1]
        vehroaddata_header_dict = header_list[1]
        vehroaddata_info_list = parse_reading_dict_to_list(vehroaddata_reading, vehroaddata_header_dict)
        # queried_passed
        veh_queried_passed = vehroaddata_info_list[0]
        # ustt
        veh_ustt_list = vehroaddata_info_list[1]
        # veh_longitude
        veh_longitude_list = vehroaddata_info_list[2]
        # veh_latitude
        veh_latitude_list = vehroaddata_info_list[3]
        # distance
        veh_distance_list = vehroaddata_info_list[4]
        # matched road_index
        veh_lane_count_list = vehroaddata_info_list[5] # TODO: road_id
        # matched road_index
        veh_road_index_list = vehroaddata_info_list[6]
        # road_start_longitude
        veh_road_start_lon_list = vehroaddata_info_list[7]
        # road_start_latitude
        veh_road_start_lat_list = vehroaddata_info_list[8]
        # road_end_longitude
        veh_road_end_lon_list = vehroaddata_info_list[9]
        # road_end_latitude
        veh_road_end_lat_list = vehroaddata_info_list[10]
        # TODO
        is_advanced_dataset = len(vehroaddata_info_list) > 12
        if (is_veh_road_data_imported and is_advanced_dataset):
            # veh_heading_deg
            veh_heading_deg_list = vehroaddata_info_list[11]
            # closest_ptx
            veh_closest_pt_lat_list = vehroaddata_info_list[12] #latitude
            # closest_pty
            veh_closest_pt_lon_list = vehroaddata_info_list[13] #longitude
            # closest_ptz
            veh_closest_ptz_list = vehroaddata_info_list[14]
            # veh2road_normalized
            # in terms of vehicle; positive: the road is on the right-hand sided of vehicle; otherwise, negative
            veh_veh2road_normalized_list = vehroaddata_info_list[15]
        else:
            print("len(vehroaddata_info_list):", len(vehroaddata_info_list))

        # ----- Timestamp -----
        default_timestamp = float(-1.0)
        start_timestamp = time_period[0]
        end_timestamp = time_period[1]
        size_last_elem = len(veh_ustt_list) - 1
        if ((start_timestamp != default_timestamp) and (end_timestamp == default_timestamp)):
            time_period[1] = veh_ustt_list[size_last_elem] # end_timestamp
        elif ((start_timestamp == default_timestamp) and (end_timestamp == default_timestamp)):
            time_period[0] = float(veh_ustt_list[0]) # start_timestamp
            time_period[1] = float(veh_ustt_list[size_last_elem]) # end_timestamp
        print("Whole journey time period [start, end]:", [veh_ustt_list[0], veh_ustt_list[size_last_elem]])
        print(" Map data size:", len(sd_road_id_list), ", veh_road_data size:", len(veh_longitude_list))

        # Iterate pose by pose, extract certain period of time, TODO
        tmp_veh_queried_passed = []
        tmp_veh_ustt_list = []
        tmp_veh_distance_list = []
        # TODO
        if (is_veh_road_data_imported and is_advanced_dataset):
            tmp_veh_heading_deg_list = []
            for idx, time in enumerate(veh_ustt_list):
                # Only draw a few poses located in the time period
                current_timestamp = veh_ustt_list[idx]
                if(is_in_range(time_period, current_timestamp)):
                    tmp_veh_ustt_list.append(veh_ustt_list[idx])
                    tmp_veh_distance_list.append(veh_distance_list[idx])
                    tmp_veh_queried_passed.append(veh_queried_passed[idx])
                    # TODO
                    if (is_veh_road_data_imported and is_advanced_dataset):
                        tmp_veh_heading_deg_list.append(veh_heading_deg_list[idx])
            print("Drawing information within the time period [start, end]:", time_period)
            print(" Map data size:", len(sd_road_id_list), ", veh_road_data size:", len(tmp_veh_queried_passed))


    # ----- Display mode -----
    is_display_start_timestamp = display_modes_list[0]
    is_display_lc = display_modes_list[1]
    is_display_frd_coord = display_modes_list[2]
    # ----- Painting -----
    # For sdmap
    painter = tl_painter.Painter()
    ax_subplot_sdmap = painter.fig.add_subplot(111)

    # For distance
    painter_dist = tl_painter.Painter()
    ax_subplot_dist = painter_dist.fig.add_subplot(211)
    # For heading
    # TODO
    if (is_veh_road_data_imported and is_advanced_dataset):
        ax_subplot_heading = painter_dist.fig.add_subplot(212)

        # Draw Distance info, TODO
        ax_subplot_dist.plot(tmp_veh_ustt_list, tmp_veh_distance_list)

    # Draw Heading info, TODO
    # TODO
    if (is_veh_road_data_imported and is_advanced_dataset):
        ax_subplot_heading.plot(tmp_veh_ustt_list, tmp_veh_heading_deg_list)

    # Draw SD map info
    ax_subplot_sdmap.plot([sd_longitude_start_list, sd_longitude_end_list], [
                          sd_latitude_start_list, sd_latitude_end_list], color='k')

    for idex, item in enumerate(sd_longitude_start_list):
        matched_road_v4 = [sd_longitude_start_list[idex], sd_latitude_start_list[idex],
                sd_longitude_end_list[idex], sd_latitude_end_list[idex]]
        painter.add_arrow(ax_subplot_sdmap, matched_road_v4, 'k')

        # Draw whole sdmap lane count information when veh_road_data is imported
        if (not is_veh_road_data_imported):
            lc_color = painter.get_color_with_index(idex)
            display_str_road_index = str(sd_road_id_list[idex]) # to align with sdmap.csv
            display_str_roadid = "rid" + display_str_road_index
            #TODO: lane count type
            if (is_display_lc):
                display_str_lc = (display_str_roadid + \
                    "_lc: 0") if (
                        type(sd_lane_count_list[idex]) == "str") else display_str_roadid + "_lc: "+ str(sd_lane_count_list[idex])
                painter.add_annotate(ax_subplot_sdmap, display_str_lc, [
                                    sd_longitude_start_list[idex], sd_latitude_start_list[idex]], lc_color, idex)

    # Draw veh_road_data, TODO: be more flexible
    if (is_veh_road_data_imported):
        # Draw starter
        is_draw_starter = True

        is_draw_in_time_period = True

        # Road segment color
        prev_road_id = 0
        prev_color = 'gray'

        # Iterate pose by pose
        for idx, is_pass in enumerate(veh_queried_passed):
            # # Only draw a few poses located in the time period
            current_timestamp = veh_ustt_list[idx]
            is_draw_in_time_period = is_in_range(time_period, current_timestamp);

            # Only draw a few poses in order to prevent heavy visualization caused by too many poses
            is_draw = idx % sampling_rate == 0
            if (is_draw and is_draw_in_time_period):
                # Draw starter
                if (is_draw_starter):
                    is_draw_starter = False
                    starter_x = veh_longitude_list[idx]
                    starter_y = veh_latitude_list[idx]
                    ax_subplot_sdmap.scatter(
                    veh_longitude_list[idx], veh_latitude_list[idx],
                    marker='^', color='y', s=100)
                    display_str = "Starter(" +str(round(starter_x, 3)) + ", " + str(round(starter_y, 3)) + ")"
                    painter.add_annotate(ax_subplot_sdmap, display_str, [starter_x, starter_y], 'y')

                # Get queried road index from current veh_pose
                road_id = veh_road_index_list[idx]
                is_road_id_changed = prev_road_id != road_id
                queried_road_index = idx
                # Default pose appearance
                pose_status = '^'
                pose_color = 'k'
                road_seg_color = 'grey'
                # Decide the pose appearance which queried a road segment
                if (is_pass == 'pass'):
                    pose_status = 'o'
                    if (is_road_id_changed):
                        pose_color = painter.get_color_with_index(queried_road_index)
                        road_seg_color = pose_color
                        prev_road_id = road_id
                        prev_color = pose_color
                    else:
                        pose_color = prev_color
                        road_seg_color = prev_color
                    # Draw linker between the veh_pose and queried road segment
                    ax_subplot_sdmap.plot([veh_longitude_list[idx], veh_road_start_lon_list[queried_road_index]],
                                          [veh_latitude_list[idx], veh_road_start_lat_list[queried_road_index]],
                                          color=pose_color, linestyle='--')

                    # Draw matched road segment
                    ax_subplot_sdmap.plot([veh_road_start_lon_list[queried_road_index], veh_road_end_lon_list[queried_road_index]],
                                          [veh_road_start_lat_list[queried_road_index], veh_road_end_lat_list[queried_road_index]],
                                          color=road_seg_color, linewidth=4)

                    # Draw sdmap lane count information
                    display_str_road_id = str(
                        veh_road_index_list[queried_road_index])  # to align with sdmap.csv
                    display_str_roadid = "rid" + display_str_road_id
                    # TODO: lane count type
                    if (is_display_lc):
                        display_str_lc = (display_str_roadid +
                                        "_lc: 0") if (
                            type(veh_lane_count_list[idex]) == "str") else display_str_roadid + "_lc: " + str(veh_lane_count_list[queried_road_index])
                        painter.add_annotate(ax_subplot_sdmap, display_str_lc, [
                            veh_road_start_lon_list[queried_road_index], veh_road_start_lat_list[queried_road_index]], pose_color, queried_road_index)

                    # TODO: refactor, standalone drawing from other items
                    # Draw closest point
                    if (is_veh_road_data_imported and is_advanced_dataset):
                        ## in terms of road's perspective
                        distance_color = 'g' if veh_distance_list[queried_road_index] > 0 else 'r'
                        ax_subplot_sdmap.plot([veh_longitude_list[queried_road_index], veh_closest_pt_lon_list[queried_road_index]],
                                              [veh_latitude_list[queried_road_index], veh_closest_pt_lat_list[queried_road_index]],
                                              color=distance_color, linewidth=2)

                    # Draw pose
                    if (is_display_frd_coord):
                        pose_v2 = [veh_longitude_list[queried_road_index], veh_latitude_list[queried_road_index]]
                        heanding_len = 0.0005
                        heading = 90 - veh_heading_deg_list[idx]
                        # front
                        painter.add_heading(ax_subplot_sdmap, pose_v2, 'salmon', heanding_len, heading)
                        # right
                        right_axis = heading - 90
                        painter.add_heading(ax_subplot_sdmap, pose_v2, 'moccasin', heanding_len, right_axis)

                # Decide the pose appearance which is unmatched road segment
                else:
                    pose_status = 'x'
                    pose_color = 'r'
                    road_seg_color = 'grey'

                # Draw poses
                ax_subplot_sdmap.scatter(
                    veh_longitude_list[idx], veh_latitude_list[idx],
                    marker=pose_status, color=pose_color, s=40)
                # TODO
                # display_msg = str(idx) + ": t" + str(veh_ustt_list[idx]) if is_display_start_timestamp else str(idx)
                display_msg = str("") + "t" + str(veh_ustt_list[idx]) if is_display_start_timestamp else str("")
                painter.add_text(ax_subplot_sdmap, display_msg, [veh_longitude_list[idx], veh_latitude_list[idx]], pose_color)

    # Setup SDMap
    ax_subplot_info = {'xlabel': "Logitude",
                       'ylabel': "Latitude",
                       'title': "Route-SDMap Query Information: " + str(filename)}
    painter.setup_ax_subplot(ax_subplot_sdmap, ax_subplot_info)
    painter.set_aspect(ax_subplot_sdmap)

    # Setup distance
    ax_subplot_dist_info = {'xlabel': "Time (ustt)",
                       'ylabel': "Distance (meters)",
                       'title': "Route-SDMap Distance: " + str(filename)}
    painter_dist.setup_ax_subplot(ax_subplot_dist, ax_subplot_dist_info)

    # Setup heading
    # TODO
    if (is_veh_road_data_imported and is_advanced_dataset):
        ax_subplot_heading_info = {'xlabel': "Time (ustt)",
                        'ylabel': "Heading (Degree)",
                        'title': "Route-SDMap Heading: " + str(filename)}
        painter_dist.setup_ax_subplot(ax_subplot_heading, ax_subplot_heading_info)

    # TODO: display once
    painter.display()

# ========================
# Main
# ========================
def main():
    in_sdmap_dir, in_vehroaddata_dir, display_modes_list, time_period, sampling_rate = options()
    sdmap_filename = os.path.basename(in_sdmap_dir)
    vehroaddata_filename = os.path.basename(in_vehroaddata_dir)
    display_filename = vehroaddata_filename if vehroaddata_filename != "" else sdmap_filename

    sdmap_header_dict = {'road_id': int,
                         'lane_count': str,
                         'longitude_start': float,
                         'start_lon': float,
                         'latitude_start': float,
                         'start_lat': float,
                         'longitude_end': float,
                         'end_lon': float,
                         'latitude_end': float,
                         'end_lat': float}

    vehroaddata_header_dict = {'queried_passed': str, #0
                               'ustt': float,#1
                               'veh_longitude': float, #2
                               'veh_latitude': float, #3
                               'distance': float, #4
                               'road_id': int, # TODO #5
                               'lane_count': int, #6
                               'road_start_longitude': float, #7
                               'road_start_latitude': float, #8
                               'road_end_longitude': float, #9
                               'road_end_latitude': float, #10
                               'heading_deg': float, #11
                               'closest_ptx': float, #12
                               'closest_pt_lat': float, #12
                               'closest_pty': float, #13
                               'closest_pt_lon': float, #13
                               'closest_ptz': float, #14
                               'closest_pt_height': float, #14
                               'veh2road_normalized': float, #15, lateral offset
                               }

    reading_directories = [in_sdmap_dir, in_vehroaddata_dir]
    header_list = [sdmap_header_dict, vehroaddata_header_dict]

    readings = read_from_directories(reading_directories, header_list)

    draw(display_filename, header_list, readings, display_modes_list, time_period, sampling_rate)
if __name__ == "__main__":
    main()