"""
Testes para o Sistema de Biblioteca
Seguindo princípios de Clean Code e Orientação a Objetos

Este conjunto de testes valida o comportamento do sistema,
não a implementação, permitindo refatoração segura.
"""

import pytest
import os
import json
import sys

# Configuração do path para importação
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PARENT_DIR)

from sistema.biblioteca import Biblioteca


# ==================== FIXTURES ====================

@pytest.fixture
def arquivo_teste_temporario():
    """Retorna um nome de arquivo temporário único."""
    return f'test_biblioteca_{os.getpid()}.json'


@pytest.fixture
def biblioteca_nova(arquivo_teste_temporario):
    """
    Cria uma biblioteca vazia para testes isolados.
    Remove o arquivo após o teste.
    """
    if os.path.exists(arquivo_teste_temporario):
        os.remove(arquivo_teste_temporario)
    
    biblioteca = Biblioteca(arquivo_dados=arquivo_teste_temporario)
    
    yield biblioteca
    
    if os.path.exists(arquivo_teste_temporario):
        os.remove(arquivo_teste_temporario)


@pytest.fixture
def biblioteca_com_dados(arquivo_teste_temporario):
    """
    Cria uma biblioteca pré-populada com dados de teste.
    """
    if os.path.exists(arquivo_teste_temporario):
        os.remove(arquivo_teste_temporario)
    
    biblioteca = Biblioteca(arquivo_dados=arquivo_teste_temporario)
    
    # Dados de teste
    biblioteca.adicionar_livro(
        titulo="1984",
        autor="George Orwell",
        isbn="9780451524935",
        ano=1949
    )
    biblioteca.adicionar_livro(
        titulo="O Senhor dos Anéis",
        autor="J.R.R. Tolkien",
        isbn="9788533613379",
        ano=1954
    )
    biblioteca.adicionar_livro(
        titulo="Dom Casmurro",
        autor="Machado de Assis",
        isbn="9788544001417",
        ano=1899
    )
    
    biblioteca.cadastrar_usuario(
        nome="João Silva",
        email="joao.silva@email.com",
        telefone="11987654321"
    )
    biblioteca.cadastrar_usuario(
        nome="Maria Santos",
        email="maria.santos@email.com",
        telefone="11976543210"
    )
    
    yield biblioteca
    
    if os.path.exists(arquivo_teste_temporario):
        os.remove(arquivo_teste_temporario)


# ==================== TESTES: ADICIONAR LIVROS ====================

