import sys
import os
import unittest

# adiciona a pasta "sistema" ao path para o Python encontrar o módulo biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sistema')))

import biblioteca


class TestBiblioteca(unittest.TestCase):
    """Testes para as funcionalidades da biblioteca."""

    def setUp(self):
        """Executa antes de cada teste para limpar os dados."""
        biblioteca.livros = []
        biblioteca.usuarios = []
        biblioteca.emprestimos = []
        biblioteca.contador_livros = 1
        biblioteca.contador_usuarios = 1
        if os.path.exists("biblioteca.json"):
            os.remove("biblioteca.json")

    # -------- TESTES DE FUNCIONALIDADES --------

    def test_adicionar_livro_valido(self):
        """Deve adicionar um livro com dados válidos."""
        resultado = biblioteca.adicionarLivro("Livro Teste", "Autor", "1234567890123", 2024)
        self.assertTrue(resultado, msg="Falha: o livro não foi adicionado corretamente.")
        self.assertEqual(len(biblioteca.livros), 1, msg="Falha: a lista de livros não contém exatamente 1 item.")
        self.assertEqual(biblioteca.livros[0]["titulo"], "Livro Teste", msg="Falha: o título do livro não corresponde ao esperado.")

    def test_cadastrar_usuario_valido(self):
        """Deve cadastrar um usuário com dados válidos."""
        resultado = biblioteca.cadastrarUsuario("Usuário", "user@example.com", "9999")
        self.assertTrue(resultado, msg="Falha: o usuário não foi cadastrado corretamente.")
        self.assertEqual(len(biblioteca.usuarios), 1, msg="Falha: a lista de usuários não contém exatamente 1 item.")
        self.assertEqual(biblioteca.usuarios[0]["email"], "user@example.com", msg="Falha: o email do usuário não corresponde ao esperado.")

    def test_realizar_emprestimo_valido(self):
        """Deve realizar o empréstimo de um livro para um usuário existente."""
        biblioteca.adicionarLivro("Livro A", "Autor A", "1234567890123", 2024)
        biblioteca.cadastrarUsuario("Usuário A", "user@example.com", "123")
        resultado = biblioteca.realizarEmprestimo(1, 1)
        self.assertTrue(resultado, msg="Falha: o empréstimo não foi realizado corretamente.")
        self.assertFalse(biblioteca.livros[0]["disponivel"], msg="Falha: o livro deveria estar indisponível após o empréstimo.")
        self.assertEqual(len(biblioteca.emprestimos), 1, msg="Falha: a lista de empréstimos não contém exatamente 1 item.")

    def test_devolver_livro_valido(self):
        """Deve devolver corretamente um livro emprestado."""
        biblioteca.adicionarLivro("Livro A", "Autor A", "1234567890123", 2024)
        biblioteca.cadastrarUsuario("Usuário A", "user@example.com", "123")
        biblioteca.realizarEmprestimo(1, 1)
        resultado = biblioteca.devolverLivro(1)
        self.assertTrue(resultado, msg="Falha: a devolução do livro não foi realizada corretamente.")
        self.assertTrue(biblioteca.livros[0]["disponivel"], msg="Falha: o livro deveria estar disponível após a devolução.")
        self.assertTrue(biblioteca.emprestimos[0]["devolvido"], msg="Falha: o empréstimo não foi marcado como devolvido.")

    def test_salvar_e_carregar_dados(self):
        """Deve salvar e carregar corretamente os dados da biblioteca."""
        biblioteca.adicionarLivro("Livro X", "Autor X", "1234567890123", 2024)
        biblioteca.cadastrarUsuario("Usuário X", "user@example.com", "123")
        biblioteca.salvarDados()

        # Simula reinício do programa
        biblioteca.livros = []
        biblioteca.usuarios = []
        biblioteca.emprestimos = []

        biblioteca.carregarDados()
        self.assertEqual(len(biblioteca.livros), 1, msg="Falha: o livro não foi carregado corretamente do arquivo JSON.")
        self.assertEqual(len(biblioteca.usuarios), 1, msg="Falha: o usuário não foi carregado corretamente do arquivo JSON.")

    # -------- TESTES DE ERROS E VALIDAÇÕES --------

    def test_nao_adicionar_livro_com_isbn_invalido(self):
        """Não deve permitir adicionar um livro com ISBN inválido."""
        resultado = biblioteca.adicionarLivro("Livro B", "Autor B", "123", 2024)
        self.assertFalse(resultado, msg="Falha: livro com ISBN inválido foi adicionado.")

    def test_nao_cadastrar_usuario_com_email_invalido(self):
        """Não deve permitir cadastrar usuário com email inválido."""
        resultado = biblioteca.cadastrarUsuario("Usuário", "emailinvalido", "999")
        self.assertFalse(resultado, msg="Falha: usuário com email inválido foi cadastrado.")

    def test_nao_permitir_emprestimo_para_usuario_inexistente(self):
        """Não deve permitir empréstimo para um usuário que não existe."""
        biblioteca.adicionarLivro("Livro A", "Autor A", "1234567890123", 2024)
        resultado = biblioteca.realizarEmprestimo(99, 1)  # Usuário 99 não existe
        self.assertFalse(resultado, msg="Falha: empréstimo realizado para usuário inexistente.")

    def test_nao_permitir_emprestimo_para_livro_inexistente(self):
        """Não deve permitir empréstimo de um livro que não existe."""
        biblioteca.cadastrarUsuario("Usuário A", "user@example.com", "999")
        resultado = biblioteca.realizarEmprestimo(1, 99)  # Livro 99 não existe
        self.assertFalse(resultado, msg="Falha: empréstimo realizado para livro inexistente.")


if __name__ == "__main__":
    unittest.main()