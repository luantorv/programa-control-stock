# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

from persistencia.productos_repo import (
    buscar_producto_por_codigo,
    agregar_producto,
    actualizar_producto,
    eliminar_producto,
)
from logica.validaciones import codigo_es_valido
from modelos.esquemas import PRODUCTO_CODIGO, PRODUCTO_NOMBRE, PRODUCTO_PRECIO, PRODUCTO_STOCK


def buscar_producto(codigo):
    return buscar_producto_por_codigo(codigo)


def dar_de_alta_producto(codigo, nombre, precio, stock):
    if not codigo_es_valido(codigo):
        return "El código debe tener entre 1 y 3 letras mayúsculas seguidas de 3 dígitos (ej: P001)."
    if nombre == "":
        return "El nombre del producto no puede estar vacío."
    if precio <= 0:
        return "El precio debe ser mayor a cero."
    if stock < 0:
        return "El stock inicial no puede ser negativo."
    if buscar_producto_por_codigo(codigo) is not None:
        return "Ya existe un producto con el código " + codigo + "."

    nuevo_producto = {
        PRODUCTO_CODIGO: codigo,
        PRODUCTO_NOMBRE: nombre,
        PRODUCTO_PRECIO: "{:.2f}".format(precio),
        PRODUCTO_STOCK: str(stock),
    }
    agregar_producto(nuevo_producto)
    return ""


def dar_de_baja_producto(codigo):
    if buscar_producto_por_codigo(codigo) is None:
        return "No existe un producto con el código " + codigo + "."
    eliminar_producto(codigo)
    return ""


def modificar_producto(codigo, nombre, precio, stock):
    if nombre == "":
        return "El nombre del producto no puede estar vacío."
    if precio <= 0:
        return "El precio debe ser mayor a cero."
    if stock < 0:
        return "El stock no puede ser negativo."

    producto = buscar_producto_por_codigo(codigo)
    if producto is None:
        return "No existe un producto con el código " + codigo + "."

    producto[PRODUCTO_NOMBRE] = nombre
    producto[PRODUCTO_PRECIO] = "{:.2f}".format(precio)
    producto[PRODUCTO_STOCK] = str(stock)
    actualizar_producto(producto)
    return ""


def ajustar_stock(codigo, nueva_cantidad):
    if nueva_cantidad < 0:
        return "La cantidad no puede ser negativa."

    producto = buscar_producto_por_codigo(codigo)
    if producto is None:
        return "No existe un producto con el código " + codigo + "."

    producto[PRODUCTO_STOCK] = str(nueva_cantidad)
    actualizar_producto(producto)
    return ""
