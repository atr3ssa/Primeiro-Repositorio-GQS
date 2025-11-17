class Usuario:
    def __init__(self, id_usuario, nome, email, telefone):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.ativo = True

    def __str__(self):
        status = "Ativo" if self.ativo else "Inativo"
        return f"[{self.id}] {self.nome} | {self.email} | {status}"