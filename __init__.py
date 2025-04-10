from cryptography.fernet import Fernet
from flask import Flask, render_template
import os

app = Flask(__name__)

# Charger la clé si elle existe, sinon en générer une
if os.path.exists("secret.key"):
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # str -> bytes
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"  # bytes -> str

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_bytes = f.decrypt(token.encode())  # str -> bytes -> decrypt
        return f"Valeur décryptée : {valeur_bytes.decode()}"  # bytes -> str
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
