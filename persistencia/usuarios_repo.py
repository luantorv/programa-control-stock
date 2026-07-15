# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
from persistencia.csv_utils import leer_csv
from persistencia.rutas import directorio_datos

def leer_usuarios():
    ruta = os.path.join(directorio_datos(), 'users.csv')
    return leer_csv(ruta)
