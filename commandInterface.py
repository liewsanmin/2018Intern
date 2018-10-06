'''
An interface to send grpc commands individually.
'''
import argparse
import os
import sys
from calampgrpc_secure import grpcLocal
rpc = grpcLocal()
chain = open('../secure_keys/CAScorpion.chain').read().encode('utf-8')
pem = open('../secure_keys/calamp_t6rx_eol_unen.pem').read().encode('utf-8')
cer = open('../secure_keys/calamp_t6rx_eol_testing_only--cert0.cer').read().encode('utf-8')

channel = rpc.getSecureClientChannel(chain, pem, cer)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description:\nAn interface to send grpc commands individually.\nAuthor:\t\tJoshua Liew\nDate Created:\t7/16/2018', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m', dest='mode', required = True, type=int,
		help='1 - modem_command | 2 - info')
    parser.add_argument('-c', dest='command', required = True, type=int,
    parser.add_argument('-v', dest='value', type=int, help='set value')
    parser.add_argument('-r', dest='rootPath', type=str, help='path to root_certificate file')
    parser.add_argument('-k', dest='keyPath', type=str, help='path to private_key file')
    parser.add_argument('-ch', dest='certPath', type=str, help='path to certificate_chain file')
    args = parser.parse_args()


    if args.mode == 1:
        rpc.sendCommand_secure(args.command, channel, value1 = args.value)
    if args.mode == 2:
    	rpc.getModemInfo_secure(args.command, channel)
