import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def generateKeys(privateKeyFilePath, publicKeyFilePath):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048*4,
        backend=default_backend())
    public_key = private_key.public_key()

    # Storing the keys
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    with open(privateKeyFilePath, 'wb') as f:
        f.write(pem)

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(publicKeyFilePath, 'wb') as f:
        f.write(pem)


def getPrivateKeyString(filePath):
    with open(filePath, "rb") as key_file:
        return str(key_file.read(),'utf-8')


def getPublicKeyString(filePath):

    with open(filePath, "rb") as key_file:
        return str(key_file.read(),'utf-8')

def encrypt(message, publicKeyString):
    public_key = serialization.load_pem_public_key(
        bytes(publicKeyString, 'utf-8'),
        backend=default_backend())
    return base64.encodebytes(public_key.encrypt(
        bytes(message, 'utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))).decode('ascii')

def decrypt(message, privateKeyString):
    private_key = serialization.load_pem_private_key(
        bytes(privateKeyString, 'utf-8'),
        password=None,
        backend=default_backend())
    return str(private_key.decrypt(
        base64.decodebytes(bytes(message, 'ascii')),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None)), 'utf-8')


def getGlobalPublicKey():
    return getPublicKeyString('D:\dev\pycharm\SecureDropbox\Common\public_key.pem')


def testEncryption():
    global private_key_string, public_key_string, encrypted
    generateKeys('private_key.pem', 'public_key.pem')
    private_key_string = json.loads(json.dumps({'pk': getPrivateKeyString("private_key.pem")}))['pk']
    public_key_string = getPublicKeyString("public_key.pem")
    message = 'encrypt me!'
    encrypted = json.loads(json.dumps({'pk': encrypt(message, public_key_string)}))['pk']
    original_message = decrypt(encrypted, private_key_string)
    # Checking the results
    print(original_message)
    print(message)
    print(encrypted)
    print(private_key_string)
    print(public_key_string)

# The key size parameter should be bigger for the global server.
# generateKeys('..\\PersonalServer\\private_key.pem', '..\\PersonalServer\\public_key.pem')
# generateKeys('private_key.pem', 'public_key.pem')
# testEncryption()