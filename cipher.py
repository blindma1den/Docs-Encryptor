import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import hashlib

def sha256_encrypt(text):
    text_bytes = text.encode('utf-8')
    sha256_hash = hashlib.sha256(text_bytes)
    encrypted_text = sha256_hash.hexdigest()
    
    return encrypted_text

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
            encrypted_text = base64.b64encode(original_bytes).decode() 
        elif algorithm == 'SHA-256':
            with open(file_path, 'r') as file:
                original_text = file.read()
            encrypted_text = sha256_encrypt(original_text)
        else:
            messagebox.showerror("Error", "Algoritmo no válido")
            return
        
        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'w') as encrypted_file:
            encrypted_file.write(encrypted_text)
        
        messagebox.showinfo("Éxito", "Archivo encriptado y guardado como " + encrypted_file_path)
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_key_entry_state(*args):
    if algorithm_var.get() == 'Cifrado César':
        key_entry.config(state='normal')
    else:
        key_entry.delete(0, tk.END)
        key_entry.config(state='disabled')

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        algorithm = algorithm_var.get()
        key = key_entry.get()  # Aquí es donde intentas obtener el valor de la entrada de texto para la clave
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

algorithms = ['Cifrado César', 'Base64','SHA-256']
algorithm_var = tk.StringVar(frame)
algorithm_var.set(algorithms[0])
algorithm_var.trace_add('write', update_key_entry_state)
algorithm_dropdown = tk.OptionMenu(frame, algorithm_var, *algorithms)
algorithm_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Etiqueta y entrada de texto para la clave del cifrado César
key_label = tk.Label(frame, text="Clave:")
key_label.grid(row=1, column=0, sticky="w")
key_entry = tk.Entry(frame)
key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Botón para seleccionar archivo
select_button = tk.Button(frame, text="Seleccionar Archivo", command=browse_file)
select_button.grid(row=2, columnspan=2, pady=10)

# Llamar a mainloop() para iniciar el bucle de eventos de Tkinter
root.mainloop()
