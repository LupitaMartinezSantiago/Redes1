import socket
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import struct

class ScreenShareClient:
    def __init__(self, root, server_ip, port):
        self.root = root
        self.root.title("Visualización de Pantalla Remota")

        # Configuración de la ventana de visualización
        self.label = tk.Label(root)
        self.label.pack()

        # Configuración del socket para recibir imágenes
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_ip, port))
            print(f"Conectado a {server_ip}:{port}")
            self.receive_images()
        except Exception as e:
            print(f"Error de conexión: {e}")
            self.client_socket.close()

    def receive_images(self):
        try:
            # Recibir el tamaño de la imagen
            image_size_data = self.client_socket.recv(8)  
            if not image_size_data:
                return

            image_size = struct.unpack("Q", image_size_data)[0] 
            image_data = b""
            while len(image_data) < image_size:
                packet = self.client_socket.recv(2048)  # Reducido el búfer para optimizar la recepción
                if not packet:
                    break
                image_data += packet

            # Convertir los datos de imagen en una imagen y mostrarla
            if image_data:
                image = Image.open(BytesIO(image_data))
                photo = ImageTk.PhotoImage(image)
                self.label.config(image=photo)
                self.label.image = photo

            # Llamar a la función de nuevo para recibir la próxima imagen
            self.root.after(10, self.receive_images)  # Ajusta el retardo de actualización de imagen
        except Exception as e:
            print("Conexión perdida:", e)
            self.client_socket.close()

# Configuración del cliente con IP y puerto del servidor
root = tk.Tk()
client = ScreenShareClient(root, "172.168.2.186", 2223)  # Cambia a la IP del servidor
root.mainloop()
