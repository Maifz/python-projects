import sys
import os


class FileHandler:
    def appendToFile(self, file_path, data):
        '''
        - helper function for writing data in file given path
        '''
        if not os.path.isfile(file_path):
            return False
        with open(file_path, "a") as file:
            file.write(data.decode("utf-8") + "\n\r")

    def readFile(self, file_path):
        '''
        - helper function for reading file of given path
        - @throws FileNotFoundError
        '''
        if not os.path.isfile(file_path):
            raise FileNotFoundError
        with open(file_path, "rb") as file:
            return file.read()
