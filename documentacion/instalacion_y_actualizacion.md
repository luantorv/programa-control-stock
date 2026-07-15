# Guía de Instalación y Actualización

Hay dos formas de instalar el programa: con Nix (recomendado, gestiona todo automáticamente) o de forma manual con Python.

---

## Instalación con Nix

La forma más simple, sin necesidad de clonar el repositorio ni instalar Python manualmente.

### Ejecutar una vez (sin instalar)

```bash
nix run github:luantorv/programa-control-stock
```

### Instalar de forma permanente

```bash
nix profile install github:luantorv/programa-control-stock
control-stock
```

### Dónde se guardan los datos

Al usar la instalación Nix, los archivos CSV se guardan en:

```
$XDG_DATA_HOME/control-stock/
```

Si la variable `XDG_DATA_HOME` no está definida (lo habitual), la ruta efectiva es:

```
~/.local/share/control-stock/
```

En el primer uso, el programa copia automáticamente los archivos iniciales a esa carpeta. No hace falta hacer nada manualmente.

### Cambiar la ubicación de los datos (avanzado)

La variable de entorno `CONTROL_STOCK_DATOS_DIR` permite indicar cualquier otra carpeta. Funciona tanto con la instalación Nix como con la manual:

```bash
export CONTROL_STOCK_DATOS_DIR="/ruta/personalizada/datos"
control-stock   # o: python main.py
```

### Actualizar (instalación Nix)

```bash
nix profile upgrade programa-control-stock
```

---

## Instalación manual

### Requisitos

- **Python 3.12** o superior.
- No se requieren librerías adicionales; el programa usa únicamente la biblioteca estándar de Python.
- Acceso de escritura a la carpeta donde se clone el proyecto (para los archivos CSV en `datos/`).

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

Con la instalación manual, los datos se leen y escriben en la carpeta `datos/` dentro del propio proyecto. Los archivos ya vienen con sus encabezados listos.

### Entorno de desarrollo con Nix (opcional)

Si el sistema tiene Nix instalado con soporte para Flakes, el entorno de Python correcto se obtiene automáticamente sin instalar nada a nivel del sistema:

```bash
nix develop
python main.py
```

### Actualizar (instalación manual)

```bash
git pull origin main
```

Esto descarga los últimos cambios sin afectar los archivos de datos en `datos/`.

> **Nota sobre el esquema de datos**: si una actualización agrega columnas nuevas a los CSV, es necesario editarlos manualmente agregando la columna con un valor por defecto en cada fila existente. Esto se indica en las notas de cada actualización.

---

## Usuarios predefinidos

El archivo `users.csv` incluye dos usuarios listos para usar:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `supervisor` | `super123` | Supervisor |
| `cajero` | `cajero123` | Cajero |

Las contraseñas están almacenadas como hash SHA-256; el archivo CSV no contiene texto plano.

---

## Agregar o modificar usuarios

El programa no incluye una pantalla para gestionar usuarios. Los cambios se hacen editando `users.csv` directamente.

| Modo | Ruta del archivo |
|------|-----------------|
| Instalación Nix | `~/.local/share/control-stock/users.csv` |
| Instalación manual | `datos/users.csv` dentro del proyecto |

### Formato del archivo

```
username,hash,rol
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

Copiar el resultado e ingresarlo en la columna `hash` del CSV.

### Ejemplo: agregar un segundo cajero

Abrir `users.csv` con cualquier editor de texto y agregar una línea:

```
cajero2,<hash de la contraseña>,cajero
```

---

## Solución de problemas comunes

### El programa no arranca (instalación manual)

- Verificar que se está ejecutando desde la carpeta raíz del proyecto (donde está `main.py`).
- Confirmar que la versión de Python es 3.12 o superior.

### "No se puede iniciar sesión"

- Confirmar que `users.csv` existe en la carpeta de datos y tiene el encabezado correcto: `username,hash,rol`.
- Verificar que el hash de la contraseña fue generado con SHA-256 en codificación UTF-8 (ver sección anterior).

### Los datos no se guardan

- **Instalación manual**: verificar que el usuario del sistema operativo tiene permiso de escritura en la carpeta `datos/`.
- **Instalación Nix**: verificar que `~/.local/share/control-stock/` existe y es escribible.

### El archivo CSV quedó corrupto

Los archivos CSV se escriben mediante escritura atómica: si el programa se interrumpe durante una escritura, el archivo original no queda modificado. Si de todas formas un archivo queda en mal estado, puede reconstruirse manualmente respetando el encabezado correspondiente (ver la documentación técnica para los esquemas).
