import sys

# 🔒 Proteção: impede execução direta
if len(sys.argv) < 2 or sys.argv[1] != "autenticado":
    print("⚠️ Acesso negado. Execute via tela_login.py.")
    sys.exit()

import tkinter as tk
import json
from tkinter import ttk
from ttkbootstrap import Style
from banco import criar_tabelas
from produtos import carregar_tela_produtos

# Cria tabelas no banco (caso ainda não existam)
criar_tabelas()

# Tema
style = Style("darkly")
root = style.master
root.title("Sistema de Controle de Estoque")
root.geometry("1200x700")
root.resizable(False, False)


# Saudação
try:
    with open("usuario_logado.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
        nome_usuario = dados.get("nome", "Usuário")
except:
    nome_usuario = "Usuário"

label_saudacao = ttk.Label(root, text=f"👋 Bem-vindo, {nome_usuario}!", font=("Segoe UI", 14, "bold"), anchor="center")
label_saudacao.pack(pady=10)


# Layout principal
frame_lateral = ttk.Frame(root, width=180, padding=10)
frame_lateral.pack(side="left", fill="y")

frame_conteudo = ttk.Frame(root, padding=10)
frame_conteudo.pack(side="right", fill="both", expand=True)

# Botões do menu lateral
ttk.Label(frame_lateral, text="Menu", font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))

def mostrar_tela_produtos():
    carregar_tela_produtos(frame_conteudo)

def mostrar_tela_movimentacoes():
    from movimentacoes import carregar_tela_movimentacoes
    carregar_tela_movimentacoes(frame_conteudo)

def mostrar_tela_usuarios():
    from usuarios import carregar_tela_usuarios
    carregar_tela_usuarios(frame_conteudo)

ttk.Button(frame_lateral, text="🛒 Produtos", width=20, command=mostrar_tela_produtos).pack(pady=5)
ttk.Button(frame_lateral, text="🔁 Movimentações", width=20, command=mostrar_tela_movimentacoes).pack(pady=5)
ttk.Button(frame_lateral, text="👤 Usuários", width=20, command=mostrar_tela_usuarios).pack(pady=5)

# Tela padrão ao iniciar
mostrar_tela_produtos()

root.mainloop()