class TestAdicionarLivros:
    """Testes relacionados à adição de livros no sistema."""
    
    def test_deve_adicionar_livro_com_dados_validos(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca vazia
        QUANDO adiciono um livro com todos os dados válidos
        ENTÃO o livro deve ser adicionado com sucesso
        """
        resultado = biblioteca_nova.adicionar_livro(
            titulo="Clean Code",
            autor="Robert C. Martin",
            isbn="9780132350884",
            ano=2008
        )
        
        assert resultado is True, "Deveria retornar True ao adicionar livro válido"
        assert len(biblioteca_nova.livros) == 1, "Deveria ter 1 livro na biblioteca"
        
        livro = biblioteca_nova.livros[0]
        assert livro.titulo == "Clean Code"
        assert livro.autor == "Robert C. Martin"
        assert livro.isbn == "9780132350884"
        assert livro.ano == 2008
        assert livro.disponivel is True, "Livro novo deve estar disponível"
    
    def test_nao_deve_adicionar_livro_sem_titulo(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO tento adicionar um livro sem título
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_nova.adicionar_livro(
            titulo="",
            autor="Autor Teste",
            isbn="1234567890",
            ano=2020
        )
        
        assert resultado is False, "Não deveria adicionar livro sem título"
        assert len(biblioteca_nova.livros) == 0, "Não deveria ter livros na biblioteca"
    
    def test_nao_deve_adicionar_livro_sem_autor(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO tento adicionar um livro sem autor
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_nova.adicionar_livro(
            titulo="Título Teste",
            autor="",
            isbn="1234567890",
            ano=2020
        )
        
        assert resultado is False
        assert len(biblioteca_nova.livros) == 0
    
    def test_nao_deve_adicionar_livro_sem_isbn(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO tento adicionar um livro sem ISBN
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_nova.adicionar_livro(
            titulo="Título Teste",
            autor="Autor Teste",
            isbn="",
            ano=2020
        )
        
        assert resultado is False
        assert len(biblioteca_nova.livros) == 0
    
    def test_nao_deve_adicionar_livro_com_isbn_duplicado(self, biblioteca_nova):
        """
        DADO que tenho um livro cadastrado
        QUANDO tento adicionar outro livro com o mesmo ISBN
        ENTÃO a operação deve falhar
        """
        biblioteca_nova.adicionar_livro(
            titulo="Livro Original",
            autor="Autor Original",
            isbn="1234567890",
            ano=2020
        )
        
        resultado = biblioteca_nova.adicionar_livro(
            titulo="Livro Duplicado",
            autor="Autor Diferente",
            isbn="1234567890",
            ano=2021
        )
        
        assert resultado is False
        assert len(biblioteca_nova.livros) == 1, "Só deveria ter o primeiro livro"
    
    def test_deve_aceitar_isbn_com_10_digitos(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO adiciono um livro com ISBN de 10 dígitos
        ENTÃO o livro deve ser aceito
        """
        resultado = biblioteca_nova.adicionar_livro(
            titulo="Livro ISBN-10",
            autor="Autor",
            isbn="0123456789",
            ano=2020
        )
        
        assert resultado is True
        assert len(biblioteca_nova.livros) == 1
    
    def test_deve_aceitar_isbn_com_13_digitos(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO adiciono um livro com ISBN de 13 dígitos
        ENTÃO o livro deve ser aceito
        """
        resultado = biblioteca_nova.adicionar_livro(
            titulo="Livro ISBN-13",
            autor="Autor",
            isbn="9780123456789",
            ano=2020
        )
        
        assert resultado is True
        assert len(biblioteca_nova.livros) == 1
    
    def test_nao_deve_aceitar_isbn_com_tamanho_invalido(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO tento adicionar livros com ISBN de tamanho inválido
        ENTÃO as operações devem falhar
        """
        # ISBN muito curto
        resultado_curto = biblioteca_nova.adicionar_livro(
            titulo="Livro",
            autor="Autor",
            isbn="123",
            ano=2020
        )
        
        # ISBN muito longo
        resultado_longo = biblioteca_nova.adicionar_livro(
            titulo="Livro",
            autor="Autor",
            isbn="12345678901234",
            ano=2020
        )
        
        assert resultado_curto is False
        assert resultado_longo is False
        assert len(biblioteca_nova.livros) == 0
    
    def test_ids_devem_ser_sequenciais(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca vazia
        QUANDO adiciono múltiplos livros
        ENTÃO os IDs devem ser sequenciais e únicos
        """
        biblioteca_nova.adicionar_livro("Livro 1", "Autor 1", "1111111111", 2020)
        biblioteca_nova.adicionar_livro("Livro 2", "Autor 2", "2222222222", 2021)
        biblioteca_nova.adicionar_livro("Livro 3", "Autor 3", "3333333333", 2022)
        
        assert biblioteca_nova.livros[0].id == 1
        assert biblioteca_nova.livros[1].id == 2
        assert biblioteca_nova.livros[2].id == 3


# ==================== TESTES: CADASTRAR USUÁRIOS ====================

class TestCadastrarUsuarios:
    """Testes relacionados ao cadastro de usuários."""
    
    def test_deve_cadastrar_usuario_com_dados_validos(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca vazia
        QUANDO cadastro um usuário com dados válidos
        ENTÃO o usuário deve ser cadastrado com sucesso
        """
        resultado = biblioteca_nova.cadastrar_usuario(
            nome="Carlos Oliveira",
            email="carlos@email.com",
            telefone="11999887766"
        )
        
        assert resultado is True
        assert len(biblioteca_nova.usuarios) == 1
        
        usuario = biblioteca_nova.usuarios[0]
        assert usuario.nome == "Carlos Oliveira"
        assert usuario.email == "carlos@email.com"
        assert usuario.telefone == "11999887766"
    
    def test_nao_deve_cadastrar_usuario_sem_nome(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO tento cadastrar usuário sem nome
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_nova.cadastrar_usuario(
            nome="",
            email="email@valido.com",
            telefone="11999999999"
        )
        
        assert resultado is False
        assert len(biblioteca_nova.usuarios) == 0
    
    def test_nao_deve_cadastrar_usuario_com_email_invalido(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca
        QUANDO tento cadastrar usuário com email inválido (sem @)
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_nova.cadastrar_usuario(
            nome="Nome Válido",
            email="emailinvalido.com",
            telefone="11999999999"
        )
        
        assert resultado is False
        assert len(biblioteca_nova.usuarios) == 0
    
    def test_nao_deve_cadastrar_usuario_com_email_duplicado(self, biblioteca_nova):
        """
        DADO que tenho um usuário cadastrado
        QUANDO tento cadastrar outro usuário com mesmo email
        ENTÃO a operação deve falhar
        """
        biblioteca_nova.cadastrar_usuario(
            nome="Primeiro Usuário",
            email="mesmo@email.com",
            telefone="11111111111"
        )
        
        resultado = biblioteca_nova.cadastrar_usuario(
            nome="Segundo Usuário",
            email="mesmo@email.com",
            telefone="22222222222"
        )
        
        assert resultado is False
        assert len(biblioteca_nova.usuarios) == 1
    
    def test_ids_de_usuarios_devem_ser_sequenciais(self, biblioteca_nova):
        """
        DADO que tenho uma biblioteca vazia
        QUANDO cadastro múltiplos usuários
        ENTÃO os IDs devem ser sequenciais
        """
        biblioteca_nova.cadastrar_usuario("User 1", "user1@test.com", "11111111111")
        biblioteca_nova.cadastrar_usuario("User 2", "user2@test.com", "22222222222")
        biblioteca_nova.cadastrar_usuario("User 3", "user3@test.com", "33333333333")
        
        assert biblioteca_nova.usuarios[0].id == 1
        assert biblioteca_nova.usuarios[1].id == 2
        assert biblioteca_nova.usuarios[2].id == 3


# ==================== TESTES: EMPRÉSTIMOS ====================

class TestRealizarEmprestimos:
    """Testes relacionados à realização de empréstimos."""
    
    def test_deve_realizar_emprestimo_valido(self, biblioteca_com_dados):
        """
        DADO que tenho livros e usuários cadastrados
        QUANDO realizo um empréstimo válido
        ENTÃO o empréstimo deve ser registrado e o livro ficar indisponível
        """
        resultado = biblioteca_com_dados.realizar_emprestimo(
            usuario_id=1,
            livro_id=1
        )
        
        assert resultado is True
        assert len(biblioteca_com_dados.emprestimos) == 1
        
        emprestimo = biblioteca_com_dados.emprestimos[0]
        assert emprestimo.usuario_id == 1
        assert emprestimo.livro_id == 1
        assert emprestimo.devolvido is False
        
        livro = biblioteca_com_dados.livros[0]
        assert livro.disponivel is False, "Livro emprestado deve estar indisponível"
    
    def test_nao_deve_emprestar_para_usuario_inexistente(self, biblioteca_com_dados):
        """
        DADO que tenho uma biblioteca com dados
        QUANDO tento emprestar para um usuário inexistente
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_com_dados.realizar_emprestimo(
            usuario_id=999,
            livro_id=1
        )
        
        assert resultado is False
        assert len(biblioteca_com_dados.emprestimos) == 0
    
    def test_nao_deve_emprestar_livro_inexistente(self, biblioteca_com_dados):
        """
        DADO que tenho uma biblioteca com dados
        QUANDO tento emprestar um livro inexistente
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_com_dados.realizar_emprestimo(
            usuario_id=1,
            livro_id=999
        )
        
        assert resultado is False
        assert len(biblioteca_com_dados.emprestimos) == 0
    
    def test_nao_deve_emprestar_livro_ja_emprestado(self, biblioteca_com_dados):
        """
        DADO que um livro já está emprestado
        QUANDO tento emprestá-lo novamente
        ENTÃO a operação deve falhar
        """
        biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=1)
        
        resultado = biblioteca_com_dados.realizar_emprestimo(usuario_id=2, livro_id=1)
        
        assert resultado is False
        assert len(biblioteca_com_dados.emprestimos) == 1
    
    def test_usuario_pode_pegar_multiplos_livros(self, biblioteca_com_dados):
        """
        DADO que tenho múltiplos livros disponíveis
        QUANDO um usuário pega múltiplos livros
        ENTÃO todos os empréstimos devem ser registrados
        """
        resultado1 = biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=1)
        resultado2 = biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=2)
        resultado3 = biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=3)
        
        assert resultado1 is True
        assert resultado2 is True
        assert resultado3 is True
        assert len(biblioteca_com_dados.emprestimos) == 3
    
    def test_multiplos_usuarios_podem_pegar_livros_diferentes(self, biblioteca_com_dados):
        """
        DADO que tenho múltiplos usuários e livros
        QUANDO cada usuário pega um livro diferente
        ENTÃO todos os empréstimos devem ser registrados
        """
        resultado1 = biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=1)
        resultado2 = biblioteca_com_dados.realizar_emprestimo(usuario_id=2, livro_id=2)
        
        assert resultado1 is True
        assert resultado2 is True
        assert len(biblioteca_com_dados.emprestimos) == 2


