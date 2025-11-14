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
    
    def __init__(self, arquivo_dados: str = 'biblioteca.json'):
        self.arquivo = arquivo_dados
        self.livros: List[Livro] = []
        self.usuarios: List[Usuario] = []
        self.emprestimos: List[Emprestimo] = []
        
        # Resetar contadores ao criar nova instância
        Livro.resetar_contador()
        Usuario.resetar_contador()
        Emprestimo.resetar_contador()
    
    # ==================== VALIDAÇÕES ====================
    
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
        return any(livro.isbn == isbn for livro in self.livros)
    
    def _validar_usuario(self, nome: str, email: str) -> bool:
        """Valida os dados de um usuário."""
        if not nome or not nome.strip():
            return False
        if not email or '@' not in email:
            return False
        return True
    
    def _email_ja_existe(self, email: str) -> bool:
        """Verifica se o email já está cadastrado."""
        return any(usuario.email == email for usuario in self.usuarios)
    
    # ==================== LIVROS ====================
    
    def adicionar_livro(self, titulo: str, autor: str, isbn: str, ano: int) -> bool:
        """
        Adiciona um novo livro à biblioteca.
        Retorna True se sucesso, False caso contrário.
        """
        if not self._validar_livro(titulo, autor, isbn):
            return False
        
        if self._isbn_ja_existe(isbn):
            return False
        
        livro = Livro(titulo, autor, isbn, ano)
        self.livros.append(livro)
        self._salvar_dados()
        return True
    
    def buscar_livro_por_id(self, livro_id: int) -> Optional[Livro]:
        """Busca um livro pelo ID."""
        livro_id = int(livro_id)
        for livro in self.livros:
            if livro.id == livro_id:
                return livro
        return None
    
    def listar_livros(self) -> None:
        """Lista todos os livros cadastrados."""
        if not self.livros:
            print("Nenhum livro cadastrado.")
            return
        
        print("\n=== LIVROS CADASTRADOS ===")
        for livro in self.livros:
            print(livro)
        print()
    
    # ==================== USUÁRIOS ====================
    
    def cadastrar_usuario(self, nome: str, email: str, telefone: str) -> bool:
        """
        Cadastra um novo usuário na biblioteca.
        Retorna True se sucesso, False caso contrário.
        """
        if not self._validar_usuario(nome, email):
            return False
        
        if self._email_ja_existe(email):
            return False
        
        usuario = Usuario(nome, email, telefone)
        self.usuarios.append(usuario)
        self._salvar_dados()
        return True
    
    def buscar_usuario_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Busca um usuário pelo ID."""
        usuario_id = int(usuario_id)
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None
    
    def listar_usuarios(self) -> None:
        """Lista todos os usuários cadastrados."""
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            return
        
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for usuario in self.usuarios:
            print(usuario)
        print()
    
    # ==================== EMPRÉSTIMOS ====================
    
    def realizar_emprestimo(self, usuario_id: int, livro_id: int) -> bool:
        """
        Realiza um empréstimo de livro.
        Retorna True se sucesso, False caso contrário.
        """
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
        self.emprestimos.append(emprestimo)
        livro.emprestar()
        self._salvar_dados()
        return True
    
    def devolver_livro(self, emprestimo_id: int) -> bool:
        """
        Realiza a devolução de um livro emprestado.
        Retorna True se sucesso, False caso contrário.
        """
        emprestimo_id = int(emprestimo_id)
        
        emprestimo = None
        for emp in self.emprestimos:
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
        if not self.emprestimos:
            print("Nenhum empréstimo registrado.")
            return
        
        #print("\n=== EMPRÉSTIMOS ===")
        for emprestimo in self.emprestimos:
            usuario = self.buscar_usuario_por_id(emprestimo.usuario_id)
            livro = self.buscar_livro_por_id(emprestimo.livro_id)
            
            if usuario and livro:
                status = "Devolvido" if emprestimo.devolvido else "Em andamento"
                print(f"[{emprestimo.id}] {usuario.nome} - {livro.titulo} | {status}")
        print()
    
    # ==================== PERSISTÊNCIA ====================
    
    def _salvar_dados(self) -> None:
        """Salva todos os dados no arquivo JSON."""
        dados = {
            'livros': [livro.to_dict() for livro in self.livros],
            'usuarios': [usuario.to_dict() for usuario in self.usuarios],
            'emprestimos': [emp.to_dict() for emp in self.emprestimos],
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
            
            # Restaurar contadores primeiro
            contadores = dados.get('contadores', {})
            if contadores:
                Livro.contador_id = contadores.get('livro', 0)
                Usuario.contador_id = contadores.get('usuario', 0)
                Emprestimo.contador_id = contadores.get('emprestimo', 0)
            
            # Carregar livros
            for livro_data in dados.get('livros', []):
                livro = Livro(
                    titulo=livro_data['titulo'],
                    autor=livro_data['autor'],
                    isbn=livro_data['isbn'],
                    ano=livro_data['ano'],
                    id=livro_data['id']
                )
                livro.disponivel = livro_data.get('disponivel', True)
                self.livros.append(livro)
            
            # Carregar usuários
            for usuario_data in dados.get('usuarios', []):
                usuario = Usuario(
                    nome=usuario_data['nome'],
                    email=usuario_data['email'],
                    telefone=usuario_data['telefone'],
                    id=usuario_data['id']
                )
                self.usuarios.append(usuario)
            
            # Carregar empréstimos
            for emp_data in dados.get('emprestimos', []):
                emprestimo = Emprestimo(
                    usuario_id=emp_data['usuario_id'],
                    livro_id=emp_data['livro_id'],
                    id=emp_data['id']
                )
                emprestimo.devolvido = emp_data.get('devolvido', False)
                emprestimo.data_emprestimo = emp_data.get('data_emprestimo')
                emprestimo.data_devolucao = emp_data.get('data_devolucao')
                self.emprestimos.append(emprestimo)
        
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erro ao carregar dados: {e}")


def main():
    """Função principal para demonstração do sistema."""
    biblioteca = Biblioteca()
    biblioteca.carregar_dados()
    
    print("=== Sistema de Biblioteca ===")
    print("Sistema pronto para uso!")
    
    # Exemplo de uso
    biblioteca.adicionar_livro("1984", "George Orwell", "9780451524935", 1949)
    biblioteca.cadastrar_usuario("João Silva", "joao@email.com", "11987654321")
    biblioteca.listar_livros()
    biblioteca.listar_usuarios()


if __name__ == "__main__":
    main()