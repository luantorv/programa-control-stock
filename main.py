# SPDX-FileCopyrightText: 2026 Luis Reis Viera
# SPDX-License-Identifier: Apache-2.0

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        import unittest
        conjunto_de_tests = unittest.TestLoader().discover('tests')
        ejecutor = unittest.TextTestRunner(verbosity=2)
        resultado = ejecutor.run(conjunto_de_tests)
        total = resultado.testsRun
        cantidad_fallos = len(resultado.failures) + len(resultado.errors)
        cantidad_exitosos = total - cantidad_fallos
        print()
        print("=== Resumen de tests ===")
        print("Total ejecutados:", total)
        print("Exitosos:        ", cantidad_exitosos)
        print("Fallidos:        ", cantidad_fallos)
        print("========================")
    else:
        from cli import flujo
        flujo.ejecutar()
