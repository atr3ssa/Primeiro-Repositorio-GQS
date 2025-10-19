usuarios = []  # lista global ⚠️ ERRO: uso de variável global

def menu():
    print("1 - Cadastrar usuário")
    print("2 - Listar usuários")
    print("3 - Sair")
    try:
        return int(input("Escolha: "))
    except:
        return -1  # ⚠️ ERRO: tratamento genérico sem especificar exceção

def cadastrar():
    nome = input("Digite o nome: ")
    usuarios.append(nome)  # ⚠️ ERRO: não valida duplicidade
    print("Usuário cadastrado!")

def listar():
    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado")  # certo, mas poderia ser melhorado
    else:
        for i in range(len(usuarios)):
            print(f"{i+1} - {usuarios[i]}")  # ⚠️ ERRO: usa índice manual, não usa enumerate

def main():
    rodando = True
    while rodando:
        opcao = menu()
        if opcao == 1:
            cadastrar()
        elif opcao == 2:
            listar()
        elif opcao == 3:
            rodando = False
        else:
            print("Opção inválida")  # ⚠️ ERRO: duplicado em vários lugares

if __name__ == '__main__':
    main() #adicionei para conseguir realizar o unittest

#main()  # ⚠️ ERRO: chamada direta, sem if _name_ == "_main_"