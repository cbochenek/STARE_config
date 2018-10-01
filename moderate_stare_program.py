import os
import time

condition = True
os.system("python /home/user/stare/start_stare_program.py")
time.sleep(18000)
while condition:
	os.system("python /home/user/stare/kill_stare_program.py")
	os.system("python /home/user/stare/start_stare_program.py")
	time.sleep(18000)
