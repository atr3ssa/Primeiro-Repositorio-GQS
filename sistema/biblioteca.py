import json
from sistema.livro import Livro
from sistema.usuario import Usuario
from sistema.emprestimo import Emprestimo


class Biblioteca:
    def __init__(self, arquivo_dados='biblioteca.json'):
        self._livros_obj = []
        self._usuarios_obj = []
        self._emprestimos_obj = []
        self.arquivo = arquivo_dados
        self.contador_livros = 1
        self.contador_usuarios = 1

        import re

    # ---------- VALIDAÇÕES ----------
    def _isbn_valido(self, isbn):
        return isbn.isdigit() and len(isbn) in (10, 13)

    def _email_valido(self, email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None


    # ---------- LIVROS ----------
    def adicionar_livro(self, titulo, autor, isbn, ano):
        if not self._isbn_valido(isbn):
            return False
        
        novo_livro = Livro(self.contador_livros, titulo, autor, isbn, ano)
        self._livros_obj.append(novo_livro)
        self.contador_livros += 1
        self.salvar_dados()
        return True


    # ---------- USUÁRIOS ----------
    def cadastrar_usuario(self, nome, email, telefone):
        if not self._email_valido(email):
            return False

        novo_usuario = Usuario(self.contador_usuarios, nome, email, telefone)
        self._usuarios_obj.append(novo_usuario)
        self.contador_usuarios += 1
        self.salvar_dados()
        return True


    # ---------- EMPRÉSTIMOS ----------
    def realizar_emprestimo(self, livro_id, usuario_id):
        usuario = next((u for u in self._usuarios_obj if u.id == usuario_id), None)
        livro = next((l for l in self._livros_obj if l.id == livro_id), None)

        if not usuario or not livro or not livro.disponivel:
            return False

        emprestimo = Emprestimo(len(self._emprestimos_obj) + 1, usuario_id, livro_id)
        livro.disponivel = False
        self._emprestimos_obj.append(emprestimo)
        self.salvar_dados()
        return True

    def devolver_livro(self, emprestimo_id):
        emprestimo = next((e for e in self._emprestimos_obj if e.id == emprestimo_id), None)
        if not emprestimo or emprestimo.devolvido:
            return False

        livro = next((l for l in self._livros_obj if l.id == emprestimo.livro_id), None)
        if livro:
            livro.disponivel = True

        emprestimo.devolver()
        self.salvar_dados()
        return True

    # ---------- PERSISTÊNCIA ----------
    def salvar_dados(self):
        dados = {
            'livros': [vars(l) for l in self._livros_obj],
            'usuarios': [vars(u) for u in self._usuarios_obj],
            'emprestimos': [vars(e) for e in self._emprestimos_obj],
            'contador_livros': self.contador_livros,
            'contador_usuarios': self.contador_usuarios
        }
        with open(self.arquivo, 'w') as f:
            json.dump(dados, f, indent=2)

    def carregar_dados(self):
        try:
            with open(self.arquivo, 'r') as f:
                dados = json.load(f)

                self._livros_obj = [
                    Livro(
                        l['id'], l['titulo'], l['autor'],
                        l['isbn'], l['ano']
                    ) for l in dados['livros']
                ]

                self._usuarios_obj = [
                    Usuario(
                        u['id'], u['nome'],
                        u['email'], u['telefone']
                    ) for u in dados['usuarios']
                ]

                self._emprestimos_obj = [
                    Emprestimo(
                        e['id'], e['usuario_id'],
                        e['livro_id'], e['devolvido']
                    ) for e in dados['emprestimos']
                ]

                self.contador_livros = dados['contador_livros']
                self.contador_usuarios = dados['contador_usuarios']

        except FileNotFoundError:
            pass
