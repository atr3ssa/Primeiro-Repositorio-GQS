def adicionar_usuario(usuarios, nome):
    """Adiciona um usuário se o nome for válido e não duplicado."""
    if nome and nome not in usuarios:
        usuarios.append(nome)

def remover_usuario(usuarios, nome):
    """Remove o usuário da lista se existir."""
    try:
        usuarios.remove(nome)
    except ValueError:
        pass  # Nome não está na lista, não faz nada

def buscar_usuario(usuarios, nome):
    """Retorna o nome se encontrado, senão None."""
    return nome if nome in usuarios else None

def listar_usuarios(usuarios):
    """Retorna a lista atual de usuários."""
    return usuarios.copy()
