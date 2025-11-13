import sys
import os
import unittest
import inspect

# adiciona a pasta "sistema" ao path para o Python encontrar o módulo biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sistema')))

import biblioteca


class TestBiblioteca(unittest.TestCase):
    """Teste universal compatível com versão legada e orientada a objetos."""

    def setUp(self):
        """Configura ambiente limpo antes de cada teste."""
        # Detecta se o código está em formato orientado a objetos
        self.is_oo = any(inspect.isclass(obj) for name, obj in vars(biblioteca).items() if name.lower() == "biblioteca")
        
        if self.is_oo:
            # Instancia a classe principal se existir
            self.sistema = biblioteca.Biblioteca()
        else:
            # Usa o módulo diretamente (código legado)
            self.sistema = biblioteca
        
        # Tenta limpar dados (funciona nos dois formatos)
        for attr in ["livros", "usuarios", "emprestimos"]:
            if hasattr(self.sistema, attr):
                setattr(self.sistema, attr, [])
        for attr in ["contador_livros", "contador_usuarios"]:
            if hasattr(self.sistema, attr):
                setattr(self.sistema, attr, 1)
        if os.path.exists("biblioteca.json"):
            os.remove("biblioteca.json")

    # -------- TESTES --------
    def test_fluxo_completo(self):
        """Testa adicionar, cadastrar, emprestar, devolver e salvar/carregar dados."""

        # Adiciona livro
        if self.is_oo:
            resultado_livro = self.sistema.adicionar_livro("Livro Teste", "Autor", "1234567890123", 2024)
        else:
            resultado_livro = self.sistema.adicionarLivro("Livro Teste", "Autor", "1234567890123", 2024)
        self.assertTrue(resultado_livro, "Falha ao adicionar livro.")

        # Cadastra usuário
        if self.is_oo:
            resultado_usuario = self.sistema.cadastrar_usuario("Usuário", "user@example.com", "123")
        else:
            resultado_usuario = self.sistema.cadastrarUsuario("Usuário", "user@example.com", "123")
        self.assertTrue(resultado_usuario, "Falha ao cadastrar usuário.")

        # Realiza empréstimo
        if self.is_oo:
            resultado_emprestimo = self.sistema.realizar_emprestimo(1, 1)
        else:
            resultado_emprestimo = self.sistema.realizarEmprestimo(1, 1)
        self.assertTrue(resultado_emprestimo, "Falha ao realizar empréstimo.")

        # Devolve livro
        if self.is_oo:
            resultado_devolucao = self.sistema.devolver_livro(1)
        else:
            resultado_devolucao = self.sistema.devolverLivro(1)
        self.assertTrue(resultado_devolucao, "Falha ao devolver livro.")

        # Salva dados
        if self.is_oo:
            self.sistema.salvar_dados()
            self.sistema.livros = []
            self.sistema.usuarios = []
            self.sistema.emprestimos = []
            self.sistema.carregar_dados()
        else:
            self.sistema.salvarDados()
            self.sistema.livros = []
            self.sistema.usuarios = []
            self.sistema.emprestimos = []
            self.sistema.carregarDados()

        self.assertGreater(len(self.sistema.livros), 0, "Livro não recarregado corretamente.")
        self.assertGreater(len(self.sistema.usuarios), 0, "Usuário não recarregado corretamente.")

    def test_validacoes(self):
        """Testa validações e cenários de erro."""
        if self.is_oo:
            add = self.sistema.adicionar_livro
            cad = self.sistema.cadastrar_usuario
            emp = self.sistema.realizar_emprestimo
        else:
            add = self.sistema.adicionarLivro
            cad = self.sistema.cadastrarUsuario
            emp = self.sistema.realizarEmprestimo

        self.assertFalse(add("Livro Inválido", "Autor", "123", 2024), "Aceitou ISBN inválido.")
        self.assertFalse(cad("Usuário", "emailinvalido", "999"), "Aceitou e-mail inválido.")
        add("Livro A", "Autor A", "1234567890123", 2024)
        self.assertFalse(emp(1, 99), "Emprestou livro para usuário inexistente.")
        cad("Usuário A", "a@a.com", "123")
        self.assertFalse(emp(99, 1), "Emprestou livro inexistente.")


if __name__ == "__main__":
    unittest.main()