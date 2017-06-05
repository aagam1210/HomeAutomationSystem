
import time
import sys
import json
import pprint
import uuid
from uuid import getnode as get_mac


try:
	import ibmiotf.application
	import ibmiotf.device
except ImportError:
	# This part is only required to run the sample from within the samples
	# directory when the module itself is not installed.
	#
	# If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
	import os
	import inspect
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
	import ibmiotf.application
	import ibmiotf.device


def myAppEventCallback(event):
	print("Received live data from %s (%s) sent at %s: %s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), json.dumps(event.data)))
		

#####################################
#FILL IN THESE DETAILS
#####################################     
# organization = "ovil5l"
# deviceType = "raspberry_pi"
# deviceId = "b827eb61ccaa"
# appId = str(uuid.uuid4())
# authMethod = "token"
# authToken = "V0b3bK7SalG@DsuQS*"

organization = "ysoznq"
deviceType = "raspberry_pi"
deviceId = "b827eb61ccaa"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "WrndLEBcQXFY_3o_9z"

##API TOKEN AND KEY
authkey = "a-ysoznq-vtcn5ycday"
authtoken = "b-x87d2Z!1qAXJ&2&0"
#authkey = "a-ovil5l-3tuq8dxuhi"
#authtoken = "uJ3-7CCOaSz&mXuLRb"
# Initialize the application client.

try:
	appOptions = {"org": organization, "id": appId,"auth-method": "apikey", "auth-key" : authkey, "auth-token":authtoken }
	

except Exception as e:
	print(str(e))
	sys.exit()

# Connect and configuration the application
# - subscribe to live data from the device we created, specifically to "greeting" events
# - use the myAppEventCallback method to process events
# while(True):
command = 'null'
# command = raw_input("Enter the command: ")
command = sys.argv[1]

if command in ['ON 1','OFF 1','ON 2','OFF 2','ON 3','OFF 3']:
	print "Turning Light "+ command[0:3] + " for Appliance "+ command[-1]
	try:
		appCli = ibmiotf.application.Client(appOptions)
		appCli.connect()
		if command[0:2] == 'ON':
			commandData={'LightON' : 1}
		else:
			commandData={'LightOFF': 0}
	
		appCli.publishCommand(deviceType, deviceId, command, "json", commandData,0)
		appCli.publishEvent(deviceType, deviceId,"status", "json", commandData, 0)
		# x=0
		# while(x<1):
		# 	appCli.deviceEventCallback = myAppEventCallback
		# 	appCli.subscribeToDeviceEvents(event="status")
		# 	x=x+1

	except Exception as e:
		print ("Connect attempt failed: "+str(e))
		sys.exit()

else:
	print "Not a valid command"

sys.stdout.flush()
appCli.disconnect()

