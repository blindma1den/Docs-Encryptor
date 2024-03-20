import wx
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
    text_bytes = text if isinstance(text, bytes) else text.encode()
    return base64.b64encode(text_bytes).decode()

def encrypt_file(file_path, algorithm, key=None):
    try:
        with open(file_path, 'rb') as file:  # Lee siempre en modo binario
            original_bytes = file.read()

        if algorithm == 'Cifrado César':
            shift = int(key)
            try:
                # Intenta decodificar como UTF-8
                original_text = original_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # Si la decodificación falla, notifica al usuario
                wx.MessageBox("El archivo seleccionado no es compatible con el Cifrado César debido a su codificación o porque no es un archivo de texto.", "Error de Decodificación", wx.OK | wx.ICON_ERROR)
                return  # Detiene la ejecución para este archivo

            encrypted_text = caesar_cipher_encrypt(original_text, shift)
            encrypted_bytes = encrypted_text.encode('utf-8')  # Codifica de nuevo a bytes

        elif algorithm == 'Base64':
            encrypted_bytes = base64.b64encode(original_bytes)  # Directamente usa los bytes originales

        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'wb') as encrypted_file:  # Escribe como binario
            encrypted_file.write(encrypted_bytes)

        wx.MessageBox("Archivo encriptado y guardado como " + encrypted_file_path, "Éxito", wx.OK | wx.ICON_INFORMATION)

    except Exception as e:
        wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


class EncryptorApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show(True)
        return True

class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None, title="Encriptador de Archivos", size=(400, 200))
        self.panel = wx.Panel(self)
        self.algorithm = 'Cifrado César'
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Algoritmo de cifrado
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        algorithm_label = wx.StaticText(self.panel, label="Algoritmo de cifrado:")
        hbox1.Add(algorithm_label, flag=wx.RIGHT, border=8)
        algorithm_choices = ['Cifrado César', 'Base64']
        self.algorithm_dropdown = wx.ComboBox(self.panel, choices=algorithm_choices, style=wx.CB_READONLY)
        self.algorithm_dropdown.Bind(wx.EVT_COMBOBOX, self.OnAlgorithmChange)
        hbox1.Add(self.algorithm_dropdown, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Clave para el cifrado César
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.key_entry = wx.TextCtrl(self.panel)
        hbox2.Add(self.key_entry, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Botón para buscar archivo
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.browse_button = wx.Button(self.panel, label="Buscar Archivo y Encriptar")
        self.browse_button.Bind(wx.EVT_BUTTON, self.OnBrowse)
        hbox3.Add(self.browse_button, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        self.panel.SetSizer(vbox)

    def OnAlgorithmChange(self, event):
        self.algorithm = self.algorithm_dropdown.GetValue()

    def OnBrowse(self, event):
        with wx.FileDialog(self, "Seleccione un archivo", wildcard="Todos los archivos (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            file_path = fileDialog.GetPath()
            key = self.key_entry.GetValue()
            if not key and self.algorithm == 'Cifrado César':
                wx.MessageBox("Por favor, ingrese una clave para el cifrado César.", "Error", wx.OK | wx.ICON_ERROR)
                return
            encrypt_file(file_path, self.algorithm, key)
if __name__ == "__main__":
    app = EncryptorApp()
    app.MainLoop()
