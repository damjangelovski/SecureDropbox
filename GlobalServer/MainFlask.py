from flask import Flask, session, redirect, url_for, escape, request
import json

from Common.MessageProperty import MessageProperty
from Common.MessageType import *
from GlobalServer import PersonalServerController as psc
from GlobalServer import DeviceController as dc
from GlobalServer import CreateDB

app = Flask(__name__)
app.secret_key = 'any random string'

router = {
    MessageType.PERSONAL_INIT_INIT.value: psc.addNewUser,
    MessageType.PERSONAL_ONLINE_INIT: psc.addPersonalServerIPadress,
    MessageType.DEVICE_INIT_INIT: psc.addOTPforNewDevice,
    MessageType.DEVICE_INIT_START: dc.addDevice,
    MessageType.DEVICE_ONLINE_INIT: dc.getPersonalServerIPadress,
}


@app.route('/hello')
def helloPing():
    return "hello from global server."


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        print('not POST request')
        return 'not POST request'
    if MessageProperty.MESSAGE_TYPE.value not in request.form:
        print('no message-type included')
        return 'no message-type included'
    if request.form[MessageProperty.MESSAGE_TYPE.value] not in router:
        print("message-type %s not handled" % (request.form[MessageProperty.MESSAGE_TYPE.value]))
        return "message-type %s not handled" % (request.form[MessageProperty.MESSAGE_TYPE.value])
    return router.get(request.form[MessageProperty.MESSAGE_TYPE.value])(request.form)


@app.route('/users', methods=['GET'])
def users():
    users = psc.getAllUsers()

    return json.dumps(users)


@app.route('/devices', methods=['GET'])
def devices():
    devices = dc.getAllDevices()

    return json.dumps(devices)

def init():
    CreateDB.initDatabase()

    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    init()