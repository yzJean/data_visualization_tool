#!/usr/bin/python3
import optparse      # file parser
import numpy as np
import os

import tool_reader as tl_reader
import tool_writer as tl_writer

help_msg = """
Version: At least Python3
Dependencies: numpy, os, optparse
Backgroud: To visualize GPS data, the input data format should be formatted in a certain way.
           The format follows the convention https://www.gpsvisualizer.com/map_input?form=data
Purpose: This tool aims at pre-processing gnss raw data including format conversion.
         To be more specific, convert GW data format to GPS visualizer data format
Expected results: A processed file named after the input file and sharing the same format as the
                 input is outputed to the input directory.

Command:
python3 main_gnss_file_processor.py -i <dir-to-*GNSS.csv>

For example,
python3 main_gnss_data_preprocessor.py -i ./GNSS.csv

Output file: ./GNSS_processed.csv
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

    # ====================================
    # file input of relocalization results
    # ====================================
    p.add_option('--in_gnss_file_dir', '-i', default='./GNSS.csv',
                 help='This is a mandatory option. It is recommended to use with the GNSS.csv')
    p.add_option('--start_timestamp', '-s', default='-1',
                 help='This is a optoinal option. It is recommended to select a start timestamp from the GNSS.csv')
    p.add_option('--end_timestamp', '-e', default='-1',
                 help='This is a optoinal option. It is recommended to select a end timestamp the GNSS.csv')
    options, arguments = p.parse_args()

    in_gnss_file_dir = options.in_gnss_file_dir
    start_timestamp = int(options.start_timestamp)
    end_timestamp = int(options.end_timestamp)

    # check input argument
    if (not in_gnss_file_dir):
        p.error("Directory to *GNSS.csv is empty, return")
        return None, None, None

    if (start_timestamp > end_timestamp):
        tmp = end_timestamp
        end_timestamp = start_timestamp
        start_timestamp = tmp
    print("start_timestamp: ", start_timestamp)
    print("end_timestamp: ", end_timestamp)
    return in_gnss_file_dir, start_timestamp, end_timestamp

def read_from_file(dir, header_list):
    reader = tl_reader.Reader(dir, header_list)
    return reader.read_file()

def write_into_file(dir, reading):
    writer = tl_writer.Writer(dir, reading)
    writer.write_reading_into_file()

def process_out_dir(in_dir_to_file, start_timestamp, end_timstamp):
    in_file_name = os.path.splitext(os.path.basename(in_dir_to_file))[0]
    in_ext_name = os.path.splitext(os.path.basename(in_dir_to_file))[1]
    parent_dir = os.path.dirname(in_dir_to_file)
    out_file_range = '_s' + str(start_timestamp) + '_e' + str(end_timstamp)
    if (start_timestamp == -1 or end_timstamp == -1):
        out_file_range = '_all'
    out_filename = in_file_name + '_processed' + out_file_range + in_ext_name
    out_dir = os.path.join(parent_dir, out_filename)
    print(out_dir)
    return out_dir

# TODO: customized, parsing gnss data
def process_readings(reading_dict, start_time, end_time):
    processed_reading_dict = {}
    new_key = ""
    # convert expression format [lon, lat] from long to double
    for key, item in reading_dict.items():
        item_arr = np.array(item)
        if (key == "lon" or key == "lat"):
            new_key, processed_item_arr = process_llh_information(key, item_arr)
        elif(key == "ustt"):
            processed_item_arr = item_arr
            new_key = key
        processed_reading_dict[new_key] = processed_item_arr

    time_mask = generate_time_mask(processed_reading_dict["ustt"], start_time, end_time);

    # Extract data within a certain range
    masked_reading_dict = {}
    for key, item in processed_reading_dict.items():
        item_arr = np.array(item)
        masked_arr = item_arr[time_mask]
        masked_reading_dict[key] = masked_arr
    return masked_reading_dict

def process_llh_information(key_str, list):
    pow_arr = np.ones(len(list))*10
    arr = np.array(list)
    if (key_str == "lon" or key_str == "lat"):
        processed_arr = arr*np.power(pow_arr, -7)
    else:
        processed_arr = arr

    new_key = ""
    if (key_str == "lon"):
        new_key = "longitude"
    if (key_str == "lat"):
        new_key = "latitude"
    return new_key, processed_arr

def generate_time_mask(time_list, start, end):
    if (start == -1 or end == -1):
        time_mask = np.full((len(time_list)), True)
        return time_mask
    pow_arr = np.ones(len(time_list))*10
    time_arr = np.array(time_list)
    processed_time_arr = time_arr*np.power(pow_arr, -3)
    time_mask = (processed_time_arr >= start) & (processed_time_arr <= end)
    return time_mask
# ========================
# Main
# ========================
def main():
    target_file_dir, start_timestamp, end_timstamp = options()
    gnss_header = {'ustt': int,
                   'lon': int,
                   'lat': int}
    out_folder_dir = process_out_dir(target_file_dir, start_timestamp, end_timstamp)

    print("Reading file :", target_file_dir)
    gnss_reading = read_from_file(target_file_dir, gnss_header)

    # TODO: customized, parsing gnss data
    gnss_reading_processed = process_readings(gnss_reading, start_timestamp, end_timstamp)

    # write
    write_into_file(out_folder_dir, gnss_reading_processed)

if __name__ == "__main__":
    main()