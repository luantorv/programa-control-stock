# Programa de Control de Stock para un Supermercado

[![Tests](https://github.com/luantorv/programa-control-stock/actions/workflows/tests.yml/badge.svg)](https://github.com/luantorv/programa-control-stock/actions/workflows/tests.yml)

Aplicación de consola en Python que reemplaza el registro manual en papel por una gestión digital del inventario y las ventas de un supermercado. El sistema diferencia dos roles —Supervisor y Cajero— y garantiza que ninguna venta pueda realizarse si no hay stock suficiente.

## Características

- **Supervisor**: alta, baja y modificación de productos; ajuste manual de stock; cierre diario.
- **Cajero**: registro de ventas (con descuento automático de stock) y consulta de precio y stock por código o nombre.
- Persistencia en archivos CSV mediante escritura atómica (sin bases de datos ni librerías externas).
- Contraseñas almacenadas con hash SHA-256.
- Código de producto validado con expresión regular.

## Requisitos

- Python 3.12

Si el proyecto está clonado con su `flake.nix`, podés obtener el entorno con:

```bash
nix develop
```

## Cómo ejecutar

```bash
python main.py
```

### Usuarios predefinidos

| Usuario | Contraseña | Rol |
|---|---|---|
| `supervisor` | `super123` | Supervisor |
| `cajero` | `cajero123` | Cajero |

## Estructura del proyecto

```
main.py                        # Punto de entrada
datos/
    productos.csv              # Catálogo de productos
    users.csv                  # Usuarios con hash de contraseña y rol
    ventas_YYYYMMDD.csv        # Ventas del día (un archivo por fecha)
    cierre_diario.csv          # Historial de cierres diarios (acumulativo)
modelos/
    esquemas.py                # Constantes de claves CSV y roles
persistencia/
    csv_utils.py               # Lectura genérica y escritura atómica de CSV
    productos_repo.py          # CRUD sobre datos/productos.csv
    usuarios_repo.py           # Lectura de datos/usuarios.csv
    ventas_repo.py             # Lectura/escritura de ventas_dia.csv y cierre_diario.csv
logica/
    autenticacion.py           # Login y hash SHA-256
    productos.py               # ABM, ajuste de stock y consulta
    ventas.py                  # Registro de venta y cierre diario
    validaciones.py            # Regex de código de producto y stock no negativo
cli/
    menus.py                   # Impresión de menús (sin input)
    entradas.py                # Todos los input() y parseo de datos del usuario
    flujo.py                   # Navegación: une menús, entradas y lógica
```

## Aclaración

Este programa fue desarrollado como trabajo práctico integrador de la cátedra **Programación 1** de la Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial (ESIM – ISFDyT), cursada en 2025. 

El diseño sigue las restricciones de la asignatura: estilo funcional y estructurado, sin programación orientada a objetos y usando únicamente la biblioteca estándar de Python.

> Para más información: [ESIM - ISFDyT](web.esim.edu.ar)

## Licencia

Copyright © 2026 Luis Reis Viera

Licensed under the Apache License, Version 2.0. See the `LICENSE` file for details.

## Autor

### **Reis Viera Luis Antonio**

_Estudiante de la Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial del Instituto Superior de Formación Docente y Técnica._

### Contacto:

- **Mail**: `luantorv@gmail.com`
- **GitHub**: [luantorv](https://github.com/luantorv)