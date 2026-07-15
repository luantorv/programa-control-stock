# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0


def pedir_credenciales():
    nombre_usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ")
    return nombre_usuario, contrasena


def pedir_texto(mensaje):
    return input(mensaje).strip()


def pedir_numero_entero(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
            return numero
        except ValueError:
            print("Ingrese un número entero válido.")


def pedir_numero_decimal(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            numero = float(texto)
            return numero
        except ValueError:
            print("Ingrese un número decimal válido (use punto como separador: 12.50).")


def pedir_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("Ingrese 's' para confirmar o 'n' para cancelar.")


def pedir_opcion(opciones_validas):
    while True:
        opcion = input("Opción: ").strip()
        if opcion in opciones_validas:
            return opcion
        print("Opción no válida. Opciones disponibles:", ", ".join(opciones_validas))
