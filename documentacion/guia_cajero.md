# Guía de uso — Cajero

## Inicio de sesión

Al ejecutar el programa, se solicita el nombre de usuario y la contraseña:

```
=== Control de Stock para un Supermercado ===

Nombre de usuario: cajero
Contraseña: 
Bienvenido, cajero. Rol: cajero.
```

Si los datos son incorrectos, el sistema lo indica y permite hasta **3 intentos**. Si se agotan, el acceso queda bloqueado para esa sesión.

---

## Menú principal

Una vez autenticado, aparece el menú del cajero:

```
=== Menú Cajero ===
1. Registrar venta
2. Consultar producto
0. Salir
```

Ingresar el número de la opción deseada y presionar Enter.

---

## 1. Registrar venta

Registra la venta de un producto y descuenta automáticamente las unidades del stock.

**Pasos:**
1. Ingresar el código del producto que se va a vender.
   - Presionar Enter sin escribir nada cancela la operación y vuelve al menú.
2. Ingresar la cantidad de unidades.
3. El sistema confirma la venta y muestra el importe total.

**Ejemplo:**
```
Código del producto a vender (Enter para cancelar): LAC001
Cantidad: 3
Venta registrada. Total: $4.50
```

### Errores posibles

| Mensaje | Causa |
|---------|-------|
| `No existe un producto con el código XXX.` | El código ingresado no está en el sistema. Verificar que esté bien escrito (mayúsculas y dígitos). |
| `Stock insuficiente. Disponible: N unidades.` | La cantidad pedida supera el stock existente. Solo se puede vender hasta la cantidad disponible. |
| `La cantidad a vender debe ser mayor a cero.` | Se ingresó 0 o un número negativo. |

En cualquier caso, el sistema muestra el error y permite intentarlo de nuevo o cancelar con Enter.

---

## 2. Consultar producto

Muestra el precio y el stock actual de un producto. Sirve para verificar disponibilidad antes de atender a un cliente.

**Pasos:**
1. Ingresar el código del producto **o** una parte del nombre.
   - Presionar Enter sin escribir nada cancela la operación y vuelve al menú.
2. El sistema muestra todos los productos que coincidan con la búsqueda.

**Búsqueda por código exacto:**
```
Código o nombre del producto (Enter para cancelar): LAC001
Código: LAC001 | Nombre: Leche entera 1 litro | Precio: $1.75 | Stock: 92 unidades
```

**Búsqueda por nombre (parcial):**
```
Código o nombre del producto (Enter para cancelar): leche
Código: LAC001 | Nombre: Leche entera 1 litro | Precio: $1.75 | Stock: 92 unidades
Código: LAC002 | Nombre: Leche descremada 1 litro | Precio: $1.90 | Stock: 45 unidades
```

La búsqueda por nombre no distingue entre mayúsculas y minúsculas.

Si no se encuentra ningún resultado, el sistema lo indica y permite intentar con otro término.

---

## Salir

Seleccionar la opción `0` en el menú principal cierra la sesión y termina el programa.

---

## Consideraciones importantes

- El cajero **no puede** crear, modificar ni eliminar productos. Esas operaciones son exclusivas del supervisor.
- El cajero **no puede** realizar el cierre diario.
- Si un producto no tiene stock suficiente, la venta es rechazada automáticamente. Es necesario avisar al supervisor para que realice un ajuste de stock.
- Cada venta queda registrada con fecha, hora, producto, cantidad y total. No es posible anular una venta desde el programa.
