class FileReader:

    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        try:
            file = open(self.file_name, "r")
            return file.read()
        except FileNotFoundError:
            return ""
