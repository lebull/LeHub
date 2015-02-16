import sys
import os
import fileinput
import time
import re

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

sys.stdout.write("Welcome to my shell!\n")



while(True):

	line = sys.stdin.readline()
	if re.match("^quit", line):
		break
	else:
		sys.stdout.write(str(line))

	#sys.stdout.flush()
	time.sleep(0.1)