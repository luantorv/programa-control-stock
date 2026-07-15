# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import datetime
from persistencia.productos_repo import buscar_producto_por_codigo, actualizar_producto
from persistencia.ventas_repo import (
    leer_ventas_del_dia,
    registrar_venta as repo_registrar_venta,
    registrar_cierre as repo_registrar_cierre,
    limpiar_ventas_del_dia,
)
from modelos.esquemas import (
    PRODUCTO_NOMBRE, PRODUCTO_PRECIO, PRODUCTO_STOCK,
    VENTA_FECHA_HORA, VENTA_CODIGO_PRODUCTO, VENTA_NOMBRE_PRODUCTO,
    VENTA_CANTIDAD, VENTA_PRECIO_UNITARIO, VENTA_TOTAL,
    CIERRE_FECHA, CIERRE_TOTAL_VENTAS, CIERRE_TOTAL_UNIDADES, CIERRE_IMPORTE_TOTAL,
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


def ejecutar_cierre_diario():
    ventas = leer_ventas_del_dia()

    total_ventas = len(ventas)
    total_unidades = 0
    importe_total = 0.0

    for venta in ventas:
        total_unidades = total_unidades + int(venta[VENTA_CANTIDAD])
        importe_total = importe_total + float(venta[VENTA_TOTAL])

    fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")

    cierre = {
        CIERRE_FECHA: fecha_hoy,
        CIERRE_TOTAL_VENTAS: str(total_ventas),
        CIERRE_TOTAL_UNIDADES: str(total_unidades),
        CIERRE_IMPORTE_TOTAL: "{:.2f}".format(importe_total),
    }

    repo_registrar_cierre(cierre)
    limpiar_ventas_del_dia()

    return cierre
