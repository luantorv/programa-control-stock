# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import datetime
from persistencia.productos_repo import buscar_producto_por_codigo, actualizar_producto
from persistencia.ventas_repo import registrar_venta as repo_registrar_venta
from modelos.esquemas import (
    PRODUCTO_NOMBRE, PRODUCTO_PRECIO, PRODUCTO_STOCK,
    VENTA_FECHA_HORA, VENTA_CODIGO_PRODUCTO, VENTA_NOMBRE_PRODUCTO,
    VENTA_CANTIDAD, VENTA_PRECIO_UNITARIO, VENTA_TOTAL,
)


def registrar_venta(codigo, cantidad):
    if cantidad <= 0:
        return "La cantidad a vender debe ser mayor a cero.", 0.0

    producto = buscar_producto_por_codigo(codigo)
    if producto is None:
        return "No existe un producto con el código " + codigo + ".", 0.0

    stock_actual = int(producto[PRODUCTO_STOCK])
    if cantidad > stock_actual:
        return "Stock insuficiente. Disponible: " + str(stock_actual) + " unidades.", 0.0

    precio_unitario = float(producto[PRODUCTO_PRECIO])
    total = precio_unitario * cantidad

    producto[PRODUCTO_STOCK] = str(stock_actual - cantidad)
    actualizar_producto(producto)

    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    venta = {
        VENTA_FECHA_HORA: fecha_hora,
        VENTA_CODIGO_PRODUCTO: codigo,
        VENTA_NOMBRE_PRODUCTO: producto[PRODUCTO_NOMBRE],
        VENTA_CANTIDAD: str(cantidad),
        VENTA_PRECIO_UNITARIO: "{:.2f}".format(precio_unitario),
        VENTA_TOTAL: "{:.2f}".format(total),
    }
    repo_registrar_venta(venta)

    return "", total
