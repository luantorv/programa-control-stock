# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os

_VARIABLE_DE_ENTORNO = "CONTROL_STOCK_DATOS_DIR"
_DIRECTORIO_PREDETERMINADO = os.path.join(os.path.dirname(__file__), '..', 'datos')

def directorio_datos():
    ruta_desde_entorno = os.environ.get(_VARIABLE_DE_ENTORNO)
    if ruta_desde_entorno:
        directorio = ruta_desde_entorno
    else:
        directorio = _DIRECTORIO_PREDETERMINADO
    os.makedirs(directorio, exist_ok=True)
    return directorio
