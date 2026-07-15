# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import unittest
from unittest.mock import patch
from logica.productos import (
    buscar_producto,
    consultar_producto,
    dar_de_alta_producto,
    dar_de_baja_producto,
    modificar_producto,
    ajustar_stock,
)

PRODUCTO_EJEMPLO = {
    'codigo': 'LA EC A1',
    'nombre': 'Leche entera 1L',
    'grupo': 'Lácteos',
    'precio': '1.50',
    'stock': '100',
}


class TestBuscarProducto(unittest.TestCase):

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_producto_existente_devuelve_el_producto(self, mock_buscar):
        mock_buscar.return_value = PRODUCTO_EJEMPLO
        resultado = buscar_producto('LA EC A1')
        self.assertEqual(resultado, PRODUCTO_EJEMPLO)

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_producto_inexistente_devuelve_none(self, mock_buscar):
        mock_buscar.return_value = None
        resultado = buscar_producto('XX YY 99')
        self.assertIsNone(resultado)


class TestConsultarProducto(unittest.TestCase):

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_busqueda_por_codigo_exacto_devuelve_lista_con_un_elemento(self, mock_buscar):
        mock_buscar.return_value = PRODUCTO_EJEMPLO
        resultado = consultar_producto('LA EC A1')
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0], PRODUCTO_EJEMPLO)

    @patch('logica.productos.buscar_productos_por_nombre')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_busqueda_por_nombre_cuando_codigo_no_coincide(self, mock_por_codigo, mock_por_nombre):
        mock_por_codigo.return_value = None
        mock_por_nombre.return_value = [PRODUCTO_EJEMPLO]
        resultado = consultar_producto('leche')
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0], PRODUCTO_EJEMPLO)

    @patch('logica.productos.buscar_productos_por_nombre')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_busqueda_sin_resultados_devuelve_lista_vacia(self, mock_por_codigo, mock_por_nombre):
        mock_por_codigo.return_value = None
        mock_por_nombre.return_value = []
        resultado = consultar_producto('termino_inexistente')
        self.assertEqual(resultado, [])

    @patch('logica.productos.buscar_productos_por_nombre')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_busqueda_por_nombre_puede_devolver_varios(self, mock_por_codigo, mock_por_nombre):
        segundo_producto = dict(PRODUCTO_EJEMPLO)
        segundo_producto['codigo'] = 'LA EC A2'
        segundo_producto['nombre'] = 'Leche descremada 1L'
        mock_por_codigo.return_value = None
        mock_por_nombre.return_value = [PRODUCTO_EJEMPLO, segundo_producto]
        resultado = consultar_producto('leche')
        self.assertEqual(len(resultado), 2)


