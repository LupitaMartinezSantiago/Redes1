import socket
#Importaciones

def conectar_a_servidor(host, puerto):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, puerto))
    print(f"Conectado al servidor {host}:{puerto}")

    while True:
     
        comando = input("Ingresa el comando a ejecutar (o 'salir' para desconectar): ")
        cliente.send(comando.encode('utf-8'))

        if comando.lower() == 'salir':
            print("Desconectado del servidor.")
            break

       
        respuesta = cliente.recv(2222).decode('utf-8')
        print(f"Respuesta del servidor:\n{respuesta}")

    cliente.close()

if __name__ == "__main__":
    SERVIDOR = "0.0.0.0"  # Dirección del servidor
    PUERTO = 9999
    conectar_a_servidor(SERVIDOR, PUERTO)
