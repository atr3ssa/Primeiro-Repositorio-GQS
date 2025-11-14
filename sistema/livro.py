class Livro:
    contador_id = 0
    
    def __init__(self, titulo, autor, isbn, ano, id=None):
        if id is not None:
            self.id = int(id)  # ← CONVERTE PARA INT
            if self.id >= Livro.contador_id:
                Livro.contador_id = self.id
        else:
            Livro.contador_id += 1
            self.id = Livro.contador_id
            
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano = ano
        self.disponivel = True