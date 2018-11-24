import sys, getopt
import random
from .ToGlobal import *
from .MainFlask import init


def main(argv):
    username = ''
    shouldAddNewUser = False
    shouldAddNewDevice = False

    try:
        opts, args = getopt.getopt(argv,"u:nd", ["new-user=", "new-device="])
    except getopt.GetoptError:
        print ('personal-server.py -u <username> [-n] [-d]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--new-user"):
            shouldAddNewUser = True
        elif opt in ("-o", "--new-device"):
            shouldAddNewDevice = True

    if username == '':
        print('personal-server.py -u <username> [-n] [-d]')
        sys.exit(2)

    if shouldAddNewUser:
        addNewUser(username)
    if shouldAddNewDevice:
        otp = random.randint(100000,999999)
        addDevice(username)
        print('ready to add device with one time pad %d' % otp)

    init()


if __name__ == "__main__":
   main(sys.argv[1:])