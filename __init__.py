from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Route avec clé personnelle pour chiffrer une valeur
@app.route('/encrypt/<key>/<valeur>')
def encrypt_personnalise(key, valeur):
    try:
        f = Fernet(key.encode())
        token = f.encrypt(valeur.encode())
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur de chiffrement : {str(e)}"

# Route avec clé personnelle pour déchiffrer un token
@app.route('/decrypt/<key>/<token>')
def decrypt_personnalise(key, token):
    try:
        f = Fernet(key.encode())
        valeur = f.decrypt(token.encode())
        return f"Valeur décryptée : {valeur.decode()}"
    except InvalidToken:
        return "Erreur : Token invalide ou clé incorrecte"
    except Exception as e:
        return f"Erreur : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
