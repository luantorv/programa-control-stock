# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

from logica.autenticacion import autenticar
from cli.entradas import pedir_credenciales

MAX_INTENTOS = 3

def _iniciar_sesion():
    for intento in range(MAX_INTENTOS):
        nombre_usuario, contrasena = pedir_credenciales()
        rol = autenticar(nombre_usuario, contrasena)

        if rol is not None:
            print("Bienvenido,", nombre_usuario + ". Rol:", rol + ".")
            return rol

        intentos_restantes = MAX_INTENTOS - intento - 1
        if intentos_restantes > 0:
            print("Credenciales incorrectas. Intentos restantes:", intentos_restantes)

    print("Acceso denegado. Demasiados intentos fallidos.")
    return None

def ejecutar():
    print("=== Control de Stock para un Supermercado ===")
    print()

    rol = _iniciar_sesion()
    if rol is None:
        return
