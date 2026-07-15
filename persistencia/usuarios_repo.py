# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
from persistencia.csv_utils import leer_csv

_RUTA_USUARIOS = os.path.join(os.path.dirname(__file__), '..', 'datos', 'users.csv')

def leer_usuarios():
    return leer_csv(_RUTA_USUARIOS)
