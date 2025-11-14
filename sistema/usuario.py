class Usuario:
    contador_id = 0
    
    def __init__(self, nome, email, telefone, id=None):
        if id is not None:
            self.id = int(id)  # ← CONVERTE PARA INT
            if self.id >= Usuario.contador_id:
                Usuario.contador_id = self.id
        else:
            Usuario.contador_id += 1
            self.id = Usuario.contador_id
            
        self.nome = nome
        self.email = email
        self.telefone = telefone