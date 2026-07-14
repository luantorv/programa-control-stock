# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
from persistencia.csv_utils import leer_csv, escribir_csv_atomico
from modelos.esquemas import PRODUCTO_CODIGO, ENCABEZADO_PRODUCTOS

_RUTA_PRODUCTOS = os.path.join(os.path.dirname(__file__), '..', 'datos', 'productos.csv')

def leer_productos():
    return leer_csv(_RUTA_PRODUCTOS)

def guardar_productos(productos):
    escribir_csv_atomico(_RUTA_PRODUCTOS, productos, ENCABEZADO_PRODUCTOS)

def buscar_producto_por_codigo(codigo):
    productos = leer_productos()
    for producto in productos:
        if producto[PRODUCTO_CODIGO] == codigo:
            return producto
    return None

def agregar_producto(producto):
    productos = leer_productos()
    productos.append(producto)
    guardar_productos(productos)

def actualizar_producto(producto_actualizado):
    productos = leer_productos()
    for i in range(len(productos)):
        if productos[i][PRODUCTO_CODIGO] == producto_actualizado[PRODUCTO_CODIGO]:
            productos[i] = producto_actualizado
            break
    guardar_productos(productos)

def eliminar_producto(codigo):
    productos = leer_productos()
    productos_restantes = []
    for producto in productos:
        if producto[PRODUCTO_CODIGO] != codigo:
            productos_restantes.append(producto)
    guardar_productos(productos_restantes)