# ==================== TESTES: DEVOLUÇÃO ====================

class TestDevolverLivros:
    """Testes relacionados à devolução de livros."""
    
    def test_deve_devolver_livro_emprestado(self, biblioteca_com_dados):
        """
        DADO que um livro está emprestado
        QUANDO faço a devolução
        ENTÃO o livro deve ficar disponível novamente
        """
        biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=1)
        
        resultado = biblioteca_com_dados.devolver_livro(emprestimo_id=1)
        
        assert resultado is True
        
        emprestimo = biblioteca_com_dados.emprestimos[0]
        assert emprestimo.devolvido is True
        
        livro = biblioteca_com_dados.livros[0]
        assert livro.disponivel is True
    
    def test_nao_deve_devolver_emprestimo_inexistente(self, biblioteca_com_dados):
        """
        DADO que tenho uma biblioteca
        QUANDO tento devolver um empréstimo inexistente
        ENTÃO a operação deve falhar
        """
        resultado = biblioteca_com_dados.devolver_livro(emprestimo_id=999)
        
        assert resultado is False
    
    def test_nao_deve_devolver_livro_ja_devolvido(self, biblioteca_com_dados):
        """
        DADO que um livro já foi devolvido
        QUANDO tento devolvê-lo novamente
        ENTÃO a operação deve falhar
        """
        biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=1)
        biblioteca_com_dados.devolver_livro(emprestimo_id=1)
        
        resultado = biblioteca_com_dados.devolver_livro(emprestimo_id=1)
        
        assert resultado is False
    
    def test_livro_devolvido_pode_ser_emprestado_novamente(self, biblioteca_com_dados):
        """
        DADO que um livro foi emprestado e devolvido
        QUANDO tento emprestá-lo novamente
        ENTÃO o empréstimo deve ter sucesso
        """
        biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=1)
        biblioteca_com_dados.devolver_livro(emprestimo_id=1)
        
        resultado = biblioteca_com_dados.realizar_emprestimo(usuario_id=2, livro_id=1)
        
        assert resultado is True
        assert len(biblioteca_com_dados.emprestimos) == 2


