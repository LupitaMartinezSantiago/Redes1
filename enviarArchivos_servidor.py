import socket
import os
import threading

def send_file(connection, dest_folder):
    try:
        filename = connection.recv(1024).decode('utf-8')
        connection.send('ACK_FILENAME'.encode('utf-8'))
        
        filesize = connection.recv(1024).decode('utf-8')
        if not filesize.isdigit():
            print(f'Error: Tamaño del archivo no es un número válido: {filesize}')
            return
        filesize = int(filesize)
        connection.send('ACK_FILESIZE'.encode('utf-8'))
        
        filepath = os.path.join(dest_folder, os.path.basename(filename))
        
        with open(filepath, "wb") as f:
            bytes_received = 0
            while bytes_received < filesize:
                bytes_read = connection.recv(4096)
                if not bytes_read:
                    break
                f.write(bytes_read)
                bytes_received += len(bytes_read)
                print(f'Bytes recibidos: {bytes_received}/{filesize}')
        
        print(f'Archivo {filename} recibido correctamente y guardado en {filepath}')
    except Exception as e:
        print(f"Error al recibir el archivo: {e}")

def receive_file(connection, dest_folder):
    try:
        filename = connection.recv(1024).decode('utf-8')
        filepath = os.path.join(dest_folder, filename)
        
        if not os.path.isfile(filepath):
            print(f"El archivo '{filepath}' no existe.")
            connection.send('ERROR: Archivo no existe'.encode('utf-8'))
            return
        
        filesize = os.path.getsize(filepath)
        connection.send(os.path.basename(filepath).encode('utf-8'))
        ack = connection.recv(1024).decode('utf-8')
        if ack != 'ACK_FILENAME':
            print(f'Error al recibir el acuse de recibo del nombre del archivo. Recibido: {ack}')
            return
        
        connection.send(str(filesize).encode('utf-8'))
        ack = connection.recv(1024).decode('utf-8')
        if ack != 'ACK_FILESIZE':
            print(f'Error al recibir el acuse de recibo del tamaño del archivo. Recibido: {ack}')
            return
        
        with open(filepath, "rb") as f:
            bytes_sent = 0
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                connection.sendall(bytes_read)
                bytes_sent += len(bytes_read)
                print(f'Bytes enviados: {bytes_sent}/{filesize}')
        
        print(f'Archivo {filename} enviado correctamente')
    except Exception as e:
        print(f"Error al enviar el archivo: {e}")

def handle_client(client_socket, dest_folder):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if data == 'SEND':
                send_file(client_socket, dest_folder)
            elif data == 'RECEIVE':
                receive_file(client_socket, dest_folder)
            elif data == 'CLOSE':
                break
    except Exception as e:
        print(f"Error en handle_client: {e}")
    finally:
        client_socket.close()

def start_server(host='0.0.0.0', port=44444, dest_folder='/Users/alexandermc/compu/doc/ciberseguridad/proyrcto/archivos_recibidos'):
    try:
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            print(f"Directorio '{dest_folder}' creado correctamente.")
        else:
            print(f"Usando directorio existente: '{dest_folder}'")
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f'Servidor escuchando en {host}:{port}')
        
        while True:
            print("\nEsperando conexiones...")
            client_socket, addr = server_socket.accept()
            print(f'Conexión desde {addr}')
            
            threading.Thread(target=handle_client, args=(client_socket, dest_folder)).start()
    
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

def connect_action():
    threading.Thread(target=start_server).start()

if __name__ == "__main__":
    connect_action()
