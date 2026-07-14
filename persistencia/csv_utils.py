# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import csv
import os

def leer_csv(ruta):
    if not os.path.exists(ruta):
        return []

    lista_de_filas = []
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            lista_de_filas.append(fila)

    return lista_de_filas

def escribir_csv_atomico(ruta, filas, encabezado):
    ruta_temporal = ruta + ".tmp"

    with open(ruta_temporal, 'w', newline='', encoding='utf-8') as archivo_temporal:
        escritor = csv.DictWriter(archivo_temporal, fieldnames=encabezado)
        escritor.writeheader()
        for fila in filas:
            escritor.writerow(fila)

    os.replace(ruta_temporal, ruta)
