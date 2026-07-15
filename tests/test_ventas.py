# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import unittest
from unittest.mock import patch
from logica.ventas import registrar_venta, ejecutar_cierre_diario, obtener_ventas_del_dia

PRODUCTO_CON_STOCK = {
    'codigo': 'LA EC A1',
    'nombre': 'Leche entera 1L',
    'grupo': 'Lácteos',
    'precio': '1.50',
    'stock': '100',
}

VENTA_EJEMPLO = {
    'fecha_hora': '2026-07-14 10:00:00',
    'nro_factura': '1',
    'usuario': 'cajero',
    'codigo': 'LA EC A1',
    'cantidad': '2',
    'precio_unit': '1.50',
    'subtotal': '3.00',
}


class TestObtenerVentasDelDia(unittest.TestCase):

    @patch('logica.ventas.leer_ventas_del_dia')
    def test_devuelve_lista_con_ventas(self, mock_leer):
        mock_leer.return_value = [VENTA_EJEMPLO]
        resultado = obtener_ventas_del_dia()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0], VENTA_EJEMPLO)

    @patch('logica.ventas.leer_ventas_del_dia')
    def test_devuelve_lista_vacia_si_no_hay_ventas(self, mock_leer):
        mock_leer.return_value = []
        resultado = obtener_ventas_del_dia()
        self.assertEqual(resultado, [])


