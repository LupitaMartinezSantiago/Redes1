import tkinter as tk
from tkinter import messagebox
import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando el comando: {e.stderr.decode()}")

def check_rule_exists(command):
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def allow_ping(ips):
    for ip in ips:
      
        check_command = f"sudo iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
        if check_rule_exists(check_command):
           
            command = f"sudo iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
            run_command(command)
        
       
        command = f"sudo iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
        run_command(command)
        print(f"Ping permitido desde la IP {ip}")

def deny_ping(ips):
    for ip in ips:
        # Verificar si la regla de aceptación existe
        check_command = f"sudo iptables -C INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
        if check_rule_exists(check_command):
            # Eliminar la regla de aceptación si existe
            command = f"sudo iptables -D INPUT -p icmp --icmp-type echo-request -s {ip} -j ACCEPT"
            run_command(command)
        
        # Agregar la regla de denegación
        command = f"sudo iptables -I INPUT -p icmp --icmp-type echo-request -s {ip} -j DROP"
        run_command(command)
        print(f"Ping denegado desde la IP {ip}")

def execute_action(action):
    if action == 'permitir':
        allow_ping(ips)
        messagebox.showinfo("Acción completada", "Ping permitido desde las IPs especificadas.")
    elif action == 'denegar':
        deny_ping(ips)
        messagebox.showinfo("Acción completada", "Ping denegado desde las IPs especificadas.")
    else:
        messagebox.showerror("Error", "Acción no válida.")

# Direcciones IP predeterminadas
ips = ['0.0.0.0']

# Crear la interfaz gráfica
root = tk.Tk()
root.title("PINGS")
root.geometry("400x200")

action_label = tk.Label(root, text="¿Quieres permitir o denegar el ping?")
action_label.pack(pady=10)

action_variable = tk.StringVar(root)
action_variable.set("Seleccione la accion")  # Valor por defecto

action_menu = tk.OptionMenu(root, action_variable, "permitir", "denegar")
action_menu.pack(pady=10)

execute_button = tk.Button(root, text="Ejecutar", command=lambda: execute_action(action_variable.get()))
execute_button.pack(pady=10)

root.mainloop()
