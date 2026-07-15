# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

from logica.autenticacion import autenticar
from logica import productos as logica_productos
from cli import entradas, menus
from modelos.esquemas import ROL_SUPERVISOR, ROL_CAJERO, PRODUCTO_NOMBRE, PRODUCTO_PRECIO, PRODUCTO_STOCK

MAX_INTENTOS = 3


# --- Login ---

def _iniciar_sesion():
    for intento in range(MAX_INTENTOS):
        nombre_usuario, contrasena = entradas.pedir_credenciales()
        rol = autenticar(nombre_usuario, contrasena)

        if rol is not None:
            print("Bienvenido,", nombre_usuario + ". Rol:", rol + ".")
            return rol

        intentos_restantes = MAX_INTENTOS - intento - 1
        if intentos_restantes > 0:
            print("Credenciales incorrectas. Intentos restantes:", intentos_restantes)

    print("Acceso denegado. Demasiados intentos fallidos.")
    return None


# --- Flujos del Supervisor ---

def _flujo_alta_producto():
    while True:
        print()
        codigo = entradas.pedir_texto("Código del producto (ej: P001 | Enter para cancelar): ").upper()
        if codigo == "":
            return
        nombre = entradas.pedir_texto("Nombre del producto: ")
        precio = entradas.pedir_numero_decimal("Precio unitario ($): ")
        stock = entradas.pedir_numero_entero("Stock inicial: ")

        error = logica_productos.dar_de_alta_producto(codigo, nombre, precio, stock)
        if error == "":
            print("Producto dado de alta con éxito.")
            return
        print("Error:", error)


def _flujo_baja_producto():
    while True:
        print()
        codigo = entradas.pedir_texto("Código del producto a eliminar (Enter para cancelar): ").upper()
        if codigo == "":
            return

        producto = logica_productos.buscar_producto(codigo)
        if producto is None:
            print("No existe un producto con ese código.")
            continue

        print("Producto encontrado:", producto[PRODUCTO_NOMBRE], "| Stock:", producto[PRODUCTO_STOCK])
        confirma = entradas.pedir_confirmacion("¿Confirma la baja? (s/n): ")
        if not confirma:
            print("Baja cancelada.")
            return

        logica_productos.dar_de_baja_producto(codigo)
        print("Producto eliminado con éxito.")
        return


def _flujo_modificar_producto():
    while True:
        print()
        codigo = entradas.pedir_texto("Código del producto a modificar (Enter para cancelar): ").upper()
        if codigo == "":
            return

        producto = logica_productos.buscar_producto(codigo)
        if producto is None:
            print("No existe un producto con ese código.")
            continue

        print("Datos actuales -> Nombre:", producto[PRODUCTO_NOMBRE],
              "| Precio: $" + producto[PRODUCTO_PRECIO],
              "| Stock:", producto[PRODUCTO_STOCK])

        while True:
            nombre = entradas.pedir_texto("Nuevo nombre: ")
            precio = entradas.pedir_numero_decimal("Nuevo precio ($): ")
            stock = entradas.pedir_numero_entero("Nuevo stock: ")

            error = logica_productos.modificar_producto(codigo, nombre, precio, stock)
            if error == "":
                print("Producto modificado con éxito.")
                return
            print("Error:", error)


def _flujo_ajustar_stock():
    while True:
        print()
        codigo = entradas.pedir_texto("Código del producto (Enter para cancelar): ").upper()
        if codigo == "":
            return
        nueva_cantidad = entradas.pedir_numero_entero("Nueva cantidad en stock: ")

        error = logica_productos.ajustar_stock(codigo, nueva_cantidad)
        if error == "":
            print("Stock actualizado con éxito.")
            return
        print("Error:", error)


# --- Menús ---

def _menu_supervisor():
    while True:
        menus.mostrar_menu_supervisor()
        opcion = entradas.pedir_opcion(["0", "1", "2", "3", "4", "5"])

        if opcion == "0":
            break
        elif opcion == "1":
            _flujo_alta_producto()
        elif opcion == "2":
            _flujo_baja_producto()
        elif opcion == "3":
            _flujo_modificar_producto()
        elif opcion == "4":
            _flujo_ajustar_stock()
        elif opcion == "5":
            print("Cierre diario: por implementar.")


def _menu_cajero():
    while True:
        menus.mostrar_menu_cajero()
        opcion = entradas.pedir_opcion(["0", "1", "2"])

        if opcion == "0":
            break
        elif opcion == "1":
            print("Registro de ventas: por implementar.")
        elif opcion == "2":
            print("Consulta de stock y precio: por implementar.")


# --- Punto de entrada ---

def ejecutar():
    print("=== Control de Stock para un Supermercado ===")
    print()

    rol = _iniciar_sesion()
    if rol is None:
        return

    if rol == ROL_SUPERVISOR:
        _menu_supervisor()
    elif rol == ROL_CAJERO:
        _menu_cajero()
