import os


def manip_message(methode, message):
    if methode == 1:
        return message
    else:
        try:
            with open(message, "rb") as f:
                return f.read()
        except Exception as e:
            return e


# ------------------------------------- ALGO CHIFFREMENT ------------------------------------

def xor_function(message, key):
    if isinstance(message, list):
        message = b"".join(message)
    elif isinstance(message, str):
        message = message.encode()

    key = key.encode()
    extended_key = (key * ((len(message) // len(key)) + 1))[:len(message)]
    result = bytes([m ^ k for m, k in zip(message, extended_key)])
    return result


# ------------------------------------- SAUVEGARDE FICHIER CHIFFRE ------------------------------------

def save_encrypted_binary(cipher_bytes, original_path=None):
    base_name = os.path.basename(original_path) if original_path else "output"
    encrypted_path = f"{base_name}.xor"

    try:
        with open(encrypted_path, "wb") as f:
            f.write(cipher_bytes)
        print(f"Fichier chiffré sauvegardé : {encrypted_path}")
    except Exception as e:
        print(f"Erreur de sauvegarde : {e}")


# ------------------------------------- SAUVEGARDE FICHIER DECHIFFRE ------------------------------------

def save_decrypted_binary(data_bytes, original_encrypted_path):
    output_name = input("Entrez le nom du fichier de sortie déchiffré (ex: image.jpg) : ")
    try:
        with open(output_name, "wb") as f:
            f.write(data_bytes)
        print(f"Fichier déchiffré sauvegardé sous : {output_name}")
    except Exception as e:
        print(f"Erreur d'écriture : {e}")


# ------------------------------------- MAIN ------------------------------------

def main():
    entree = int(input("Souhaites-tu chiffrer (1) ou déchiffrer (2) ? "))

    if entree == 1:
        message_type = int(input("Chaine (1) ou fichier (2) ? "))
        if message_type == 1:
            message = input("Entrez votre message : ")
            message = manip_message(1, message)
            key = input("Entrez une clé : ")
            cipher_bytes = xor_function(message, key)
            hex_output = cipher_bytes.hex()
            with open("message_chiffre.hex", "w") as f:
                f.write(hex_output)
            print(f"Message chiffré (hex) sauvegardé dans 'message_chiffre.hex'")
        elif message_type == 2:
            path = input("Entrez le chemin du fichier (image, texte, etc.) : ")
            message = manip_message(2, path)
            if isinstance(message, Exception):
                print("Chemin de fichier invalide.")
                return
            key = input("Entrez une clé : ")
            cipher_bytes = xor_function(message, key)
            save_encrypted_binary(cipher_bytes, path)
        else:
            print("Mauvaise entrée.")
            return

    elif entree == 2:
        message_type = int(input("Message texte chiffré (1) ou fichier binaire chiffré (2) ? "))
        if message_type == 1:
            hex_input = input("Entrez le message chiffré en hexadécimal : ")
            key = input("Entrez la clé de déchiffrement : ")
            decrypted = xor_function(bytes.fromhex(hex_input), key)
            try:
                print(f"Message déchiffré : {decrypted.decode()}")
            except UnicodeDecodeError:
                print(f"(Contenu binaire non affichable)")
        elif message_type == 2:
            path = input("Entrez le chemin du fichier chiffré (.xor) : ")
            key = input("Entrez la clé de déchiffrement : ")
            try:
                with open(path, "rb") as f:
                    cipher_data = f.read()
                decrypted_bytes = xor_function(cipher_data, key)
                save_decrypted_binary(decrypted_bytes, path)
            except:
                print("Erreur lors de la lecture du fichier.")
        else:
            print("Mauvaise entrée.")
            return
    else:
        print("Entrée invalide.")
        return


if __name__ == "__main__":
    main()
