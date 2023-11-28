import csv

class Writer:
    def __init__(self, directory, reading):
        self.directory = directory
        self.reading = reading
        self.file = open(directory, 'w')
        self.writer = csv.writer(self.file)

    def write_reading_into_file(self):
        header = []
        reading_data = []
        for key, data_list in self.reading.items():
            header.append(key)
            reading_data.append(data_list)

        self.writer.writerow(header)
        zipped_data = zip(*reading_data)
        for column in zipped_data:
            self.writer.writerow(column)
        print("Wrote reading into file:", self.directory)