# ==================== TESTES: PERSISTÊNCIA ====================

class TestPersistenciaDados:
    """Testes relacionados ao salvamento e carregamento de dados."""
    
    def test_deve_salvar_dados_automaticamente(self, biblioteca_nova):
        """
        DADO que faço operações na biblioteca
        QUANDO adiciono livros e usuários
        ENTÃO os dados devem ser salvos automaticamente
        """
        biblioteca_nova.adicionar_livro("Livro", "Autor", "1234567890", 2020)
        biblioteca_nova.cadastrar_usuario("Usuario", "user@test.com", "11999999999")
        
        assert os.path.exists(biblioteca_nova.arquivo)
        
        with open(biblioteca_nova.arquivo, 'r') as f:
            dados = json.load(f)
            assert len(dados['livros']) == 1
            assert len(dados['usuarios']) == 1
    
    def test_deve_carregar_dados_salvos(self, biblioteca_nova):
        """
        DADO que tenho dados salvos
        QUANDO crio nova instância e carrego os dados
        ENTÃO os dados devem ser restaurados corretamente
        """
        biblioteca_nova.adicionar_livro("Livro Teste", "Autor Teste", "1234567890", 2023)
        biblioteca_nova.cadastrar_usuario("Usuario Teste", "user@test.com", "11999999999")
        biblioteca_nova.realizar_emprestimo(usuario_id=1, livro_id=1)
        
        nova_instancia = Biblioteca(arquivo_dados=biblioteca_nova.arquivo)
        nova_instancia.carregar_dados()
        
        assert len(nova_instancia.livros) == 1
        assert len(nova_instancia.usuarios) == 1
        assert len(nova_instancia.emprestimos) == 1
        assert nova_instancia.livros[0].titulo == "Livro Teste"
        assert nova_instancia.usuarios[0].nome == "Usuario Teste"
    
    def test_deve_iniciar_novo_sistema_sem_arquivo(self, arquivo_teste_temporario):
        """
        DADO que não existe arquivo de dados
        QUANDO inicio o sistema
        ENTÃO deve iniciar com dados vazios sem erros
        """
        arquivo_inexistente = 'arquivo_que_nao_existe_12345.json'
        
        if os.path.exists(arquivo_inexistente):
            os.remove(arquivo_inexistente)
        
        biblioteca = Biblioteca(arquivo_dados=arquivo_inexistente)
        biblioteca.carregar_dados()
        
        assert len(biblioteca.livros) == 0
        assert len(biblioteca.usuarios) == 0
        assert len(biblioteca.emprestimos) == 0
        
        if os.path.exists(arquivo_inexistente):
            os.remove(arquivo_inexistente)
    
    def test_contadores_devem_persistir(self, biblioteca_nova):
        """
        DADO que adiciono itens e recarrego
        QUANDO adiciono novos itens
        ENTÃO os IDs devem continuar a sequência
        """
        biblioteca_nova.adicionar_livro("Livro 1", "Autor 1", "1111111111", 2020)
        biblioteca_nova.cadastrar_usuario("User 1", "user1@test.com", "11111111111")
        
        nova_instancia = Biblioteca(arquivo_dados=biblioteca_nova.arquivo)
        nova_instancia.carregar_dados()
        
        nova_instancia.adicionar_livro("Livro 2", "Autor 2", "2222222222", 2021)
        nova_instancia.cadastrar_usuario("User 2", "user2@test.com", "22222222222")
        
        assert nova_instancia.livros[1].id == 2
        assert nova_instancia.usuarios[1].id == 2


