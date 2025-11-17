from datetime import datetime, timedelta

class Emprestimo:
    def __init__(self, id_emp, usuario_id, livro_id, data_emp=None):
        self.id = id_emp
        self.usuario_id = usuario_id
        self.livro_id = livro_id
        self.data_emprestimo = data_emp or datetime.now().strftime('%Y-%m-%d')
        self.data_devolucao = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        self.devolvido = False
        self.data_devolucao_real = None

    def devolver(self):
        self.devolvido = True
        self.data_devolucao_real = datetime.now().strftime('%Y-%m-%d')