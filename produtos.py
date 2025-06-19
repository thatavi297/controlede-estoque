import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

def carregar_tela_produtos(frame_pai):
    for widget in frame_pai.winfo_children():
        widget.destroy()

    entry_nome = ttk.Entry(frame_pai)
    entry_nome.grid(row=0, column=0, padx=5, pady=5)
    entry_nome.insert(0, "Nome")

    entry_desc = ttk.Entry(frame_pai)
    entry_desc.grid(row=0, column=1, padx=5, pady=5)
    entry_desc.insert(0, "Descrição")

    entry_qtd = ttk.Entry(frame_pai)
    entry_qtd.grid(row=0, column=2, padx=5, pady=5)
    entry_qtd.insert(0, "Qtd")

    entry_preco = ttk.Entry(frame_pai)
    entry_preco.grid(row=0, column=3, padx=5, pady=5)
    entry_preco.insert(0, "Preço")

    produto_selecionado_id = tk.StringVar()

    def atualizar_tabela():
        for i in tree.get_children():
            tree.delete(i)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def limpar():
        entry_nome.delete(0, tk.END)
        entry_desc.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        produto_selecionado_id.set("")

    def adicionar():
        try:
            nome = entry_nome.get()
            desc = entry_desc.get()
            qtd = int(entry_qtd.get())
            preco = float(entry_preco.get())
        except ValueError:
            messagebox.showerror("Erro", "Campos numéricos inválidos.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, descricao, quantidade, preco) VALUES (?, ?, ?, ?)",
                       (nome, desc, qtd, preco))
        conn.commit()
        conn.close()
        atualizar_tabela()
        limpar()

    def remover():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um item.")
            return
        produto_id = tree.item(item)["values"][0]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
        conn.commit()
        conn.close()
        atualizar_tabela()
        limpar()

    def editar():
        if not produto_selecionado_id.get():
            messagebox.showwarning("Atenção", "Selecione um produto para editar.")
            return
        try:
            nome = entry_nome.get()
            desc = entry_desc.get()
            qtd = int(entry_qtd.get())
            preco = float(entry_preco.get())
        except ValueError:
            messagebox.showerror("Erro", "Campos numéricos inválidos.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE produtos SET nome=?, descricao=?, quantidade=?, preco=? WHERE id=?
        """, (nome, desc, qtd, preco, int(produto_selecionado_id.get())))
        conn.commit()
        conn.close()
        atualizar_tabela()
        limpar()

    def ao_selecionar(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            produto_selecionado_id.set(valores[0])
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, valores[1])
            entry_desc.delete(0, tk.END)
            entry_desc.insert(0, valores[2])
            entry_qtd.delete(0, tk.END)
            entry_qtd.insert(0, valores[3])
            entry_preco.delete(0, tk.END)
            entry_preco.insert(0, valores[4])

    ttk.Button(frame_pai, text="➕ Adicionar", command=adicionar).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(frame_pai, text="✏️ Editar", command=editar).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(frame_pai, text="🗑️ Remover", command=remover).grid(row=1, column=2, padx=5, pady=5)

    tree = ttk.Treeview(frame_pai, columns=("ID", "Nome", "Descrição", "Qtd", "Preço"), show="headings")
    for col in ("ID", "Nome", "Descrição", "Qtd", "Preço"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)
    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    frame_pai.rowconfigure(2, weight=1)
    frame_pai.columnconfigure(3, weight=1)

    atualizar_tabela()
