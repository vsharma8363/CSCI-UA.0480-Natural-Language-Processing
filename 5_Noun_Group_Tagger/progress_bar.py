import sys
class progress_bar:

    total_file_size = 0
    bytes_completed = 0
    last_integer = 0

    def __init__(self, filesize):
        self.total_file_size = filesize

    def make_progress(self, byte_progress):
        self.bytes_completed += byte_progress

    def get_percent_progress(self):
        return round(100.0*(self.bytes_completed/self.total_file_size), 2)

    def print_progress(self):
        if int(self.get_percent_progress()) != self.last_integer:
            print(str(int(self.get_percent_progress())) + "% Completed ...")
            self.last_integer = int(self.get_percent_progress())
