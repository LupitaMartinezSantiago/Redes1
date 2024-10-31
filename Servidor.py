import socket
import threading
import pyautogui  # Para ver las pantallas recibidas
import os

# Configuración del servidor
HOST = '0.0.0.0'  # Escuchar en todas las interfaces de red disponibles
PORT = 12345

clientes = []

def manejar_cliente(conn, addr):
    print(f"Conexión establecida con {addr}")
    clientes.append(conn)

    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            # Comando de chat
            if data.startswith("CHAT:"):
                mensaje = data.replace("CHAT:", "")
                print(f"[{addr}] dice: {mensaje}")
                broadcast(f"CHAT:{mensaje}", conn)

            # Comando para captura de pantalla
            elif data.startswith("SCREENSHOT"):
                recibir_pantalla(conn)

            # Comando para bloquear teclado y mouse
            elif data.startswith("BLOCK"):
                print(f"[{addr}] Bloquear teclado/mouse")
                # Aquí puedes agregar lógica adicional si se requiere

            # Comando para desbloquear teclado y mouse
            elif data.startswith("UNBLOCK"):
                print(f"[{addr}] Desbloquear teclado/mouse")
                # Aquí puedes agregar lógica adicional si se requiere

        except ConnectionResetError:
            break

    print(f"Conexión cerrada con {addr}")
    conn.close()
    clientes.remove(conn)

def broadcast(mensaje, cliente_remitente):
    for cliente in clientes:
        if cliente != cliente_remitente:
            cliente.sendall(mensaje.encode('utf-8'))

def recibir_pantalla(conn):
    with open(f"screenshot_{conn.getpeername()}.png", 'wb') as f:
        while True:
            datos = conn.recv(1024)
            if not datos:
                break
            f.write(datos)
    print("Captura de pantalla recibida")

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = servidor.accept()
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
        thread.start()

if _name_ == "_main_":
    iniciar_servidor()