class TestRegistrarVenta(unittest.TestCase):

    # --- Validaciones que no requieren acceso a datos ---

    def test_cantidad_cero_devuelve_error(self):
        error, total = registrar_venta('LA EC A1', 0, 'cajero')
        self.assertNotEqual(error, '')
        self.assertEqual(total, 0.0)

    def test_cantidad_negativa_devuelve_error(self):
        error, total = registrar_venta('LA EC A1', -3, 'cajero')
        self.assertNotEqual(error, '')
        self.assertEqual(total, 0.0)

    # --- Validaciones que requieren consultar productos ---

    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_producto_inexistente_devuelve_error(self, mock_buscar):
        mock_buscar.return_value = None
        error, total = registrar_venta('XX YY 99', 1, 'cajero')
        self.assertNotEqual(error, '')
        self.assertEqual(total, 0.0)

    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_stock_insuficiente_devuelve_error(self, mock_buscar):
        producto_poco_stock = dict(PRODUCTO_CON_STOCK)
        producto_poco_stock['stock'] = '3'
        mock_buscar.return_value = producto_poco_stock
        error, total = registrar_venta('LA EC A1', 5, 'cajero')
        self.assertNotEqual(error, '')
        self.assertEqual(total, 0.0)

    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_stock_insuficiente_no_modifica_datos(self, mock_buscar):
        producto_poco_stock = dict(PRODUCTO_CON_STOCK)
        producto_poco_stock['stock'] = '3'
        mock_buscar.return_value = producto_poco_stock
        with patch('logica.ventas.actualizar_producto') as mock_actualizar:
            registrar_venta('LA EC A1', 5, 'cajero')
            mock_actualizar.assert_not_called()

    # --- Ventas exitosas ---

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_venta_valida_devuelve_cadena_vacia(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        mock_buscar.return_value = dict(PRODUCTO_CON_STOCK)
        mock_leer.return_value = []
        error, total = registrar_venta('LA EC A1', 2, 'cajero')
        self.assertEqual(error, '')

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_venta_valida_devuelve_subtotal_correcto(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        mock_buscar.return_value = dict(PRODUCTO_CON_STOCK)
        mock_leer.return_value = []
        error, total = registrar_venta('LA EC A1', 2, 'cajero')
        self.assertAlmostEqual(total, 3.0)

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_venta_con_stock_exacto_es_exitosa(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        producto = dict(PRODUCTO_CON_STOCK)
        producto['stock'] = '5'
        mock_buscar.return_value = producto
        mock_leer.return_value = []
        error, total = registrar_venta('LA EC A1', 5, 'cajero')
        self.assertEqual(error, '')

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_venta_descuenta_stock_correctamente(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        producto = dict(PRODUCTO_CON_STOCK)
        mock_buscar.return_value = producto
        mock_leer.return_value = []
        registrar_venta('LA EC A1', 10, 'cajero')
        producto_guardado = mock_actualizar.call_args[0][0]
        self.assertEqual(producto_guardado['stock'], '90')

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_nro_factura_es_secuencial(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        mock_buscar.return_value = dict(PRODUCTO_CON_STOCK)
        mock_leer.return_value = [VENTA_EJEMPLO, VENTA_EJEMPLO]
        registrar_venta('LA EC A1', 1, 'cajero')
        venta_guardada = mock_repo.call_args[0][0]
        self.assertEqual(venta_guardada['nro_factura'], '3')

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_primera_venta_del_dia_tiene_nro_factura_uno(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        mock_buscar.return_value = dict(PRODUCTO_CON_STOCK)
        mock_leer.return_value = []
        registrar_venta('LA EC A1', 1, 'cajero')
        venta_guardada = mock_repo.call_args[0][0]
        self.assertEqual(venta_guardada['nro_factura'], '1')

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_venta_registra_el_usuario_correcto(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        mock_buscar.return_value = dict(PRODUCTO_CON_STOCK)
        mock_leer.return_value = []
        registrar_venta('LA EC A1', 1, 'cajero_prueba')
        venta_guardada = mock_repo.call_args[0][0]
        self.assertEqual(venta_guardada['usuario'], 'cajero_prueba')

    @patch('logica.ventas.repo_registrar_venta')
    @patch('logica.ventas.leer_ventas_del_dia')
    @patch('logica.ventas.actualizar_producto')
    @patch('logica.ventas.buscar_producto_por_codigo')
    def test_venta_registra_el_codigo_del_producto(self, mock_buscar, mock_actualizar, mock_leer, mock_repo):
        mock_buscar.return_value = dict(PRODUCTO_CON_STOCK)
        mock_leer.return_value = []
        registrar_venta('LA EC A1', 1, 'cajero')
        venta_guardada = mock_repo.call_args[0][0]
        self.assertEqual(venta_guardada['codigo'], 'LA EC A1')


class TestEjecutarCierreDiario(unittest.TestCase):

    @patch('logica.ventas.repo_registrar_cierre')
    @patch('logica.ventas.leer_ventas_del_dia')
    def test_cierre_sin_ventas_devuelve_ceros(self, mock_leer, mock_cierre):
        mock_leer.return_value = []
        cierre = ejecutar_cierre_diario()
        self.assertEqual(cierre['total_ventas'], '0')
        self.assertEqual(cierre['total_unidades'], '0')
        self.assertEqual(cierre['importe_total'], '0.00')

    @patch('logica.ventas.repo_registrar_cierre')
    @patch('logica.ventas.leer_ventas_del_dia')
    def test_cierre_suma_ventas_correctamente(self, mock_leer, mock_cierre):
        ventas = [
            {'cantidad': '2', 'subtotal': '3.00'},
            {'cantidad': '1', 'subtotal': '5.00'},
            {'cantidad': '3', 'subtotal': '9.00'},
        ]
        mock_leer.return_value = ventas
        cierre = ejecutar_cierre_diario()
        self.assertEqual(cierre['total_ventas'], '3')
        self.assertEqual(cierre['total_unidades'], '6')
        self.assertEqual(cierre['importe_total'], '17.00')

    @patch('logica.ventas.repo_registrar_cierre')
    @patch('logica.ventas.leer_ventas_del_dia')
    def test_cierre_llama_registrar_cierre_una_vez(self, mock_leer, mock_cierre):
        mock_leer.return_value = []
        ejecutar_cierre_diario()
        mock_cierre.assert_called_once()

    @patch('logica.ventas.repo_registrar_cierre')
    @patch('logica.ventas.leer_ventas_del_dia')
    def test_cierre_devuelve_dict_con_todas_las_claves(self, mock_leer, mock_cierre):
        mock_leer.return_value = []
        cierre = ejecutar_cierre_diario()
        self.assertIn('fecha', cierre)
        self.assertIn('total_ventas', cierre)
        self.assertIn('total_unidades', cierre)
        self.assertIn('importe_total', cierre)

    @patch('logica.ventas.repo_registrar_cierre')
    @patch('logica.ventas.leer_ventas_del_dia')
    def test_cierre_con_una_sola_venta(self, mock_leer, mock_cierre):
        mock_leer.return_value = [{'cantidad': '5', 'subtotal': '7.50'}]
        cierre = ejecutar_cierre_diario()
        self.assertEqual(cierre['total_ventas'], '1')
        self.assertEqual(cierre['total_unidades'], '5')
        self.assertEqual(cierre['importe_total'], '7.50')


if __name__ == '__main__':
    unittest.main()
