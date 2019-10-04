class FileHandler():

    def appendToFile(self, file_path, data):
        with open(file_path, 'a') as file:
            file.write(data.decode('utf-8') + '\n\r')

    def readFile(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()
