class Player:
	name = "unknown"
	address = "unknown"

	def __init__(self, name, address, playermodel):
		self.name = name
		self.address = address
		self.playermodel = playermodel
		self.location = [0, 0, 0]
		self.rotation = 0

	def getname(self):
		return self.name

	def getaddress(self):
		return self.address

	def setpos(self, x, y, z):
		self.location = [x, y, z]

	def getpos(self):
		return self.location

	def setrot(self, rot):
		self.location = rot

	def getrot(self):
		return self.location

	def getmodel(self):
		return self.playermodel

