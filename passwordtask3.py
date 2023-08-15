from cryptography.fernet import Fernet
import hashlib
import os

def generate_key():
    return Fernet.generate_key()

def load_key():
    return open("secret.key", "rb").read()

def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def hash_master_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def store_password(service, username, password, key):
    encrypted_password = encrypt_password(password, key)
    with open("passwords.txt", "a") as file:
        file.write(f"{service},{username},{encrypted_password}\n")

def retrieve_password(service, username, key):
    with open("passwords.txt", "r") as file:
        for line in file:
            stored_service, stored_username, encrypted_password = line.strip().split(",")
            if stored_service == service and stored_username == username:
                decrypted_password = decrypt_password(encrypted_password.encode(), key)
                return decrypted_password

def main():
    master_password = input("Enter your master password: ")
    hashed_master_password = hash_master_password(master_password)

    if not os.path.isfile("secret.key"):
        key = generate_key()
        save_key(key)
    else:
        key = load_key()

   

    while True:
        print("==== Password Manager ====")
        print("1. Store Password")
        print("2. Retrieve Password")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service or website name: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            store_password(service, username, password, key)
            print("Password stored successfully.")
        elif choice == "2":
            service = input("Enter the service or website name: ")
            username = input("Enter your username: ")
            password = retrieve_password(service, username, key)
            if password:
                print(f"Your password for {service} - {username} is: {password}")
            else:
                print("Password not found.")
        elif choice == "0":
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
