# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
from persistencia.csv_utils import leer_csv, escribir_csv_atomico
from modelos.esquemas import ENCABEZADO_VENTAS, ENCABEZADO_CIERRE

_RUTA_VENTAS = os.path.join(os.path.dirname(__file__), '..', 'datos', 'ventas_dia.csv')
_RUTA_CIERRE = os.path.join(os.path.dirname(__file__), '..', 'datos', 'cierre_diario.csv')


def leer_ventas_del_dia():
    return leer_csv(_RUTA_VENTAS)


def registrar_venta(venta):
    ventas = leer_ventas_del_dia()
    ventas.append(venta)
    escribir_csv_atomico(_RUTA_VENTAS, ventas, ENCABEZADO_VENTAS)


def limpiar_ventas_del_dia():
    escribir_csv_atomico(_RUTA_VENTAS, [], ENCABEZADO_VENTAS)


def leer_cierres():
    return leer_csv(_RUTA_CIERRE)


def registrar_cierre(cierre):
    cierres = leer_cierres()
    cierres.append(cierre)
    escribir_csv_atomico(_RUTA_CIERRE, cierres, ENCABEZADO_CIERRE)
