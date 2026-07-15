# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import re

# Formato acordado: entre 1 y 3 letras mayúsculas seguidas de exactamente 3 dígitos.
# Ejemplos válidos: P001, AB123, XYZ999
PATRON_CODIGO_PRODUCTO = r'^[A-Z]{1,3}\d{3}$'

def codigo_es_valido(codigo):
    resultado = re.match(PATRON_CODIGO_PRODUCTO, codigo)
    return resultado is not None
