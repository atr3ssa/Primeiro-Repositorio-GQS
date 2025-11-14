"""
Sistema de Biblioteca
Implementação seguindo princípios de Clean Code e Orientação a Objetos
"""

import json
import os
from datetime import datetime
from typing import List, Optional


class Livro:
    """Representa um livro no sistema da biblioteca."""
    
    contador_id = 0
    
    def __init__(self, titulo: str, autor: str, isbn: str, ano: int, id: Optional[int] = None):
        if id is not None:
            self.id = int(id)
            if self.id > Livro.contador_id:
                Livro.contador_id = self.id
        else:
            Livro.contador_id += 1
            self.id = Livro.contador_id
        
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano = ano
        self.disponivel = True
    
    def emprestar(self) -> None:
        """Marca o livro como emprestado."""
        self.disponivel = False
    
    def devolver(self) -> None:
        """Marca o livro como disponível."""
        self.disponivel = True
    
    def to_dict(self) -> dict:
        """Converte o livro para dicionário."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'ano': self.ano,
            'disponivel': self.disponivel
        }
    
    def __str__(self) -> str:
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"[{self.id}] {self.titulo} - {self.autor} ({self.ano}) | {status}"
    
    @classmethod
    def resetar_contador(cls) -> None:
        """Reseta o contador de IDs (útil para testes)."""
        cls.contador_id = 0


class Usuario:
    """Representa um usuário da biblioteca."""
    
    contador_id = 0
    
    def __init__(self, nome: str, email: str, telefone: str, id: Optional[int] = None):
        if id is not None:
            self.id = int(id)
            if self.id > Usuario.contador_id:
                Usuario.contador_id = self.id
        else:
            Usuario.contador_id += 1
            self.id = Usuario.contador_id
        
        self.nome = nome
        self.email = email
        self.telefone = telefone
    
    def to_dict(self) -> dict:
        """Converte o usuário para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone
        }
    
    def __str__(self) -> str:
        return f"[{self.id}] {self.nome} - {self.email} - {self.telefone}"
    
    @classmethod
    def resetar_contador(cls) -> None:
        """Reseta o contador de IDs (útil para testes)."""
        cls.contador_id = 0


