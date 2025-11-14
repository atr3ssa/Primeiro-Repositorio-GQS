from datetime import datetime, timedelta

class Emprestimo:
    def _init_(self, id_emp: int, usuario_id: int, livro_id: int, data_emp=None):
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

    def _str_(self):
        status = "Devolvido" if self.devolvido else "Em andamento"
        return f"[{self.id}] Usuário {self.usuario_id} - Livro {self.livro_id} | {status}"