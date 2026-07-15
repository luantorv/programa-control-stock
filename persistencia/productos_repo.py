# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
from persistencia.csv_utils import leer_csv, escribir_csv_atomico
from persistencia.rutas import directorio_datos
from modelos.esquemas import PRODUCTO_CODIGO, PRODUCTO_NOMBRE, ENCABEZADO_PRODUCTOS

def _ruta_productos():
    return os.path.join(directorio_datos(), 'productos.csv')

def leer_productos():
    return leer_csv(_ruta_productos())

def guardar_productos(productos):
    escribir_csv_atomico(_ruta_productos(), productos, ENCABEZADO_PRODUCTOS)

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

def buscar_productos_por_nombre(nombre):
    productos = leer_productos()
    encontrados = []
    nombre_lower = nombre.lower()
    for producto in productos:
        if nombre_lower in producto[PRODUCTO_NOMBRE].lower():
            encontrados.append(producto)
    return encontrados
