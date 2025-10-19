import unittest # módulo pararealização de testes no Python
#from sistema_legado import adicionar_usuario, remover_usuario, buscar_usuario, listar_usuarios

from test_helpers import (
    adicionar_usuario,
    remover_usuario,
    buscar_usuario,
    listar_usuarios 
)

class TestSistema(unittest.TestCase):

    # ---------------------------
    # TESTES DA FUNÇÃO ADICIONAR
    # ---------------------------

    def test_adicionar_usuario_valido(self):
        """Deve adicionar um nome corretamente na lista."""
        usuarios = []
        adicionar_usuario(usuarios, "Maria")
        self.assertIn("Maria", usuarios)

    def test_adicionar_usuario_vazio(self):
        """Não deve adicionar usuário com nome vazio."""
        usuarios = []
        adicionar_usuario(usuarios, "")
        self.assertEqual(len(usuarios), 0)

    def test_adicionar_usuario_duplicado(self):
        """Não deve permitir duplicatas."""
        usuarios = ["Ana"]
        adicionar_usuario(usuarios, "Ana")
        self.assertEqual(usuarios.count("Ana"), 1)

    # ---------------------------
    # TESTES DA FUNÇÃO REMOVER
    # ---------------------------

    def test_remover_usuario_existente(self):
        """Deve remover o usuário corretamente."""
        usuarios = ["João", "Maria"]
        remover_usuario(usuarios, "Maria")
        self.assertNotIn("Maria", usuarios)

    def test_remover_usuario_inexistente(self):
        """Não deve quebrar se tentar remover alguém que não existe."""
        usuarios = ["Carlos"]
        try:
            remover_usuario(usuarios, "Zeca")
            resultado = True
        except Exception:
            resultado = False
        self.assertTrue(resultado)

    # ---------------------------
    # TESTES DA FUNÇÃO BUSCAR
    # ---------------------------

    def test_buscar_usuario_existente(self):
        """Deve encontrar o usuário correto."""
        usuarios = ["Ana", "Bruno"]
        resultado = buscar_usuario(usuarios, "Ana")
        self.assertEqual(resultado, "Ana")

    def test_buscar_usuario_inexistente(self):
        """Deve retornar None quando o usuário não for encontrado."""
        usuarios = ["Ana"]
        resultado = buscar_usuario(usuarios, "Pedro")
        self.assertIsNone(resultado)

    # ---------------------------
    # TESTES DA FUNÇÃO LISTAR
    # ---------------------------

    def test_listar_usuarios(self):
        """Deve retornar todos os usuários corretamente."""
        usuarios = ["Ana", "Bruno", "Carla"]
        resultado = listar_usuarios(usuarios)
        self.assertEqual(resultado, ["Ana", "Bruno", "Carla"])

    def test_listar_usuarios_vazio(self):
        """Deve retornar lista vazia se não houver usuários."""
        usuarios = []
        resultado = listar_usuarios(usuarios)
        self.assertEqual(resultado, [])

if __name__ == '__main__':
    unittest.main()
