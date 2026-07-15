# Guía de Instalación y Actualización

## Requisitos

- **Python 3.12** o superior.
- No se requieren librerías adicionales; el programa usa únicamente la biblioteca estándar de Python.
- Acceso de escritura a la carpeta donde se instale el proyecto (para crear y modificar los archivos CSV en `datos/`).

---

## Instalación

### 1. Obtener el código fuente

Clonar el repositorio con Git:

```bash
git clone <url-del-repositorio>
cd program
```

O bien, descomprimir el archivo `.zip` del proyecto y abrir una terminal en esa carpeta.

### 2. Verificar la instalación de Python

```bash
python --version
```

Debe mostrar `Python 3.12.x` o superior. En algunos sistemas el comando es `python3`:

```bash
python3 --version
```

### 3. Ejecutar el programa

```bash
python main.py
```

O bien:

```bash
python3 main.py
```

Al iniciar por primera vez, los archivos `datos/ventas_dia.csv` y `datos/cierre_diario.csv` ya vienen con su encabezado. `datos/productos.csv` puede estar vacío o contener productos de ejemplo. `datos/usuarios.csv` contiene los usuarios predefinidos.

---

## Entorno con Nix (opcional)

Si el sistema tiene Nix instalado con soporte para Flakes, el entorno de Python correcto se obtiene automáticamente:

```bash
nix develop
python main.py
```

No es necesario instalar Python manualmente en ese caso.

---

## Usuarios predefinidos

El archivo `datos/usuarios.csv` incluye dos usuarios listos para usar:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `supervisor` | `super123` | Supervisor |
| `cajero` | `cajero123` | Cajero |

Las contraseñas están almacenadas como hash SHA-256; el archivo CSV no contiene texto plano.

---

## Agregar o modificar usuarios

El programa no incluye una pantalla para gestionar usuarios. Los cambios se hacen editando `datos/usuarios.csv` directamente.

### Formato del archivo

```
nombre,contrasena_hash,rol
supervisor,<hash>,supervisor
cajero,<hash>,cajero
```

El campo `rol` debe ser exactamente `supervisor` o `cajero`.

### Generar el hash de una contraseña

Desde la terminal de Python:

```python
import hashlib
contrasena = "mi_contraseña_nueva"
hash_resultado = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
print(hash_resultado)
```

Copiar el resultado e ingresarlo en la columna `contrasena_hash` del CSV.

### Ejemplo: agregar un segundo cajero

Abrir `datos/usuarios.csv` con cualquier editor de texto y agregar una línea:

```
cajero2,<hash de la contraseña>,cajero
```

---

## Actualización del programa

### Actualizar desde el repositorio Git

```bash
git pull origin main
```

Esto descarga los últimos cambios sin afectar los archivos de datos en `datos/`.

> Los archivos CSV en `datos/` están fuera del control de versiones y no se modifican al actualizar el código.

### Verificar compatibilidad del esquema de datos

Si una actualización agrega columnas nuevas a los CSV, es necesario actualizar los archivos existentes manualmente agregando la columna con un valor por defecto en cada fila existente. Esto se indica en las notas de la actualización correspondiente.

---

## Solución de problemas comunes

### El programa no arranca

- Verificar que se está ejecutando desde la carpeta raíz del proyecto (donde está `main.py`).
- Confirmar que la versión de Python es 3.12 o superior.

### "No se puede iniciar sesión"

- Confirmar que `datos/usuarios.csv` existe y tiene el encabezado correcto: `nombre,contrasena_hash,rol`.
- Verificar que el hash de la contraseña fue generado con SHA-256 en codificación UTF-8.

### Los datos no se guardan

- Verificar que el usuario del sistema operativo tiene permiso de escritura en la carpeta `datos/`.

### El archivo CSV quedó corrupto

Los archivos CSV se escriben mediante escritura atómica: si el programa se interrumpe durante una escritura, el archivo original no se modifica. Si de todas formas un archivo queda en mal estado, puede restaurarse desde la última copia de seguridad o reconstruirse manualmente respetando el encabezado de cada archivo.
