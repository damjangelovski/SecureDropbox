import sys, getopt
from Device.Communication import *


def main(argv):
    username = ''
    otp = ''
    try:
        opts, args = getopt.getopt(argv,"u:o:", ["username=", "one-time-pad="])
    except getopt.GetoptError:
        print ('device.py -u <username> [-o <one-time-pad>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        elif opt in ("-o", "--one-time-pad"):
            otp = arg

    if username == '':
        print('personal-server.py -u <username> [-n] [-d]')
        sys.exit(2)

    if otp != '':
        registerDevice(username, otp)
    else:
        startDevice(username)


if __name__ == "__main__":
   main(sys.argv[1:])