import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import os
from PIL import Image
from PyPDF2 import PdfFileReader

def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted_char = chr((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26 + ord('a' if char.islower() else 'A'))
            encrypted_text += shifted_char
        else:
            encrypted_text += char
    return encrypted_text

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def encrypt_file(file_path, algorithm, key=None):
    try:
        if algorithm == 'Cifrado César':
            shift = int(key)
            with open(file_path, 'r') as file:
                original_text = file.read()
            encrypted_text = caesar_cipher_encrypt(original_text, shift)
        elif algorithm == 'Base64':
            with open(file_path, 'rb') as file:
                original_bytes = file.read()
            encrypted_text = base64_encode(original_bytes)
        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'w') as encrypted_file:
            encrypted_file.write(encrypted_text)
        messagebox.showinfo("Éxito", "Archivo encriptado y guardado como " + encrypted_file_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        algorithm = algorithm_var.get()
        key = key_entry.get()
        if not key and algorithm == 'Cifrado César':
            messagebox.showerror("Error", "Por favor, ingrese una clave para el cifrado César.")
            return
        encrypt_file(file_path, algorithm, key)

# Crear ventana principal
root = tk.Tk()
root.title("Encriptador de Archivos")

# Marco para los elementos de la interfaz
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Etiqueta y lista desplegable para elegir el algoritmo de cifrado
algorithm_label = tk.Label(frame, text="Algoritmo de cifrado:")
algorithm_label.grid(row=0, column=0, sticky="w")
algorithms = ['Cifrado César', 'Base64']
algorithm_var = tk.StringVar(frame)
algorithm_var.set(algorithms[0])
algorithm_dropdown = tk.OptionMenu(frame, algorithm_var, *algorithms)
