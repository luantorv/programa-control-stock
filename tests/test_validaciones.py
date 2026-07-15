# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import unittest
from logica.validaciones import codigo_es_valido


class TestCodigoEsValido(unittest.TestCase):

    # --- Formatos válidos ---

    def test_codigo_valido_con_digitos_en_tipo(self):
        self.assertTrue(codigo_es_valido("AB CD 12"))

    def test_codigo_valido_con_letras_en_tipo(self):
        self.assertTrue(codigo_es_valido("AB CD AB"))

    def test_codigo_valido_alfanumerico_mixto_en_tipo(self):
        self.assertTrue(codigo_es_valido("LA EC A1"))

    def test_codigo_valido_todo_letras_mayusculas(self):
        self.assertTrue(codigo_es_valido("ZZ ZZ ZZ"))

    def test_codigo_valido_digito_al_inicio_del_tipo(self):
        self.assertTrue(codigo_es_valido("AB CD 1A"))

    # --- Errores en la sección de marca (primeras 2 letras) ---

    def test_codigo_invalido_marca_una_sola_letra(self):
        self.assertFalse(codigo_es_valido("A CD 12"))

    def test_codigo_invalido_marca_tres_letras(self):
        self.assertFalse(codigo_es_valido("ABC CD 12"))

    def test_codigo_invalido_marca_con_digito(self):
        self.assertFalse(codigo_es_valido("1B CD 12"))

    def test_codigo_invalido_marca_minusculas(self):
        self.assertFalse(codigo_es_valido("ab CD 12"))

    # --- Errores en la sección de grupo (letras del medio) ---

    def test_codigo_invalido_grupo_una_sola_letra(self):
        self.assertFalse(codigo_es_valido("AB C 12"))

    def test_codigo_invalido_grupo_tres_letras(self):
        self.assertFalse(codigo_es_valido("AB CDE 12"))

    def test_codigo_invalido_grupo_minusculas(self):
        self.assertFalse(codigo_es_valido("AB cd 12"))

    def test_codigo_invalido_grupo_con_digito(self):
        self.assertFalse(codigo_es_valido("AB C1 12"))

    # --- Errores en la sección de tipo (2 alfanuméricos finales) ---

    def test_codigo_invalido_tipo_un_solo_caracter(self):
        self.assertFalse(codigo_es_valido("AB CD 1"))

    def test_codigo_invalido_tipo_tres_caracteres(self):
        self.assertFalse(codigo_es_valido("AB CD 123"))

    def test_codigo_invalido_tipo_minusculas(self):
        self.assertFalse(codigo_es_valido("AB CD ab"))

    def test_codigo_invalido_tipo_caracter_especial(self):
        self.assertFalse(codigo_es_valido("AB CD 1!"))

    # --- Errores en los separadores ---

    def test_codigo_invalido_separador_guion(self):
        self.assertFalse(codigo_es_valido("AB-CD-12"))

    def test_codigo_invalido_sin_separadores(self):
        self.assertFalse(codigo_es_valido("ABCD12"))

    def test_codigo_invalido_separador_punto(self):
        self.assertFalse(codigo_es_valido("AB.CD.12"))

    def test_codigo_invalido_doble_espacio(self):
        self.assertFalse(codigo_es_valido("AB  CD 12"))

    # --- Casos extremos ---

    def test_codigo_invalido_cadena_vacia(self):
        self.assertFalse(codigo_es_valido(""))

    def test_codigo_invalido_solo_espacios(self):
        self.assertFalse(codigo_es_valido("     "))

    def test_codigo_invalido_formato_viejo(self):
        self.assertFalse(codigo_es_valido("P001"))

    def test_codigo_invalido_con_espacios_al_final(self):
        self.assertFalse(codigo_es_valido("AB CD 12 "))

    def test_codigo_invalido_con_espacios_al_inicio(self):
        self.assertFalse(codigo_es_valido(" AB CD 12"))


if __name__ == '__main__':
    unittest.main()
