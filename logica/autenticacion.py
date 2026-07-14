# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import hashlib
from modelos.esquemas import USUARIO_NOMBRE, USUARIO_CONTRASENA_HASH, USUARIO_ROL
from persistencia.usuarios_repo import leer_usuarios

def hashear_contrasena(contrasena):
    objeto_hash = hashlib.sha256(contrasena.encode('utf-8'))
    return objeto_hash.hexdigest()

def autenticar(nombre_usuario, contrasena):
    hash_ingresado = hashear_contrasena(contrasena)
    usuarios = leer_usuarios()

    for usuario in usuarios:
        if usuario[USUARIO_NOMBRE] == nombre_usuario:
            if usuario[USUARIO_CONTRASENA_HASH] == hash_ingresado:
                return usuario[USUARIO_ROL]

    return None
