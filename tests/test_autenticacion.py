# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import unittest
from unittest.mock import patch
from logica.autenticacion import hashear_contrasena, autenticar


class TestHashearContrasena(unittest.TestCase):

    def test_retorna_string(self):
        resultado = hashear_contrasena("cualquier_texto")
        self.assertIsInstance(resultado, str)

    def test_longitud_es_64_caracteres(self):
        resultado = hashear_contrasena("cualquier_texto")
        self.assertEqual(len(resultado), 64)

    def test_es_determinista(self):
        primera_llamada = hashear_contrasena("super123")
        segunda_llamada = hashear_contrasena("super123")
        self.assertEqual(primera_llamada, segunda_llamada)

    def test_contrasenas_distintas_producen_hashes_distintos(self):
        hash_supervisor = hashear_contrasena("super123")
        hash_cajero = hashear_contrasena("cajero123")
        self.assertNotEqual(hash_supervisor, hash_cajero)

    def test_contrasena_vacia_produce_hash_valido(self):
        resultado = hashear_contrasena("")
        self.assertEqual(len(resultado), 64)

    def test_hash_conocido_de_super123(self):
        # Hash precalculado que coincide con el almacenado en datos/users.csv
        hash_esperado = "4e4c56e4a15f89f05c2f4c72613da2a18c9665d4f0d6acce16415eb06f9be776"
        self.assertEqual(hashear_contrasena("super123"), hash_esperado)

    def test_hash_conocido_de_cajero123(self):
        hash_esperado = "1ed4353e845e2e537e017c0fac3a0d402d231809b7989e90da15191c1148a93f"
        self.assertEqual(hashear_contrasena("cajero123"), hash_esperado)


class TestAutenticar(unittest.TestCase):

    def _usuarios_de_prueba(self):
        return [
            {
                'username': 'supervisor',
                'hash': hashear_contrasena('super123'),
                'rol': 'supervisor',
            },
            {
                'username': 'cajero',
                'hash': hashear_contrasena('cajero123'),
                'rol': 'cajero',
            },
        ]

    @patch('logica.autenticacion.leer_usuarios')
    def test_credenciales_correctas_devuelve_rol_supervisor(self, mock_leer):
        mock_leer.return_value = self._usuarios_de_prueba()
        resultado = autenticar('supervisor', 'super123')
        self.assertEqual(resultado, 'supervisor')

    @patch('logica.autenticacion.leer_usuarios')
    def test_credenciales_correctas_devuelve_rol_cajero(self, mock_leer):
        mock_leer.return_value = self._usuarios_de_prueba()
        resultado = autenticar('cajero', 'cajero123')
        self.assertEqual(resultado, 'cajero')

    @patch('logica.autenticacion.leer_usuarios')
    def test_contrasena_incorrecta_devuelve_none(self, mock_leer):
        mock_leer.return_value = self._usuarios_de_prueba()
        resultado = autenticar('supervisor', 'contrasena_incorrecta')
        self.assertIsNone(resultado)

    @patch('logica.autenticacion.leer_usuarios')
    def test_usuario_inexistente_devuelve_none(self, mock_leer):
        mock_leer.return_value = self._usuarios_de_prueba()
        resultado = autenticar('usuario_desconocido', 'super123')
        self.assertIsNone(resultado)

    @patch('logica.autenticacion.leer_usuarios')
    def test_lista_vacia_de_usuarios_devuelve_none(self, mock_leer):
        mock_leer.return_value = []
        resultado = autenticar('supervisor', 'super123')
        self.assertIsNone(resultado)

    @patch('logica.autenticacion.leer_usuarios')
    def test_contrasena_vacia_devuelve_none(self, mock_leer):
        mock_leer.return_value = self._usuarios_de_prueba()
        resultado = autenticar('supervisor', '')
        self.assertIsNone(resultado)

    @patch('logica.autenticacion.leer_usuarios')
    def test_usuario_correcto_contrasena_de_otro_usuario_devuelve_none(self, mock_leer):
        mock_leer.return_value = self._usuarios_de_prueba()
        resultado = autenticar('supervisor', 'cajero123')
        self.assertIsNone(resultado)

    @patch('logica.autenticacion.leer_usuarios')
    def test_nombre_usuario_distingue_mayusculas(self, mock_leer):
        mock_leer.return_value = self._usuarios_de_prueba()
        resultado = autenticar('Supervisor', 'super123')
        self.assertIsNone(resultado)


if __name__ == '__main__':
    unittest.main()