class TestDarDeAltaProducto(unittest.TestCase):

    @patch('logica.productos.agregar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_producto_valido_devuelve_cadena_vacia(self, mock_buscar, mock_agregar):
        mock_buscar.return_value = None
        resultado = dar_de_alta_producto('LA EC A1', 'Leche entera 1L', 'Lácteos', 1.50, 100)
        self.assertEqual(resultado, '')

    @patch('logica.productos.agregar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_producto_valido_llama_agregar_producto(self, mock_buscar, mock_agregar):
        mock_buscar.return_value = None
        dar_de_alta_producto('LA EC A1', 'Leche entera 1L', 'Lácteos', 1.50, 100)
        mock_agregar.assert_called_once()

    @patch('logica.productos.agregar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_stock_cero_es_valido(self, mock_buscar, mock_agregar):
        mock_buscar.return_value = None
        resultado = dar_de_alta_producto('LA EC A1', 'Leche entera 1L', 'Lácteos', 1.50, 0)
        self.assertEqual(resultado, '')

    def test_codigo_con_formato_invalido_devuelve_error(self):
        resultado = dar_de_alta_producto('P001', 'Leche', 'Lácteos', 1.50, 100)
        self.assertNotEqual(resultado, '')

    def test_nombre_vacio_devuelve_error(self):
        resultado = dar_de_alta_producto('LA EC A1', '', 'Lácteos', 1.50, 100)
        self.assertNotEqual(resultado, '')

    def test_grupo_vacio_devuelve_error(self):
        resultado = dar_de_alta_producto('LA EC A1', 'Leche', '', 1.50, 100)
        self.assertNotEqual(resultado, '')

    def test_precio_cero_devuelve_error(self):
        resultado = dar_de_alta_producto('LA EC A1', 'Leche', 'Lácteos', 0, 100)
        self.assertNotEqual(resultado, '')

    def test_precio_negativo_devuelve_error(self):
        resultado = dar_de_alta_producto('LA EC A1', 'Leche', 'Lácteos', -1.0, 100)
        self.assertNotEqual(resultado, '')

    def test_stock_negativo_devuelve_error(self):
        resultado = dar_de_alta_producto('LA EC A1', 'Leche', 'Lácteos', 1.50, -1)
        self.assertNotEqual(resultado, '')

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_codigo_duplicado_devuelve_error(self, mock_buscar):
        mock_buscar.return_value = PRODUCTO_EJEMPLO
        resultado = dar_de_alta_producto('LA EC A1', 'Otro producto', 'Bebidas', 2.00, 50)
        self.assertNotEqual(resultado, '')

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_codigo_duplicado_no_llama_agregar(self, mock_buscar):
        mock_buscar.return_value = PRODUCTO_EJEMPLO
        with patch('logica.productos.agregar_producto') as mock_agregar:
            dar_de_alta_producto('LA EC A1', 'Otro', 'Bebidas', 2.00, 50)
            mock_agregar.assert_not_called()


class TestDarDeBajaProducto(unittest.TestCase):

    @patch('logica.productos.eliminar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_baja_de_producto_existente_devuelve_cadena_vacia(self, mock_buscar, mock_eliminar):
        mock_buscar.return_value = PRODUCTO_EJEMPLO
        resultado = dar_de_baja_producto('LA EC A1')
        self.assertEqual(resultado, '')

    @patch('logica.productos.eliminar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_baja_llama_eliminar_con_el_codigo_correcto(self, mock_buscar, mock_eliminar):
        mock_buscar.return_value = PRODUCTO_EJEMPLO
        dar_de_baja_producto('LA EC A1')
        mock_eliminar.assert_called_once_with('LA EC A1')

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_baja_de_producto_inexistente_devuelve_error(self, mock_buscar):
        mock_buscar.return_value = None
        resultado = dar_de_baja_producto('XX YY 99')
        self.assertNotEqual(resultado, '')

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_baja_de_producto_inexistente_no_llama_eliminar(self, mock_buscar):
        mock_buscar.return_value = None
        with patch('logica.productos.eliminar_producto') as mock_eliminar:
            dar_de_baja_producto('XX YY 99')
            mock_eliminar.assert_not_called()


class TestModificarProducto(unittest.TestCase):

    @patch('logica.productos.actualizar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_modificacion_valida_devuelve_cadena_vacia(self, mock_buscar, mock_actualizar):
        mock_buscar.return_value = dict(PRODUCTO_EJEMPLO)
        resultado = modificar_producto('LA EC A1', 'Nuevo nombre', 'Nuevo grupo', 2.00, 50)
        self.assertEqual(resultado, '')

    @patch('logica.productos.actualizar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_modificacion_llama_actualizar(self, mock_buscar, mock_actualizar):
        mock_buscar.return_value = dict(PRODUCTO_EJEMPLO)
        modificar_producto('LA EC A1', 'Nuevo nombre', 'Nuevo grupo', 2.00, 50)
        mock_actualizar.assert_called_once()

    def test_nombre_vacio_devuelve_error(self):
        resultado = modificar_producto('LA EC A1', '', 'Lácteos', 1.50, 100)
        self.assertNotEqual(resultado, '')

    def test_grupo_vacio_devuelve_error(self):
        resultado = modificar_producto('LA EC A1', 'Leche', '', 1.50, 100)
        self.assertNotEqual(resultado, '')

    def test_precio_cero_devuelve_error(self):
        resultado = modificar_producto('LA EC A1', 'Leche', 'Lácteos', 0, 100)
        self.assertNotEqual(resultado, '')

    def test_precio_negativo_devuelve_error(self):
        resultado = modificar_producto('LA EC A1', 'Leche', 'Lácteos', -5.0, 100)
        self.assertNotEqual(resultado, '')

    def test_stock_negativo_devuelve_error(self):
        resultado = modificar_producto('LA EC A1', 'Leche', 'Lácteos', 1.50, -10)
        self.assertNotEqual(resultado, '')

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_producto_inexistente_devuelve_error(self, mock_buscar):
        mock_buscar.return_value = None
        resultado = modificar_producto('XX YY 99', 'Nombre', 'Grupo', 1.50, 10)
        self.assertNotEqual(resultado, '')

    @patch('logica.productos.actualizar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_stock_cero_es_valido(self, mock_buscar, mock_actualizar):
        mock_buscar.return_value = dict(PRODUCTO_EJEMPLO)
        resultado = modificar_producto('LA EC A1', 'Leche', 'Lácteos', 1.50, 0)
        self.assertEqual(resultado, '')


class TestAjustarStock(unittest.TestCase):

    @patch('logica.productos.actualizar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_ajuste_valido_devuelve_cadena_vacia(self, mock_buscar, mock_actualizar):
        mock_buscar.return_value = dict(PRODUCTO_EJEMPLO)
        resultado = ajustar_stock('LA EC A1', 200)
        self.assertEqual(resultado, '')

    @patch('logica.productos.actualizar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_ajuste_a_cero_es_valido(self, mock_buscar, mock_actualizar):
        mock_buscar.return_value = dict(PRODUCTO_EJEMPLO)
        resultado = ajustar_stock('LA EC A1', 0)
        self.assertEqual(resultado, '')

    @patch('logica.productos.actualizar_producto')
    @patch('logica.productos.buscar_producto_por_codigo')
    def test_ajuste_actualiza_stock_correctamente(self, mock_buscar, mock_actualizar):
        producto = dict(PRODUCTO_EJEMPLO)
        mock_buscar.return_value = producto
        ajustar_stock('LA EC A1', 250)
        producto_guardado = mock_actualizar.call_args[0][0]
        self.assertEqual(producto_guardado['stock'], '250')

    def test_cantidad_negativa_devuelve_error(self):
        resultado = ajustar_stock('LA EC A1', -1)
        self.assertNotEqual(resultado, '')

    @patch('logica.productos.buscar_producto_por_codigo')
    def test_producto_inexistente_devuelve_error(self, mock_buscar):
        mock_buscar.return_value = None
        resultado = ajustar_stock('XX YY 99', 50)
        self.assertNotEqual(resultado, '')

    def test_cantidad_negativa_no_llama_actualizar(self):
        with patch('logica.productos.actualizar_producto') as mock_actualizar:
            ajustar_stock('LA EC A1', -5)
            mock_actualizar.assert_not_called()


if __name__ == '__main__':
    unittest.main()
