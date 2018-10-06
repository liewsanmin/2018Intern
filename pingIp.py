import os, RadioManager_pb2_grpc, RadioManager_pb2, sys, getUnsecureClientChannel
import argparse

p = os.path.abspath('../')
if p not in sys.path:
    sys.path.append(p)

import atsCalampgrpc as grpcLib
COMMAND = RadioManager_pb2.ATS_PING_IP

def grpcAtsPingIp(value1 = None, value2 = None, value3 = None, value4 = None):
	try:
		RadioManager_pb2_grpc.ModemManagerStub(getInsecureClientChannel())
		RadioManager_pb2.ModemCommandRequest(Command = int(COMMAND), CommandValue = value1, AtsCommandValue1 = value2, AtsCommandValue2 = value3, AtsCommandValue3 = value4)
		return 0
	except Exception as e:
		print("Grpc send command error: " + str(e))
		return -1

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Description:\nAn interface to send grpc ATS commands individually.\nAuthor:\t\tJoshua Liew\nDate Created:\t7/24/2018', formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-v',  dest='value',  default = '', type=str,  help='v - CommandValue')
	parser.add_argument('-v1', dest='value1', default = '', type=str, help='v1 - AtsCommandValue1')
	parser.add_argument('-v2', dest='value2', default = '', type=str, help='v2 - AtsCommandValue2')
	parser.add_argument('-v3', dest='value3', default = '', type=str, help='v3 - AtsCommandValue3')
	args = parser.parse_args()
	grpcAtsPingIp(args.value, args.value1, args.value2, args.value3)
