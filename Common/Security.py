
def encrypt(message, key):
    return key+message


def decrypt(message, key):
    if len(message) >= len(key) and message[:len(key)] == key:
        return message[len(key):]
    return "FAILED TO DECRYPT!!"


def sign(message, key):
    return key+message


def checkSignature(message, key):
    return len(message) >= len(key) and message[:len(key)] == key

def getGlobalPublicKey():
    return 'globalKey'