# ==================== TESTES: LISTAGENS ====================

class TestListagens:
    """Testes relacionados às funcionalidades de listagem."""
    
    def test_listar_livros_deve_mostrar_todos_livros(self, biblioteca_com_dados, capsys):
        """
        DADO que tenho livros cadastrados
        QUANDO listo os livros
        ENTÃO todos devem aparecer na saída
        """
        biblioteca_com_dados.listar_livros()
        saida = capsys.readouterr().out
        
        assert "1984" in saida
        assert "O Senhor dos Anéis" in saida
        assert "Dom Casmurro" in saida
    
    def test_listar_usuarios_deve_mostrar_todos_usuarios(self, biblioteca_com_dados, capsys):
        """
        DADO que tenho usuários cadastrados
        QUANDO listo os usuários
        ENTÃO todos devem aparecer na saída
        """
        biblioteca_com_dados.listar_usuarios()
        saida = capsys.readouterr().out
        
        assert "João Silva" in saida
        assert "Maria Santos" in saida
    
    def test_listar_emprestimos_deve_mostrar_todos_emprestimos(self, biblioteca_com_dados, capsys):
        """
        DADO que tenho empréstimos registrados
        QUANDO listo os empréstimos
        ENTÃO todos devem aparecer na saída
        """
        biblioteca_com_dados.realizar_emprestimo(usuario_id=1, livro_id=1)
        biblioteca_com_dados.realizar_emprestimo(usuario_id=2, livro_id=2)
        
        biblioteca_com_dados.listar_emprestimos()
        saida = capsys.readouterr().out
        
        assert saida.strip() != ""
        assert len(saida.strip().split('\n')) == 2

# ==================== EXECUÇÃO ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])