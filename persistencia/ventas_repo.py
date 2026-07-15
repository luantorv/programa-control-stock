# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
import datetime
from persistencia.csv_utils import leer_csv, escribir_csv_atomico
from persistencia.rutas import directorio_datos
from modelos.esquemas import ENCABEZADO_VENTAS, ENCABEZADO_CIERRE

def _ruta_ventas_hoy():
    fecha_hoy = datetime.date.today().strftime("%Y%m%d")
    return os.path.join(directorio_datos(), 'ventas_' + fecha_hoy + '.csv')

def _ruta_cierre():
    return os.path.join(directorio_datos(), 'cierre_diario.csv')

def leer_ventas_del_dia():
    return leer_csv(_ruta_ventas_hoy())

def registrar_venta(venta):
    ventas = leer_ventas_del_dia()
    ventas.append(venta)
    escribir_csv_atomico(_ruta_ventas_hoy(), ventas, ENCABEZADO_VENTAS)

def leer_cierres():
    return leer_csv(_ruta_cierre())

def registrar_cierre(cierre):
    cierres = leer_cierres()
    cierres.append(cierre)
    escribir_csv_atomico(_ruta_cierre(), cierres, ENCABEZADO_CIERRE)
