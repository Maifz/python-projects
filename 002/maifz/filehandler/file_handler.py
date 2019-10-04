class FileHandler():

    def appendToFile(self, file_path, data):
        with open(file_path, 'a') as file:
            file.write(str(data) + '\n\r')

    def readFile(self, file_path):
        with open('index.html', 'rb') as file:
            return file.read()


