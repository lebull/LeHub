import async_subprocess
from subprocess import PIPE

class GameServer(object):

	launch_command = "python echo.py".split(" ")
	launch_params = ['-n', '3']

	def __init__(self):
		self.subprocess = async_subprocess.AsyncPopen(self.launch_command + self.launch_params, stdin = PIPE, stdout = PIPE, stderr = PIPE)

	def startServer(self):
		pass
	def tick(self):
		pass
	def run(self):
		pass
	def stopServer(self):
		self.killServer()#Only because we're not actually working with a server xD
		pass#nice

	def killServer(self):
		self.subprocess.kill()#rude

	def isAlive(self):
		if myServer.subprocess.poll() == None: #If the process has terminated...
			return True
		else:
			return False

class TF2Server(GameServer):
	launch_command = ["C:/Steam/tf2/srcds.exe"]
	launch_params = '-console -game tf +sv_pure 1 +map ctf_2fort +maxplayers 24 +rcon_password "password"'.split(" ")
	def sendMessage(self, message):
		self.subprocess.communicate(message)



if __name__ == "__main__":
	import time
	import sys
	"""
	myServer = TF2Server()


	time.sleep(1)

	output, error = myServer.subprocess.communicate(input = "Hi")
	if(error != None):
		print error
	print output

	time.sleep(1)

	output, error = myServer.subprocess.communicate(input = "Quit")
	if(error != None):
		print error
	print output

	myServer.killServer()

	while myServer.isAlive():
		time.sleep(0.1)
	"""


	myServer = TF2Server()
	
	while(True):
		output, error = myServer.subprocess.communicate()
		if output != None:
			sys.stdout.write(output)
		else:
			print myServer.subprocess.poll()
			if not myServer.isAlive():
				break
		time.sleep(0.1)

