class Livro:
    _id_counter = 1   # contador interno para gerar IDs automáticos

    def __init__(self, id_livro, titulo, autor, isbn, ano, disponivel=True):
        # Se o ID vier do JSON, usa ele; caso contrário, gera novo ID
        if id_livro is None:
            self.id = Livro._id_counter
            Livro._id_counter += 1
        else:
            self.id = id_livro
        
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano = ano
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"[{self.id}] {self.titulo} - {self.autor} ({self.ano}) | {status}"

    @classmethod
    def resetar_contador(cls):
        cls._id_counter = 1

    
 