class Emprestimo:
    """Representa um empréstimo de livro."""
    
    contador_id = 0
    
    def __init__(self, usuario_id: int, livro_id: int, id: Optional[int] = None):
        if id is not None:
            self.id = int(id)
            if self.id > Emprestimo.contador_id:
                Emprestimo.contador_id = self.id
        else:
            Emprestimo.contador_id += 1
            self.id = Emprestimo.contador_id
        
        self.usuario_id = int(usuario_id)
        self.livro_id = int(livro_id)
        self.devolvido = False
        self.data_emprestimo = datetime.now().isoformat()
        self.data_devolucao = None
    
    def realizar_devolucao(self) -> None:
        """Marca o empréstimo como devolvido."""
        self.devolvido = True
        self.data_devolucao = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Converte o empréstimo para dicionário."""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'livro_id': self.livro_id,
            'devolvido': self.devolvido,
            'data_emprestimo': self.data_emprestimo,
            'data_devolucao': self.data_devolucao
        }
    
    @classmethod
    def resetar_contador(cls) -> None:
        """Reseta o contador de IDs (útil para testes)."""
        cls.contador_id = 0


class Biblioteca:
    """Sistema de gerenciamento de biblioteca."""
    
    # Atributos de classe para compatibilidade com testes estáticos
    livros: List[dict] = []
    usuarios: List[dict] = []
    emprestimos: List[dict] = []
    contador_livros: int = 1
    contador_usuarios: int = 1
    
    def __init__(self, arquivo_dados: str = 'biblioteca.json'):
        self.arquivo = arquivo_dados
        self._livros_obj: List[Livro] = []
        self._usuarios_obj: List[Usuario] = []
        self._emprestimos_obj: List[Emprestimo] = []
        
        # Resetar contadores ao criar nova instância
        Livro.resetar_contador()
        Usuario.resetar_contador()
        Emprestimo.resetar_contador()
    
    # ==================== MÉTODOS ESTÁTICOS (para testes antigos) ====================
    
    @staticmethod
    def adicionarLivro(titulo: str, autor: str, isbn: str, ano: int) -> bool:
        """Adiciona um livro usando método estático."""
        if not titulo or not autor or not isbn:
            return False
        
        if len(isbn) not in [10, 13]:
            return False
        
        for livro in Biblioteca.livros:
            if livro['isbn'] == isbn:
                return False
        
        livro = {
            'id': Biblioteca.contador_livros,
            'titulo': titulo,
            'autor': autor,
            'isbn': isbn,
            'ano': ano,
            'disponivel': True
        }
        
        Biblioteca.livros.append(livro)
        Biblioteca.contador_livros += 1
        return True
    
    @staticmethod
    def cadastrarUsuario(nome: str, email: str, telefone: str) -> bool:
        """Cadastra um usuário usando método estático."""
        if not nome or '@' not in email:
            return False
        
        for usuario in Biblioteca.usuarios:
            if usuario['email'] == email:
                return False
        
        usuario = {
            'id': Biblioteca.contador_usuarios,
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'ativo': True
        }
        
        Biblioteca.usuarios.append(usuario)
        Biblioteca.contador_usuarios += 1
        return True
    
    @staticmethod
    def realizarEmprestimo(usuario_id: int, livro_id: int) -> bool:
        """Realiza um empréstimo usando método estático."""
        usuario = None
        livro = None
        
        for u in Biblioteca.usuarios:
            if u['id'] == usuario_id:
                usuario = u
                break
        
        if not usuario:
            return False
        
        for l in Biblioteca.livros:
            if l['id'] == livro_id:
                livro = l
                break
        
        if not livro:
            return False
        
        if not livro['disponivel']:
            return False
        
        emprestimo = {
            'id': len(Biblioteca.emprestimos) + 1,
            'usuario_id': usuario_id,
            'livro_id': livro_id,
            'devolvido': False,
            'data_emprestimo': datetime.now().isoformat()
        }
        
        Biblioteca.emprestimos.append(emprestimo)
        livro['disponivel'] = False
        return True
    
    @staticmethod
    def devolverLivro(emprestimo_id: int) -> bool:
        """Devolve um livro usando método estático."""
        emprestimo = None
        
        for emp in Biblioteca.emprestimos:
            if emp['id'] == emprestimo_id:
                emprestimo = emp
                break
        
        if not emprestimo:
            return False
        
        if emprestimo['devolvido']:
            return False
        
        for livro in Biblioteca.livros:
            if livro['id'] == emprestimo['livro_id']:
                livro['disponivel'] = True
                break
        
        emprestimo['devolvido'] = True
        return True
    
    @staticmethod
    def salvarDados() -> None:
        """Salva dados usando método estático."""
        dados = {
            'livros': Biblioteca.livros,
            'usuarios': Biblioteca.usuarios,
            'emprestimos': Biblioteca.emprestimos,
            'contador_livros': Biblioteca.contador_livros,
            'contador_usuarios': Biblioteca.contador_usuarios
        }
        with open('biblioteca.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def carregarDados() -> None:
        """Carrega dados usando método estático."""
        if not os.path.exists('biblioteca.json'):
            return
        
        with open('biblioteca.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            Biblioteca.livros = dados.get('livros', [])
            Biblioteca.usuarios = dados.get('usuarios', [])
            Biblioteca.emprestimos = dados.get('emprestimos', [])
            Biblioteca.contador_livros = dados.get('contador_livros', 1)
            Biblioteca.contador_usuarios = dados.get('contador_usuarios', 1)
    
    # ==================== MÉTODOS DE INSTÂNCIA (POO) ====================
    
    def _validar_livro(self, titulo: str, autor: str, isbn: str) -> bool:
        """Valida os dados de um livro."""
        if not titulo or not titulo.strip():
            return False
        if not autor or not autor.strip():
            return False
        if not isbn or not isbn.strip():
            return False
        if len(isbn) not in [10, 13]:
            return False
        return True
    
    def _isbn_ja_existe(self, isbn: str) -> bool:
        """Verifica se o ISBN já está cadastrado."""
        return any(livro.isbn == isbn for livro in self._livros_obj)
    
    def _validar_usuario(self, nome: str, email: str) -> bool:
        """Valida os dados de um usuário."""
        if not nome or not nome.strip():
            return False
        if not email or '@' not in email:
            return False
        return True
    
    def _email_ja_existe(self, email: str) -> bool:
        """Verifica se o email já está cadastrado."""
        return any(usuario.email == email for usuario in self._usuarios_obj)
    
    def adicionar_livro(self, titulo: str, autor: str, isbn: str, ano: int) -> bool:
        """Adiciona um novo livro à biblioteca."""
        if not self._validar_livro(titulo, autor, isbn):
            return False
        
        if self._isbn_ja_existe(isbn):
            return False
        
        livro = Livro(titulo, autor, isbn, ano)
        self._livros_obj.append(livro)
        self._salvar_dados()
        return True
    
    def buscar_livro_por_id(self, livro_id: int) -> Optional[Livro]:
        """Busca um livro pelo ID."""
        livro_id = int(livro_id)
        for livro in self._livros_obj:
            if livro.id == livro_id:
                return livro
        return None
    
    def listar_livros(self) -> None:
        """Lista todos os livros cadastrados."""
        if not self._livros_obj:
            print("Nenhum livro cadastrado.")
            return
        
        print("\n=== LIVROS CADASTRADOS ===")
        for livro in self._livros_obj:
            print(livro)
        print()
    
    def cadastrar_usuario(self, nome: str, email: str, telefone: str) -> bool:
        """Cadastra um novo usuário na biblioteca."""
        if not self._validar_usuario(nome, email):
            return False
        
        if self._email_ja_existe(email):
            return False
        
        usuario = Usuario(nome, email, telefone)
        self._usuarios_obj.append(usuario)
        self._salvar_dados()
        return True
    
    def buscar_usuario_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Busca um usuário pelo ID."""
        usuario_id = int(usuario_id)
        for usuario in self._usuarios_obj:
            if usuario.id == usuario_id:
                return usuario
        return None
    
    def listar_usuarios(self) -> None:
        """Lista todos os usuários cadastrados."""
        if not self._usuarios_obj:
            print("Nenhum usuário cadastrado.")
            return
        
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for usuario in self._usuarios_obj:
            print(usuario)
        print()
    
    def realizar_emprestimo(self, usuario_id: int, livro_id: int) -> bool:
        """Realiza um empréstimo de livro."""
        usuario_id = int(usuario_id)
        livro_id = int(livro_id)
        
        usuario = self.buscar_usuario_por_id(usuario_id)
        if not usuario:
            return False
        
        livro = self.buscar_livro_por_id(livro_id)
        if not livro:
            return False
        
        if not livro.disponivel:
            return False
        
        emprestimo = Emprestimo(usuario_id, livro_id)
        self._emprestimos_obj.append(emprestimo)
        livro.emprestar()
        self._salvar_dados()
        return True
    
    def devolver_livro(self, emprestimo_id: int) -> bool:
        """Realiza a devolução de um livro emprestado."""
        emprestimo_id = int(emprestimo_id)
        
        emprestimo = None
        for emp in self._emprestimos_obj:
            if emp.id == emprestimo_id:
                emprestimo = emp
                break
        
        if not emprestimo:
            return False
        
        if emprestimo.devolvido:
            return False
        
        livro = self.buscar_livro_por_id(emprestimo.livro_id)
        if livro:
            livro.devolver()
        
        emprestimo.realizar_devolucao()
        self._salvar_dados()
        return True
    
    def listar_emprestimos(self) -> None:
        """Lista todos os empréstimos."""
        if not self._emprestimos_obj:
            print("Nenhum empréstimo registrado.")
            return
        
        for emprestimo in self._emprestimos_obj:
            usuario = self.buscar_usuario_por_id(emprestimo.usuario_id)
            livro = self.buscar_livro_por_id(emprestimo.livro_id)
            
            if usuario and livro:
                status = "Devolvido" if emprestimo.devolvido else "Em andamento"
                print(f"[{emprestimo.id}] {usuario.nome} - {livro.titulo} | {status}")
    
    def _salvar_dados(self) -> None:
        """Salva todos os dados no arquivo JSON."""
        dados = {
            'livros': [livro.to_dict() for livro in self._livros_obj],
            'usuarios': [usuario.to_dict() for usuario in self._usuarios_obj],
            'emprestimos': [emp.to_dict() for emp in self._emprestimos_obj],
            'contadores': {
                'livro': Livro.contador_id,
                'usuario': Usuario.contador_id,
                'emprestimo': Emprestimo.contador_id
            }
        }
        
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    
    def carregar_dados(self) -> None:
        """Carrega os dados do arquivo JSON."""
        if not os.path.exists(self.arquivo):
            return
        
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            contadores = dados.get('contadores', {})
            if contadores:
                Livro.contador_id = contadores.get('livro', 0)
                Usuario.contador_id = contadores.get('usuario', 0)
                Emprestimo.contador_id = contadores.get('emprestimo', 0)
            
            for livro_data in dados.get('livros', []):
                livro = Livro(
                    titulo=livro_data['titulo'],
                    autor=livro_data['autor'],
                    isbn=livro_data['isbn'],
                    ano=livro_data['ano'],
                    id=livro_data['id']
                )
                livro.disponivel = livro_data.get('disponivel', True)
                self._livros_obj.append(livro)
            
            for usuario_data in dados.get('usuarios', []):
                usuario = Usuario(
                    nome=usuario_data['nome'],
                    email=usuario_data['email'],
                    telefone=usuario_data['telefone'],
                    id=usuario_data['id']
                )
                self._usuarios_obj.append(usuario)
            
            for emp_data in dados.get('emprestimos', []):
                emprestimo = Emprestimo(
                    usuario_id=emp_data['usuario_id'],
                    livro_id=emp_data['livro_id'],
                    id=emp_data['id']
                )
                emprestimo.devolvido = emp_data.get('devolvido', False)
                emprestimo.data_emprestimo = emp_data.get('data_emprestimo')
                emprestimo.data_devolucao = emp_data.get('data_devolucao')
                self._emprestimos_obj.append(emprestimo)
        
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erro ao carregar dados: {e}")


def main():
    """Função principal para demonstração do sistema."""
    biblioteca = Biblioteca()
    biblioteca.carregar_dados()
    
    print("=== Sistema de Biblioteca ===")
    print("Sistema pronto para uso!")
    
    biblioteca.adicionar_livro("1984", "George Orwell", "9780451524935", 1949)
    biblioteca.cadastrar_usuario("João Silva", "joao@email.com", "11987654321")
    biblioteca.listar_livros()
    biblioteca.listar_usuarios()


if __name__ == "__main__":
    main()