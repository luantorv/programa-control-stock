# Documentación Técnica

## Descripción general

Aplicación de consola en Python que digitaliza la gestión de inventario y ventas de un supermercado. Reemplaza un registro manual en papel por un sistema con persistencia en archivos CSV, validaciones de negocio y diferenciación de roles de usuario.

---

## Arquitectura

El sistema está organizado en cuatro capas independientes. Cada capa solo depende de la capa inferior; nunca al revés.

```
CLI  →  Lógica  →  Persistencia  →  Datos (CSV)
              ↑
           Modelos (constantes compartidas)
```

| Capa | Paquete | Responsabilidad |
|------|---------|-----------------|
| Modelos | `modelos/` | Constantes de claves CSV y roles |
| Persistencia | `persistencia/` | Lectura y escritura de archivos CSV |
| Lógica | `logica/` | Reglas de negocio, validaciones |
| Interfaz CLI | `cli/` | Menús, entrada de datos, navegación |

---

## Estructura de módulos

### `modelos/esquemas.py`

Define todas las constantes usadas como claves de diccionario al leer o escribir CSV. Ningún otro módulo usa strings literales para acceder a campos.

| Constante | Valor |
|-----------|-------|
| `USUARIO_NOMBRE` | `"username"` |
| `USUARIO_CONTRASENA_HASH` | `"hash"` |
| `USUARIO_ROL` | `"rol"` |
| `ROL_SUPERVISOR` | `"supervisor"` |
| `ROL_CAJERO` | `"cajero"` |
| `PRODUCTO_CODIGO` | `"codigo"` |
| `PRODUCTO_NOMBRE` | `"nombre"` |
| `PRODUCTO_GRUPO` | `"grupo"` |
| `PRODUCTO_PRECIO` | `"precio"` |
| `PRODUCTO_STOCK` | `"stock"` |
| `VENTA_FECHA_HORA` | `"fecha_hora"` |
| `VENTA_NRO_FACTURA` | `"nro_factura"` |
| `VENTA_USUARIO` | `"usuario"` |
| `VENTA_CODIGO` | `"codigo"` |
| `VENTA_CANTIDAD` | `"cantidad"` |
| `VENTA_PRECIO_UNIT` | `"precio_unit"` |
| `VENTA_SUBTOTAL` | `"subtotal"` |
| `CIERRE_FECHA` | `"fecha"` |
| `CIERRE_TOTAL_VENTAS` | `"total_ventas"` |
| `CIERRE_TOTAL_UNIDADES` | `"total_unidades"` |
| `CIERRE_IMPORTE_TOTAL` | `"importe_total"` |

También define las listas de encabezados (`ENCABEZADO_PRODUCTOS`, `ENCABEZADO_VENTAS`, `ENCABEZADO_CIERRE`) usadas al escribir CSV.

---

### `persistencia/csv_utils.py`

Utilidades de I/O compartidas por todos los repositorios.

#### `leer_csv(ruta) → list[dict]`
Lee un archivo CSV y devuelve una lista de diccionarios. Si el archivo no existe, devuelve una lista vacía.

#### `escribir_csv_atomico(ruta, filas, encabezado) → bool`
Escribe el CSV mediante escritura atómica:
1. Escribe en un archivo temporal (`ruta + ".tmp"`).
2. Si la escritura falla, elimina el temporal y devuelve `False`.
3. Si tiene éxito, reemplaza el archivo destino con `os.replace()` (operación atómica en el sistema operativo).

Este patrón garantiza que el archivo original nunca queda en estado corrupto si el programa se interrumpe durante la escritura.

---

### `persistencia/usuarios_repo.py`

| Función | Descripción |
|---------|-------------|
| `leer_usuarios()` | Devuelve todos los usuarios del CSV. |

Los usuarios no se modifican desde el programa; se gestionan manualmente editando `datos/usuarios.csv`.

---

### `persistencia/productos_repo.py`

