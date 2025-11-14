class Livro:
    def _init_(self, id_livro: int, titulo: str, autor: str, isbn: str, ano: int):
        self.id = id_livro
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano = ano
        self.disponivel = True

    def marcar_como_emprestado(self):
        self.disponivel = False

    def marcar_como_disponivel(self):
        self.disponivel = True

    def _str_(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"[{self.id}] {self.titulo} - {self.autor} ({self.ano}) | {status}"