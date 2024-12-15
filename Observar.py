import socket
import threading
import io
import time
from PIL import ImageGrab, Image

class ScreenShareServer:
    def __init__(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(1)
        print("Servidor de compartición de pantalla iniciado...")
    
    def handle_client(self, client_socket):
        try:
            while True:
              
                screenshot = ImageGrab.grab()
                
              
                width, height = screenshot.size
                resized_screenshot = screenshot.resize((width // 2, height // 2), Image.ANTIALIAS)
                
                byte_io = io.BytesIO()
                resized_screenshot.save(byte_io, format='JPEG', quality=50)  
                image_data = byte_io.getvalue()

            
                client_socket.sendall(len(image_data).to_bytes(4, byteorder='big'))
                client_socket.sendall(image_data)

                time.sleep(0.5)  
        except Exception as e:
            print("Conexión cerrada:", e)
            client_socket.close()

    def run(self):
        print("Esperando conexión del cliente...")
        client_socket, addr = self.server_socket.accept()
        print(f"Cliente conectado desde: {addr}")
        threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

# Configuración del servidor
server = ScreenShareServer("0.0.0.0", 2222)
server.run()
