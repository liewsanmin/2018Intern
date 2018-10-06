'''This class contains commands for secure grpc's MODEM_COMMAND and MODEM_MESSAGE'''
import os
import re
import sys
import grpc

import RadioManager_pb2
import RadioManager_pb2_grpc

if not re.search("3.5", sys.version):
    print("You need to use Python version 3.5.x")
    os._exit(1)
else:
    import thd35
    import configparser
    cfg = configparser.ConfigParser()
    absPath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(absPath)
    cfg.read('grpcconfig.cfg')
    msg = cfg['MODEM_MESSAGE']

class grpcLocal():
	def __init__(self):
		pass

	def getSecureClientChannel(self, chain, pem, cer):
		#creds = grpc.ssl_channel_credentials(open('CAScorpion.chain').read().encode('utf-8'), open('calamp_t6rx_eol_unen.pem').read().encode('utf-8'), open('calamp_t6rx_eol_testing_only--cert0.cer').read().encode('utf-8'))
		creds = grpc.ssl_channel_credentials(chain , pem, cer)
		channel = grpc.secure_channel('000111222333444555:60051', creds)
		return channel

	def getSecureClientChannel_sever(self, chain, pem, cer, server):
		creds = grpc.ssl_channel_credentials(chain , pem, cer)
		channel = grpc.secure_channel(server, creds)
		return channel

################################################################################################################
	def getModemInfo_secure(self, msgId, secureChannel):
		try:
			modemMgr_stub = RadioManager_pb2_grpc.ModemManagerStub(secureChannel)
			request = RadioManager_pb2.ModemManagerFilterMessage(ModemManagerFilter = int(msgId))
			response = modemMgr_stub.GetInfo(request)
			return response
		except Exception as e:
			#print("Error getting modem info: " + str(e))
			return e

	def sendCommand_secure(self, msgId, secureChannel, value1 = None, value2 = None, value3 = None):
		try:
			modemMgr_stub = RadioManager_pb2_grpc.ModemManagerStub(secureChannel)
			request = RadioManager_pb2.ModemCommandRequest(Command = msgId, CommandValue = value1)
			response = modemMgr_stub.SendCommand(request)
			return 0
		except Exception as e:
			#print("Error: " + str(e))
			return e

	def getModemDataStream_secure(self, msgId, secureChannel):
		try:
			f = open("report", "a")
			modemMgr_stub = RadioManager_pb2_grpc.ModemManagerStub(secureChannel)
			request = RadioManager_pb2.ModemManagerFilterMessage(ModemManagerFilter = int(msgId))
			responses = modemMgr_stub.GetModemDataStream(request)
			initial = True
			prev = ""
			for response in responses:
				f.write("Tag Id: " + str(hex(id(responses))) + "\n")
				f.write(str(response) + "\n")
				if initial == True:
					prev = id(responses)
					initial = False
				elif prev != id(responses):
					print("Stream " + msg.get(str(msgId)) + ": FAIL")
					return -1
				else:
					f.write("Verified ID: " + str(hex(id(responses))) + "\n")
					print("Stream " + msg.get(str(msgId)) + ": PASS")
					return 0
			f.close()
		except Exception as e:
			print("grpc stream info error")
			print(e)
			return str(e)
