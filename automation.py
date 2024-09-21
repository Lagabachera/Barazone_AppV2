import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Función para ejecutar comandos en el shell
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return stderr.decode('utf-8')
    else:
        return stdout.decode('utf-8')

# Función para actualizar dependencias
def update_dependencies():
    output = run_command("pip install -r requirements.txt")
    messagebox.showinfo("Resultado", output)

# Función para ejecutar migraciones
def make_migrations():
    output = run_command("python manage.py makemigrations")
    output += run_command("python manage.py migrate")
    messagebox.showinfo("Resultado", output)

# Función para recopilar archivos estáticos (solo producción)
def collect_static():
    output = run_command("python manage.py collectstatic --noinput")
    messagebox.showinfo("Resultado", output)

# Función para hacer un commit y push a GitHub
def git_commit_and_push():
    commit_message = commit_entry.get()
    if not commit_message:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un mensaje de commit")
        return
    
    output = run_command("git add .")
    output += run_command(f'git commit -m "{commit_message}"')
    output += run_command("git push")
    messagebox.showinfo("Resultado", output)

# Función para reiniciar el servidor (solo en producción)
def restart_server():
    output = run_command("sudo systemctl restart gunicorn")
    messagebox.showinfo("Resultado", output)

# Función para mostrar logs
def show_logs():
    logs_output.delete(1.0, tk.END)
    logs = run_command("tail -n 20 /var/log/gunicorn/error.log")
    logs_output.insert(tk.END, logs)

# Función principal para ejecutar las acciones
def main():
    root = tk.Tk()
    root.title("Automatización de Proyecto Django")

    # Título de la ventana
    tk.Label(root, text="Automatización de Proyecto Django", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Botón para actualizar dependencias
    tk.Button(root, text="Actualizar Dependencias", command=update_dependencies, width=25).grid(row=1, column=0, padx=10, pady=5)

    # Botón para hacer migraciones
    tk.Button(root, text="Hacer Migraciones", command=make_migrations, width=25).grid(row=2, column=0, padx=10, pady=5)

    # Botón para recopilar archivos estáticos (producción)
    tk.Button(root, text="Recopilar Archivos Estáticos", command=collect_static, width=25).grid(row=3, column=0, padx=10, pady=5)

    # Entrada y botón para commit y push a GitHub
    tk.Label(root, text="Mensaje de Commit:").grid(row=4, column=0, padx=10, pady=5)
    global commit_entry
    commit_entry = tk.Entry(root, width=30)
    commit_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(root, text="Hacer Commit & Push", command=git_commit_and_push, width=25).grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    # Botón para reiniciar el servidor (producción)
    tk.Button(root, text="Reiniciar Servidor (Producción)", command=restart_server, width=25).grid(row=6, column=0, columnspan=2, padx=10, pady=5)

    # Botón para mostrar logs del servidor
    tk.Button(root, text="Mostrar Logs", command=show_logs, width=25).grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    # Sección para mostrar los logs en tiempo real
    global logs_output
    logs_output = scrolledtext.ScrolledText(root, width=60, height=10)
    logs_output.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    # Ejecuta la interfaz
    root.mainloop()

if __name__ == "__main__":
    main()
