from socket import *
import copy
import struct


# The function 'parseMessage' inputs a byte array -- i.e. as obtained from the Vicon Tracker
# UDP broadcast packets -- and it parses that array into native python data for the objects
# being tracked

def parseMessage(m):
	# Using dictionaries here is inefficient, but it makes things more readable
	# (i.e. change this aspect before implementing on a robot)
	packetInfo = { \
		'frame':0, \
		'numItems':0 \
		}
	objectData = { \
		'itemID':0, \
		'itemDataSize':0, \
		'objectName':'', \
		'xPos':0.0, \
		'yPos':0.0, \
		'zPos':0.0, \
		'xRot':0.0, \
		'yRot':0.0, \
		'zRot':0.0 \
		}
	byteIdx = 0

	packetInfo['frame'] = int.from_bytes(m[0][0:4], byteorder='little', signed=False)
	packetInfo['numItems'] = m[0][4]
	byteIdx = 5
	retObjects = []

	for numItems in range(0,packetInfo['numItems']):
		retObjects.append(copy.copy(objectData))

		retObjects[-1]['itemID'] = m[0][byteIdx]
		byteIdx = byteIdx + 1
		
		# **** NOTE: ****
		# This code assumes that each object has exactly 72 bytes of data, since it is
		# not documented where extra bytes would go if that field is set differently 
		# (although these extra/fewer bytes would probably go to/from the object name...)
		# ***************
		retObjects[-1]['itemDataSize'] = int.from_bytes(m[0][byteIdx:byteIdx+2], byteorder='little', signed=False)
		byteIdx = byteIdx + 2

		retObjects[-1]['objectName'] = m[0][byteIdx:byteIdx+24].decode('utf-8').strip(b'\x00'.decode())
		byteIdx = byteIdx + 24

		for floatParam in ['xPos','yPos','zPos','xRot','yRot','zRot']:
			retObjects[-1][floatParam] = struct.unpack('d',m[0][byteIdx:byteIdx+8])[0]/1000
			byteIdx = byteIdx + 8
            
	return packetInfo,retObjects




# Straightforward code to initiate a UDP socket and read packets:


# Open a UDP socket
s=socket(AF_INET, SOCK_DGRAM)

# UDP port 51001 is set by default in the vicon tracker software
# ** Note: ** 
#     This port number should be incremented by one on each robot if "object per port"
#     is selected; the order of the objects is the order in which they appear in the
#     tracker software
udpPort = 51001

# Bind the socket to the localhost on udpPort (which allows to read broadcast UDP packets)
s.bind(('',udpPort))

# 256 is set(able) in the vicon tracker software
datagramSize = 256

# Receive one packet:
m = s.recvfrom(datagramSize)
pi,ob = parseMessage(m)

# Print the packet information
print(pi)
# Print the object information contained in that packet
print(ob) #States in numeric description

# Read another 10 packets, and print out their contents:
pktCnt = 0
while m and pktCnt < 10:
	m = s.recvfrom(datagramSize)
	pi,ob = parseMessage(m)
	print(pi)
	print(ob)
	pktCnt = pktCnt + 1





