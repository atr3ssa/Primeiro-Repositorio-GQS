import sys
import os
import unittest

# adiciona a pasta "sistema" ao path para o Python encontrar o módulo biblioteca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sistema.biblioteca_poo import Biblioteca, Livro, Usuario, Emprestimo
#from sistema.biblioteca import Biblioteca, Livro, Usuario, Emprestimo


class TestBiblioteca(unittest.TestCase):
    """Testes para as funcionalidades da biblioteca usando POO."""

    def setUp(self):
        """Executa antes de cada teste para limpar os dados."""
        # Cria uma nova instância da biblioteca para cada teste
        self.biblioteca = Biblioteca('test_biblioteca.json')
        
        # Limpa o arquivo de teste se existir
        if os.path.exists("test_biblioteca.json"):
            os.remove("test_biblioteca.json")
        
        # Reseta contadores
        #Livro.resetar_contador()
        #Usuario.resetar_contador()
        #Emprestimo.resetar_contador()

    def tearDown(self):
        """Executa após cada teste para limpar."""
        if os.path.exists("test_biblioteca.json"):
            os.remove("test_biblioteca.json")

    # -------- TESTES DE FUNCIONALIDADES --------

    def test_adicionar_livro_valido(self):
        """Deve adicionar um livro com dados válidos."""
        resultado = self.biblioteca.adicionar_livro("Livro Teste", "Autor", "1234567890123", 2024)
        self.assertTrue(resultado, msg="Falha: o livro não foi adicionado corretamente.")
        self.assertEqual(len(self.biblioteca._livros_obj), 1, msg="Falha: a lista de livros não contém exatamente 1 item.")
        self.assertEqual(self.biblioteca._livros_obj[0].titulo, "Livro Teste", msg="Falha: o título do livro não corresponde ao esperado.")

    def test_cadastrar_usuario_valido(self):
        """Deve cadastrar um usuário com dados válidos."""
        resultado = self.biblioteca.cadastrar_usuario("Usuário", "user@example.com", "9999")
        self.assertTrue(resultado, msg="Falha: o usuário não foi cadastrado corretamente.")
        self.assertEqual(len(self.biblioteca._usuarios_obj), 1, msg="Falha: a lista de usuários não contém exatamente 1 item.")
        self.assertEqual(self.biblioteca._usuarios_obj[0].email, "user@example.com", msg="Falha: o email do usuário não corresponde ao esperado.")

    def test_realizar_emprestimo_valido(self):
        """Deve realizar o empréstimo de um livro para um usuário existente."""
        self.biblioteca.adicionar_livro("Livro A", "Autor A", "1234567890123", 2024)
        self.biblioteca.cadastrar_usuario("Usuário A", "user@example.com", "123")
        resultado = self.biblioteca.realizar_emprestimo(1, 1)
        self.assertTrue(resultado, msg="Falha: o empréstimo não foi realizado corretamente.")
        self.assertFalse(self.biblioteca._livros_obj[0].disponivel, msg="Falha: o livro deveria estar indisponível após o empréstimo.")
        self.assertEqual(len(self.biblioteca._emprestimos_obj), 1, msg="Falha: a lista de empréstimos não contém exatamente 1 item.")

    def test_devolver_livro_valido(self):
        """Deve devolver corretamente um livro emprestado."""
        self.biblioteca.adicionar_livro("Livro A", "Autor A", "1234567890123", 2024)
        self.biblioteca.cadastrar_usuario("Usuário A", "user@example.com", "123")
        self.biblioteca.realizar_emprestimo(1, 1)
        resultado = self.biblioteca.devolver_livro(1)
        self.assertTrue(resultado, msg="Falha: a devolução do livro não foi realizada corretamente.")
        self.assertTrue(self.biblioteca._livros_obj[0].disponivel, msg="Falha: o livro deveria estar disponível após a devolução.")
        self.assertTrue(self.biblioteca._emprestimos_obj[0].devolvido, msg="Falha: o empréstimo não foi marcado como devolvido.")

    def test_salvar_e_carregar_dados(self):
        """Deve salvar e carregar corretamente os dados da biblioteca."""
        self.biblioteca.adicionar_livro("Livro X", "Autor X", "1234567890123", 2024)
        self.biblioteca.cadastrar_usuario("Usuário X", "user@example.com", "123")
        #self.biblioteca._salvar_dados()

        # Cria nova instância simulando reinício do programa
        nova_biblioteca = Biblioteca('test_biblioteca.json')
        nova_biblioteca.carregar_dados()
        
        self.assertEqual(len(nova_biblioteca._livros_obj), 1, msg="Falha: o livro não foi carregado corretamente do arquivo JSON.")
        self.assertEqual(len(nova_biblioteca._usuarios_obj), 1, msg="Falha: o usuário não foi carregado corretamente do arquivo JSON.")

    # -------- TESTES DE ERROS E VALIDAÇÕES --------

    def test_nao_adicionar_livro_com_isbn_invalido(self):
        """Não deve permitir adicionar um livro com ISBN inválido."""
        resultado = self.biblioteca.adicionar_livro("Livro B", "Autor B", "123", 2024)
        self.assertFalse(resultado, msg="Falha: livro com ISBN inválido foi adicionado.")

    def test_nao_cadastrar_usuario_com_email_invalido(self):
        """Não deve permitir cadastrar usuário com email inválido."""
        resultado = self.biblioteca.cadastrar_usuario("Usuário", "emailinvalido", "999")
        self.assertFalse(resultado, msg="Falha: usuário com email inválido foi cadastrado.")

    def test_nao_permitir_emprestimo_para_usuario_inexistente(self):
        """Não deve permitir empréstimo para um usuário que não existe."""
        self.biblioteca.adicionar_livro("Livro A", "Autor A", "1234567890123", 2024)
        resultado = self.biblioteca.realizar_emprestimo(99, 1)  # Usuário 99 não existe
        self.assertFalse(resultado, msg="Falha: empréstimo realizado para usuário inexistente.")

    def test_nao_permitir_emprestimo_para_livro_inexistente(self):
        """Não deve permitir empréstimo de um livro que não existe."""
        self.biblioteca.cadastrar_usuario("Usuário A", "user@example.com", "999")
        resultado = self.biblioteca.realizar_emprestimo(1, 99)  # Livro 99 não existe
        self.assertFalse(resultado, msg="Falha: empréstimo realizado para livro inexistente.")


if __name__ == "__main__":
    unittest.main()