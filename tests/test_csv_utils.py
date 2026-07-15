# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import os
import tempfile
import unittest
from persistencia.csv_utils import leer_csv, escribir_csv_atomico


class TestLeerCsv(unittest.TestCase):

    def test_archivo_inexistente_devuelve_lista_vacia(self):
        resultado = leer_csv('/ruta/que/no/existe/nunca/archivo.csv')
        self.assertEqual(resultado, [])

    def test_archivo_solo_con_encabezado_devuelve_lista_vacia(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as archivo:
            archivo.write('nombre,precio,stock\n')
            ruta = archivo.name
        try:
            resultado = leer_csv(ruta)
            self.assertEqual(resultado, [])
        finally:
            os.remove(ruta)

    def test_archivo_con_una_fila_devuelve_lista_con_un_elemento(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as archivo:
            archivo.write('nombre,precio\nLeche,1.50\n')
            ruta = archivo.name
        try:
            resultado = leer_csv(ruta)
            self.assertEqual(len(resultado), 1)
        finally:
            os.remove(ruta)

    def test_archivo_con_varias_filas_devuelve_todos_los_elementos(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as archivo:
            archivo.write('nombre,precio\nLeche,1.50\nPan,0.80\nAzucar,2.00\n')
            ruta = archivo.name
        try:
            resultado = leer_csv(ruta)
            self.assertEqual(len(resultado), 3)
        finally:
            os.remove(ruta)

    def test_los_valores_devueltos_son_strings(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as archivo:
            archivo.write('cantidad,precio\n42,1.50\n')
            ruta = archivo.name
        try:
            resultado = leer_csv(ruta)
            self.assertIsInstance(resultado[0]['cantidad'], str)
            self.assertIsInstance(resultado[0]['precio'], str)
        finally:
            os.remove(ruta)

    def test_las_claves_coinciden_con_el_encabezado(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as archivo:
            archivo.write('codigo,nombre,grupo\nLA EC A1,Leche,Lácteos\n')
            ruta = archivo.name
        try:
            resultado = leer_csv(ruta)
            self.assertIn('codigo', resultado[0])
            self.assertIn('nombre', resultado[0])
            self.assertIn('grupo', resultado[0])
        finally:
            os.remove(ruta)

    def test_los_valores_leidos_son_correctos(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as archivo:
            archivo.write('nombre,precio\nLeche,1.50\nPan,0.80\n')
            ruta = archivo.name
        try:
            resultado = leer_csv(ruta)
            self.assertEqual(resultado[0]['nombre'], 'Leche')
            self.assertEqual(resultado[0]['precio'], '1.50')
            self.assertEqual(resultado[1]['nombre'], 'Pan')
            self.assertEqual(resultado[1]['precio'], '0.80')
        finally:
            os.remove(ruta)


class TestEscribirCsvAtomico(unittest.TestCase):

    def setUp(self):
        self.directorio_temporal = tempfile.mkdtemp()
        self.ruta_archivo = os.path.join(self.directorio_temporal, 'prueba.csv')

    def tearDown(self):
        if os.path.exists(self.ruta_archivo):
            os.remove(self.ruta_archivo)
        ruta_temporal = self.ruta_archivo + '.tmp'
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
        os.rmdir(self.directorio_temporal)

    def test_crea_el_archivo_destino(self):
        escribir_csv_atomico(self.ruta_archivo, [], ['col1', 'col2'])
        self.assertTrue(os.path.exists(self.ruta_archivo))

    def test_devuelve_true_en_escritura_exitosa(self):
        resultado = escribir_csv_atomico(self.ruta_archivo, [], ['col1'])
        self.assertTrue(resultado)

    def test_no_deja_archivo_temporal_tras_exito(self):
        escribir_csv_atomico(self.ruta_archivo, [], ['col1'])
        self.assertFalse(os.path.exists(self.ruta_archivo + '.tmp'))

    def test_escribe_una_fila_y_se_puede_leer(self):
        filas = [{'nombre': 'Leche', 'precio': '1.50'}]
        escribir_csv_atomico(self.ruta_archivo, filas, ['nombre', 'precio'])
        resultado = leer_csv(self.ruta_archivo)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['nombre'], 'Leche')
        self.assertEqual(resultado[0]['precio'], '1.50')

    def test_escribe_multiples_filas(self):
        filas = [
            {'nombre': 'Producto A', 'precio': '1.00'},
            {'nombre': 'Producto B', 'precio': '2.00'},
            {'nombre': 'Producto C', 'precio': '3.00'},
        ]
        escribir_csv_atomico(self.ruta_archivo, filas, ['nombre', 'precio'])
        resultado = leer_csv(self.ruta_archivo)
        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado[2]['nombre'], 'Producto C')

    def test_sobreescribe_el_contenido_anterior(self):
        filas_originales = [{'col1': 'valor_original'}]
        escribir_csv_atomico(self.ruta_archivo, filas_originales, ['col1'])
        filas_nuevas = [{'col1': 'valor_nuevo'}]
        escribir_csv_atomico(self.ruta_archivo, filas_nuevas, ['col1'])
        resultado = leer_csv(self.ruta_archivo)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['col1'], 'valor_nuevo')

    def test_escribir_lista_vacia_deja_solo_encabezado(self):
        escribir_csv_atomico(self.ruta_archivo, [], ['col1', 'col2'])
        resultado = leer_csv(self.ruta_archivo)
        self.assertEqual(resultado, [])

    def test_preserva_el_orden_de_las_columnas(self):
        filas = [{'z_ultima': 'Z', 'a_primera': 'A'}]
        encabezado = ['a_primera', 'z_ultima']
        escribir_csv_atomico(self.ruta_archivo, filas, encabezado)
        with open(self.ruta_archivo, encoding='utf-8') as archivo:
            primera_linea = archivo.readline().strip()
        self.assertEqual(primera_linea, 'a_primera,z_ultima')


if __name__ == '__main__':
    unittest.main()
