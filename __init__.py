from cryptography.fernet import Fernet
from flask import Flask, request
import base64

app = Flask(__name__)

def generate_key(user_key):
    """Génère une clé Fernet à partir de la clé fournie par l'utilisateur"""
    user_key = user_key.ljust(32)[:32]  # Assurer que la clé fait 32 caractères
    return base64.urlsafe_b64encode(user_key.encode())

@app.route('/encrypt', methods=['GET'])
def encryptage():
    valeur = request.args.get('valeur')
    user_key = request.args.get('key')

    if not valeur or not user_key:
        return "Erreur : Veuillez fournir une valeur et une clé."

    # Générer une clé unique à partir de la clé utilisateur
    key = generate_key(user_key)
    f = Fernet(key)

    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {base64.urlsafe_b64encode(token).decode()}"

@app.route('/decrypt', methods=['GET'])
def decryptage():
    valeur_chiffree = request.args.get('valeur_chiffree')
    user_key = request.args.get('key')

    if not valeur_chiffree or not user_key:
        return "Erreur : Veuillez fournir une valeur chiffrée et une clé."

    try:
        # Générer la même clé utilisateur
        key = generate_key(user_key)
        f = Fernet(key)

        # Décoder et déchiffrer
        token_bytes = base64.urlsafe_b64decode(valeur_chiffree.encode())
        valeur_dechiffree = f.decrypt(token_bytes).decode()
        return f"Valeur décryptée : {valeur_dechiffree}"

    except Exception as e:
        return f"Erreur lors du déchiffrement : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
