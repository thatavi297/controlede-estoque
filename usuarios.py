import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

def carregar_tela_usuarios(frame_pai):
    for widget in frame_pai.winfo_children():
        widget.destroy()

    # Título
    ttk.Label(frame_pai, text="Gerenciar Usuários", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

    # Campos
    entry_nome = ttk.Entry(frame_pai)
    entry_nome.insert(0, "Nome")
    entry_nome.grid(row=1, column=0, padx=5, pady=5)

    entry_login = ttk.Entry(frame_pai)
    entry_login.insert(0, "Login")
    entry_login.grid(row=1, column=1, padx=5, pady=5)

    entry_senha = ttk.Entry(frame_pai, show="*")
    entry_senha.insert(0, "Senha")
    entry_senha.grid(row=1, column=2, padx=5, pady=5)

    combo_nivel = ttk.Combobox(frame_pai, values=["Administrador", "Comum"], state="readonly")
    combo_nivel.set("Nível")
    combo_nivel.grid(row=1, column=3, padx=5, pady=5)

    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, login, senha, nivel FROM usuarios")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def limpar():
        entry_nome.delete(0, tk.END)
        entry_login.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
        combo_nivel.set("Nível")

    def adicionar():
        nome = entry_nome.get()
        login = entry_login.get()
        senha = entry_senha.get()
        nivel = combo_nivel.get()

        if not nome or not login or not senha or not nivel:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, login, senha, nivel) VALUES (?, ?, ?, ?)",
                           (nome, login, senha, nivel))
            conn.commit()
            conn.close()
            atualizar_tabela()
            limpar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir: {e}")

    def remover():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um usuário para remover.")
            return
        usuario_id = tree.item(item)["values"][0]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()
        atualizar_tabela()

    ttk.Button(frame_pai, text="➕ Adicionar", command=adicionar).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(frame_pai, text="🗑️ Remover", command=remover).grid(row=2, column=1, padx=5, pady=5)

    # Tabela
    tree = ttk.Treeview(frame_pai, columns=("ID", "Nome", "Login", "Senha", "Nível"), show="headings")
    for col in ("ID", "Nome", "Login", "Senha", "Nível"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=3, column=0, columnspan=4, pady=10, sticky="nsew")

    frame_pai.rowconfigure(3, weight=1)
    frame_pai.columnconfigure(3, weight=1)

    atualizar_tabela()
