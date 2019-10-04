import sys
import os


class FileHandler():

    def appendToFile(self, file_path, data):
        if not os.path.isfile(file_path):
            return False
        with open(file_path, 'a') as file:
            file.write(data.decode('utf-8') + '\n\r')

    def readFile(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError
        with open(file_path, 'rb') as file:
            return file.read()
