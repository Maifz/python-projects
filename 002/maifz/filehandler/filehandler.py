"""Filehandler class."""
import os


class FileHandler:
    """Filehandler helper for read and write."""

    def appendToFile(self, file_path, data):
        """Write data into file of given path."""
        if not os.path.isfile(file_path):
            return False
        with open(file_path, "a") as file:
            file.write(data.decode("utf-8") + "\n\r")

    def readFile(self, file_path):
        """Read file of given file path.

        - @throws FileNotFoundError
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError
        with open(file_path, "rb") as file:
            return file.read()
