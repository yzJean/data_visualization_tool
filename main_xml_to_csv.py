#!/usr/bin/python3

# import tkinter
# from tokenize import Double
# import matplotlib.pyplot as plt
import optparse      # file parser
# import numpy as np
import os
# import matplotlib
# matplotlib.use('TkAgg')
import csv
from xml.etree import ElementTree
# import tool_writer as tl_writer
import collections

help_msg = """
Version: At least Python3
Dependencies: matplotlib, numpy, os, optparse
Purpose:
Expected results:

Command:

For example,

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
    p.add_option('--in_xml_dir', '-i', default='./map.osm',
                 help='This is a mandatory option.')
    options, arguments = p.parse_args()

    in_xml_dir = options.in_xml_dir

    display_modes_list = []

    # check input arguments
    if (not in_xml_dir):
        p.error("Directory to map_*.csv is empty, return")
        return None, None, None, None

    return in_xml_dir, display_modes_list

# ========================
# TODO: Parser and writer
# ========================
def parse_and_write(xml_file_dir, map_name):
    # PARSE XML
    xml = ElementTree.parse(xml_file_dir)
    
    # create writer
    csvfile = open(map_name,'w',encoding='utf-8')
    csvfile_writer = csv.writer(csvfile)

    # ADD THE HEADER TO CSV FILE
    header_list =["lane_count","road_id","longitude_start","latitude_start","longitude_end","latitude_end"]
    csvfile_writer.writerow(header_list)

    # node_dict = collections.defaultdict(list)
    node_dict = {} # id: [lat, lon] (deg, deg)
    # for node in xml.findall("node"):
    for el in xml.iter():
        if (el.tag == "node"):
            node = el
            # if (node):
            # iterate node with attributes
            for elem in node.iter():
                # print("elem.attrib")
                # print(elem.attrib)
                if (elem.tag == "node"):
                    node_id = elem.attrib["id"]
                    node_coord = [elem.attrib["lon"], elem.attrib["lat"]]
                    node_dict.update({str(node_id): node_coord})
    # print("len(node_dict): ", len(node_dict))
    
    for way in xml.findall("way"):
        # each one: [lon_node, lat_node]
        way_nodes_lc = []
        if (way):
            lane_count = 1
            road_id = 0
            for elem in way.iter():
                if (elem.tag == "way"):
                    road_id = elem.attrib["id"]
                    # print("=== road_id: ", road_id)
                # collect nodes
                elif (elem.tag == "nd"):
                    node_ref = elem.attrib["ref"]
                    # print("node_ref: ", node_ref)
                    node_info = node_dict.get(node_ref, None)
                    # print("(lon, lat): ", node_info)
                    if node_info is not None:
                        way_nodes_lc.append(node_info)
                elif (elem.tag == "tag"):
                    if (elem.attrib["k"] == "lanes"):
                        lane_count = elem.attrib["v"]

            # header_list =["lane_count","road_id","longitude_start","latitude_start","longitude_end","latitude_end"]
            for way_node_index in range(len(way_nodes_lc) - 1):
                start_node_info = way_nodes_lc[way_node_index]
                end_node_info = way_nodes_lc[way_node_index + 1]
                route = [lane_count, road_id] + start_node_info + end_node_info
                csvfile_writer.writerow(route)
                
    csvfile.close()

# ========================
# Main
# ========================
def main():
    in_xml_dir, display_modes_list = options()
    out_ext = ".csv"
    map_filename = os.path.splitext(in_xml_dir)[0] + "_area_map" + out_ext
    out_path = "./"
    out_file_name = os.path.join(out_path,map_filename)
    print("Writing file to ", out_file_name)
    parse_and_write(in_xml_dir, out_file_name)

if __name__ == "__main__":
    main()