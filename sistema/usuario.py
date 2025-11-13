class Usuario:
    def __init__(self, id_usuario: int, nome: str, email: str, telefone: str):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.ativo = True

    def desativar(self):
        self.ativo = False

    def __str__(self):
        status = "Ativo" if self.ativo else "Inativo"
        return f"[{self.id}] {self.nome} | {self.email} | {status}"