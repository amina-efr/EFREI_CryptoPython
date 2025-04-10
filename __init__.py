from flask import Flask, request
from cryptography.fernet import Fernet, InvalidToken

app = Flask(__name__)

@app.route('/')
def accueil():
    return '''
    <h1>Bienvenue sur CryptoPython</h1>
    <p>Utilisez /key pour générer une clé</p>
    <p>Utilisez /encrypt?key=VOTRE_CLE&value=VOTRE_TEXTE</p>
    <p>Utilisez /decrypt?key=VOTRE_CLE&token=VOTRE_TOKEN</p>
    '''

@app.route('/key')
def generer_cle():
    cle = Fernet.generate_key().decode()
    return f"Clé générée : {cle}"

@app.route('/encrypt')
def encrypt():
    key = request.args.get('key')
    value = request.args.get('value')

    if not key or not value:
        return "Paramètres manquants : key et value requis"

    try:
        f = Fernet(key.encode())
        token = f.encrypt(value.encode())
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur de chiffrement : {str(e)}"

@app.route('/decrypt')
def decrypt():
    key = request.args.get('key')
    token = request.args.get('token')

    if not key or not token:
        return "Paramètres manquants : key et token requis"

    try:
        f = Fernet(key.encode())
        decrypted = f.decrypt(token.encode())
        return f"Valeur décryptée : {decrypted.decode()}"
    except InvalidToken:
        return "Erreur : token invalide ou clé incorrecte"
    except Exception as e:
        return f"Erreur : {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
