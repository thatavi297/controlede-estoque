import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from banco import conectar, criar_tabelas
import subprocess
import sys
import json

# Inicializa banco
criar_tabelas()

def autenticar():
    login = entry_usuario.get()
    senha = entry_senha.get()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios WHERE login=? AND senha=?", (login, senha))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nome = resultado[0]
        with open("usuario_logado.json", "w", encoding="utf-8") as f:
            json.dump({"nome": nome}, f)
        root.destroy()
        subprocess.run([sys.executable, "main.py", "autenticado"])
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# Interface
style = Style("darkly")
root = style.master
root.title("Login - Controle de Estoque")
root.geometry("600x400")
root.resizable(False, False)

frame = ttk.Frame(root, padding=30)
frame.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(frame, text="Usuário:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=10)
entry_usuario = ttk.Entry(frame, font=("Segoe UI", 12), width=30)
entry_usuario.grid(row=0, column=1)

ttk.Label(frame, text="Senha:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", pady=10)
entry_senha = ttk.Entry(frame, show="*", font=("Segoe UI", 12), width=30)
entry_senha.grid(row=1, column=1)

ttk.Button(frame, text="Entrar", command=autenticar).grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()