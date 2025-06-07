from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from fpdf import FPDF
import os

def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def encrypt_file(filename, key):
    try:
        with open(filename, 'rb') as f:
            plaintext = f.read()
        plaintext = pad(plaintext)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = iv + cipher.encrypt(plaintext)

        base_name = os.path.basename(filename)
        output_file = input("Enter the name for the encrypted file (e.g. encrypted_file.enc): ").strip()
        desktop_path = get_desktop_path()
        output_path = os.path.join(desktop_path, output_file)

        with open(output_path, 'wb') as f:
            f.write(encrypted)

        generate_pdf("ENCRYPTION", os.path.abspath(filename), output_path, desktop_path)
        print(f"\n Encryption complete.")
        print(f" Encrypted File saved to: {output_path}")
    except Exception as e:
        print(" Encryption failed:", e)

def decrypt_file(filename, key):
    try:
        with open(filename, 'rb') as f:
            encrypted = f.read()
        iv = encrypted[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted[AES.block_size:])
        decrypted = decrypted.rstrip(b"\0")

        output_file = input("Enter the name for the decrypted file (e.g. decrypted.txt): ").strip()
        desktop_path = get_desktop_path()
        output_path = os.path.join(desktop_path, output_file)

        with open(output_path, 'wb') as f:
            f.write(decrypted)

        generate_pdf("DECRYPTION", os.path.abspath(filename), output_path, desktop_path)
        print(f"\n Decryption complete.")
        print(f" Decrypted File saved to: {output_path}")
    except Exception as e:
        print(" Decryption failed:", e)

def generate_pdf(operation, input_file, output_file, output_folder):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"SLANT Encryption Tool - {operation}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Input File: {input_file}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Output File: {output_file}", ln=True, align='L')

    pdf_name = f"{operation}_{os.path.basename(input_file)}.pdf"
    pdf_path = os.path.join(output_folder, pdf_name)
    pdf.output(pdf_path)
    print(f" PDF Report saved to: {pdf_path}")

def main():
    print("""             
                SSSSSSSSSSSSS        LLLLL               AAAAAAAAAAAAAAA     NNNNNN          NNNN      YYYY            YYYY
                SSSSSSSSSSSSS        LLLLL               AAAAAAAAAAAAAAA     NNNNNNNN        NNNN       YYYY          YYYY
                SSSS                 LLLLL               AAAA       AAAA     NNNN NNNN       NNNN        YYYY        YYYY  
                SSSS                 LLLLL               AAAA       AAAA     NNNN  NNNN      NNNN         YYYY      YYYY  
                SSSSSSSSSSSSS        LLLLL               AAAA       AAAA     NNNN   NNNN     NNNN          YYYYY   YYYY 
                SSSSSSSSSSSSS        LLLLL               AAAAAAAAAAAAAAA     NNNN    NNNN    NNNN           YYYYYYYYYY
                SSSSSSSSSSSSS        LLLLL               AAAAAAAAAAAAAAA     NNNN     NNNN   NNNN            YYYYYYYY
                         SSSS        LLLLL               AAAA       AAAA     NNNN      NNNN  NNNN             YYYYYY 
                         SSSS        LLLLL               AAAA       AAAA     NNNN       NNNN NNNN             YYYYYY
                SSSSSSSSSSSSS        LLLLLLLLLLLLLLL     AAAA       AAAA     NNNN         NNNNNNN             YYYYYY   
                SSSSSSSSSSSSS        LLLLLLLLLLLLLLL     AAAA       AAAA     NNNN          NNNNNN             YYYYYY 
          
          
                                                                                                                                       """)
    print(" Welcome to SLANY , A Military Grade Encryption Tool")
    while True:
        print("\n1. Encrypt a File")
        print("2. Decrypt a File")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            file = input("Enter path of file to encrypt: ").strip().strip('"')
            password = input("Enter Encryption Password: ")
            key = get_key(password)
            encrypt_file(file, key)
        elif choice == '2':
            file = input("Enter path of file to decrypt: ").strip().strip('"')
            password = input("Enter Decryption Password: ")
            key = get_key(password)
            decrypt_file(file, key)
        elif choice == '3':
            print(" Exiting SLANY. Goodbye!")
            break
        else:
            print(" Invalid Option")

if __name__ == "__main__":
    main()
