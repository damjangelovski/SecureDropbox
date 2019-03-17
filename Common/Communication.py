import json

import requests

from Common.MessageProperty import MessageProperty
from Common.Security import *

globalIP = 'http://127.0.0.1:5000/'

def sendEncryptedMessage(IPsocket, jsonDictMessage, publicKey):
    data = json.dumps(jsonDictMessage)
    encryptedData = encrypt(data, publicKey)
    return requests.request('POST', IPsocket, data={MessageProperty.ENCRYPTED_MESSAGE.value: encryptedData})


def sendEncryptedMessageToGlobal(jsonDictMessage):
    return sendEncryptedMessage(globalIP, jsonDictMessage, getGlobalPublicKey())