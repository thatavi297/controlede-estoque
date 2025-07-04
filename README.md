📘 README.txt — Sistema de Controle de Estoque

✅ Descrição
Este é um sistema de controle de estoque simples, funcional e protegido por login. Ele permite:

- Gerenciar produtos
- Registrar movimentações de entrada/saída
- Cadastrar/remover usuários
- Tudo dentro de uma única janela com interface moderna (azul escuro)

🧩 Estrutura dos Arquivos

controle_estoque/

├── banco.py                  - Conexão e criação do banco de dados (SQLite)

├── tela_login.py             - Tela de login (ponto de entrada do sistema)

├── main.py                   - Interface principal com menu lateral

├── produtos.py               - Tela de gerenciamento de produtos

├── movimentacoes.py          - Tela de movimentações de estoque

├── usuarios.py               - Tela de gerenciamento de usuários

├── estoque.db                - Banco de dados gerado automaticamente

🔑 Acesso Padrão

- Login: admin
- Senha: 123

🚀 Como executar

1. Instale o pacote de interface moderna:
   pip install ttkbootstrap

2. Execute o sistema sempre por este comando:
   python tela_login.py

⚠️ Não execute main.py, produtos.py, etc. diretamente.
Eles são protegidos contra acesso sem login.

💬 Observações

- O sistema cria automaticamente o banco estoque.db na primeira execução.
- Ao editar ou remover produtos, o estoque será atualizado corretamente.
- Movimentações não permitem saída com quantidade maior que o disponível.
