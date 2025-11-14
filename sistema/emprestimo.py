class Emprestimo:
    contador_id = 0
    
    def __init__(self, usuario, livro, id=None):
        if id is not None:
            self.id = int(id)  # ← CONVERTE PARA INT
            if self.id >= Emprestimo.contador_id:
                Emprestimo.contador_id = self.id
        else:
            Emprestimo.contador_id += 1
            self.id = Emprestimo.contador_id
            
        self.usuario = usuario
        self.livro = livro
        self.ativo = True
        self.data_emprestimo = datetime.now()
        self.data_devolucao = None