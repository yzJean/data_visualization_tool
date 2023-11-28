import pandas as pd  # read from csv file
import os

def version_tuple(v):
    return tuple(map(int, (v.split("."))))

pd_version = pd.__version__
# print("panda version= ", pd_version)
class Reader:
    def __init__(self, directory, header_dict_list):
        self.directory = directory
        self.header_dict_list = header_dict_list
        self.reading_list = []
        self.in_file_name = os.path.splitext(os.path.basename(directory))[0]
        self.in_ext_name = os.path.splitext(os.path.basename(directory))[1]

    def make_dictionary(self, header_dict_list, reading_list):
        # return value
        reading_dic = {}
        for index, (header, reading_type) in enumerate(header_dict_list.items()):
            reading_dic[str(header)] = reading_list[index]
        return reading_dic

    # TODO: reading type
    def read_file(self):
        header_length = len(self.header_dict_list)
        if (self.in_ext_name == '.csv'):
            if version_tuple(pd_version) > version_tuple("1.4.0"):
                reading_info = pd.read_csv(self.directory, sep='\n|,', dtype=self.header_dict_list, on_bad_lines='skip', engine="python")  # panda.Series
            else: # for gw4 whose pandas ia at v1.1.5
                reading_info = pd.read_csv(self.directory, sep='\n|,',  dtype=self.header_dict_list,error_bad_lines='skip', engine="python")  # panda.Series
            for header, reading_type in self.header_dict_list.items():
                # print(header)
                if header not in reading_info.keys():
                    print('Skip reading header info: ', header)
                    continue
                reading_info[header] = reading_info[header].tolist()

        # TODO: align with header_dict
        if (self.in_ext_name == '.txt'):
            reading_info = pd.read_csv(self.directory, sep=',', engine="python", header=None, skiprows=1)  # panda.Series
            for i in range(header_length):
                self.reading_list.append(reading_info.iloc[:,i].tolist())

        # make dictionary
        reading_dic = reading_info
        return reading_dic