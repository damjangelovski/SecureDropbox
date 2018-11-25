import sys, getopt
import random
from PersonalServer import ToGlobal, MainFlask
import inspect



def main(argv):
    username = ''
    shouldAddNewUser = False
    shouldAddNewDevice = False

    try:
        opts, args = getopt.getopt(argv,"u:nd", ["new-user=", "new-device="])
    except getopt.GetoptError:
        print('getopt error, usage: personal-server.py -u <username> [-n] [-d]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        if opt in ("-n", "--new-user"):
            shouldAddNewUser = True
        elif opt in ("-d", "--new-device"):
            shouldAddNewDevice = True

    if username == '':
        print('personal-server.py -u <username> [-n] [-d]')
        sys.exit(1)

    if shouldAddNewUser:
        ToGlobal.addNewUser(username)
        exit(0)


    if shouldAddNewDevice:
        otp = random.randint(100000, 999999)
        ToGlobal.addDevice(username, otp)
        print('ready to add device with one time pad %d' % otp)

    MainFlask.init(username)

if __name__ == "__main__":
        main(sys.argv[1:])
