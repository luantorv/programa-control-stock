# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
import datetime
from persistencia.csv_utils import leer_csv, escribir_csv_atomico
from modelos.esquemas import ENCABEZADO_VENTAS, ENCABEZADO_CIERRE

_DIRECTORIO_DATOS = os.path.join(os.path.dirname(__file__), '..', 'datos')
_RUTA_CIERRE = os.path.join(_DIRECTORIO_DATOS, 'cierre_diario.csv')

def _ruta_ventas_hoy():
    fecha_hoy = datetime.date.today().strftime("%Y%m%d")
    return os.path.join(_DIRECTORIO_DATOS, 'ventas_' + fecha_hoy + '.csv')

def leer_ventas_del_dia():
    return leer_csv(_ruta_ventas_hoy())

def registrar_venta(venta):
    ventas = leer_ventas_del_dia()
    ventas.append(venta)
    escribir_csv_atomico(_ruta_ventas_hoy(), ventas, ENCABEZADO_VENTAS)

def leer_cierres():
    return leer_csv(_RUTA_CIERRE)

def registrar_cierre(cierre):
    cierres = leer_cierres()
    cierres.append(cierre)
    escribir_csv_atomico(_RUTA_CIERRE, cierres, ENCABEZADO_CIERRE)
