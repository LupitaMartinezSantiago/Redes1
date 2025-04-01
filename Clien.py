import subprocess

def abrir_cliente_nomachine(host):
    """
    Abre el cliente gráfico de NoMachine para conectarse al servidor remoto.
    """
    try:
        print(f"Abriendo cliente NoMachine para conectar a {host}...")
        
        subprocess.run(["/usr/NX/bin/nxplayer", "--session", f"nx://{host}"])
    except FileNotFoundError:
        print("Error: Asegúrate de tener instalado el cliente NoMachine en tu máquina local.")
    except Exception as e:
        print(f"Error: {e}")


abrir_cliente_nomachine("0.0.0.0")
