class FileHandler():

    def appendToFile(self, file_path, data):
        with open(file_path, 'a') as file:
            file.write(data + '\n\r')

    def readFile(self):
        with open('index.html', 'rb') as file:
            file.read()
        print("read")
