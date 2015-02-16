import sys
from subprocess import Popen, PIPE
from threading import Thread
import time
import logging

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

#http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading
class AsynchronousFileReader(Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''
 
    def __init__(self, fd, queue):
        assert isinstance(queue, Queue)
        assert callable(fd.readline)
        Thread.__init__(self)
        self._fd = fd
        self._queue = queue
 
    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)
 
    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

    def dump(self):
        returnContents = "" #TODO: Not really sure if we can keep this a string.  Hince the Contents part of the name
        while not self._queue.empty():
            returnContents += str(self._queue.get())

        if returnContents == "":
            returnContents = None
        return returnContents
     

class GameServer(Thread):

    name = ""
    launch_path = ""

    def __init__(self, params = {}, *kwargs):
        super(GameServer, self).__init__(*kwargs)
        self.subprocess = None
        self.params = params

    #Redefine to set the launch command's parameters
    def calculateLaunchParameters(self):

        returnString = ""
        for key, value in self.params:
            returnString += " {key} {value}".format(key = key, value = value)

        return returnString

    def stopServer(self):
        self.subprocess.terminate()

    def startServer(self):
        logging.info("Starting {}".format(self.name))
        #params = self.calculateLaunchParameters
        self.subprocess = Popen(['python', 'C:\Users\Tyler\Desktop\DevProjects\LeHub'], stdin=PIPE, stdout=PIPE, stderr=PIPE)

        output_queue = Queue()
        self.output_reader = AsynchronousFileReader(self.subprocess.stdout, output_queue)
        self.output_reader.start()

        error_queue = Queue()
        self.error_reader = AsynchronousFileReader(self.subprocess.stderr, error_queue)
        self.error_reader.start()

    def run(self):
        #Check the queues if we received some output (until there is nothing more to get).
        while not self.output_reader.eof() or not self.error_reader.eof():
            self.tick()
            # Sleep a bit before asking the readers again.
            time.sleep(0.1)
        self.onTerminated()

    #Called by the .run() method.  Use this if you want to use your own asynchronous loop.
    def tick(self):
         # Show what we received from standard output.
        output = self.output_reader.dump()
        if(output != None):
            self.onRecieveOutput(output)

        error = self.error_reader.dump()
        if(error != None):
            self.onRecieveOutput(error)

    def writeToInput(self, message):
        self.subprocess.stdin.write(message)

    def onRecieveOutput(self, output):
        sys.stdout.write(output)

    def onRecieveError(self, error):
        sys.stdout.write(error)

    def onTerminated(self):
        self.output_reader.join()
        self.error_reader.join()

        self.subprocess.stdout.close()
        self.subprocess.stderr.close()

class Launcher(object):

    def __init__(self):
        self.game_servers = []
        self.available_game_servers = []

    def startGame(self):
        #Make sure to check if we have reached some sort of limit...
        pass

if __name__ == "__main__":
    myGameServer = GameServer()
    myGameServer.startServer()
    myGameServer.start()
    myGameServer.writeToInput("Hello!")
    time.sleep(1)
    myGameServer.writeToInput("quit")
    time.sleep(1)
    myGameServer.join()



