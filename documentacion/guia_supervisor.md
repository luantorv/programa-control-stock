# Guía de uso — Supervisor

## Inicio de sesión

Al ejecutar el programa, se solicita el nombre de usuario y la contraseña:

```
=== Control de Stock para un Supermercado ===

Nombre de usuario: supervisor
Contraseña: 
Bienvenido, supervisor. Rol: supervisor.
```

Si los datos son incorrectos, el sistema lo indica y permite hasta **3 intentos**. Si se agotan, el acceso queda bloqueado para esa sesión.

---

## Menú principal

Una vez autenticado, aparece el menú del supervisor:

```
=== Menú Supervisor ===
1. Alta de producto
2. Baja de producto
3. Modificar producto
4. Ajustar stock
5. Cierre diario
0. Salir
```

Ingresar el número de la opción deseada y presionar Enter.

---

## 1. Alta de producto

Permite registrar un nuevo producto en el sistema.

**Pasos:**
1. Ingresar el código del producto (ej: `LA EC A1`, `AB CD 12`).
   - Formato obligatorio: 2 letras de marca + espacio + 2 letras de grupo + espacio + 2 caracteres alfanuméricos de tipo.
   - Presionar Enter sin escribir nada cancela la operación.
2. Ingresar el nombre del producto.
3. Ingresar el grupo del producto (ej: `Lácteos`, `Bebidas`).
4. Ingresar el precio unitario (puede tener decimales, ej: `1.50`).
5. Ingresar el stock inicial (número entero).

Si el código ya existe o algún dato no es válido, el sistema muestra el error y permite volver a intentarlo.

**Ejemplo:**
```
Código del producto (ej: LA EC A1 | Enter para cancelar): LA EC A1
Nombre del producto: Leche entera 1L
Grupo del producto: Lácteos
Precio unitario ($): 1.50
Stock inicial: 100
Producto dado de alta con éxito.
```

---

## 2. Baja de producto

Elimina un producto del catálogo.

**Pasos:**
1. Ingresar el código del producto a eliminar.
   - Presionar Enter sin escribir nada cancela la operación.
2. El sistema muestra el nombre y stock actual del producto encontrado.
3. Confirmar la baja ingresando `s` (sí) o `n` (no).

La baja es permanente. No se puede deshacer desde el programa.

**Ejemplo:**
```
Código del producto a eliminar (Enter para cancelar): LA EC A1
Producto encontrado: Leche entera 1L | Stock: 100
¿Confirma la baja? (s/n): s
Producto eliminado con éxito.
```

---

## 3. Modificar producto

Actualiza el nombre, grupo, precio o stock de un producto existente.

**Pasos:**
1. Ingresar el código del producto a modificar.
   - Presionar Enter sin escribir nada cancela la operación.
2. El sistema muestra los datos actuales del producto.
3. Ingresar el nuevo nombre, grupo, precio y stock.
   - Todos los campos son obligatorios; no es posible modificar solo uno.

**Ejemplo:**
```
Código del producto a modificar (Enter para cancelar): LA EC A1
Datos actuales -> Nombre: Leche entera 1L | Grupo: Lácteos | Precio: $1.50 | Stock: 100

Nuevo nombre: Leche entera 1 litro
Nuevo grupo: Lácteos
Nuevo precio ($): 1.75
Nuevo stock: 95
Producto modificado con éxito.
```

---

## 4. Ajustar stock

Establece una cantidad de stock específica para un producto, sin necesidad de pasar por una venta.

Útil para corregir diferencias de inventario, registrar mercadería recibida o ajustar por pérdidas.

**Pasos:**
1. Ingresar el código del producto.
   - Presionar Enter sin escribir nada cancela la operación.
2. Ingresar la nueva cantidad en stock.

**Ejemplo:**
```
Código del producto (Enter para cancelar): LA EC A1
Nueva cantidad en stock: 120
Stock actualizado con éxito.
```

> La cantidad mínima aceptada es 0. No se permiten valores negativos.

---

## 5. Cierre diario

Consolida todas las ventas del día en el historial. El archivo de ventas del día **no se elimina**; queda guardado como historial con el nombre `ventas_YYYYMMDD.csv`. El día siguiente el sistema empieza automáticamente con un archivo nuevo y vacío.

**Esta operación no se puede deshacer.**

**Pasos:**
1. El sistema muestra la lista de todas las ventas registradas en el día.
2. Ingresar `s` para confirmar el cierre o `n` para cancelar.
3. Si se confirma, se muestra el resumen del día.

**Ejemplo:**
```
=== Ventas del día ===
N°1 | 2026-07-14 09:15:32 | Cód: LA EC A1 | 2 unid. x $1.75 | Subtotal: $3.50
N°2 | 2026-07-14 10:44:01 | Cód: AB CD 12 | 1 unid. x $5.00 | Subtotal: $5.00
======================

¿Confirma el cierre del día? Se consolidarán las ventas y no se podrá deshacer. (s/n): s

=== Resumen del cierre diario ===
Fecha:               2026-07-14
Ventas realizadas:   2
Unidades vendidas:   3
Importe total:       $8.50
=================================
Ventas del día consolidadas en cierre_diario.csv.
```

El historial de cierres se acumula en `cierre_diario.csv` y nunca se borra automáticamente.

---

## Salir

Seleccionar la opción `0` en el menú principal cierra la sesión y termina el programa.

---

## Consideraciones importantes

- El stock nunca puede quedar en valores negativos, ya sea por ajuste manual o por venta.
- Los códigos de producto tienen un formato fijo: 2 letras de marca + espacio + 2 letras de grupo + espacio + 2 caracteres alfanuméricos de tipo (ej: `LA EC A1`, `AB CD 12`). El sistema rechaza cualquier código que no cumpla este formato.
- Una vez realizado el cierre diario, las ventas del día quedan archivadas en su archivo `ventas_YYYYMMDD.csv` y no pueden editarse desde el programa.
