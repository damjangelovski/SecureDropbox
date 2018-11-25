import socket

from flask import Flask, session, redirect, url_for, escape, request

from Common.MessageProperty import MessageProperty
from Common.MessageType import *
from PersonalServer import Controller, ToGlobal

app = Flask(__name__)
app.secret_key = 'any random string'

router = {
    MessageType.DEVICE_INIT_OK_TO_PERSONAL.value: Controller.deviceInitFromGlobal ,
    MessageType.DEVICE_INIT_CONNECT_TO_PERSONAL.value: Controller.deviceInitFromDevice,
    MessageType.DEVICE_ONLINE_CONNECT.value: Controller.connectDevice,
}

myIPsocket = ''
username = ''

@app.route('/')
def index():
    if request.method != 'POST':
        print('not POST request')
        return 'not POST request'
    if MessageProperty.MESSAGE_TYPE.value not in request.form:
        print('no message-type included')
        return 'no message-type included'
    if request.form[MessageProperty.MESSAGE_TYPE.value] not in router:
        print("message-type %d not handled" % (request.form[MessageProperty.MESSAGE_TYPE.value]))
        return "message-type %d not handled" % (request.form[MessageProperty.MESSAGE_TYPE.value])
    return router.get(request.form[MessageProperty.MESSAGE_TYPE.value])(request.form)


def init(usernameTmp):
    global myIPsocket
    myIPsocket = socket.gethostbyname(socket.gethostname())+':5000'
    print("socket '%s'"%myIPsocket)
    global username
    username = usernameTmp
    ToGlobal.registerIPadress(username, myIPsocket)

    app.run(debug=True)
