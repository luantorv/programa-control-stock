# Programa de Control de Stock para un Supermercado

## Estructura del Proyecto

```
.
|    .github/workflows
|    |    mirror.yml
|    datos/                     # Archivos en tiempo de ejecución
|    |    cierre_diario.csv
|    |    productos.csv
|    |    usuarios.csv
|    |    ventas_dia.csv
|    persistencia/
|    |    csv_utils.py          # Escritura atómica y lectura genérica de CSV
|    |    productos_repo.py     # CRUD sobre datos/productos.csv
|    |    usuarios_repo.py      # lectura de datos/usuarios.csv
|    |    ventas_repo.py        # ventas_dia.csv y cierre_diario.csv
|    modelos/
|    |    esquemas.py           # Forma en la que se manejan los datos
|    logica/
|    |    autenticacion.py      # Login y hash SHA-256
|    |    productos.py          # ABM y ajuste de stock
|    |    validaciones.py       # RegEx de código y sotck no negativo
|    |    ventas.py             # Registro de vejtay cierre diario
|    cli/
|    |    entradas.py           # Sólo imprime menús (sin input)
|    |    flujo.py              # Todos los input() y parseo de lo que ingresa el usuario
|    |    menus.py              # Navegación: une menús + entradas + lógica
|    flake.nix
|    flake.lock
|    main.py                    # Punto de entrada
|    LICENSE
```

## Licencia

Copyright © 2026 Luis Reis Viera

Licensed under the Apache License, Version 2.0. See the `LICENSE` file for details.