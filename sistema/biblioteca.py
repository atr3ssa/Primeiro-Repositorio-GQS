import datetime
import json

# Variáveis globais - MÁ PRÁTICA
livros = []
usuarios = []
emprestimos = []
contador_livros = 1
contador_usuarios = 1

#def adicionarLivro(titulo, autor, isbn, ano):
    #global contador_livros
    if titulo == "" or autor == "" or isbn == "":
        print("Erro: campos obrigatórios")
        return False

    for livro in livros:
        if livro['isbn'] == isbn:
            print("Livro já existe")
            return False

    if len(isbn) != 13 and len(isbn) != 10:
        print("ISBN inválido")
        return False

    l = {
        'id': contador_livros,
        'titulo': titulo,
        'autor': autor,
        'isbn': isbn,
        'ano': ano,
        'disponivel': True
    }

    livros.append(l)
    contador_livros += 1
    print("Livro adicionado com sucesso")
    salvarDados()
    return True


def cadastrarUsuario(nome, email, telefone):
    global contador_usuarios
    if nome == "":
        print("Nome é obrigatório")
        return False

    for usuario in usuarios:
        if usuario['email'] == email:
            print("Email já cadastrado")
            return False

    if "@" not in email:
        print("Email inválido")
        return False

    u = {
        'id': contador_usuarios,
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'ativo': True
    }

    usuarios.append(u)
    contador_usuarios += 1

    print("Usuário cadastrado com sucesso")
    salvarDados()
    return True


def realizarEmprestimo(usuario_id, livro_id):
    u = None
    l = None

    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            u = usuario
            break

    if u is None:
        print("Usuário não encontrado")
        return False

    for livro in livros:
        if livro['id'] == livro_id:
            l = livro
            break

    if l is None:
        print("Livro não encontrado")
        return False

    if not l['disponivel']:
        print("Livro não disponível")
        return False

    data_emprestimo = datetime.datetime.now()
    data_devolucao = data_emprestimo + datetime.timedelta(days=14)

    emp = {
        'id': len(emprestimos) + 1,
        'usuario_id': usuario_id,
        'livro_id': livro_id,
        'data_emprestimo': data_emprestimo.strftime('%Y-%m-%d'),
        'data_devolucao': data_devolucao.strftime('%Y-%m-%d'),
        'devolvido': False
    }

    emprestimos.append(emp)
    l['disponivel'] = False
    print("Empréstimo realizado com sucesso")
    salvarDados()
    return True


def devolverLivro(emprestimo_id):
    e = None

    for emprestimo in emprestimos:
        if emprestimo['id'] == emprestimo_id:
            e = emprestimo
            break

    if e is None:
        print("Empréstimo não encontrado")
        return False

    if e['devolvido']:
        print("Livro já foi devolvido")
        return False

    for livro in livros:
        if livro['id'] == e['livro_id']:
            livro['disponivel'] = True
            break

    e['devolvido'] = True
    e['data_devolucao_real'] = datetime.datetime.now().strftime('%Y-%m-%d')
    print("Livro devolvido com sucesso")
    salvarDados()
    return True


def listarLivros():
    if not livros:
        print("Nenhum livro cadastrado")
        return
    print("=== LIVROS ===")
    for livro in livros:
        status = "Disponível" if livro['disponivel'] else "Emprestado"
        print(f"ID: {livro['id']} | {livro['titulo']} | {livro['autor']} | {status}")


def listarUsuarios():
    if not usuarios:
        print("Nenhum usuário cadastrado")
        return
    print("=== USUÁRIOS ===")
    for usuario in usuarios:
        status = "Ativo" if usuario['ativo'] else "Inativo"
        print(f"ID: {usuario['id']} | {usuario['nome']} | {usuario['email']} | {status}")


def listarEmprestimos():
    if not emprestimos:
        print("Nenhum empréstimo cadastrado")
        return
    print("=== EMPRÉSTIMOS ===")
    for emp in emprestimos:
        status = "Devolvido" if emp['devolvido'] else "Em andamento"
        print(f"ID: {emp['id']} | Usuário: {emp['usuario_id']} | Livro: {emp['livro_id']} | {status}")


def salvarDados():
    dados = {
        'livros': livros,
        'usuarios': usuarios,
        'emprestimos': emprestimos,
        'contador_livros': contador_livros,
        'contador_usuarios': contador_usuarios
    }
    with open('biblioteca.json', 'w') as f:
        json.dump(dados, f, indent=2)


def carregarDados():
    global livros, usuarios, emprestimos, contador_livros, contador_usuarios
    with open('biblioteca.json', 'r') as f:
        dados = json.load(f)
        livros = dados['livros']
        usuarios = dados['usuarios']
        emprestimos = dados['emprestimos']
        contador_livros = dados['contador_livros']
        contador_usuarios = dados['contador_usuarios']


def menu():
    while True:
        print("\n=== SISTEMA DE BIBLIOTECA ===")
        print("1. Adicionar Livro")
        print("2. Cadastrar Usuário")
        print("3. Realizar Empréstimo")
        print("4. Devolver Livro")
        print("5. Listar Livros")
        print("6. Listar Usuários")
        print("7. Listar Empréstimos")
        print("8. Salvar Dados")
        print("9. Carregar Dados")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            isbn = input("ISBN: ")
            ano = int(input("Ano: "))
            adicionarLivro(titulo, autor, isbn, ano)
        elif opcao == "2":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            cadastrarUsuario(nome, email, telefone)
        elif opcao == "3":
            usuario_id = int(input("ID do Usuário: "))
            livro_id = int(input("ID do Livro: "))
            realizarEmprestimo(usuario_id, livro_id)
        elif opcao == "4":
            emprestimo_id = int(input("ID do Empréstimo: "))
            devolverLivro(emprestimo_id)
        elif opcao == "5":
            listarLivros()
        elif opcao == "6":
            listarUsuarios()
        elif opcao == "7":
            listarEmprestimos()
        elif opcao == "8":
            salvarDados()
            print("Dados salvos com sucesso")
        elif opcao == "9":
            carregarDados()
            print("Dados carregados com sucesso")
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    adicionarLivro("1984", "George Orwell", "9780451524935", 1949)
    adicionarLivro("Dom Casmurro", "Machado de Assis", "9788525406958", 1899)
    cadastrarUsuario("João Silva", "joao@email.com", "11999999999")
    cadastrarUsuario("Maria Santos", "maria@email.com", "11888888888")
    menu()