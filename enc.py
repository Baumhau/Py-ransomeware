from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

# Laden des RSA-öffentlichen Schlüssels
def load_public_key():
    with open("public_key.pem", "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())
    return public_key

# Laden des RSA-privaten Schlüssels
def load_private_key():
    with open("private_key.pem", "rb") as priv_file:
        private_key = RSA.import_key(priv_file.read())
    return private_key

# Fernet-Schlüssel generieren und mit RSA-öffentlichem Schlüssel verschlüsseln
def generate_encrypted_key():
    fernet_key = Fernet.generate_key()
    fernet = Fernet(fernet_key)
    public_key = load_public_key()
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_fernet_key = cipher_rsa.encrypt(fernet_key)
    with open("encrypted_fernet_key.key", "wb") as key_file:
        key_file.write(encrypted_fernet_key)
    return fernet

# RSA-verschlüsselten Fernet-Schlüssel entschlüsseln
def load_decrypted_key():
    private_key = load_private_key()
    cipher_rsa = PKCS1_OAEP.new(private_key)
    with open("encrypted_fernet_key.key", "rb") as key_file:
        encrypted_fernet_key = key_file.read()
    fernet_key = cipher_rsa.decrypt(encrypted_fernet_key)
    return Fernet(fernet_key)

def encrypt_file(file_path, fernet):
    with open(file_path, "rb") as file:
        original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)
    with open(file_path + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
    os.remove(file_path)  # Originaldatei löschen
    print(f"Die Datei '{file_path}' wurde verschlüsselt.")

def decrypt_file(file_path, fernet):
    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    original_file_path = file_path.replace(".enc", "")
    with open(original_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
    os.remove(file_path)  # Verschlüsselte Datei löschen
    print(f"Die Datei '{file_path}' wurde entschlüsselt.")

def encrypt_all_files():
    fernet = generate_encrypted_key()
    script_name = os.path.basename(__file__)  # Name des Skripts selbst
    for root, dirs, files in os.walk("."):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename not in ["public_key.pem", "private_key.pem", "encrypted_fernet_key.key","genkey.py" ,"start.bat", "README.md",script_name] and not filename.endswith(".enc"):
                encrypt_file(file_path, fernet)

def decrypt_all_files():
    fernet = load_decrypted_key()
    for root, dirs, files in os.walk("."):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith(".enc"):
                decrypt_file(file_path, fernet)

if __name__ == "__main__":
    action = input("Möchten Sie alle Dateien im Ordner und Unterverzeichnissen verschlüsseln oder entschlüsseln? (v/e): ")
    
    if action.lower() == 'v':
        encrypt_all_files()
    elif action.lower() == 'e':
        decrypt_all_files()
    else:
        print("Ungültige Eingabe! Bitte 'v' für Verschlüsseln oder 'e' für Entschlüsseln eingeben.")


