#Password Manager

import os
import pickle
from cryptography.fernet import Fernet
from tkinter import filedialog, Tk
from colorama import init, Fore, Style

init(autoreset=True)

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select the secret key file")
    with open(file_path, "rb") as key_file:
        key = key_file.read()
    return key

def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def save_passwords(passwords, key):
    with open("passwords.dat", "wb") as password_file:
        encrypted_data = []
        for service, username, password in passwords:
            encrypted_service = encrypt_password(service, key)
            encrypted_username = encrypt_password(username, key)
            encrypted_password = encrypt_password(password, key)
            encrypted_data.append((encrypted_service, encrypted_username, encrypted_password))
        pickle.dump(encrypted_data, password_file)

def load_passwords(key):
    passwords = []
    if os.path.exists("passwords.dat"):
        with open("passwords.dat", "rb") as password_file:
            encrypted_data = pickle.load(password_file)
            for encrypted_service, encrypted_username, encrypted_password in encrypted_data:
                service = decrypt_password(encrypted_service, key)
                username = decrypt_password(encrypted_username, key)
                password = decrypt_password(encrypted_password, key)
                passwords.append((service, username, password))
    return passwords

def add_password(passwords, key):
    service = input("Enter the service name: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    passwords.append((service, username, password))
    save_passwords(passwords, key)
    print(Fore.GREEN + "Password saved successfully!")

def view_password(passwords, key):
    service_name = input("Enter the service name to view the password: ")
    found = False
    for i, (service, username, password) in enumerate(passwords):
        if service == service_name:
            print(Fore.YELLOW + f"\nService: {service}")
            print(Fore.YELLOW + f"Username: {username}")
            print(Fore.YELLOW + f"Password: {password}")
            found = True
            break
    if not found:
        print(Fore.RED + f"Password for the service '{service_name}' Not found.")

    # Attendi l'invio prima di tornare al menu
    input("Press Enter to return to the main menu...")

def change_password(passwords, key):
    service_name = input("Enter the service name to change the password: ")
    found = False
    for i, (service, username, password) in enumerate(passwords):
        if service == service_name:
            new_password = input("Enter the new password: ")
            passwords[i] = (service, username, new_password)
            save_passwords(passwords, key)
            print(Fore.GREEN + "Password changed successfully!")
            found = True
            break
    if not found:
        print(Fore.RED + f"Password for the service '{service_name}' Not Found.")

def list_services(passwords):
    if not passwords:
        print(Fore.YELLOW + "No service saved.")
    else:
        print(Fore.YELLOW + "List of saved services:")
        for service, _, _ in passwords:
            print(Fore.LIGHTGREEN_EX + f"{service}")

def main():
    choice = input("Do you already have a secret key? (yes/No): ").strip().lower()
    
    if choice in ["si", "sì", "s", "y", "yes"]:
        key = load_key()
    elif choice in ["n", "no"]:
        print(Fore.CYAN + "\nYour secret key has been generated in the current folder (secret.key). HIDE IT AND KEEP IT SAFE, it's needed to recover your passwords!")
        generate_key()
        key = load_key()
    else:
        print(Fore.RED + "Invalid option.")
        main()

    passwords = load_passwords(key)

    while True:
        print(Fore.CYAN + f"\nMenu:")
        print("1. Add new service, username, and password")
        print("2. Display the password for a service")
        print("3. Change the password for a service")
        print("4. Display the list of saved services")
        print("5. Exit")
        choice = input("Choose an option (1/2/3/4/5): ").strip()

        if choice == "1":
            add_password(passwords, key)
        elif choice == "2":
            view_password(passwords, key)
        elif choice == "3":
            change_password(passwords, key)
        elif choice == "4":
            list_services(passwords)
        elif choice == "5":
            print(Fore.CYAN + "Goodbye!")
            break
        else:
            print(Fore.RED + Fore.YELLOW + "Invalid choice. Please respond with 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()