| Función | Descripción |
|---------|-------------|
| `leer_productos()` | Devuelve todos los productos. |
| `guardar_productos(productos)` | Reemplaza el CSV completo con la lista recibida. |
| `buscar_producto_por_codigo(codigo)` | Devuelve el dict del producto o `None`. |
| `agregar_producto(producto)` | Agrega un producto y guarda. |
| `actualizar_producto(producto_actualizado)` | Reemplaza el producto con el mismo código y guarda. |
| `eliminar_producto(codigo)` | Filtra el producto con ese código y guarda. |
| `buscar_productos_por_nombre(nombre)` | Búsqueda por subcadena, sin distinción de mayúsculas. |

---

### `persistencia/ventas_repo.py`

El nombre del archivo de ventas incluye la fecha: `ventas_YYYYMMDD.csv`. Cada día genera su propio archivo; no se eliminan al hacer el cierre.

| Función | Descripción |
|---------|-------------|
| `_ruta_ventas_hoy()` | Devuelve la ruta del archivo de ventas de la fecha actual. |
| `leer_ventas_del_dia()` | Devuelve las ventas del archivo de hoy (lista vacía si no existe). |
| `registrar_venta(venta)` | Agrega una venta al archivo de hoy. |
| `leer_cierres()` | Devuelve el historial de cierres. |
| `registrar_cierre(cierre)` | Agrega un cierre al CSV acumulativo. |

---

### `logica/autenticacion.py`

| Función | Descripción |
|---------|-------------|
| `hashear_contrasena(contrasena)` | Devuelve el hash SHA-256 en hexadecimal. |
| `autenticar(nombre_usuario, contrasena)` | Compara hash y devuelve el rol, o `None` si falla. |

Las contraseñas **nunca** se almacenan ni comparan en texto plano.

---

### `logica/validaciones.py`

#### Patrón de código de producto

```
r'^[A-Z]{2}\s[A-Z]{2}\s[A-Z0-9]{2}$'
```

El código tiene tres partes separadas por un espacio:
- 2 letras mayúsculas: marca.
- 2 letras mayúsculas: grupo de producto.
- 2 caracteres alfanuméricos (letras mayúsculas o dígitos): tipo.

Ejemplos válidos: `LA EC A1`, `AB CD 12`, `XX YY 3Z`.

| Función | Descripción |
|---------|-------------|
| `codigo_es_valido(codigo)` | Devuelve `True` si el código cumple el patrón. |

---

### `logica/productos.py`

Todas las funciones devuelven `""` en caso de éxito, o un string con el mensaje de error en español en caso de fallo.

| Función | Descripción |
|---------|-------------|
| `buscar_producto(codigo)` | Wrapper de `buscar_producto_por_codigo`. |
| `consultar_producto(termino)` | Intenta coincidencia exacta por código; si no, busca por nombre. Devuelve lista. |
| `dar_de_alta_producto(codigo, nombre, grupo, precio, stock)` | Valida formato, unicidad y valores; agrega el producto. |
| `dar_de_baja_producto(codigo)` | Verifica existencia y elimina. |
| `modificar_producto(codigo, nombre, grupo, precio, stock)` | Valida y actualiza. |
| `ajustar_stock(codigo, nueva_cantidad)` | Valida ≥ 0 y actualiza. |

---

### `logica/ventas.py`

#### `registrar_venta(codigo, cantidad, nombre_usuario) → tuple`

Devuelve `("", subtotal)` en caso de éxito, o `("mensaje de error", 0.0)` en caso de fallo. Verifica:
- Cantidad mayor a cero.
- Producto existente.
- Stock suficiente (la venta no puede dejar el stock en negativo).

Si todo es válido, descuenta el stock, calcula el número de factura (secuencial por día), y registra la venta con fecha, hora y usuario.

#### `ejecutar_cierre_diario() → dict`

