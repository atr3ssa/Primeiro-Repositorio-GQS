class Livro:
    contador_id = 0
    
    def __init__(self, titulo, autor, isbn, ano, id=None):
        if id is not None:
            self.id = id
            # Atualiza o contador se o id carregado for maior
            if id >= Livro.contador_id:
                Livro.contador_id = id
        else:
            Livro.contador_id += 1
            self.id = Livro.contador_id
            
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano = ano
        self.disponivel = True