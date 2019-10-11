"""Argshelper class."""


class ArgsHelper:
    """Singleton."""

    __instance = None

    # DEFAULTS
    DEFAULT_CONTENT_TYPE = "text/plain"
    DEFAULT_FILE_PATH_WRITE = "test.txt"
    DEFAULT_INDEX_FILE_PATH = "../index.html"

    content_type = None
    file_path = None
    index_file_path = None

    @staticmethod
    def getInstance():
        """Return Class Instance."""
        if ArgsHelper.__instance is None:
            ArgsHelper()
        return ArgsHelper.__instance

    def __init__(self):
        """Virtually private constructor."""
        if ArgsHelper.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            ArgsHelper.__instance = self

    def setContentType(self, content_type):
        """Setter for content type header."""
        self.content_type = content_type

    def getContentType(self):
        """Getter for content type header."""
        return self.content_type

    def setWriteFilePath(self, file_path):
        """Setter for path of post-file."""
        self.file_path = file_path

    def getWriteFilePath(self):
        """Getter for path of post-file."""
        return self.file_path

    def setIndexFilePath(self, index_file_path):
        """Setter for index file for the webserver."""
        self.index_file_path = index_file_path

    def getIndexFilePath(self):
        """Getter for index file of the webserver."""
        return self.index_file_path

    def initializeArguments(self, ct, fpw, ifp):
        """Init function for argument defaults."""
        self.setContentType(self.DEFAULT_CONTENT_TYPE if ct is None else ct)
        self.setWriteFilePath(self.DEFAULT_FILE_PATH_WRITE if fpw is None else fpw)
        self.setIndexFilePath(self.DEFAULT_INDEX_FILE_PATH if ifp is None else ifp)