Consolida las ventas del día: suma totales y escribe el cierre en `cierre_diario.csv`. El archivo `ventas_YYYYMMDD.csv` **no se elimina**; queda como historial. Devuelve el diccionario del cierre para mostrarlo en pantalla.

---

### `cli/menus.py`

Solo imprime menús en pantalla. No realiza ningún `input()`. Funciones: `mostrar_menu_supervisor()`, `mostrar_menu_cajero()`.

---

### `cli/entradas.py`

Centraliza toda interacción de entrada. Funciones:

| Función | Descripción |
|---------|-------------|
| `pedir_credenciales()` | Devuelve `(nombre_usuario, contrasena)`. |
| `pedir_texto(mensaje)` | Devuelve el string ingresado, sin espacios al inicio/fin. |
| `pedir_numero_entero(mensaje)` | Repite hasta obtener un entero válido. |
| `pedir_numero_decimal(mensaje)` | Repite hasta obtener un float válido. |
| `pedir_confirmacion(mensaje)` | Repite hasta recibir `"s"` (True) o `"n"` (False). |
| `pedir_opcion(opciones_validas)` | Repite hasta que la entrada esté en la lista. |

---

### `cli/flujo.py`

Punto de navegación. Une menús, entradas y lógica. Define:
- `_iniciar_sesion()` — hasta 3 intentos de login; devuelve `(rol, nombre_usuario)` o `(None, None)`.
- Flujos del supervisor: `_flujo_alta_producto`, `_flujo_baja_producto`, `_flujo_modificar_producto`, `_flujo_ajustar_stock`, `_flujo_cierre_diario`.
- `_menu_supervisor()` — bucle principal del supervisor.
- Flujos del cajero: `_flujo_venta`, `_flujo_consulta`.
- `_menu_cajero()` — bucle principal del cajero.
- `ejecutar()` — punto de entrada público; lo llama `main.py`.

---

## Archivos de datos

Todos en la carpeta `datos/`. Se crean con solo el encabezado si no existen (excepto `usuarios.csv`, que debe existir con al menos un usuario).

| Archivo | Descripción |
|---------|-------------|
| `productos.csv` | Catálogo completo de productos |
| `users.csv` | Usuarios con hash y rol |
| `ventas_YYYYMMDD.csv` | Ventas del día (uno por fecha, nunca se eliminan) |
| `cierre_diario.csv` | Historial de cierres (acumulativo) |

### Esquema de `productos.csv`

```
codigo,nombre,grupo,precio,stock
LA EC A1,Leche entera 1L,Lácteos,1.50,100
```

### Esquema de `users.csv`

```
username,hash,rol
supervisor,<hash SHA-256>,supervisor
cajero,<hash SHA-256>,cajero
```

### Esquema de `ventas_YYYYMMDD.csv`

```
fecha_hora,nro_factura,usuario,codigo,cantidad,precio_unit,subtotal
2026-07-14 10:23:45,1,cajero,LA EC A1,2,1.50,3.00
```

### Esquema de `cierre_diario.csv`

```
fecha,total_ventas,total_unidades,importe_total
2026-07-14,5,12,48.50
```

---

## Reglas de negocio

1. **Stock nunca negativo**: toda venta que llevaría el stock por debajo de cero es rechazada antes de registrarse.
2. **Código de producto con formato obligatorio**: cualquier alta o modificación valida el código contra la expresión regular antes de persistir.
3. **Contraseñas como hash SHA-256**: ni `autenticar` ni ningún otro módulo compara o guarda contraseñas en texto plano.

---

## Convenciones de código

- Sin programación orientada a objetos: no hay clases ni instancias. Toda la lógica se implementa con funciones y diccionarios.
- Sin librerías externas: únicamente la biblioteca estándar de Python (`csv`, `re`, `hashlib`, `os`, `tempfile`, `datetime`).
- Sin abreviaturas en nombres de variables o funciones.
- Sin comprensiones de lista ni llamadas encadenadas: se usan bucles `for` y variables intermedias para facilitar la lectura.
