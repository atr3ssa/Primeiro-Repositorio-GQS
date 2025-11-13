import json
from sistema.livro import Livro
from sistema.usuario import Usuario
from sistema.emprestimo import Emprestimo


class Biblioteca:
    def __init__(self, arquivo_dados='biblioteca.json'):
        self.livros = []
        self.usuarios = []
        self.emprestimos = []
        self.arquivo = arquivo_dados
        self.contador_livros = 1
        self.contador_usuarios = 1

    # -------------------- LIVROS --------------------
    def adicionar_livro(self, titulo, autor, isbn, ano):
        if not titulo or not autor or not isbn:
            print("Erro: campos obrigatórios")
            return False

        if any(l.isbn == isbn for l in self.livros):
            print("Livro já existe")
            return False

        if len(isbn) not in (10, 13):
            print("ISBN inválido")
            return False

        novo_livro = Livro(self.contador_livros, titulo, autor, isbn, ano)
        self.livros.append(novo_livro)
        self.contador_livros += 1
        self.salvar_dados()
        print("Livro adicionado com sucesso.")
        return True

    # -------------------- USUÁRIOS --------------------
    def cadastrar_usuario(self, nome, email, telefone):
        if not nome or '@' not in email:
            print("Nome ou email inválido")
            return False

        if any(u.email == email for u in self.usuarios):
            print("Email já cadastrado")
            return False

        novo_usuario = Usuario(self.contador_usuarios, nome, email, telefone)
        self.usuarios.append(novo_usuario)
        self.contador_usuarios += 1
        self.salvar_dados()
        print("Usuário cadastrado com sucesso.")
        return True

    # -------------------- EMPRÉSTIMOS --------------------
    def realizar_emprestimo(self, usuario_id, livro_id):
        usuario = next((u for u in self.usuarios if u.id == usuario_id), None)
        livro = next((l for l in self.livros if l.id == livro_id), None)

        if not usuario:
            print("Usuário não encontrado.")
            return False
        if not livro:
            print("Livro não encontrado.")
            return False
        if not livro.disponivel:
            print("Livro não disponível.")
            return False

        novo_emp = Emprestimo(len(self.emprestimos) + 1, usuario_id, livro_id)
        livro.marcar_como_emprestado()
        self.emprestimos.append(novo_emp)
        self.salvar_dados()
        print("Empréstimo realizado com sucesso.")
        return True

    def devolver_livro(self, emprestimo_id):
        emprestimo = next((e for e in self.emprestimos if e.id == emprestimo_id), None)
        if not emprestimo:
            print("Empréstimo não encontrado.")
            return False
        if emprestimo.devolvido:
            print("Livro já devolvido.")
            return False

        livro = next((l for l in self.livros if l.id == emprestimo.livro_id), None)
        if livro:
            livro.marcar_como_disponivel()

        emprestimo.devolver()
        self.salvar_dados()
        print("Livro devolvido com sucesso.")
        return True

    # -------------------- PERSISTÊNCIA --------------------
    def salvar_dados(self):
        dados = {
            'livros': [vars(l) for l in self.livros],
            'usuarios': [vars(u) for u in self.usuarios],
            'emprestimos': [vars(e) for e in self.emprestimos],
            'contador_livros': self.contador_livros,
            'contador_usuarios': self.contador_usuarios
        }
        with open(self.arquivo, 'w') as f:
            json.dump(dados, f, indent=2)

    def carregar_dados(self):
        try:
            with open(self.arquivo, 'r') as f:
                dados = json.load(f)
                self.livros = [Livro(**l) for l in dados['livros']]
                self.usuarios = [Usuario(**u) for u in dados['usuarios']]
                self.emprestimos = [Emprestimo(**e) for e in dados['emprestimos']]
                self.contador_livros = dados['contador_livros']
                self.contador_usuarios = dados['contador_usuarios']
            print("Dados carregados com sucesso.")
        except FileNotFoundError:
            print("Nenhum arquivo encontrado, iniciando novo sistema.")

    # -------------------- LISTAGENS --------------------
    def listar_livros(self):
        for livro in self.livros:
            print(livro)

    def listar_usuarios(self):
        for usuario in self.usuarios:
            print(usuario)

    def listar_emprestimos(self):
        for emp in self.emprestimos:
            print(emp)