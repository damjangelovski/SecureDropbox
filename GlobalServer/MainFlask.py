from flask import Flask, session, redirect, url_for, escape, request
import json
from Common.MessageType import *
from GlobalServer import PersonalServerController as psc
from GlobalServer import DeviceController as dc
from GlobalServer import DeviceController as dc
from GlobalServer import CreateDB

app = Flask(__name__)
app.secret_key = 'any random string'

router = {
    MessageType.PERSONAL_INIT_INIT.value: psc.addNewUser,
    MessageType.PERSONAL_ONLINE_INIT.value: psc.addPersonalServerIPadress,
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
        return 'not POST request'
    if request.form['messageType'] not in router:
        return "messageType %s not handled" % (request.form['messageType'])
    return router.get(request.form['messageType'])(request.form)


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