import tkinter as tk
from tkinter import ttk, messagebox
from banco import conectar

def carregar_tela_movimentacoes(frame_pai):
    for widget in frame_pai.winfo_children():
        widget.destroy()

    # Campos de entrada
    label_info = ttk.Label(frame_pai, text="Registrar Movimentação", font=("Segoe UI", 14, "bold"))
    label_info.grid(row=0, column=0, columnspan=4, pady=10)

    combo_produto = ttk.Combobox(frame_pai, state="readonly")
    combo_produto.grid(row=1, column=0, padx=5, pady=5)

    combo_tipo = ttk.Combobox(frame_pai, values=["Entrada", "Saída"], state="readonly")
    combo_tipo.set("Tipo")
    combo_tipo.grid(row=1, column=1, padx=5, pady=5)

    entry_qtd = ttk.Entry(frame_pai)
    entry_qtd.insert(0, "Quantidade")
    entry_qtd.grid(row=1, column=2, padx=5, pady=5)

    entry_obs = ttk.Entry(frame_pai)
    entry_obs.insert(0, "Observação")
    entry_obs.grid(row=1, column=3, padx=5, pady=5)

    def atualizar_combo():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM produtos")
        produtos = cursor.fetchall()
        conn.close()
        combo_produto['values'] = [f"{id} - {nome}" for id, nome in produtos]

    def registrar():
        try:
            produto_id = int(combo_produto.get().split(" - ")[0])
            tipo = combo_tipo.get()
            qtd = int(entry_qtd.get())
            obs = entry_obs.get()
        except Exception:
            messagebox.showerror("Erro", "Preencha os campos corretamente.")
            return

        if tipo not in ["Entrada", "Saída"]:
            messagebox.showerror("Erro", "Tipo inválido.")
            return

        conn = conectar()
        cursor = conn.cursor()

        # Atualiza estoque
        cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto_id,))
        atual = cursor.fetchone()
        if atual is None:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        nova_qtd = atual[0] + qtd if tipo == "Entrada" else atual[0] - qtd
        if nova_qtd < 0:
            messagebox.showwarning("Estoque insuficiente", "Quantidade insuficiente para saída.")
            return

        cursor.execute("UPDATE produtos SET quantidade=? WHERE id=?", (nova_qtd, produto_id))
        cursor.execute("""
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
            VALUES (?, ?, ?, ?)
        """, (produto_id, tipo, qtd, obs))
        conn.commit()
        conn.close()
        atualizar_tabela()
        limpar()

    def limpar():
        combo_tipo.set("Tipo")
        entry_qtd.delete(0, tk.END)
        entry_obs.delete(0, tk.END)

    def atualizar_tabela():
        for i in tree.get_children():
            tree.delete(i)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, p.nome, m.tipo, m.quantidade, m.observacao, m.data
            FROM movimentacoes m
            JOIN produtos p ON p.id = m.produto_id
            ORDER BY m.data DESC
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    ttk.Button(frame_pai, text="➕ Registrar", command=registrar).grid(row=1, column=4, padx=5, pady=5)

    # Tabela
    tree = ttk.Treeview(frame_pai, columns=("ID", "Produto", "Tipo", "Qtd", "Obs", "Data"), show="headings")
    for col in ("ID", "Produto", "Tipo", "Qtd", "Obs", "Data"):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=2, column=0, columnspan=5, pady=10, sticky="nsew")

    frame_pai.rowconfigure(2, weight=1)
    frame_pai.columnconfigure(4, weight=1)

    atualizar_combo()
    atualizar_tabela()
