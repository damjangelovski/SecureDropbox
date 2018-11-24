import sqlite3
import time

conn = sqlite3.connect('securedropbox.db')


def setNewUser(username, publicKey):
    conn = sqlite3.connect('securedropbox.db')
    conn.execute("INSERT INTO USER (USERNAME,PUBLICKEY,IP,OTP,OTPDATE,IPDATE) \
      VALUES ('" + username + "', '" + publicKey + "', null, null, \
      " + str(time.time()) + ", " + str(time.time()) + ")")
    conn.commit()
    conn.close()
    print('added user with username ' + username)


def getPersonalPubKey(username):
    conn = sqlite3.connect('securedropbox.db')
    cursor = conn.execute("SELECT PUBLICKEY from USER WHERE USERNAME = '" + username + "'")
    rez = getFirst(cursor)
    conn.close()
    return rez


def getIP(username):
    conn = sqlite3.connect('securedropbox.db')
    cursor = conn.execute("SELECT IP from USER WHERE USERNAME = '" + username + "'")
    rez = getFirst(cursor)
    conn.close()
    return rez


def setIP(username, IP):
    conn = sqlite3.connect('securedropbox.db')
    cmd = "UPDATE USER set IP = '" + IP + "', IPDATE = " + str(time.time()) + " where USERNAME = '" + username + "'"
    conn.execute(cmd)
    conn.commit()
    print('added IP:'+IP+' for user '+username)
    conn.close()


def setOTP(username,OTP):
    conn = sqlite3.connect('securedropbox.db')
    cmd = "UPDATE USER set OTP = '" + OTP + "', OTPDATE = " + str(time.time()) + " where USERNAME = '" + username + "'"
    conn.execute(cmd)
    conn.commit()
    conn.close()
    print('set OTP:'+OTP+' for user '+username)


def getOTP(username):
    conn = sqlite3.connect('securedropbox.db')
    cursor = conn.execute("SELECT OTP from USER WHERE USERNAME = '" + username + "'")
    getFirst(cursor)
    conn.close()


def setDevice(deviceId, username, devicePubKey):
    conn = sqlite3.connect('securedropbox.db')
    conn.execute("INSERT INTO DEVICE (ID, USERNAME,PUBLICKEY) \
      VALUES ('" + deviceId + "', '" + username + "', '" + publicKey + "' )")
    conn.commit()
    conn.close()
    
    print("set device for username %s with pubKey %s and id %d" %(username,devicePubKey, deviceId))


def getDevicePubKey(username, deviceId):
    conn = sqlite3.connect('securedropbox.db')
    cursor = conn.execute("SELECT PUBLICKEY from DEVICE WHERE USERNAME = '" + username + "'")
    conn.close()


def testing():
    conn = sqlite3.connect('securedropbox.db')
    cursor = conn.execute('select * from USER')
    for row in cursor:
        print(row)
    conn.close()


def getFirst(cursor):
    for row in cursor:
        return row[0]

