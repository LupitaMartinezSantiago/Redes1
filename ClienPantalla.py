import socket

def conectar_a_servidor(host, puerto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, puerto))
    print(f"Conectado al servidor {host}:{puerto}")

    while True:
        # Solicitar comando al usuario
        comando = input("Ingresa el comando a ejecutar (o 'salir' para desconectar): ")
        cliente.send(comando.encode('utf-8'))

        if comando.lower() == 'salir':
            print("Desconectado del servidor.")
            break

        # Recibir y mostrar la respuesta
        respuesta = cliente.recv(1024).decode('utf-8')
        print(f"Respuesta del servidor:\n{respuesta}")

    cliente.close()

if __name__ == "__main__":
    SERVIDOR = "172.168.0.150"  # Dirección del servidor
    PUERTO = 9999
    conectar_a_servidor(SERVIDOR, PUERTO)
