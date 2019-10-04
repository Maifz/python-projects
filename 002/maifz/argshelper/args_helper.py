class ArgsHelper:
	__instance = None

	content_type = "text/plain"

	@staticmethod
	def getInstance():
		""" Static access method. """
		if ArgsHelper.__instance == None:
			ArgsHelper()
		return ArgsHelper.__instance

	def __init__(self):
		""" Virtually private constructor. """
		if ArgsHelper.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			ArgsHelper.__instance = self

	def setContentType(self, content_type):
		self.content_type = content_type

	def getContentType(self):
		return self.content_type