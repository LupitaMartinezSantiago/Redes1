import socket
import tkinter as tk
from tkinter import scrolledtext
import threading


class ChatClient:
    def __init__(self, root, server_ip, port):
        self.server_ip = server_ip
        self.port = port

      
        self.root = root
        self.root.title("Cliente de Chat")
        
        tk.Label(root, text="Cliente de Chat").pack(pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(root, state="normal", height=15, wrap="word")
        self.chat_display.pack(fill="both", padx=20, pady=10)
        self.chat_display.insert(tk.END, "Conectado al servidor.\n")

        tk.Label(root, text="Mensaje:").pack(anchor="w", padx=20)
        self.mensaje_entry = tk.Text(root, height=3)
        self.mensaje_entry.pack(fill="x", padx=20)

        btn_enviar = tk.Button(root, text="Enviar", command=self.enviar_mensaje)
        btn_enviar.pack(pady=20)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.port))
        threading.Thread(target=self.recibir_mensajes, daemon=True).start()  
#Enviar los mensajes
    def enviar_mensaje(self):
        mensaje = self.mensaje_entry.get("1.0", tk.END).strip()
        if mensaje:
            self.client_socket.send(mensaje.encode("utf-8"))  
            self.chat_display.insert(tk.END, f"Tú: {mensaje}\n")
            self.mensaje_entry.delete("1.0", tk.END)
        else:
            self.chat_display.insert(tk.END, "Mensaje vacío.\n")
#Funcion para recibir los mensajes
    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.client_socket.recv(1024).decode("utf-8")  
                if mensaje:
                    self.chat_display.insert(tk.END, f"Servidor: {mensaje}\n")  # Mostrar mensaje en el chat
            except Exception as e:
                break

# Configuración del cliente
root = tk.Tk()
client = ChatClient(root, "172.168.3.121", 2222)  # Cambia "172.168.0.192" por la IP de tu servidor
root.mainloop()
