# test_helpers.py

import sistema.sistema_legado

def adicionar_usuario(nome):
    if nome:
        sistema_legado.usuarios.append(nome)

def remover_usuario(nome):
    if nome in sistema_legado.usuarios:
        sistema_legado.usuarios.remove(nome)

def buscar_usuario(nome):
    return nome if nome in sistema_legado.usuarios else None

def listar_usuarios():
    return sistema_legado.usuarios.copy()
