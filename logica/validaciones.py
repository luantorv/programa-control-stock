# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import re

# Formato acordado: 2 letras (marca) + espacio + 2 letras (grupo) + espacio + 2 alfanuméricos (tipo).
# Ejemplos válidos: LA EC A1, AB CD 12, XX YY 3Z
PATRON_CODIGO_PRODUCTO = r'^[A-Z]{2}\s[A-Z]{2}\s[A-Z0-9]{2}$'

def codigo_es_valido(codigo):
    resultado = re.match(PATRON_CODIGO_PRODUCTO, codigo)
    return resultado is not None
