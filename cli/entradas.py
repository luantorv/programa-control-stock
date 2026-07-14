# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

def pedir_credenciales():
    nombre_usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ")
    return nombre_usuario, contrasena
