import sys
import os
import unittest

# adiciona a pasta "sistema" ao path para o Python encontrar o módulo biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sistema')))

import biblioteca


class TestBiblioteca(unittest.TestCase):

    def setUp(self):
        print("\n🏁 Iniciando teste da classe TestBiblioteca")
        """Executa antes de cada teste para limpar os dados."""
        biblioteca.livros = []
        biblioteca.usuarios = []
        biblioteca.emprestimos = []
        biblioteca.contador_livros = 1
        biblioteca.contador_usuarios = 1
        if os.path.exists("biblioteca.json"):
            os.remove("biblioteca.json")

    # -------- TESTES DE FUNCIONALIDADES --------

    def test_adicionar_livro(self):
        resultado = biblioteca.adicionarLivro("Livro Teste", "Autor", "1234567890123", 2024)
        self.assertTrue(resultado)
        self.assertEqual(len(biblioteca.livros), 1)
        self.assertEqual(biblioteca.livros[0]["titulo"], "Livro Teste")

    def test_cadastrar_usuario(self):
        resultado = biblioteca.cadastrarUsuario("Usuário", "user@example.com", "9999")
        self.assertTrue(resultado)
        self.assertEqual(len(biblioteca.usuarios), 1)
        self.assertEqual(biblioteca.usuarios[0]["email"], "user@example.com")

    def test_realizar_emprestimo(self):
        biblioteca.adicionarLivro("Livro A", "Autor A", "1234567890123", 2024)
        biblioteca.cadastrarUsuario("Usuário A", "user@example.com", "123")
        resultado = biblioteca.realizarEmprestimo(1, 1)
        self.assertTrue(resultado)
        self.assertFalse(biblioteca.livros[0]["disponivel"])
        self.assertEqual(len(biblioteca.emprestimos), 1)

    def test_devolver_livro(self):
        biblioteca.adicionarLivro("Livro A", "Autor A", "1234567890123", 2024)
        biblioteca.cadastrarUsuario("Usuário A", "user@example.com", "123")
        biblioteca.realizarEmprestimo(1, 1)
        resultado = biblioteca.devolverLivro(1)
        self.assertTrue(resultado)
        self.assertTrue(biblioteca.livros[0]["disponivel"])
        self.assertTrue(biblioteca.emprestimos[0]["devolvido"])

    def test_salvar_e_carregar_dados(self):
        biblioteca.adicionarLivro("Livro X", "Autor X", "1234567890123", 2024)
        biblioteca.cadastrarUsuario("Usuário X", "user@example.com", "123")
        biblioteca.salvarDados()

        # Simula novo programa (limpa variáveis)
        biblioteca.livros = []
        biblioteca.usuarios = []
        biblioteca.emprestimos = []

        biblioteca.carregarDados()
        self.assertEqual(len(biblioteca.livros), 1)
        self.assertEqual(len(biblioteca.usuarios), 1)

    # -------- TESTES DE ERROS E VALIDAÇÕES --------

    def test_nao_deve_adicionar_livro_com_isbn_invalido(self):
        resultado = biblioteca.adicionarLivro("Livro B", "Autor B", "123", 2024)
        self.assertFalse(resultado)

    def test_nao_deve_cadastrar_usuario_com_email_invalido(self):
        resultado = biblioteca.cadastrarUsuario("Usuário", "emailinvalido", "999")
        self.assertFalse(resultado)

    def test_nao_deve_permitir_emprestimo_usuario_inexistente(self):
        biblioteca.adicionarLivro("Livro A", "Autor A", "1234567890123", 2024)
        resultado = biblioteca.realizarEmprestimo(99, 1)
        self.assertFalse(resultado)

    def test_nao_deve_permitir_emprestimo_livro_inexistente(self):
        biblioteca.cadastrarUsuario("Usuário A", "user@example.com", "999")
        resultado = biblioteca.realizarEmprestimo(1, 99)
        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()