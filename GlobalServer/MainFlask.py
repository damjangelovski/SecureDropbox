from flask import Flask, session, redirect, url_for, escape, request, jsonify
import json

from Common.MessageProperty import MessageProperty
from Common.MessageType import *
from Common.Security import *
from GlobalServer import PersonalServerController as psc
from GlobalServer import DeviceController as dc
from GlobalServer import CreateDB

app = Flask(__name__)
app.secret_key = 'any random string'

router = {
    MessageType.PERSONAL_INIT_INIT.value: psc.addNewUser,
    MessageType.PERSONAL_ONLINE_INIT.value: psc.addPersonalServerIPadress,
    MessageType.DEVICE_INIT_INIT.value: psc.addOTPforNewDevice,
    MessageType.DEVICE_INIT_START.value: dc.addDevice,
    MessageType.DEVICE_ONLINE_INIT.value: dc.getPersonalServerIPadress,
}


@app.route('/hello')
def helloPing():
    return "hello from global server."


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        print('not POST request')
        return 'not POST request'
    print('got message' + json.dumps(request.form))
    if MessageProperty.ENCRYPTED_MESSAGE.value not in request.form:
        print('no encrypted message included')
        return 'no encrypted message included'
    try:
        privateKey = getPrivateKeyString('D:\\dev\\pycharm\\SecureDropbox\\Common\\private_key.pem')
        requestForm = json.loads(decrypt(request.form[MessageProperty.ENCRYPTED_MESSAGE.value], privateKey))
    except:
        print('cant decrypt: '+request.form[MessageProperty.ENCRYPTED_MESSAGE.value])
        return 'cant decrypt'

    if MessageProperty.MESSAGE_TYPE.value not in requestForm:
        print('no message-type included')
        return 'no message-type included'
    if requestForm[MessageProperty.MESSAGE_TYPE.value] not in router:
        print("message-type %s not handled" % (requestForm[MessageProperty.MESSAGE_TYPE.value]))
        return "message-type %s not handled" % (requestForm[MessageProperty.MESSAGE_TYPE.value])
    return router.get(requestForm[MessageProperty.MESSAGE_TYPE.value])(requestForm)


@app.route('/users', methods=['GET'])
def users():
    users = psc.getAllUsers()

    return json.dumps(users)


@app.route('/devices', methods=['GET'])
def devices():
    devices = dc.getAllDevices()

    return json.dumps(devices)


@app.route('/drop', methods=['GET'])
def dropAllTables():
    CreateDB.dropDatabase()
    CreateDB.initDatabase()

    resp = jsonify(success=True)
    return resp

def init():
    CreateDB.initDatabase()

    app.run(debug=True, host='0.0.0.0', use_reloader=False)

if __name__ == '__main__':
    init()