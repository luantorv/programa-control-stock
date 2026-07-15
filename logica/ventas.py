# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import datetime
from persistencia.productos_repo import buscar_producto_por_codigo, actualizar_producto
from persistencia.ventas_repo import (
    leer_ventas_del_dia,
    registrar_venta as repo_registrar_venta,
    registrar_cierre as repo_registrar_cierre,
)
from modelos.esquemas import (
    PRODUCTO_NOMBRE, PRODUCTO_PRECIO, PRODUCTO_STOCK,
    VENTA_FECHA_HORA, VENTA_NRO_FACTURA, VENTA_USUARIO,
    VENTA_CODIGO, VENTA_CANTIDAD, VENTA_PRECIO_UNIT, VENTA_SUBTOTAL,
    CIERRE_FECHA, CIERRE_TOTAL_VENTAS, CIERRE_TOTAL_UNIDADES, CIERRE_IMPORTE_TOTAL,
)


def registrar_venta(codigo, cantidad, nombre_usuario):
    if cantidad <= 0:
        return "La cantidad a vender debe ser mayor a cero.", 0.0

    producto = buscar_producto_por_codigo(codigo)
    if producto is None:
        return "No existe un producto con el código " + codigo + ".", 0.0

    stock_actual = int(producto[PRODUCTO_STOCK])
    if cantidad > stock_actual:
        return "Stock insuficiente. Disponible: " + str(stock_actual) + " unidades.", 0.0

    precio_unitario = float(producto[PRODUCTO_PRECIO])
    subtotal = precio_unitario * cantidad

    producto[PRODUCTO_STOCK] = str(stock_actual - cantidad)
    actualizar_producto(producto)

    ventas_existentes = leer_ventas_del_dia()
    nro_factura = len(ventas_existentes) + 1

    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    venta = {
        VENTA_FECHA_HORA: fecha_hora,
        VENTA_NRO_FACTURA: str(nro_factura),
        VENTA_USUARIO: nombre_usuario,
        VENTA_CODIGO: codigo,
        VENTA_CANTIDAD: str(cantidad),
        VENTA_PRECIO_UNIT: "{:.2f}".format(precio_unitario),
        VENTA_SUBTOTAL: "{:.2f}".format(subtotal),
    }
    repo_registrar_venta(venta)

    return "", subtotal


def ejecutar_cierre_diario():
    ventas = leer_ventas_del_dia()

    total_ventas = len(ventas)
    total_unidades = 0
    importe_total = 0.0

    for venta in ventas:
        total_unidades = total_unidades + int(venta[VENTA_CANTIDAD])
        importe_total = importe_total + float(venta[VENTA_SUBTOTAL])

    fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")

    cierre = {
        CIERRE_FECHA: fecha_hoy,
        CIERRE_TOTAL_VENTAS: str(total_ventas),
        CIERRE_TOTAL_UNIDADES: str(total_unidades),
        CIERRE_IMPORTE_TOTAL: "{:.2f}".format(importe_total),
    }

    repo_registrar_cierre(cierre)

    return cierre
