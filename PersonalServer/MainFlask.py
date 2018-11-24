from flask import Flask, session, redirect, url_for, escape, request
from Common.MessageType import *
from PersonalServer import Controller
app = Flask(__name__)
app.secret_key = 'any random string'

router = {
    MessageType.DEVICE_INIT_OK_TO_PERSONAL: Controller.deviceInitFromGlobal ,
    MessageType.DEVICE_INIT_CONNECT_TO_PERSONAL: Controller.deviceInitFromDevice,
    MessageType.DEVICE_ONLINE_CONNECT: Controller.connectDevice,
}


@app.route('/')
def index():
    if request.method != 'POST':
        print('not POST request')
        return 'not POST request'
    if 'messageType' not in request.form:
        print('no messageType included')
        return 'no messageType included'
    if request.form['messageType'] not in router:
        print("messageType %d not handled" % (request.form['messageType']))
        return "messageType %d not handled" % (request.form['messageType'])
    return router.get(request.form['messageType'])(request.form)


def init():
    app.run(debug=True)


if __name__ == '__main__':
    init()